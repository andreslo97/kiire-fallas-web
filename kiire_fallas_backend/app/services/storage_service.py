from uuid import uuid4
from urllib.parse import quote

import httpx

from app.core.config import settings


def subir_imagen_ticket(nombre_archivo: str, contenido: bytes, content_type: str) -> str:
    extension = ""
    if "." in nombre_archivo:
        extension = nombre_archivo[nombre_archivo.rfind("."):].lower()

    nombre_unico = f"tickets/{uuid4()}{extension}"

    upload_url = (
        f"{settings.SUPABASE_URL}/storage/v1/object/"
        f"{settings.SUPABASE_BUCKET}/{nombre_unico}"
    )

    headers = {
        "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
        "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
        "Content-Type": content_type or "application/octet-stream",
        "x-upsert": "false",
    }

    response = httpx.post(
        upload_url,
        headers=headers,
        content=contenido,
        timeout=60.0,
    )

    if response.status_code >= 400:
        raise Exception(f"{response.status_code} - {response.text}")

    nombre_unico_encoded = quote(nombre_unico, safe="/")
    url_publica = (
        f"{settings.SUPABASE_URL}/storage/v1/object/public/"
        f"{settings.SUPABASE_BUCKET}/{nombre_unico_encoded}"
    )

    return url_publica