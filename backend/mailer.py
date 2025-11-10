import os
import requests

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "portal@onresend.com")

def send_email(to_email: str, temp_password: str):
    subject = "Acesso ao Portal Assinaturas AI"
    body_html = f"""
    <p>Olá! 👋</p>
    <p>Sua assinatura foi confirmada com sucesso.</p>
    <p><b>Credenciais de acesso:</b><br>
    E-mail: {to_email}<br>
    Senha: {temp_password}</p>
    <p>Acesse o portal e altere sua senha assim que fizer login.</p>
    <p>Atenciosamente,<br>Portal Assinaturas AI</p>
    """

    data = {
        "from": f"Portal Assinaturas AI <{FROM_EMAIL}>",
        "to": [to_email],
        "subject": subject,
        "html": body_html
    }

    print("📨 Enviando e-mail via Resend...")
    try:
        resp = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            },
            json=data
        )
        resp.raise_for_status()
        print(f"✅ E-mail enviado para {to_email}")
    except Exception as e:
        print(f"⚠️ Erro ao enviar e-mail: {e}")
        print(f"Resposta Resend: {resp.text if 'resp' in locals() else 'sem resposta'}")
