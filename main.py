from fastapi import FastAPI

# Importar modelos antes de crear las tablas permite que SQLModel registre la metadata.
from models.cancha import CanchaID  # noqa: F401
from models.reserva import ReservaID  # noqa: F401
from db import create_all_tables
from routes.cancha_routes import router as cancha_router
from routes.reserva_routes import router as reserva_router

app = FastAPI(
    title="API de Reservas de Canchas Deportivas",
    description="Proyecto FastAPI conectado a Neon DB con dos tablas: canchas y reservas.",
    version="1.0.0",
    lifespan=create_all_tables,
)

app.include_router(cancha_router)
app.include_router(reserva_router)


@app.get("/", tags=["Inicio"])
async def root():
    return {
        "message": "API de reservas de canchas deportivas funcionando correctamente",
        "docs": "/docs",
    }
