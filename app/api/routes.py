import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse

from app.core.config import settings
from app.models.schemas import ProcessResponse
from app.services.blur import blur_plates, load_image, save_image
from app.services.detection import detect_plates

router = APIRouter()


@router.post("/process", response_model=ProcessResponse)
async def process_image(file: UploadFile = File(...)) -> ProcessResponse:
    """
    Pipeline complet de traitement d'une image :
    1. Validation du format
    2. Détection des plaques (YOLOv8)
    3. Floutage des zones détectées (OpenCV)
    4. Sauvegarde de l'image anonymisée
    """
    # --- 1. Validation du format ---
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

    # --- 2. Chargement de l'image ---
    image = load_image(contents)
    if image is None:
        raise HTTPException(
            status_code=400,
            detail="Impossible de lire l'image. Vérifie qu'elle n'est pas corrompue."
        )

    # --- 3. Détection des plaques ---
    detections = detect_plates(image)

    # --- 4. Floutage ---
    blurred = blur_plates(image, detections)

    # --- 5. Sauvegarde de l'image anonymisée ---
    output_filename = f"{uuid.uuid4().hex}{extension}"
    output_path = Path(settings.processed_dir) / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_image(blurred, str(output_path))

    return ProcessResponse(
        filename=output_filename,
        status="traité",
        detections_count=len(detections),
    )


@router.get("/result/{filename}")
def get_result(filename: str) -> FileResponse:
    """
    Permet de récupérer une image anonymisée par son nom de fichier.
    """
    file_path = Path(settings.processed_dir) / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Fichier introuvable.")
    return FileResponse(str(file_path))


def _get_extension(filename: str | None) -> str:
    """Extrait l'extension d'un nom de fichier, en minuscule, avec le point."""
    if not filename or "." not in filename:
        return ""
    return "." + filename.rsplit(".", 1)[-1].lower()