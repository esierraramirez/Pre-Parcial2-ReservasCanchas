from datetime import datetime
from sqlmodel import Field, SQLModel

#Definición de modelos para la entidad "Cancha" en el sistema de reservas deportivas.
class CanchaBase(SQLModel):

    nombre: str = Field(min_length=3, max_length=100, index=True)
    ubicacion: str = Field(min_length=3, max_length=150)
    precio_hora: float = Field(gt=0)

# Tabla de cancha en la base de datos, con campos adicionales para gestión interna.
class CanchaID(CanchaBase, table=True):

    id: int | None = Field(default=None, primary_key=True)
    activa: bool = Field(default=True, index=True)
    fecha_eliminacion: datetime | None = Field(default=None)

# Datos opcionales para mofificar parcialmente una cancha
class CanchaUpdate(SQLModel):

    nombre: str | None = Field(default=None, min_length=3, max_length=100)
    ubicacion: str | None = Field(default=None, min_length=3, max_length=150)
    precio_hora: float | None = Field(default=None, gt=0)
    activa: bool | None = Field(default=None)
