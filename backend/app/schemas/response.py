from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field
from pydantic.generics import GenericModel

T = TypeVar("T")


class Pagination(BaseModel):
    limit: int = Field(..., description="Maximum number of items returned in this page.", example=100)
    offset: int = Field(..., description="Offset of the current page.", example=0)
    count: int = Field(..., description="Number of items returned in this response.", example=5)
    total: int | None = Field(
        None,
        description="Total number of items available, if known.",
        example=1024,
    )

    model_config = ConfigDict(from_attributes=True)


class ApiResponse(GenericModel, Generic[T]):
    success: bool = Field(True, description="Indicates whether the request succeeded.", example=True)
    message: str = Field(
        ...,
        description="Human-readable summary of the operation result.",
        example="Request completed successfully.",
    )
    data: T | None = Field(None, description="The response payload.")
    pagination: Pagination | None = Field(
        None,
        description="Pagination metadata for list responses.",
    )
    errors: Any | None = Field(None, description="Validation or error details when the request failed.")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Request completed successfully.",
                "data": None,
                "pagination": None,
                "errors": None,
            }
        },
    )
