import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse

from .auth.auth_routes import router as auth_router
from .dependencies.database_dependency import get_db
from .middlewares.request_middleware import limiter, request_middleware
from .routes.device_routes import router as device_router
from .routes.loan_routes import router as loan_router
from .routes.user_routes import router as user_router

load_dotenv()


def _cors_origins() -> list[str]:
    configured_origins = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:3000",
    )
    return [origin.strip() for origin in configured_origins.split(",") if origin.strip()]


def _rate_limit_handler(request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Límite de peticiones excedido. Intenta más tarde."},
    )


app = FastAPI(
    title="device_systems API",
    description=(
        "API REST segura para gestión de usuarios, dispositivos y préstamos."
    ),
    version="3.0.0",
    openapi_tags=[
        {
            "name": "Auth",
            "description": "Registro, login y sesión OAuth2 con JWT.",
        },
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
        {
            "name": "Security",
            "description": "Controles globales de seguridad y trazabilidad.",
        },
    ],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(request_middleware)

app.include_router(auth_router)
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
