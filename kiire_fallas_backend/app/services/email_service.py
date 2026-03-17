import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core.config import settings


def enviar_correo(destinatario: str, asunto: str, html: str):
    if not settings.EMAIL_ENABLED:
        raise Exception("EMAIL_ENABLED está en false")

    if not destinatario:
        raise Exception("No hay destinatario")

    msg = MIMEMultipart()
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = destinatario
    msg["Subject"] = asunto

    msg.attach(MIMEText(html, "html"))

    try:
        print("Conectando a SMTP...")
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            print("Login SMTP...")
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            print("Enviando correo...")
            server.send_message(msg)

        print("Correo enviado correctamente")
        return {"status": "ok"}

    except Exception as e:
        raise Exception(f"Error SMTP: {str(e)}")