from datetime import datetime
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from models.cancha import CanchaBase, CanchaID, CanchaUpdate

#Funcion para Crear una cancha en la tabla de canchas
def create_cancha_db(cancha: CanchaBase, session: Session) -> CanchaID:
    
    new_cancha = CanchaID.model_validate(cancha)
    session.add(new_cancha)
    session.commit()
    session.refresh(new_cancha)
    return new_cancha

#Funcion para visualizar canchas activas
def show_all_canchas_db(session: Session) -> list[CanchaID]:

    statement = select(CanchaID).where(CanchaID.activa == True)  # noqa: E712
    return session.exec(statement).all()

#Lista las canchas eliminadas lógicamente
def show_deleted_canchas_db(session: Session) -> list[CanchaID]:

    statement = select(CanchaID).where(CanchaID.activa == False)  # noqa: E712
    return session.exec(statement).all()

#Busca una cancha por ID. Por defecto solo responde si está activa
def find_one_cancha_db(cancha_id: int, session: Session, include_deleted: bool = False) -> CanchaID | None:

    try:
        cancha = session.get_one(CanchaID, cancha_id)
        if not include_deleted and not cancha.activa:
            return None
        return cancha
    except NoResultFound:
        return None
    
#Actualizacion parcial de cancha
def update_one_cancha_db(cancha_id: int, new_data: CanchaUpdate, session: Session) -> CanchaID | None:
    """Actualiza parcialmente una cancha."""
    cancha = find_one_cancha_db(cancha_id, session, include_deleted=True)
    if cancha is None:
        return None

    cancha_update = new_data.model_dump(exclude_unset=True)

    # Si se reactiva una cancha, se borra la fecha de eliminación.
    if cancha_update.get("activa") is True:
        cancha_update["fecha_eliminacion"] = None

    for field, value in cancha_update.items():
        setattr(cancha, field, value)

    session.add(cancha)
    session.commit()
    session.refresh(cancha)
    return cancha
