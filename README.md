# 🔐 Auth Service — Red Bicicletas

Microservicio de autenticación para la plataforma **Red Bicicletas**. Construido con **FastAPI** y **PostgreSQL**, implementa registro, login, recuperación de contraseña, autenticación con Google y gestión de tokens JWT (Access + Refresh Token).

---

## 🚀 Características

- ✅ **Registro y autenticación** con bcrypt
- ✅ **JWT** — Access Token (15-60 min) + Refresh Token (7 días)
- ✅ **Login con Google** (OAuth 2.0)
- ✅ **Recuperación de contraseña** vía correo electrónico
- ✅ **Bloqueo de cuenta** tras 5 intentos fallidos de login
- ✅ **Revocación de Refresh Tokens** (logout seguro)
- ✅ **PostgreSQL** para almacenamiento de usuarios y tokens
- ✅ **Dockerizado** con Docker Compose
- 🔜 **Endpoint `/auth/me`** — información del usuario autenticado
- 🔜 **Eventos RabbitMQ** — publica `user.registered` al registrar un usuario

---

---

## 🛠️ Tecnologías

| Tecnología | Uso |
|---|---|
| FastAPI | Framework web |
| PostgreSQL | Base de datos relacional |
| SQLAlchemy | ORM |
| Passlib + bcrypt | Hash de contraseñas |
| python-jose | Generación y validación de JWT |
| Authlib | OAuth 2.0 con Google |
| Docker + Docker Compose | Contenedores |

---

## 📁 Estructura del proyecto

```
auth-service/
├── app/
│   ├── api/
│   │   └── auth.py             # Endpoints
│   ├── core/
│   │   ├── config.py           # Variables de entorno
│   │   ├── database.py         # Conexión a PostgreSQL
│   │   └── security.py         # Hash y JWT
│   ├── models/
│   │   └── user.py             # Modelos de base de datos
│   ├── schemas/
│   │   └── auth.py             # Validación de datos (Pydantic)
│   ├── services/
│   │   ├── auth_service.py     # Lógica de negocio
│   │   └── oauth_service.py    # Configuración OAuth Google
│   └── main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── .gitignore
```

---

## 📡 Endpoints

| Método | Ruta | Descripción | Auth requerida |
|---|---|---|---|
| `POST` | `/auth/register` | Registro de nuevo usuario | No |
| `POST` | `/auth/login` | Login con correo y contraseña | No |
| `POST` | `/auth/refresh` | Obtener nuevo access token | No |
| `POST` | `/auth/logout` | Revocar refresh token | No |
| `POST` | `/auth/password-recovery` | Solicitar recuperación de contraseña | No |
| `POST` | `/auth/password-reset` | Restablecer contraseña con token | No |
| `GET` | `/auth/google/login` | Redirige a pantalla de login de Google | No |
| `GET` | `/auth/google/callback` | Callback OAuth de Google | No |
| `GET` | `/auth/me` | Información del usuario autenticado | ✅ Sí |
| `GET` | `/health` | Health check del servicio | No |

La documentación interactiva está disponible en `http://localhost:8000/docs`.

---

## 🔐 Flujo JWT

```
Login exitoso
  → Servidor genera Access Token (30 min) + Refresh Token (7 días)
  → Cliente incluye Access Token en cada request:
    Authorization: Bearer {access_token}
  → Al expirar el Access Token, usa el Refresh Token:
    POST /auth/refresh { "refresh_token": "..." }
  → Al hacer logout, el Refresh Token queda revocado en base de datos
```

### Estructura del JWT

```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "type": "access",
  "exp": 1704123456
}
```

---

## 🌐 Flujo OAuth con Google

```
Usuario visita GET /auth/google/login
  → Redirigido a pantalla de Google
  → Usuario aprueba permisos
  → Google redirige a GET /auth/google/callback
  → Sistema crea cuenta si no existe
  → Retorna Access Token + Refresh Token
```

---

## ⚙️ Configuración

Copia el archivo de ejemplo y completa los valores:

```bash
cp .env.example .env
```

```dotenv
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres123
POSTGRES_DB=auth_db

DATABASE_URL=postgresql://postgres:postgres123@postgres:5432/auth_db

# Generar con: openssl rand -hex 32
SECRET_KEY=

ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_MINUTES=15

# Google OAuth — obtener en console.cloud.google.com
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
```

---

## 🐳 Correr con Docker

```bash
# Levantar servicios
docker-compose up --build

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (borra la base de datos)
docker-compose down -v
```

## 💻 Correr sin Docker

```bash
# Instalar dependencias
pip install -r requirements.txt

# Levantar la app (requiere PostgreSQL corriendo localmente)
uvicorn app.main:app --reload
```

---

## 🛡️ Seguridad

- Contraseñas almacenadas con **bcrypt** (mínimo 8 caracteres, máximo 72).
- Tokens firmados con **HS256**.
- Cuentas bloqueadas temporalmente tras **5 intentos fallidos** de login durante **15 minutos**.
- Refresh tokens almacenados en base de datos con soporte de revocación.
- Recuperación de contraseña con token temporal de **1 hora** de validez.
- Comunicación recomendada mediante **HTTPS + TLS 1.2** o superior en producción.