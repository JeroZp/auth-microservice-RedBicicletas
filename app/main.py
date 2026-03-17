from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.api.auth import router as auth_router

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth Service - Red Bicicletas",
    description="Microservice for authentication in the Red Bicicletas application.",
    version="1.0.0"
)

# Add session middleware for Google OAuth2
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.include_router(auth_router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "auth-service"}