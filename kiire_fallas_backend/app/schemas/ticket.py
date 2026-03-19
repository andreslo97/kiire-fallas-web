from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class TicketUpdateEstado(BaseModel):
    estado: str = Field(..., max_length=20)


class TicketUpdateResponsable(BaseModel):
    responsable: str = Field(..., max_length=100)
    correo_responsable: EmailStr


class TicketResponse(BaseModel):
    id: int
    ticket_codigo: Optional[str]
    fecha_reporte: datetime
    fecha_actualizacion: datetime
    nombre_reportante: str
    correo_reportante: EmailStr
    comercio: str
    titulo_error: str
    categoria: str
    prioridad: str
    descripcion: str
    imagen_url: Optional[str]
    observacion: Optional[str]
    responsable: Optional[str]
    correo_responsable: Optional[EmailStr]
    estado: str

    class Config:
        from_attributes = True