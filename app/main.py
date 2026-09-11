from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from .database.connection import Base, engine
from .dependencies.database_dependency import get_db
from .models.user_model import User  # noqa: F401
from .routes.user_routes import router as user_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems",
    description="API para gestionar usuarios con persistencia en SQLite.",
    version="1.0.0",
)

app.include_router(user_router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "device_systems funcionando"}


@app.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
