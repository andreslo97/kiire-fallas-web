import httpx

from app.core.config import settings


def enviar_correo(destinatario: str, asunto: str, html: str) -> dict:
    if not settings.EMAIL_ENABLED:
        raise Exception("EMAIL_ENABLED está en false")

    if not destinatario:
        raise Exception("No hay destinatario")

    if not settings.BREVO_API_KEY:
        raise Exception("Falta BREVO_API_KEY en el .env")

    if not settings.EMAIL_FROM_ADDRESS or not settings.EMAIL_FROM_NAME:
        raise Exception("Falta EMAIL_FROM_NAME o EMAIL_FROM_ADDRESS en el .env")

    payload = {
        "sender": {
            "name": settings.EMAIL_FROM_NAME,
            "email": settings.EMAIL_FROM_ADDRESS,
        },
        "to": [
            {
                "email": destinatario,
            }
        ],
        "subject": asunto,
        "htmlContent": html,
    }

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json",
    }

    response = httpx.post(
        "https://api.brevo.com/v3/smtp/email",
        headers=headers,
        json=payload,
        timeout=30.0,
    )

    if response.status_code >= 400:
        raise Exception(f"Error Brevo {response.status_code}: {response.text}")

    return response.json()