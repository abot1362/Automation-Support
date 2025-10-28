from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# In a full project, you would import all your API routers here
# from routers import devices, users, etc.

app = FastAPI(
    title="Unified Platform API",
    description="The central API service for the Unified Infrastructure Management Platform.",
    version="1.0.0"
)

# --- CORS Middleware for Next.js Frontends ---
origins = [
    "http://localhost:3000",  # Default Next.js port for Admin Frontend
    "http://localhost:3001",  # A different port for User Frontend
    "https://admin.your-production-domain.com",
    "https://portal.your-production-domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include API Routers ---
# This is where you would register all your API endpoints
# app.include_router(devices.router, prefix="/api", tags=["Devices"])
# ...

@app.get("/api/health", tags=["System"])
def health_check():
    """Provides a simple health check to confirm the API is running."""
    return {"status": "ok", "message": "Backend API is alive!"}

# Note: The StaticFiles mounts are removed as Next.js will handle the frontend.
# backend/main.py
# from fastapi_kerberos import KerberosMiddleware, KerberosConfig

# config = KerberosConfig(service="HTTP@your-server-hostname.mycorp.local")
# app.add_middleware(KerberosMiddleware, config=config)
