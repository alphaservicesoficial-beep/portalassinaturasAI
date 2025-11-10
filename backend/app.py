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
from flask import Flask, request, jsonify
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
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SENDER_NAME = os.getenv("SENDER_NAME", "Kirvano")

# --- Configurações de leitura de código (IMAP Gmail) ---
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")
IMAP_SERVER = "imap.gmail.com"

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "https://seusite.com"])

# --- Funções auxiliares ---

def gerar_senha(tamanho: int = 10) -> str:
    caracteres = string.ascii_letters + string.digits
    return "".join(secrets.choice(caracteres) for _ in range(tamanho))

def enviar_email_credenciais(destinatario: str, senha: str):
    assunto = "Acesso à sua conta Kirvano"
    corpo = f"""Olá!

Sua conta foi criada com sucesso.

E-mail: {destinatario}
Senha:  {senha}

Recomendamos alterar sua senha após o primeiro login.

Atenciosamente,
{SENDER_NAME}
"""

    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = f"{SENDER_NAME} <{EMAIL_USER}>"
    msg["To"] = destinatario
    msg.set_content(corpo)

    contexto = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls(context=contexto)
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

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

# --- Webhook da Kirvano ---
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

# --- Nova rota: leitura do último código do e-mail ---
@app.get("/gerar-codigo")
def gerar_codigo():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(GMAIL_USER, GMAIL_PASS)
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
                    body += part.get_payload(decode=True).decode()
        else:
            body = msg.get_payload(decode=True).decode()

        match = re.search(r"\b\d{6}\b", body)
        code = match.group() if match else None

        if not code:
            return jsonify({"ok": False, "error": "Código não encontrado"}), 404

        return jsonify({"ok": True, "code": code}), 200

    except Exception as e:
        print("❌ ERRO AO LER CÓDIGO:")
        print(traceback.format_exc())
        return jsonify({"ok": False, "error": str(e)}), 500

# --- Inicialização ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
