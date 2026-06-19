import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse

from app.core.config import settings
from app.models.schemas import ProcessResponse, ErrorResponse
from app.services.blur import blur_plates, load_image, save_image
from app.services.detection import detect_plates

router = APIRouter()


@router.post(
    "/process",
    response_model=ProcessResponse,
    summary="Traiter une image",
    description="""
Reçoit une image, détecte les plaques d'immatriculation via YOLOv8,
applique un floutage gaussien sur chaque plaque détectée, et sauvegarde
l'image anonymisée.

**Formats acceptés** : JPG, JPEG, PNG

**Retourne** le nom du fichier anonymisé à utiliser avec `GET /result/{filename}`.
    """,
    responses={
        400: {"model": ErrorResponse, "description": "Format invalide ou fichier vide"},
    },
)
async def process_image(file: UploadFile = File(
    ...,
    description="Image à anonymiser (JPG, JPEG ou PNG)"
)) -> ProcessResponse:
    extension = _get_extension(file.filename)
    if extension not in settings.allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Format non supporté : '{extension}'. "
                f"Formats acceptés : {sorted(settings.allowed_extensions)}"
            ),
        )

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Le fichier envoyé est vide.")

    image = load_image(contents)
    if image is None:
        raise HTTPException(
            status_code=400,
            detail="Impossible de lire l'image. Vérifie qu'elle n'est pas corrompue."
        )

    detections = detect_plates(image)
    blurred = blur_plates(image, detections)

    output_filename = f"{uuid.uuid4().hex}{extension}"
    output_path = Path(settings.processed_dir) / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_image(blurred, str(output_path))

    return ProcessResponse(
        filename=output_filename,
        status="traité",
        detections_count=len(detections),
    )


@router.get(
    "/result/{filename}",
    summary="Récupérer une image anonymisée",
    description="""
Retourne l'image anonymisée identifiée par son nom de fichier,
tel que retourné par `POST /process`.
    """,
    responses={
        200: {"content": {"image/jpeg": {}}, "description": "Image anonymisée"},
        404: {"model": ErrorResponse, "description": "Fichier introuvable"},
    },
)
def get_result(filename: str) -> FileResponse:
    file_path = Path(settings.processed_dir) / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Fichier introuvable.")
    return FileResponse(str(file_path))


def _get_extension(filename: str | None) -> str:
    """Extrait l'extension d'un nom de fichier, en minuscule, avec le point."""
    if not filename or "." not in filename:
        return ""
    return "." + filename.rsplit(".", 1)[-1].lower()