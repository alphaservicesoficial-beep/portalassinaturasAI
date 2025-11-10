import os
import requests
from dotenv import load_dotenv

# 🔧 Carrega variáveis de ambiente do .env (opcional em produção)
load_dotenv()

# 🔑 Variáveis do Render (.env ou configuradas no painel)
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
FROM_NAME = os.getenv("FROM_NAME", "Portal Assinaturas AI")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@portalassinaturas.ai")

def send_email(to_email: str, temp_password: str):
    """
    Envia e-mail de boas-vindas usando a API HTTPS do Resend.
    Compatível com Render Free Plan.
    """

    subject = "Acesso ao Portal Assinaturas AI"
    html_body = f"""
    <p>Olá! 👋</p>
    <p>Sua assinatura foi confirmada com sucesso.</p>
    <b>Credenciais de acesso:</b><br>
    E-mail: {to_email}<br>
    Senha: {temp_password}<br><br>
    <p>Acesse o portal e altere sua senha assim que fizer login.</p>
    <p>Atenciosamente,<br>{FROM_NAME}</p>
    """

    data = {
        "from": f"{FROM_NAME} <{FROM_EMAIL}>",
        "to": [to_email],
        "subject": subject,
        "html": html_body
    }

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        print("📤 Enviando e-mail via Resend...")

        # Timeout evita travar indefinidamente caso o Render perca rede
        response = requests.post(
            "https://api.resend.com/emails",
            json=data,
            headers=headers,
            timeout=10
        )

        print(f"🔎 Resposta Resend: {response.status_code} - {response.text}")

        response.raise_for_status()
        print(f"✅ E-mail enviado para {to_email}")
        return True

    except requests.exceptions.Timeout:
        print("⏱️ Erro: Timeout ao tentar conectar com o Resend.")
        return False

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Erro na requisição ao Resend: {e}")
        return False

    except Exception as e:
        print(f"❌ Erro inesperado no envio de e-mail: {e}")
        return False
