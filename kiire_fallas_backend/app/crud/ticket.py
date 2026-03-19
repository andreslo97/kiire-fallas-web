from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.schemas.ticket import TicketUpdateEstado, TicketUpdateResponsable
from app.services.ticket_code_service import generar_ticket_codigo


def crear_ticket(
    db: Session,
    nombre_reportante: str,
    correo_reportante: str,
    comercio: str,
    titulo_error: str,
    categoria: str,
    prioridad: str,
    descripcion: str,
    imagen_url: str | None = None,
) -> Ticket:

    if not nombre_reportante or not nombre_reportante.strip():
        raise HTTPException(status_code=400, detail="El nombre del reportante es obligatorio")

    if not correo_reportante or not correo_reportante.strip():
        raise HTTPException(status_code=400, detail="El correo del reportante es obligatorio")

    if not comercio or not comercio.strip():
        raise HTTPException(status_code=400, detail="El comercio es obligatorio")

    if not titulo_error or not titulo_error.strip():
        raise HTTPException(status_code=400, detail="El título del error es obligatorio")

    if not categoria or not categoria.strip():
        raise HTTPException(status_code=400, detail="La categoría es obligatoria")

    if not prioridad or not prioridad.strip():
        raise HTTPException(status_code=400, detail="La prioridad es obligatoria")

    if not descripcion or not descripcion.strip():
        raise HTTPException(status_code=400, detail="La descripción es obligatoria")

    nuevo_ticket = Ticket(
        nombre_reportante=nombre_reportante.strip(),
        correo_reportante=correo_reportante.strip(),
        comercio=comercio.strip(),
        titulo_error=titulo_error.strip(),
        categoria=categoria.strip(),
        prioridad=prioridad.strip(),
        descripcion=descripcion.strip(),
        imagen_url=imagen_url,
        observacion=None,
        responsable="Andrés Loaiza",
        correo_responsable="jloaiza037@grupo-exito.com",
        estado="Abierto",
    )

    db.add(nuevo_ticket)
    db.commit()
    db.refresh(nuevo_ticket)

    nuevo_ticket.ticket_codigo = generar_ticket_codigo(nuevo_ticket.id)
    db.commit()
    db.refresh(nuevo_ticket)

    return nuevo_ticket


def listar_tickets(db: Session):
    return db.query(Ticket).order_by(Ticket.fecha_reporte.desc()).all()


def obtener_ticket_por_id(db: Session, ticket_id: int):
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()


def actualizar_estado(db: Session, ticket: Ticket, data: TicketUpdateEstado):
    ticket.estado = data.estado
    db.commit()
    db.refresh(ticket)
    return ticket


def actualizar_responsable(db: Session, ticket: Ticket, data: TicketUpdateResponsable):
    ticket.responsable = data.responsable
    ticket.correo_responsable = data.correo_responsable
    db.commit()
    db.refresh(ticket)
    return ticket