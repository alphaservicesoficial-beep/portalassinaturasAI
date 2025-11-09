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
firebase_key = os.getenv("FIREBASE_KEY")

if firebase_key:
    cred = credentials.Certificate(json.loads(firebase_key))
else:
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
    email: EmailStr  # Mudamos para 'email' para estar compatível com o modelo
    status: str
    sale_id: str  # Usando 'sale_id' ao invés de 'subscriptionId'

# ==============================
@app.post("/webhook/kirvano")
async def kirvano_webhook(payload: dict):
    """
    Webhook da Kirvano - compatível com payload real da plataforma.
    """
    try:
        # Extrai os dados necessários do payload
        email = payload.get("customer", {}).get("email")  # Usando o e-mail do comprador
        status = payload.get("status")
        sale_id = payload.get("sale_id")

        # Verifica se o e-mail ou sale_id está ausente
        if not email or not sale_id:
            raise ValueError("Campos obrigatórios ausentes (email ou sale_id).")

        # Gera senha aleatória para o novo usuário
        alphabet = string.ascii_letters + string.digits
        plain_password = "".join(secrets.choice(alphabet) for _ in range(10))

        # Verifica se o usuário já existe
        try:
            user = auth.get_user_by_email(email)
            user_created = False  # O usuário já existe
            # Atualiza a senha se necessário
            auth.update_user(user.uid, password=plain_password)
            password_updated = True
        except auth.UserNotFoundError:
            # Se o usuário não existir, cria um novo usuário
            user = auth.create_user(
                email=email,
                password=plain_password,
                email_verified=True
            )
            user_created = True
            password_updated = False

        # Salva assinatura no Firestore
        db.collection("subscriptions").document(sale_id).set({
            "user_id": user.uid,
            "email": email,
            "status": status,
        }, merge=True)

        # Envia o e-mail de boas-vindas com a senha temporária
        send_email(email, plain_password)

        return {
            "ok": True,
            "email": email,
            "user_created": user_created,
            "temp_password": plain_password if user_created else None,
            "password_updated": password_updated if not user_created else None
        }

    except Exception as e:
        print(f"❌ Erro no webhook: {e}")
        return {"ok": False, "error": str(e)}


# ==============================
# 🧠 Rota simples de teste
# ==============================
@app.get("/")
def root():
    return {"message": "API do Portal Assinaturas AI está online 🚀"}
