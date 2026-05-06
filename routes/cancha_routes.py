from fastapi import APIRouter, HTTPException
from db import SessionDep
from models.cancha import CanchaBase, CanchaID, CanchaUpdate

#Importamos las funciones de operaciones para canchas
from operations.operations_cancha_db import (
    create_cancha_db,
    delete_one_cancha_db,
    find_one_cancha_db,
    show_all_canchas_db,
    show_deleted_canchas_db,
    update_one_cancha_db,
)

router = APIRouter(prefix="/canchas", tags=["Canchas"])

#Endpoints para la gestión de canchas deportivas en el sistema de reservas

#Crear una nueva cancha
@router.post("", response_model=CanchaID, status_code=201)
async def create_cancha(cancha: CanchaBase, session: SessionDep):

    return create_cancha_db(cancha, session)

#Consultar todas las canchas activas
@router.get("", response_model=list[CanchaID])
async def show_canchas(session: SessionDep):

    return show_all_canchas_db(session)

#Consultar canchas eliminadas lógicamente
@router.get("/eliminadas", response_model=list[CanchaID])
async def show_deleted_canchas(session: SessionDep):

    return show_deleted_canchas_db(session)

#Consultar una cancha por ID
@router.get("/{cancha_id}", response_model=CanchaID)
async def show_one_cancha(cancha_id: int, session: SessionDep):

    cancha = find_one_cancha_db(cancha_id, session)
    if not cancha:
        raise HTTPException(status_code=404, detail=f"Cancha con ID {cancha_id} no encontrada")
    return cancha

#Modificar parcialmente una cancha por ID
@router.patch("/{cancha_id}", response_model=CanchaID)
async def update_cancha(cancha_id: int, cancha: CanchaUpdate, session: SessionDep):

    updated = update_one_cancha_db(cancha_id, cancha, session)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Cancha con ID {cancha_id} no encontrada")
    return updated

#Eliminar una cancha por ID (borrado lógico)
@router.delete("/{cancha_id}", response_model=CanchaID)
async def delete_cancha(cancha_id: int, session: SessionDep):

    deleted = delete_one_cancha_db(cancha_id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Cancha con ID {cancha_id} no encontrada")
    return deleted
