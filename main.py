from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import engine ,Base
from app.api.routes import auth, policies, claims
from app.api.routes import admin
import logging
# Ensure all SQLAlchemy models are imported and registered
from app.models import user, policy, user_policy, claim  # noqa: F401





@asynccontextmanager
async def lifespan(app:FastAPI):
    logger = logging.getLogger("insureflow")
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        # Allow the API to boot even if the DB is down so auth-only
        # endpoints can still be exercised (e.g., 401s for missing tokens).
        logger.exception("Database init failed during startup: %s", e)
    print("insureflow started")
    yield
    print("insureflow shutting down ")


app=FastAPI(
    title="insureflow application",
    description="insurance policy management system",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(policies.router, prefix="/api")
app.include_router(claims.router,prefix="/api")

@app.get("/")
def root():
    return {"message": "InsureFlow API running"}




