# Users API

API REST sencilla para registrar usuarios, desarrollada con **FastAPI** y
**Pydantic**. Actualmente los usuarios se almacenan en memoria, por lo que la
información se pierde al reiniciar la aplicación.

## Requisitos

- Python 3.10 o superior
- `pip`

## Instalación

Desde la carpeta raíz del proyecto (`device_systems`), instala las
dependencias:

```bash
pip install -r app/requeriments.txt
```

## Ejecución

Desde la carpeta raíz del proyecto:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en:

- http://127.0.0.1:8000
- Documentación interactiva: http://127.0.0.1:8000/docs
- Documentación alternativa: http://127.0.0.1:8000/redoc

## Endpoints

### `GET /`

Comprueba que la API está funcionando.

Respuesta:

```json
{
  "message": "API funcionando"
}
```

### `POST /users`

Crea un usuario. El cuerpo debe incluir:

| Campo | Tipo | Reglas |
| --- | --- | --- |
| `name` | string | Entre 2 y 50 caracteres |
| `email` | string | Debe tener formato de correo válido |
| `age` | integer | Entre 18 y 100 años |

Ejemplo de solicitud:

```bash
curl -X POST "http://127.0.0.1:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"name":"Ana Pérez","email":"ANA@example.com","age":25}'
```

Respuesta exitosa (`201 Created`):

```json
{
  "id": 1,
  "name": "Ana Pérez",
  "email": "ana@example.com",
  "age": 25
}
```

El correo se guarda en minúsculas. Si ya existe un usuario con el mismo
correo, la API responde `409 Conflict`:

```json
{
  "detail": "El correo ya está registrado"
}
```

Los datos que no cumplen las reglas de validación producen una respuesta
`422 Unprocessable Entity`.

## Estructura del proyecto

```text
app/
├── main.py                    # Configuración y punto de entrada de FastAPI
├── requeriments.txt           # Dependencias del proyecto
├── routes/
│   └── user_routes.py         # Endpoint POST /users y almacenamiento temporal
└── schemas/
    └── user_schema.py         # Modelos y validaciones de usuarios
```

## Notas

- El almacenamiento actual usa una lista en memoria (`users_db`); no hay una
  base de datos configurada.
- Solo está implementado el registro de usuarios. No existen todavía
  endpoints para listar, consultar, actualizar o eliminar usuarios.
- `UserRole` y el modelo `User` están definidos en los esquemas, pero el
  endpoint actual de creación utiliza `UserCreate` y `UserResponse`, que no
  incluyen el rol.
