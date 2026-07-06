from typing import Any

from app.schemas.response import ApiResponse, Pagination


def make_api_response(
    data: Any = None,
    message: str = "Request completed successfully.",
    pagination: Pagination | None = None,
    errors: Any | None = None,
) -> dict:
    return {
        "success": errors is None,
        "message": message,
        "data": data,
        "pagination": pagination,
        "errors": errors,
    }


def make_paginated_response(
    data: Any,
    message: str,
    limit: int,
    offset: int,
    count: int,
    total: int | None = None,
) -> dict:
    pagination = Pagination(limit=limit, offset=offset, count=count, total=total)
    return make_api_response(data=data, message=message, pagination=pagination)
