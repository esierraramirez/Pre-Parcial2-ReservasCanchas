from fastapi import APIRouter, HTTPException
from db import SessionDep
from models.reserva import ReservaBase, ReservaID, ReservaUpdate

#Importamos las funciones de operaciones para reservas
from operations.operations_reserva_db import (
    create_reserva_db,
    delete_one_reserva_db,
    find_one_reserva_db,
    show_all_reservas_db,
    show_deleted_reservas_db,
    update_one_reserva_db,
)

router = APIRouter(prefix="/reservas", tags=["Reservas"])

#Endpoints para la gestión de reservas en el sistema de reservas de canchas deportivas

#Crear una nueva reserva
@router.post("", response_model=ReservaID, status_code=201)
async def create_reserva(reserva: ReservaBase, session: SessionDep):

    created = create_reserva_db(reserva, session)
    if not created:
        raise HTTPException(
            status_code=404,
            detail="No se puede crear la reserva porque la cancha no existe o está eliminada",
        )
    return created

#Consultar todas las reservas activas
@router.get("", response_model=list[ReservaID])
async def show_reservas(session: SessionDep):

    return show_all_reservas_db(session)

#Consultar las reservas eliminadas lógicamente
@router.get("/eliminadas", response_model=list[ReservaID])
async def show_deleted_reservas(session: SessionDep):
    
    return show_deleted_reservas_db(session)

#Consultar una reserva por ID
@router.get("/{reserva_id}", response_model=ReservaID)
async def show_one_reserva(reserva_id: int, session: SessionDep):

    reserva = find_one_reserva_db(reserva_id, session)
    if not reserva:
        raise HTTPException(status_code=404, detail=f"Reserva con ID {reserva_id} no encontrada")
    return reserva

#Modificar parcialmente una reserva por ID
@router.patch("/{reserva_id}", response_model=ReservaID)
async def update_reserva(reserva_id: int, reserva: ReservaUpdate, session: SessionDep):

    updated = update_one_reserva_db(reserva_id, reserva, session)
    if not updated:
        raise HTTPException(
            status_code=404,
            detail=f"Reserva con ID {reserva_id} no encontrada o cancha inválida",
        )
    return updated

#Eliminar una reserva por ID (borrado lógico)
@router.delete("/{reserva_id}", response_model=ReservaID)
async def delete_reserva(reserva_id: int, session: SessionDep):

    deleted = delete_one_reserva_db(reserva_id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Reserva con ID {reserva_id} no encontrada")
    return deleted
