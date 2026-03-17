from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class TicketCreate(BaseModel):
    nombre_reportante: str = Field(..., max_length=100)
    correo_reportante: EmailStr
    comercio: str = Field(..., max_length=150)
    titulo_error: str = Field(..., max_length=100)
    categoria: str = Field(..., max_length=50)
    prioridad: str = Field(..., max_length=20)
    descripcion: str
    imagen_url: Optional[str] = None
    responsable: Optional[str] = Field(default=None, max_length=100)
    correo_responsable: Optional[EmailStr] = None


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
    responsable: Optional[str]
    correo_responsable: Optional[EmailStr]
    estado: str

    class Config:
        from_attributes = True