from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# In a full project, you would import and include all your API routers.
# Example: from routers import devices, surveillance, users, etc.

app = FastAPI(
    title="Unified Infrastructure Management Platform",
    description="A central dashboard for managing multi-vendor network and infrastructure devices.",
    version="1.0.0"
)

# --- API Routers would be included here ---
# app.include_router(devices.router)
# ...

@app.get("/api/health", tags=["System"])
def health_check():
    """Check if the backend service is running."""
    return {"status": "ok"}

# --- Serve Frontend Files ---
# In a production environment, this is best handled by Nginx.
# These lines are for local development convenience.
app.mount("/portal", StaticFiles(directory="user_portal_public", html=True), name="user_portal")
app.mount("/", StaticFiles(directory="public", html=True), name="admin_portal")
