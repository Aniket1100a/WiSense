from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

# Include v1 endpoints
from app.api.v1.endpoints.connect import router as connect_router
from app.api.v1.endpoints.sensor import router as sensor_router
from app.api.v1.endpoints.room import router as room_router
from app.api.v1.endpoints.capability import router as capability_router
from app.api.v1.endpoints.signalsample import router as signalsample_router

router.include_router(connect_router, prefix="", tags=["Connect"])
router.include_router(sensor_router, prefix="", tags=["Sensors"])
router.include_router(room_router, prefix="", tags=["Rooms"])
router.include_router(capability_router, prefix="", tags=["Capabilities"])
router.include_router(signalsample_router, prefix="", tags=["SignalSamples"])
