from datetime import datetime
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from models.estado_reserva import EstadoReserva
from models.reserva import ReservaBase, ReservaID, ReservaUpdate
from operations.operations_cancha_db import find_one_cancha_db

#Funcion para calcular el valor total de la reserva 
def _calculate_total(cancha_price: float, horas: int) -> float:

    return round(cancha_price * horas, 2)

#Funcion para Crear una reserva si la cancha existe y está activa
def create_reserva_db(reserva: ReservaBase, session: Session) -> ReservaID | None:

    cancha = find_one_cancha_db(reserva.cancha_id, session)
    if cancha is None:
        return None

    new_reserva = ReservaID.model_validate(reserva)
    new_reserva.valor_total = _calculate_total(cancha.precio_hora, reserva.horas_reservadas)
    session.add(new_reserva)
    session.commit()
    session.refresh(new_reserva)
    return new_reserva