import os
import json
import secrets
import string
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
import firebase_admin
from firebase_admin import credentials, auth, firestore
from mailer import send_email

# ==============================
# 🔧 Inicialização do Firebase
# ==============================
# Se a chave estiver no Render (como variável FIREBASE_KEY)
firebase_key = os.getenv("FIREBASE_KEY")

if firebase_key:
    # Lê a chave do ambiente (Render)
    cred = credentials.Certificate(json.loads(firebase_key))
else:
    # Ambiente local: usa o arquivo físico
    cred_path = os.path.join(os.path.dirname(__file__), "firebase-key.json")
    cred = credentials.Certificate(cred_path)

firebase_admin.initialize_app(cred)
db = firestore.client()


# ==============================
# 🚀 Inicialização do FastAPI
# ==============================
app = FastAPI(title="Portal Assinaturas Backend", version="1.0.0")


# ==============================
# 📦 Modelo de dados da Kirvano
# ==============================
class KirvanoPayload(BaseModel):
    email: EmailStr
    subscriptionId: str
    status: str


# ==============================
# 🔗 Webhook da Kirvano
# ==============================
@app.post("/webhook/kirvano")
async def kirvano_webhook(payload: dict):
    """
    Recebe o webhook da Kirvano:
    - Cria usuário no Firebase Auth (se não existir)
    - Salva assinatura no Firestore
    - Envia o e-mail com senha gerada
    """
    # Log para debug
    print("🔔 Webhook recebido:", payload)

    # Extrai informações com segurança
    email = (
        payload.get("email")
        or payload.get("buyer_email")
        or payload.get("client", {}).get("email")
    )

    subscription = payload.get("subscription", {})
    subscription_id = subscription.get("id") or payload.get("subscriptionId")
    status = subscription.get("status") or payload.get("status", "unknown")

    if not email or not subscription_id:
        return {"ok": False, "error": "Campos ausentes", "payload": payload}

    # Gera senha aleatória
    import secrets, string
    alphabet = string.ascii_letters + string.digits
    plain_password = ''.join(secrets.choice(alphabet) for _ in range(10))

    try:
        # Verifica se o usuário já existe
        user = auth.get_user_by_email(email)
        created = False
    except auth.UserNotFoundError:
        # Cria novo usuário
        user = auth.create_user(
            email=email,
            password=plain_password,
            email_verified=True
        )
        created = True

    # Salva assinatura no Firestore
    db.collection("subscriptions").document(subscription_id).set({
        "user_id": user.uid,
        "email": email,
        "status": status
    }, merge=True)

    # Envia e-mail se for novo usuário
    if created:
        try:
            send_email(email, plain_password)
        except Exception as e:
            print(f"⚠️ Erro ao enviar e-mail para {email}: {e}")

    return {
        "ok": True,
        "user_created": created,
        "email": email,
        "temp_password": plain_password if created else None
    }


# ==============================
# 🧠 Rota simples de teste
# ==============================
@app.get("/")
def root():
    return {"message": "API do Portal Assinaturas AI está online 🚀"}


# ==============================
# Execução local (modo dev)
# ==============================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8001)))
