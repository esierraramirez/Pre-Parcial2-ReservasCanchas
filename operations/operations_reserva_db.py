from datetime import datetime
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from models.estado_reserva import EstadoReserva
from models.reserva import ReservaBase, ReservaID, ReservaUpdate
from operations.operations_cancha_db import find_one_cancha_db

#Funcion para calcular el valor total de la reserva 
def _calculate_total(cancha_price: float, horas: int) -> float:

    return round(cancha_price * horas, 2)

