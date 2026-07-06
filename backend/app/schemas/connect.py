from pydantic import BaseModel


class ConnectResponse(BaseModel):
    """Schema returned to the frontend when checking connectivity."""

    ok: bool
    message: str
