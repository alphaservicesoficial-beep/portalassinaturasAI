import os
import smtplib
import ssl
import secrets
import string
import json
import traceback
import imaplib
import email
import re
from email.message import EmailMessage
from datetime import datetime, timezone
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
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://aiportalacesso.netlify.app",
]

# CORS para todas as rotas, permitindo os domínios acima
CORS(
    app,
    resources={r"/*": {"origins": ALLOWED_ORIGINS}},
    supports_credentials=True
)

# Garante headers de CORS em TODAS as respostas (inclusive preflight)
@app.after_request
def after_request(response):
    origin = request.headers.get("Origin")
    if origin in ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"]  = origin
    else:
        # se não for um origin permitido, não injeta o header (evita barulho)
        pass

    response.headers["Vary"] = "Origin"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
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
              box-shadow:0 0 25px rgba(0,255,255,0.2); overflow:visible;">
    
    <!-- Cabeçalho -->
    <div style="background:linear-gradient(90deg, #00ffff, #0077ff); 
                border-top-left-radius:16px; border-top-right-radius:16px; padding:20px 0; text-align:center;">
      <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
        <tr>
          <td align="center" valign="middle">
            <table role="presentation" cellspacing="0" cellpadding="0" border="0">
              <tr>
                <td style="padding-right:10px;">
                  <img src="cid:kirvano_logo" alt="Logo Kirvano" width="50" style="border-radius:10px;">
                </td>
                <td>
                  <h1 style="margin:0; font-size:20px; color:#fff; font-weight:800; font-family:Arial,Helvetica,sans-serif;">
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
      <h2 style="color:#00ffff;">Sua conta foi criada com sucesso!</h2>
      <p style="font-size:16px; color:#cbd5e1;">Agora você pode acessar o portal e explorar todas as ferramentas disponíveis.</p>
      <div style="background-color:#1e293b; border:1px solid rgba(0,255,255,0.3); border-radius:12px; padding:20px; margin:25px 0;">
        <p style="font-size:16px; margin:6px 0;"><strong>E-mail:</strong> {destinatario}</p>
        <p style="font-size:16px; margin:6px 0;"><strong>Senha:</strong> {senha}</p>
      </div>
      <a href="https://portal.kirvano.com"
         style="background:linear-gradient(90deg,#00ffff,#0077ff); padding:12px 30px; color:#0e1726;
                text-decoration:none; font-weight:bold; border-radius:10px; display:inline-block;">
        Acessar o Portal
      </a>
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

    if data.get("event") != "SALE_APPROVED" or data.get("status") != "APPROVED":
        return jsonify({"ok": True, "msg": "Evento ignorado"}), 200

    customer = data.get("customer", {})
    email = customer.get("email")
    nome = customer.get("name", "Cliente Kirvano")

    if not email:
        return jsonify({"ok": False, "error": "E-mail não encontrado no payload"}), 400

    produtos = data.get("products", [])
    produto_nome = produtos[0].get("name") if produtos else "Produto Kirvano"

    try:
        resultado = criar_usuario_e_enviar(email)

        db.collection("kirvano_compras").add({
            "email": email,
            "nome": nome,
            "produto": produto_nome,
            "status": data.get("status"),
            "metodo_pagamento": data.get("payment_method"),
            "data_compra": data.get("created_at"),
            "sale_id": data.get("sale_id"),
            "valor_total": data.get("total_price"),
            "criado_em": datetime.now(timezone.utc).isoformat()
        })

        return jsonify({
            "ok": True,
            "msg": "Usuário criado e e-mail enviado com sucesso",
            "uid": resultado["uid"]
        }), 200

    except Exception as e:
        print("❌ ERRO NO WEBHOOK:")
        print(traceback.format_exc())
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/gerar-codigo", methods=["POST", "OPTIONS"])
def gerar_codigo():
    # 1️⃣ Preflight: navegador testa antes do POST real
    if request.method == "OPTIONS":
        resp = make_response("", 204)  # 204 = no content
        origin = request.headers.get("Origin")
        if origin in ALLOWED_ORIGINS:
            resp.headers["Access-Control-Allow-Origin"] = origin
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return resp

    # 2️⃣ POST normal (a partir daqui é o código de verdade)
    try:
        data = request.get_json(silent=True) or {}
        email_usuario = data.get("email")

        if not email_usuario:
            return jsonify({"ok": False, "error": "E-mail do usuário não informado"}), 400

        # --- Limite de 2 códigos por dia ---
        hoje = datetime.now(timezone.utc).date()
        ref = db.collection("codigos_gerados").document(email_usuario)
        doc = ref.get()

        if doc.exists:
            dados = doc.to_dict()
            ultima_data = dados.get("data")
            total = dados.get("total", 0)

            if ultima_data == str(hoje) and total >= 2:
                return jsonify({"ok": False, "error": "Limite diário de 2 códigos atingido"}), 403
            elif ultima_data == str(hoje):
                ref.update({"total": total + 1})
            else:
                ref.set({"data": str(hoje), "total": 1})
        else:
            ref.set({"data": str(hoje), "total": 1})

        # --- Leitura do e-mail IMAP ---
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        result, data = mail.search(None, "ALL")
        mail_ids = data[0].split()
        if not mail_ids:
            return jsonify({"ok": False, "error": "Nenhum e-mail encontrado"}), 404

        latest_email_id = mail_ids[-1]
        result, data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload(decode=True).decode(errors="ignore")
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        match = re.search(r"\b\d{6}\b", body)
        code = match.group() if match else None

        if not code:
            return jsonify({"ok": False, "error": "Código não encontrado"}), 404

        return jsonify({"ok": True, "code": code}), 200

    except Exception as e:
        print("❌ ERRO AO LER CÓDIGO:")
        print(traceback.format_exc())
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


# --- Inicialização ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
