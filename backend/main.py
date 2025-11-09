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
    Webhook da Kirvano:
    Recebe o evento de compra e cria o usuário no Firebase + envia e-mail.
    """
    # Extrai os dados conforme o formato real do webhook da Kirvano
    try:
        email = payload.get("customer", {}).get("email")
        subscription_id = payload.get("sale_id")
        status = payload.get("status", "UNKNOWN")

        if not email or not subscription_id:
            return {"ok": False, "error": "Campos obrigatórios ausentes."}

        # Gera senha temporária
        import secrets, string
        alphabet = string.ascii_letters + string.digits
        plain_password = ''.join(secrets.choice(alphabet) for _ in range(10))

        # Verifica/cria usuário
        try:
            user = auth.get_user_by_email(email)
            created = False
        except auth.UserNotFoundError:
            user = auth.create_user(
                email=email,
                password=plain_password,
                email_verified=True
            )
            created = True

        # Salva no Firestore
        db.collection("subscriptions").document(subscription_id).set({
            "user_id": user.uid,
            "email": email,
            "status": status
        }, merge=True)

        # Envia o e-mail com senha se for novo
        if created:
            send_email(email, plain_password)

        return {
            "ok": True,
            "user_created": created,
            "email": email,
            "temp_password": plain_password if created else None
        }

    except Exception as e:
        print(f"⚠️ Erro no webhook: {e}")
        return {"ok": False, "error": str(e)}



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
