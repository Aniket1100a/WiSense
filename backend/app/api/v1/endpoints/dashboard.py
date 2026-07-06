from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.common import make_api_response
from app.database.session import get_db
from app.schemas.dashboard import ChartData, DashboardOverview, SignalHistoryData
from app.schemas.response import ApiResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def get_dashboard_service(db: Session = Depends(get_db)) -> DashboardService:
    return DashboardService(db)


@router.get(
    "/overview",
    response_model=ApiResponse[DashboardOverview],
    status_code=status.HTTP_200_OK,
    summary="Dashboard overview",
    description="Return summary metrics for the dashboard, including device counts, providers, and discovery state.",
)
def get_overview(service: DashboardService = Depends(get_dashboard_service)) -> dict:
    return make_api_response(data=service.get_overview(), message="Dashboard overview retrieved successfully.")


@router.get(
    "/device-health",
    response_model=ApiResponse[ChartData],
    status_code=status.HTTP_200_OK,
    summary="Device health chart",
    description="Return sensor health distribution data for frontend charts.",
)
def get_device_health(service: DashboardService = Depends(get_dashboard_service)) -> dict:
    return make_api_response(data=service.get_device_health_chart(), message="Device health chart data retrieved successfully.")


@router.get(
    "/signal-history",
    response_model=ApiResponse[SignalHistoryData],
    status_code=status.HTTP_200_OK,
    summary="Signal history chart",
    description="Return historical signal data for frontend timeline charts.",
)
def get_signal_history(
    days: int = Query(14, ge=1, le=30, description="Number of days to include in the signal history chart."),
    service: DashboardService = Depends(get_dashboard_service),
) -> dict:
    data = service.get_signal_history_chart()
    return make_api_response(data=data, message="Signal history chart data retrieved successfully.")


@router.get(
    "/provider-distribution",
    response_model=ApiResponse[ChartData],
    status_code=status.HTTP_200_OK,
    summary="Provider distribution chart",
    description="Return provider distribution counts for frontend charts.",
)
def get_provider_distribution(service: DashboardService = Depends(get_dashboard_service)) -> dict:
    return make_api_response(data=service.get_provider_distribution(), message="Provider distribution data retrieved successfully.")


@router.get(
    "/status-distribution",
    response_model=ApiResponse[ChartData],
    status_code=status.HTTP_200_OK,
    summary="Status distribution chart",
    description="Return sensor status distribution counts for frontend charts.",
)
def get_status_distribution(service: DashboardService = Depends(get_dashboard_service)) -> dict:
    return make_api_response(data=service.get_status_distribution(), message="Status distribution data retrieved successfully.")
