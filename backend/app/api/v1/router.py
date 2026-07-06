from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

# Include v1 endpoints
from app.api.v1.endpoints.connect import router as connect_router
from app.api.v1.endpoints.sensor import router as sensor_router
from app.api.v1.endpoints.room import router as room_router
from app.api.v1.endpoints.capability import router as capability_router
from app.api.v1.endpoints.signalsample import router as signalsample_router
from app.api.v1.endpoints.sensor_management import router as sensor_mgmt_router
from app.api.v1.endpoints.discovery import router as discovery_router
from app.api.v1.endpoints.dashboard import router as dashboard_router
from app.api.v1.endpoints.activity import router as activity_router

router.include_router(connect_router, prefix="", tags=["Connect"])
router.include_router(sensor_router, prefix="", tags=["Sensors"])
router.include_router(room_router, prefix="", tags=["Rooms"])
router.include_router(capability_router, prefix="", tags=["Capabilities"])
router.include_router(signalsample_router, prefix="", tags=["SignalSamples"])
router.include_router(sensor_mgmt_router, prefix="", tags=["Sensors Management"])
router.include_router(discovery_router, prefix="", tags=["Discovery"])
router.include_router(dashboard_router, prefix="", tags=["Dashboard"])
router.include_router(activity_router, prefix="", tags=["Activity"])
