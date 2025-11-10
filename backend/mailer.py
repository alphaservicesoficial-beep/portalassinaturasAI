import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_EMAIL = os.getenv("SMTP_EMAIL")  # testeconcursopdf@gmail.com
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # senha de app do Gmail
FROM_NAME = os.getenv("FROM_NAME", "Portal Assinaturas AI")


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

    # Cria a mensagem MIME
    msg = MIMEMultipart("alternative")
    msg["From"] = f"{FROM_NAME} <{SMTP_EMAIL}>"
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body_html, "html"))

    print("📨 Enviando e-mail via Gmail SMTP...")

    try:
        # Conecta ao servidor SMTP do Gmail
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # segurança
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)

        print(f"✅ E-mail enviado com sucesso para {to_email}")
        return True

    except Exception as e:
        print(f"⚠️ Erro ao enviar e-mail: {e}")
        return False
