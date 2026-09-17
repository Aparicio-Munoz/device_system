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

La revisión `20260917_02` crea `devices` y `loans`, incluyendo las claves foráneas, el estado del préstamo y los índices de consulta.

## Estructura relacionada

Un usuario puede tener muchos préstamos y un dispositivo puede aparecer en muchos préstamos históricos. Cada préstamo pertenece exactamente a un usuario y a un dispositivo mediante claves foráneas.

## Endpoints de dispositivos

- `POST /devices`: crear dispositivo.
- `GET /devices`: listar dispositivos con filtros `device_type`, `is_available`, `brand` y `search`.
- `GET /devices/{device_id}`: consultar dispositivo.
- `PUT /devices/{device_id}`: reemplazar dispositivo.
- `PATCH /devices/{device_id}`: actualizar parcialmente.
- `DELETE /devices/{device_id}`: eliminar dispositivo sin historial de préstamos.

## Endpoints de préstamos

- `POST /loans`: crear préstamo y marcar el dispositivo como no disponible.
- `GET /loans`: listar préstamos con filtros opcionales.
- `GET /loans/details`: listar préstamos con información del usuario y del dispositivo usando joins.
- `GET /loans/{loan_id}`: consultar préstamo detallado.
- `PATCH /loans/{loan_id}/return`: registrar devolución y liberar el dispositivo.
- `GET /users/{user_id}/loans`: historial del usuario.
- `GET /devices/{device_id}/loans`: historial del dispositivo.

Ejemplos de filtros:

```text
/loans?status=active
/loans?user_email=ana@sena.edu.co
/loans?device_type=laptop
/loans?search=thinkpad
/devices?is_available=true&brand=lenovo
```

## Evidencias de aprendizaje

Las capturas se almacenan en `docs/evidencias/` y documentan la ejecución de migraciones, Swagger, creación de recursos, consultas relacionadas, filtros y devolución.

### Alembic y base de datos

![Inicialización de Alembic](docs/evidencias/alembic_init.png)

![Creación de migración](docs/evidencias/alembic_revision.png)

![Aplicación de migración](docs/evidencias/alembic_upgrade.png)

![Historial de migraciones](docs/evidencias/alembic_history.png)

![Estructura de tablas](docs/evidencias/estructura_tablas.png)

### API y Swagger

![Swagger UI](docs/evidencias/swagger_ui.png)

![Creación de usuario](docs/evidencias/usuario_creado.png)

![Creación de dispositivo](docs/evidencias/crear_dispositivo.png)

![Creación de préstamo](docs/evidencias/crear_prestamo.png)

![Consulta con joins](docs/evidencias/consulta_join.png)

![Filtros aplicados](docs/evidencias/filtro_prestamos.png)

![Devolución de dispositivo](docs/evidencias/devolver_dispositivo.png)

## Reflexión

Alembic permite controlar la evolución de la base de datos mediante migraciones versionadas, evitando cambios manuales y facilitando el trabajo colaborativo. Las relaciones entre usuarios, dispositivos y préstamos mantienen la integridad referencial del sistema. Finalmente, las consultas con `join`, `where`, `ilike`, `and_` y `or_` permiten entregar información relacionada y aplicar búsquedas útiles sin duplicar lógica en los endpoints.
