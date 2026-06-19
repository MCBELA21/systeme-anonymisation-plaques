from pathlib import Path

import numpy as np
from ultralytics import YOLO

# Chemin vers le modèle entraîné
MODEL_PATH = Path(__file__).parent / "models" / "best.pt"

# Chargement du modèle une seule fois au démarrage (pas à chaque requête)
model = YOLO(str(MODEL_PATH))


def detect_plates(image: np.ndarray, confidence: float = 0.5) -> list[dict]:
    """
    Détecte les plaques d'immatriculation dans une image.

    Args:
        image       : image sous forme de tableau NumPy (BGR, format OpenCV)
        confidence  : seuil de confiance minimum pour retenir une détection

    Returns:
        Liste de détections, chacune étant un dictionnaire :
        {
            "bbox"       : [x1, y1, x2, y2]  (coordonnées en pixels),
            "confidence" : float              (score de confiance entre 0 et 1),
        }
    """
    results = model.predict(
        source=image,
        conf=confidence,
        verbose=False,  # désactive les logs ultralytics dans le terminal
    )

    detections = []
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            detections.append(
                {
                    "bbox": [int(x1), int(y1), int(x2), int(y2)],
                    "confidence": round(float(box.conf[0]), 3),
                }
            )

    return detections