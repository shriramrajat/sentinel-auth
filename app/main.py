"""
SentinelAuth - FastAPI Application Entry Point

This is the main application file that creates and configures
the FastAPI application instance.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import engine
from app.db.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events for the application.
    This is the modern way to handle startup/shutdown in FastAPI.
    
    Startup:
        - Log application start
        - Verify database connection
    
    Shutdown:
        - Clean up resources
        - Close database connections
    """
    # Startup
    print(f"🚀 Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f"📊 Database: {settings.DATABASE_URL.split('@')[-1]}")  # Hide credentials
    print(f"🔒 Debug Mode: {settings.DEBUG}")
    
    # Verify database connection by trying to connect
    try:
        with engine.connect() as conn:
            print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise
    
    yield
    
    # Shutdown
    print(f"🛑 Shutting down {settings.PROJECT_NAME}")
    engine.dispose()
    print("✅ Database connections closed")


# Create FastAPI application instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Centralized authentication and authorization service",
    lifespan=lifespan,
    docs_url="/docs",      # Swagger UI at /docs
    redoc_url="/redoc",    # ReDoc at /redoc
    openapi_url="/openapi.json"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API information.
    
    Returns basic information about the API.
    """
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Used by monitoring systems and load balancers to verify
    the application is running and healthy.
    
    Returns:
        dict: Health status information
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }


# Future: Include API routers here
# Example:
# from app.api.router import api_router
# app.include_router(api_router, prefix=settings.API_V1_PREFIX)
