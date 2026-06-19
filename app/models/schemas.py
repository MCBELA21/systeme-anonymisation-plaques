from pydantic import BaseModel, Field


class ProcessResponse(BaseModel):
    """Réponse renvoyée après traitement d'une image."""

    filename: str = Field(
        ...,
        description="Nom du fichier anonymisé généré, récupérable via GET /result/{filename}",
        examples=["3f7a2c1d8e4b5f6a9c0d1e2f3a4b5c6d.jpg"],
    )
    status: str = Field(
        ...,
        description="Statut du traitement",
        examples=["traité"],
    )
    detections_count: int = Field(
        ...,
        description="Nombre de plaques détectées et floutées dans l'image",
        examples=[1],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "filename": "3f7a2c1d8e4b5f6a9c0d1e2f3a4b5c6d.jpg",
                    "status": "traité",
                    "detections_count": 1,
                }
            ]
        }
    }


class ErrorResponse(BaseModel):
    """Réponse en cas d'erreur."""

    detail: str = Field(
        ...,
        description="Message d'erreur explicatif",
        examples=["Format non supporté : '.txt'. Formats acceptés : ['.jpeg', '.jpg', '.png']"],
    )