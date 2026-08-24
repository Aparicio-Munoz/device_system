from fastapi import FastAPI, Request

from app.routes.user_routes import router as user_router

app = FastAPI(
    title="Device Systems API",
    version="1.0",
    description="API REST para la gestión de usuarios de device_systems.",
)


@app.get("/", tags=["Health"])
def health_check():
    return {"message": "API funcionando"}


@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    response = await call_next(request)

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    return response


app.include_router(user_router)
