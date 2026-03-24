from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.core.limiter import limiter
from app.api.auth import router as auth_router

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth Service - Red Bicicletas",
    description="Microservice for authentication in the Red Bicicletas application.",
    version="1.0.0"
)

# Add rate limiting middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Add session middleware for Google OAuth2
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.include_router(auth_router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "auth-service"}