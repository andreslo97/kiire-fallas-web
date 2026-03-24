from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.ticket import (
    crear_ticket,
    listar_tickets,
    obtener_ticket_por_id,
    actualizar_estado,
    actualizar_responsable,
    cerrar_ticket,
)
from app.schemas.ticket import (
    TicketResponse,
    TicketUpdateEstado,
    TicketUpdateResponsable,
    TicketCerrarCaso,
)
from app.services.email_service import enviar_correo
from app.services.storage_service import subir_imagen_ticket
from app.utils.constants import ESTADOS_VALIDOS, PRODUCTOS_VALIDOS

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("", response_model=TicketResponse)
async def crear_ticket_endpoint(
    nombre_reportante: str = Form(...),
    correo_reportante: str = Form(...),
    comercio: str = Form(...),
    nit: str = Form(...),
    titulo_error: str = Form(...),
    producto: str = Form(...),
    prioridad: str = Form(...),
    descripcion: str = Form(...),
    imagen: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    if producto not in PRODUCTOS_VALIDOS:
        raise HTTPException(status_code=400, detail="Producto no válido")

    imagen_url = None

    if imagen:
        contenido = await imagen.read()

        try:
            imagen_url = subir_imagen_ticket(
                nombre_archivo=imagen.filename,
                contenido=contenido,
                content_type=imagen.content_type,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error subiendo imagen: {str(e)}")

    ticket = crear_ticket(
        db=db,
        nombre_reportante=nombre_reportante,
        correo_reportante=correo_reportante,
        comercio=comercio,
        nit=nit,
        titulo_error=titulo_error,
        producto=producto,
        prioridad=prioridad,
        descripcion=descripcion,
        imagen_url=imagen_url,
    )

    asunto = f"Confirmación de ticket creado: {ticket.ticket_codigo}"
    html = f"""
    <h2>Tu ticket fue creado correctamente</h2>
    <p>Hemos recibido tu reporte en Kiire Fallas.</p>
    <p><strong>Código del ticket:</strong> {ticket.ticket_codigo}</p>
    <p><strong>Comercio:</strong> {ticket.comercio}</p>
    <p><strong>NIT:</strong> {ticket.nit}</p>
    <p><strong>Título:</strong> {ticket.titulo_error}</p>
    <p><strong>Producto:</strong> {ticket.producto}</p>
    <p><strong>Prioridad:</strong> {ticket.prioridad}</p>
    <p><strong>Estado inicial:</strong> {ticket.estado}</p>
    <p><strong>Descripción:</strong> {ticket.descripcion}</p>
    <p>Conserva este código para hacer seguimiento.</p>
    """

    try:
        resultado_email = enviar_correo(ticket.correo_reportante, asunto, html)
        print("Correo enviado correctamente:", resultado_email)
    except Exception as e:
        print("Error enviando correo:", str(e))

    return ticket


@router.get("", response_model=list[TicketResponse])
def listar_tickets_endpoint(db: Session = Depends(get_db)):
    return listar_tickets(db)


@router.get("/{ticket_id}", response_model=TicketResponse)
def obtener_ticket_endpoint(ticket_id: int, db: Session = Depends(get_db)):
    ticket = obtener_ticket_por_id(db, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    return ticket


@router.put("/{ticket_id}/estado", response_model=TicketResponse)
def actualizar_estado_endpoint(
    ticket_id: int,
    data: TicketUpdateEstado,
    db: Session = Depends(get_db),
):
    if data.estado not in ESTADOS_VALIDOS:
        raise HTTPException(status_code=400, detail="Estado no válido")

    ticket = obtener_ticket_por_id(db, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    return actualizar_estado(db, ticket, data)


@router.put("/{ticket_id}/responsable", response_model=TicketResponse)
def actualizar_responsable_endpoint(
    ticket_id: int,
    data: TicketUpdateResponsable,
    db: Session = Depends(get_db),
):
    ticket = obtener_ticket_por_id(db, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    ticket_actualizado = actualizar_responsable(db, ticket, data)

    if data.correo_responsable:
        asunto = f"Nuevo ticket asignado: {ticket.ticket_codigo}"
        html = f"""
        <h2>Se te ha asignado un ticket</h2>
        <p><strong>Código:</strong> {ticket.ticket_codigo}</p>
        <p><strong>Comercio:</strong> {ticket.comercio}</p>
        <p><strong>NIT:</strong> {ticket.nit}</p>
        <p><strong>Error:</strong> {ticket.titulo_error}</p>
        <p><strong>Producto:</strong> {ticket.producto}</p>
        <p><strong>Estado:</strong> {ticket.estado}</p>
        <p><strong>Descripción:</strong> {ticket.descripcion}</p>
        """

        try:
            resultado_email = enviar_correo(data.correo_responsable, asunto, html)
            print("Correo enviado correctamente:", resultado_email)
        except Exception as e:
            print("Error enviando correo:", str(e))

    return ticket_actualizado


@router.put("/{ticket_id}/cerrar", response_model=TicketResponse)
def cerrar_ticket_endpoint(
    ticket_id: int,
    data: TicketCerrarCaso,
    db: Session = Depends(get_db),
):
    ticket = obtener_ticket_por_id(db, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    ticket_actualizado = cerrar_ticket(db, ticket, data)

    asunto = f"Tu caso fue cerrado: {ticket_actualizado.ticket_codigo}"
    html = f"""
    <h2>Tu caso ha sido cerrado</h2>
    <p><strong>Código del ticket:</strong> {ticket_actualizado.ticket_codigo}</p>
    <p><strong>Comercio:</strong> {ticket_actualizado.comercio}</p>
    <p><strong>NIT:</strong> {ticket_actualizado.nit}</p>
    <p><strong>Título:</strong> {ticket_actualizado.titulo_error}</p>
    <p><strong>Producto:</strong> {ticket_actualizado.producto}</p>
    <p><strong>Estado:</strong> {ticket_actualizado.estado}</p>
    <p><strong>Descripción inicial:</strong> {ticket_actualizado.descripcion}</p>
    <p><strong>Observación de cierre:</strong> {ticket_actualizado.observacion}</p>
    """

    try:
        resultado_email = enviar_correo(ticket_actualizado.correo_reportante, asunto, html)
        print("Correo enviado correctamente:", resultado_email)
    except Exception as e:
        print("Error enviando correo:", str(e))

    return ticket_actualizado