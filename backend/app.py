import os
import smtplib
import ssl
import secrets
import string
import json
import traceback
from email.message import EmailMessage
from datetime import datetime, timezone

from flask import Flask, request, jsonify
from flask_cors import CORS  # 👈 importa o CORS
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
SENDER_NAME = os.getenv("SENDER_NAME", "Equipe Kirvano")

# --- Inicializa Flask ---
app = Flask(__name__)

# ✅ Libera o front local e o domínio do Render
CORS(app, origins=[
    "http://localhost:5173",
    "https://kirvano-frontend.onrender.com"
])

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
    """Cria um usuário no Firebase Auth, sobrescreve se já existir, e envia o e-mail"""
    try:
        email_validado = validate_email(email, check_deliverability=False).normalized
    except EmailNotValidError as e:
        return {"ok": False, "error": f"E-mail inválido: {str(e)}"}

    senha = gerar_senha()

    # 🔁 Se já existir, apaga e recria
    try:
        old_user = auth.get_user_by_email(email_validado)
        auth.delete_user(old_user.uid)
    except auth.UserNotFoundError:
        pass

    # Cria o novo usuário com senha
    user = auth.create_user(email=email_validado, password=senha)

    # Salva no Firestore
    db.collection("usuarios").document(user.uid).set({
        "email": email_validado,
        "criado_em": datetime.now(timezone.utc).isoformat()
    })

    # Envia o e-mail
    enviar_email_credenciais(email_validado, senha)

    return {"ok": True, "uid": user.uid}


# --- Rota do webhook da Kirvano ---
@app.post("/webhook/kirvano")
def kirvano_webhook():
    """Recebe notificações da Kirvano e cria usuário quando a compra é aprovada."""
    data = request.get_json(silent=True) or {}
    print("📦 Payload recebido:", data)

    # Ignora eventos não relacionados a venda aprovada
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


# --- Inicialização local ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
