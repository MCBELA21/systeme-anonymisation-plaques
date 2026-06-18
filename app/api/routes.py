from fastapi import APIRouter, UploadFile, File, HTTPException

from app.core.config import settings
from app.models.schemas import ProcessResponse

router = APIRouter()


@router.post("/process", response_model=ProcessResponse)
async def process_image(file: UploadFile = File(...)) -> ProcessResponse:
    """
    Point d'entrée principal du pipeline de traitement d'une image.

    Pour l'instant (étape 6), cette route se contente de :
    - valider le format du fichier reçu
    - vérifier qu'il n'est pas vide
    - renvoyer une réponse de confirmation

    Les étapes suivantes viendront brancher ici, dans cet ordre :
    - Détection des plaques avec YOLOv8   -> app/services/detection.py
    - Floutage des zones détectées        -> app/services/blur.py
    - Sauvegarde image + métadonnées      -> app/services/storage.py
    """
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

    # --- Points d'extension pour les prochaines étapes ---
    # detections = detect_plates(contents)
    # blurred_image = blur_plates(contents, detections)
    # save_image(blurred_image, detections)

    return ProcessResponse(
        filename=file.filename,
        status="reçu",
        detections_count=0,
    )


def _get_extension(filename: str | None) -> str:
    """Extrait l'extension d'un nom de fichier, en minuscule, avec le point."""
    if not filename or "." not in filename:
        return ""
    return "." + filename.rsplit(".", 1)[-1].lower()