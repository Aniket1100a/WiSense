from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

# Include v1 endpoints
from app.api.v1.endpoints.connect import router as connect_router

router.include_router(connect_router, prefix="", tags=["Connect"])
