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

#Funcion para visualizar reservas activas
def show_all_reservas_db(session: Session) -> list[ReservaID]:

    statement = select(ReservaID).where(ReservaID.activa == True)  # noqa: E712
    return session.exec(statement).all()

#Lista las reservas eliminadas
def show_deleted_reservas_db(session: Session) -> list[ReservaID]:

    statement = select(ReservaID).where(ReservaID.activa == False)  # noqa: E712
    return session.exec(statement).all()

#Funcion para buscar una reserva por ID. Por defecto solo responde si está activa.
def find_one_reserva_db(reserva_id: int, session: Session, include_deleted: bool = False) -> ReservaID | None:

    try:
        reserva = session.get_one(ReservaID, reserva_id)
        if not include_deleted and not reserva.activa:
            return None
        return reserva
    except NoResultFound:
        return None

#Actualiza parcialmente una reserva y recalcula el valor total si aplica
def update_one_reserva_db(reserva_id: int, new_data: ReservaUpdate, session: Session) -> ReservaID | None:
    
    reserva = find_one_reserva_db(reserva_id, session, include_deleted=True)
    if reserva is None:
        return None

    reserva_update = new_data.model_dump(exclude_unset=True)

    if "cancha_id" in reserva_update:
        cancha = find_one_cancha_db(reserva_update["cancha_id"], session)
        if cancha is None:
            return None
    else:
        cancha = find_one_cancha_db(reserva.cancha_id, session, include_deleted=True)

    if reserva_update.get("activa") is True:
        reserva_update["fecha_eliminacion"] = None
        if reserva.estado == EstadoReserva.CANCELADA:
            reserva_update["estado"] = EstadoReserva.CONFIRMADA

    for field, value in reserva_update.items():
        setattr(reserva, field, value)

    if cancha is not None:
        reserva.valor_total = _calculate_total(cancha.precio_hora, reserva.horas_reservadas)

    session.add(reserva)
    session.commit()
    session.refresh(reserva)
    return reserva

#Elimina una reserva pasandola a inactiva
def delete_one_reserva_db(reserva_id: int, session: Session) -> ReservaID | None:

    reserva = find_one_reserva_db(reserva_id, session)
    if reserva is None:
        return None

    reserva.activa = False
    reserva.estado = EstadoReserva.CANCELADA
    reserva.fecha_eliminacion = datetime.utcnow()
    session.add(reserva)
    session.commit()
    session.refresh(reserva)
    return reserva
