import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

# Neon puede llamarse DATABASE_URL_NEON o DATABASE_URL según la plataforma.
neon_db = os.getenv("DATABASE_URL_NEON") or os.getenv("DATABASE_URL")

# Fallback local para que el servidor también pueda iniciar sin Neon mientras pruebas.
sqlite_name = "reservas_canchas.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

if neon_db:
    # Algunas plataformas entregan postgres:// y SQLAlchemy espera postgresql://
    database_url = neon_db.replace("postgres://", "postgresql://", 1)
    engine = create_engine(database_url, echo=False)
else:
    engine = create_engine(
        sqlite_url,
        echo=False,
        connect_args={"check_same_thread": False},
    )


def create_all_tables(app: FastAPI):
    """
    Crea las tablas al iniciar el servidor.
    En Neon crea las tablas si no existen. En local usa SQLite como respaldo.
    """
    SQLModel.metadata.create_all(engine)
    yield


def get_session() -> Session:
    """Entrega una sesión de base de datos por cada petición."""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
