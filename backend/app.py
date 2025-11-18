import os
import smtplib
import ssl
import secrets
import string
import json
import traceback
import imaplib
import email
import email as eml
import re
import hashlib
import pyotp
from email.message import EmailMessage
from datetime import datetime, timezone, timedelta
from flask import Flask, request, jsonify, send_from_directory, make_response  
from flask_cors import CORS
from dotenv import load_dotenv
from email_validator import validate_email, EmailNotValidError
import firebase_admin
from firebase_admin import credentials, auth, firestore

# --- Carrega variáveis do .env ---
load_dotenv()

# --- Inicializa Firebase ---
cred_json = os.getenv("FIREBASE_CRED_JSON")
if not firebase_admin._apps:
    try:
        if cred_json:
            cred = credentials.Certificate(json.loads(cred_json))
        else:
            cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print("❌ ERRO AO INICIALIZAR FIREBASE:")
        print(traceback.format_exc())

db = firestore.client()

# --- Configurações de e-mail ---
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SENDER_NAME = os.getenv("SENDER_NAME", "Kirvano")

# --- IMAP (leitura de e-mails) ---
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))

# --- Flask App ---
app = Flask(__name__)

# Domínios do seu front
# --- CORS robusto ---
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://aiportalacesso.netlify.app",
    "https://www.aiportalacesso.netlify.app",
    "https://portal.dominandoanimacao.com"",
]


SECRET_ADSPOWER = "TBR5NVNRSUHSJ2UUR2ADAEPWBIWBTTPD"


CODIGO_RE = re.compile(r"\b(\d{6})\b")

def buscar_codigo_no_email(target_email: str,
                           sender_filter: str = "security@email.adspower.net",
                           subject_keywords: list[str] = None,
                           search_days: int = 1,
                           mark_seen: bool = True,
                           max_messages_to_check: int = 10) -> str | None:
    """
    Conecta ao IMAP (configurado por IMAP_SERVER, IMAP_PORT, EMAIL_USER, EMAIL_PASS),
    procura por e-mails do `sender_filter` (ou contendo palavras-chave no assunto),
    varre as mensagens mais recentes e retorna o primeiro código de 6 dígitos encontrado
    (ou None se não encontrar).
    """
    try:
        # Conecta por SSL
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT, timeout=30)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("INBOX")

        # Formata data SINCE (IMAP usa formato DD-Mon-YYYY)
        since_date = (datetime.now(timezone.utc) - timedelta(days=search_days)).strftime("%d-%b-%Y")

        # Monta critérios de busca: por remetente e desde a data
        criteria = f'(FROM "{sender_filter}" SINCE "{since_date}")'

        # Se o servidor for Gmail e quiser usar X-GM-RAW (opcional melhor filtro),
        # poderíamos usar: mail.search(None, 'X-GM-RAW', f'from:{sender_filter} newer_than:1d')
        # Mas usaremos o padrão IMAP por compatibilidade.
        status, data = mail.search(None, criteria)

        if status != "OK":
            # fallback: procurar por assunto keywords, se fornecidas
            if subject_keywords:
                # cria OR para os keywords no SUBJECT
                subject_criteria = " ".join([f'(SUBJECT "{kw}")' for kw in subject_keywords])
                status, data = mail.search(None, subject_criteria)
                if status != "OK":
                    mail.logout()
                    return None
            else:
                mail.logout()
                return None

        msg_nums = data[0].split()
        if not msg_nums:
            mail.logout()
            return None

        # vamos iterar das mais recentes para as mais antigas (últimas N mensagens)
        for num in msg_nums[::-1][:max_messages_to_check]:
            status, msg_data = mail.fetch(num, "(RFC822)")
            if status != "OK":
                continue

            raw = msg_data[0][1]
            parsed = eml.message_from_bytes(raw)

            # tenta extrair do body text/plain e html (fallback)
            parts = []
            if parsed.is_multipart():
                for part in parsed.walk():
                    ctype = part.get_content_type()
                    disp = str(part.get("Content-Disposition"))
                    if ctype in ("text/plain", "text/html") and "attachment" not in disp:
                        try:
                            payload = part.get_payload(decode=True)
                            if not payload:
                                continue
                            charset = part.get_content_charset() or "utf-8"
                            parts.append(payload.decode(charset, errors="ignore"))
                        except Exception:
                            continue
            else:
                try:
                    payload = parsed.get_payload(decode=True)
                    charset = parsed.get_content_charset() or "utf-8"
                    parts.append(payload.decode(charset, errors="ignore"))
                except Exception:
                    pass

            # junta conteúdo e procura por código
            for text in parts:
                # busca padrão genérico (6 dígitos)
                m = CODIGO_RE.search(text)
                if m:
                    codigo = m.group(1)

                    # opcional: marcar como lida
                    if mark_seen:
                        try:
                            mail.store(num, "+FLAGS", r"(\Seen)")
                        except Exception:
                            pass

                    mail.logout()
                    return codigo

        mail.logout()
        return None

    except imaplib.IMAP4.error as e:
        print("❌ Erro IMAP:", e)
        return None
    except Exception as e:
        print("❌ Erro ao buscar código no e-mail:", str(e))
        print(traceback.format_exc())
        return None

@app.after_request
def after_request(response):
    origin = request.headers.get("Origin", "")
    # Verifica se algum domínio permitido está contido na origem
    if any(allowed in origin for allowed in ALLOWED_ORIGINS):
        response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Vary"] = "Origin"
    return response

# --- Servir arquivos da pasta /public ---
@app.route('/public/<path:filename>')
def serve_public(filename):
    public_path = os.path.join(os.path.dirname(__file__), '../public')
    return send_from_directory(public_path, filename)

# --- Funções auxiliares ---

def gerar_senha(tamanho: int = 10) -> str:
    caracteres = string.ascii_letters + string.digits
    return "".join(secrets.choice(caracteres) for _ in range(tamanho))


def enviar_email_credenciais(destinatario: str, senha: str):
    assunto = "Acesso liberado ao Portal de Ferramentas"

    corpo_html = f"""
<div style="background-color:#0e1726; padding:40px; font-family:Arial, Helvetica, sans-serif; color:#ffffff;">
  <div style="max-width:600px; margin:auto; background-color:#141e30; border-radius:16px;
              box-shadow:0 0 25px rgba(0,255,255,0.2); overflow:hidden;">
    
    <!-- Cabeçalho -->
    <div style="background-color:#00bcd4;
                border-top-left-radius:16px;
                border-top-right-radius:16px;
                padding:20px 0; text-align:center;">
      <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
        <tr>
          <td align="center" valign="middle">
            <table role="presentation" cellspacing="0" cellpadding="0" border="0">
              <tr>
                <td style="padding-right:10px;">
                  <img src="cid:kirvano_logo" alt="Logo Kirvano" width="50" style="border-radius:10px; display:block;">
                </td>
                <td>
                  <h1 style="margin:0; font-size:20px; color:#ffffff; font-weight:800; font-family:Arial,Helvetica,sans-serif;">
                    Dominando Animações
                  </h1>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </div>

    <!-- Corpo -->
    <div style="padding:30px; text-align:center;">
      <h2 style="color:#00ffff; margin-top:0;">Sua conta foi criada com sucesso!</h2>
      <p style="font-size:16px; color:#cbd5e1; margin:10px 0 25px;">
        Agora você pode acessar o portal e explorar todas as ferramentas disponíveis.
      </p>
      
      <div style="background-color:#1e293b; border:1px solid rgba(0,255,255,0.3); border-radius:12px;
                  padding:20px; margin:25px 0; display:inline-block; text-align:left;">
        <p style="font-size:16px; margin:6px 0;"><strong>E-mail:</strong> {destinatario}</p>
        <p style="font-size:16px; margin:6px 0;"><strong>Senha:</strong> {senha}</p>
      </div>

      <div style="margin-top:25px;">
        <a href="https://portal.dominandoanimacao.com"
           style="background-color:#00bcd4; padding:12px 30px; color:#0e1726;
                  text-decoration:none; font-weight:bold; border-radius:10px;
                  display:inline-block;">
          Acessar o Portal
        </a>
      </div>

      <p style="margin-top:30px; color:#94a3b8; font-size:14px;">
        Recomendamos alterar sua senha após o primeiro login.<br>
        Caso tenha dúvidas, entre em contato com nosso suporte.
      </p>
    </div>

    <!-- Rodapé -->
    <div style="background-color:#0f172a; text-align:center; padding:14px; color:#64748b; font-size:13px;
                border-top:1px solid rgba(0,255,255,0.1); border-bottom-left-radius:16px; border-bottom-right-radius:16px;">
      &copy; {datetime.now().year} Dominando Animações • Todos os direitos reservados
    </div>

  </div>
</div>
"""



    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = f"{SENDER_NAME} <{EMAIL_USER}>"
    msg["To"] = destinatario
    msg.add_alternative(corpo_html, subtype="html")

    logo_path = os.path.join(os.path.dirname(__file__), "../public/marca.png")

    if os.path.exists(logo_path):
        with open(logo_path, "rb") as img:
            msg.get_payload()[0].add_related(
                img.read(),
                maintype="image",
                subtype="png",
                cid="<kirvano_logo>",
                filename="marca.png",
            )
    else:
        print("⚠️ Logo não encontrada em:", logo_path)

    contexto = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls(context=contexto)
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

    print(f"📧 E-mail enviado com sucesso para {destinatario}")


def criar_usuario_e_enviar(email: str):
    try:
        email_validado = validate_email(email, check_deliverability=False).normalized
    except EmailNotValidError as e:
        return {"ok": False, "error": f"E-mail inválido: {str(e)}"}

    senha = gerar_senha()

    try:
        user = auth.create_user(email=email_validado, password=senha)
    except auth.EmailAlreadyExistsError:
        user = auth.get_user_by_email(email_validado)
        auth.update_user(user.uid, password=senha)

    db.collection("usuarios").document(user.uid).set({
        "email": email_validado,
        "criado_em": datetime.now(timezone.utc).isoformat()
    })

    enviar_email_credenciais(email_validado, senha)
    return {"ok": True, "uid": user.uid}


@app.post("/webhook/kirvano")
def kirvano_webhook():
    data = request.get_json(silent=True) or {}
    print("📦 Payload recebido:", data)

    event = data.get("event", "").upper()
    status = data.get("status", "").upper()
    customer = data.get("customer", {})
    email = customer.get("email")
    nome = customer.get("name", "Cliente Kirvano")

    if not email:
        return jsonify({"ok": False, "error": "E-mail não encontrado no payload"}), 400

    produtos = data.get("products", [])
    produto_nome = produtos[0].get("name") if produtos else "Produto Kirvano"

    # --- Função auxiliar para atualizar status no Firestore ---
    def atualizar_status_usuario(email, ativo):
        docs = db.collection("usuarios").where("email", "==", email).stream()
        for doc in docs:
            ref = db.collection("usuarios").document(doc.id)
            ref.update({"ativo": ativo, "atualizado_em": datetime.now(timezone.utc).isoformat()})
            print(f"🔥 Status do usuário {email} atualizado para {'ativo' if ativo else 'inativo'}")

    try:
        if event == "SALE_APPROVED" or status == "APPROVED":
            # ✅ Compra aprovada — cria ou reativa o usuário
            resultado = criar_usuario_e_enviar(email)

            db.collection("kirvano_compras").add({
                "email": email,
                "nome": nome,
                "produto": produto_nome,
                "status": "APROVADO",
                "evento": event,
                "metodo_pagamento": data.get("payment_method"),
                "data_compra": data.get("created_at"),
                "sale_id": data.get("sale_id"),
                "valor_total": data.get("total_price"),
                "criado_em": datetime.now(timezone.utc).isoformat()
            })

            atualizar_status_usuario(email, True)
            return jsonify({"ok": True, "msg": "Usuário criado ou reativado com sucesso"}), 200

        elif event in ["SUBSCRIPTION_RENEWED", "SUBSCRIPTION_RENEWAL"] or "RENOVADA" in status:
            # 🔄 Renovação de assinatura — mantém acesso ativo
            atualizar_status_usuario(email, True)
            print(f"🔁 Assinatura renovada para {email}")
            return jsonify({"ok": True, "msg": "Assinatura renovada, acesso mantido"}), 200

        elif event in ["SUBSCRIPTION_CANCELED", "SUBSCRIPTION_CANCELLED"] or "CANCELADA" in status:
            # ❌ Assinatura cancelada — bloqueia acesso
            atualizar_status_usuario(email, False)
            print(f"🚫 Assinatura cancelada para {email}")
            return jsonify({"ok": True, "msg": "Acesso bloqueado (assinatura cancelada)"}), 200

        elif event in ["SUBSCRIPTION_DELAYED", "SUBSCRIPTION_OVERDUE"] or "ATRASADA" in status:
            # ⚠️ Assinatura atrasada — suspende acesso
            atualizar_status_usuario(email, False)
            print(f"⚠️ Assinatura atrasada para {email}")
            return jsonify({"ok": True, "msg": "Acesso suspenso (assinatura atrasada)"}), 200

        else:
            print(f"ℹ️ Evento ignorado: {event} ({status})")
            return jsonify({"ok": True, "msg": f"Evento ignorado: {event}"}), 200

    except Exception as e:
        print("❌ ERRO NO WEBHOOK:")
        print(traceback.format_exc())
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/gerar-codigo", methods=["POST"])
def gerar_codigo():
    try:
        data = request.get_json(silent=True) or {}
        email_usuario = data.get("email")

        if not email_usuario:
            return jsonify({"ok": False, "error": "E-mail não informado"}), 400

        # ========== TOTP ==========
        totp = pyotp.TOTP(SECRET_ADSPOWER)
        codigo = totp.now()  # código igual ao Authenticator

        # ===== Limite diário 2 códigos =====
        hoje = datetime.now(timezone.utc).date()
        id_usuario = hashlib.sha256(email_usuario.encode()).hexdigest()
        ref = db.collection("codigos_gerados").document(id_usuario)
        doc = ref.get()

        if doc.exists:
            dados = doc.to_dict()
            ultima_data = dados.get("data")
            total = dados.get("total", 0)

            if ultima_data == str(hoje) and total >= 2:
                return jsonify({
                    "ok": False,
                    "error": "Limite diário de 2 códigos atingido"
                }), 403

            elif ultima_data == str(hoje):
                ref.update({
                    "total": total + 1,
                    "ultimo_codigo": codigo,
                    "gerado_em": datetime.now(timezone.utc).isoformat()
                })
            else:
                ref.set({
                    "data": str(hoje),
                    "total": 1,
                    "ultimo_codigo": codigo,
                    "gerado_em": datetime.now(timezone.utc).isoformat()
                })
        else:
            ref.set({
                "data": str(hoje),
                "total": 1,
                "ultimo_codigo": codigo,
                "gerado_em": datetime.now(timezone.utc).isoformat()
            })

        return jsonify({"ok": True, "code": codigo}), 200

    except Exception as e:
        print("❌ ERRO AO GERAR CÓDIGO:", e)
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/preview-email")
def preview_email():
    destinatario = request.args.get("email", "teste@exemplo.com")
    senha = request.args.get("senha", "Senha123!")

    corpo_html = f"""
    <div style="background-color:#0e1726; padding:40px; font-family:Arial, Helvetica, sans-serif; color:#ffffff;">
      <div style="max-width:600px; margin:auto; background-color:#141e30; border-radius:16px; overflow:hidden; box-shadow:0 0 25px rgba(0,255,255,0.2);">
        <div style="background:linear-gradient(90deg, #00ffff, #0077ff); padding:20px 30px; display:flex; align-items:center; gap:15px;">
          <img src="/public/marca.png" alt="Logo Kirvano" width="50" style="border-radius:10px;">
          <h1 style="margin:0; font-size:18px; color:#fff; letter-spacing:1px;">Portal de Ferramentas Dominando Animações</h1>
        </div>

        <div style="padding:30px; text-align:center;">
          <h2 style="color:#00ffff;">Sua conta foi criada com sucesso!</h2>
          <p style="font-size:16px; color:#cbd5e1;">Agora você pode acessar o portal e explorar todas as ferramentas disponíveis.</p>

          <div style="background-color:#1e293b; border:1px solid rgba(0,255,255,0.3); border-radius:12px; padding:20px; margin:25px 0;">
            <p style="font-size:16px; margin:6px 0;"><strong>E-mail:</strong> {destinatario}</p>
            <p style="font-size:16px; margin:6px 0;"><strong>Senha:</strong> {senha}</p>
          </div>

          <a href="https://aiportalacesso.netlify.app"
            style="background:linear-gradient(90deg,#00ffff,#0077ff); padding:12px 30px; color:#0e1726; text-decoration:none;
                   font-weight:bold; border-radius:10px; display:inline-block; margin-top:10px;">
            Acessar o Portal
          </a>

          <p style="margin-top:30px; color:#94a3b8; font-size:14px;">
            Recomendamos alterar sua senha após o primeiro login.<br>
            Caso tenha dúvidas, entre em contato com nosso suporte.
          </p>
        </div>

        <footer style="background-color:#0f172a; text-align:center; padding:14px; color:#64748b; font-size:13px; border-top:1px solid rgba(0,255,255,0.1);">
          &copy; {datetime.now().year} Dominando Animações • Todos os direitos reservados
        </footer>
      </div>
    </div>
    """

    return corpo_html


@app.route("/testar-email", methods=["POST"])
def testar_email():
    try:
        data = request.get_json(force=True)
        destinatario = data.get("email")
        senha = data.get("senha", "SenhaTeste123")

        if not destinatario:
            return jsonify({"ok": False, "error": "Informe um e-mail válido."}), 400

        enviar_email_credenciais(destinatario, senha)
        return jsonify({"ok": True, "msg": f"E-mail de teste enviado para {destinatario}"}), 200

    except Exception as e:
        print("❌ ERRO AO TESTAR E-MAIL:", str(e))
        return jsonify({"ok": False, "error": str(e)}), 500



# --- Inicialização ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
