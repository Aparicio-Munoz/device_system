# device_systems

API REST de usuarios creada con FastAPI, SQLAlchemy, Alembic, Pydantic y SQLite.

## Ejecutar el proyecto

```bash
# Crear/actualizar el esquema antes de iniciar la API
venv/bin/alembic upgrade head
venv/bin/uvicorn app.main:app --reload
```

Documentación:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Estructura

- `app/database/connection.py`: engine, sesiones y Base.
- `app/models/user_model.py`: tabla `users` de SQLAlchemy.
- `alembic/env.py`: configuración de Alembic y metadata de SQLAlchemy.
- `alembic/versions/`: historial versionado de cambios de base de datos.
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

## Migraciones con Alembic

Alembic administra la estructura de la base de datos. La aplicación no crea tablas automáticamente al iniciar; primero deben aplicarse las migraciones.

```bash
# Ver el estado actual
venv/bin/alembic current

# Aplicar todas las migraciones pendientes
venv/bin/alembic upgrade head

# Consultar el historial
venv/bin/alembic history
```

Cuando se modifiquen los modelos, generar una nueva revisión y revisarla antes de aplicarla:

```bash
venv/bin/alembic revision --autogenerate -m "describe schema change"
venv/bin/alembic upgrade head
```

La migración inicial `20260917_01` crea la tabla `users`, sus restricciones y sus índices. Si se usa una base SQLite existente que ya contiene esa tabla, registrar la línea base una sola vez con:

```bash
venv/bin/alembic stamp 20260917_01
```
