from pydantic import BaseModel, ConfigDict


class ConnectResponse(BaseModel):
    """Schema returned to the frontend when checking connectivity."""

    ok: bool
    message: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "ok": True,
                "message": "Backend connectivity verified.",
            }
        }
    )
