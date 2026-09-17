from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from .dependencies.database_dependency import get_db
from .routes.device_routes import router as device_router
from .routes.loan_routes import router as loan_router
from .routes.user_routes import router as user_router

app = FastAPI(
    title="device_systems",
    description=(
        "API para gestionar usuarios, dispositivos y préstamos con "
        "persistencia en SQLite."
    ),
    version="2.0.0",
    openapi_tags=[
        {
            "name": "Users",
            "description": "Operaciones CRUD y filtros de usuarios.",
        },
        {
            "name": "Devices",
            "description": "Administración y búsqueda de dispositivos tecnológicos.",
        },
        {
            "name": "Loans",
            "description": "Préstamos, devoluciones, joins e historial.",
        },
        {
            "name": "Health",
            "description": "Comprobaciones de disponibilidad de la API y la base de datos.",
        },
    ],
)

app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "device_systems funcionando"}


@app.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
