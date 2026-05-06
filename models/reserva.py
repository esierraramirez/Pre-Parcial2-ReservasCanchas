from datetime import datetime
from sqlmodel import Field, SQLModel
from models.estado_reserva import EstadoReserva

#Datos obligatorios para crear una reserva.
class ReservaBase(SQLModel):

    cancha_id: int = Field(foreign_key="canchas.id", gt=0)
    cliente_nombre: str = Field(min_length=3, max_length=100, index=True)
    cliente_documento: str = Field(min_length=5, max_length=20, index=True)
    fecha_hora: datetime
    horas_reservadas: int = Field(gt=0, le=12)

#Tabla reservas en la base de datos
class ReservaID(ReservaBase, table=True):

    __tablename__ = "reservas"

    id: int | None = Field(default=None, primary_key=True)
    estado: EstadoReserva = Field(default=EstadoReserva.CONFIRMADA, index=True)
    valor_total: float = Field(default=0, ge=0)
    activa: bool = Field(default=True, index=True)
    fecha_eliminacion: datetime | None = Field(default=None)

#Campos opcionales para modificar parcialmente una reserva
class ReservaUpdate(SQLModel):

    cancha_id: int | None = Field(default=None, gt=0)
    cliente_nombre: str | None = Field(default=None, min_length=3, max_length=100)
    cliente_documento: str | None = Field(default=None, min_length=5, max_length=20)
    fecha_hora: datetime | None = Field(default=None)
    horas_reservadas: int | None = Field(default=None, gt=0, le=12)
    estado: EstadoReserva | None = Field(default=None)
    activa: bool | None = Field(default=None)
