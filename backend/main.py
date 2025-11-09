from firebase_admin import auth
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
import json
import secrets
import string
from mailer import send_email
import firebase_admin
from firebase_admin import credentials, firestore

# ==============================
# 🔧 Inicialização do Firebase
# ==============================
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
@app.post("/webhook/kirvano")
async def kirvano_webhook(payload: dict):
    """
    Webhook da Kirvano - compatível com payload real da plataforma.
    """
    try:
        # Extrai dados do payload
        email = payload.get("email")
        subscription_id = payload.get("subscriptionId")
        status = payload.get("status")

        if not email or not subscription_id:
            raise ValueError("Campos obrigatórios ausentes (email ou subscriptionId).")

        # Gera senha aleatória para o novo usuário
        alphabet = string.ascii_letters + string.digits
        plain_password = "".join(secrets.choice(alphabet) for _ in range(10))

        # Verifica se o usuário já existe
        try:
            user = auth.get_user_by_email(email)
            user_created = False  # O usuário já existe
        except auth.UserNotFoundError:
            # Se o usuário não existir, cria um novo usuário
            user = auth.create_user(
                email=email,
                password=plain_password,
                email_verified=True
            )
            user_created = True

        # Salva assinatura no Firestore
        db.collection("subscriptions").document(subscription_id).set({
            "user_id": user.uid,
            "email": email,
            "status": status,
        }, merge=True)

        # Envia o e-mail de boas-vindas com a senha temporária (se novo usuário)
        send_email(email, plain_password)

        return {
            "ok": True,
            "email": email,
            "user_created": user_created,
            "temp_password": plain_password if user_created else None
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
