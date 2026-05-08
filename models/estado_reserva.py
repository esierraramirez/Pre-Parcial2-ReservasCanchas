from enum import Enum

class EstadoReserva(str, Enum):
    CONFIRMADA = "confirmada"
    PENDIENTE = "pendiente"
    CANCELADA = "cancelada"
    FINALIZADA = "finalizada"
