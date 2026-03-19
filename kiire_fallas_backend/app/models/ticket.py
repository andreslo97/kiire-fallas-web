from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.core.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_codigo = Column(String(20), unique=True, nullable=True, index=True)

    fecha_reporte = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    fecha_actualizacion = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    nombre_reportante = Column(String(100), nullable=False)
    correo_reportante = Column(String(150), nullable=False)

    comercio = Column(String(150), nullable=False)

    titulo_error = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False)
    prioridad = Column(String(20), nullable=False)

    descripcion = Column(Text, nullable=False)
    imagen_url = Column(Text, nullable=True)
    observacion = Column(Text, nullable=True)

    responsable = Column(String(100), nullable=True)
    correo_responsable = Column(String(150), nullable=True)

    estado = Column(String(20), nullable=False, default="Abierto")