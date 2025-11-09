import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_NAME = os.getenv("FROM_NAME", "Portal Assinaturas")

def send_email(to_email: str, temp_password: str):
    subject = "Acesso ao Portal Assinaturas AI"
    body = f"""
    Olá! 👋<br><br>
    Sua assinatura foi confirmada.<br><br>
    <b>Credenciais de acesso:</b><br>
    E-mail: {to_email}<br>
    Senha: {temp_password}<br><br>
    Acesse o portal e altere sua senha assim que fizer login.<br><br>
    Atenciosamente,<br>
    {FROM_NAME}
    """

    msg = MIMEMultipart()
    msg["From"] = f"{FROM_NAME} <{SMTP_EMAIL}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"✅ E-mail enviado para {to_email}")
    except Exception as e:
        print(f"⚠️ Erro ao enviar e-mail: {e}")
