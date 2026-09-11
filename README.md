# device_systems

API REST de usuarios creada con FastAPI, SQLAlchemy, Pydantic y SQLite.

## Ejecutar el proyecto

```bash
venv/bin/uvicorn app.main:app --reload
```

Documentación:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Estructura

- `app/database/connection.py`: engine, sesiones y Base.
- `app/models/user_model.py`: tabla `users` de SQLAlchemy.
- `app/schemas/user_schema.py`: validaciones Pydantic.
- `app/dependencies/database_dependency.py`: sesión para los endpoints.
- `app/services/user_service.py`: operaciones CRUD y reglas de negocio.
- `app/routes/user_routes.py`: endpoints `/users`.

## Endpoints principales

- `POST /users`: crear usuario.
- `GET /users`: listar y filtrar por `role` o `is_active`.
- `GET /users/{user_id}`: consultar por ID.
- `PUT /users/{user_id}`: actualizar todos los campos.
- `PATCH /users/{user_id}`: actualizar algunos campos.
- `DELETE /users/{user_id}`: eliminar usuario.

El modelo SQLAlchemy representa la tabla de la base de datos. Los schemas Pydantic validan los datos que entran y salen de la API.
