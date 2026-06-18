from pydantic import BaseModel


class ProcessResponse(BaseModel):
    """Réponse renvoyée par la route /process."""

    filename: str
    status: str
    detections_count: int


class ErrorResponse(BaseModel):
    detail: str