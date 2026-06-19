import cv2
import numpy as np


def blur_plates(image: np.ndarray, detections: list[dict]) -> np.ndarray:
    """
    Applique un floutage gaussien sur les zones de plaques détectées.

    Args:
        image      : image originale sous forme de tableau NumPy (BGR)
        detections : liste de détections retournée par detect_plates()
                     chaque détection contient une clé "bbox" : [x1, y1, x2, y2]

    Returns:
        Image avec les plaques floutées, sous forme de tableau NumPy (BGR)
    """
    # On travaille sur une copie pour ne pas modifier l'image originale
    result = image.copy()

    for detection in detections:
        x1, y1, x2, y2 = detection["bbox"]

        # Sécurité : s'assurer que les coordonnées restent dans les limites de l'image
        h, w = result.shape[:2]
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)

        if x2 <= x1 or y2 <= y1:
            continue  # bbox invalide, on passe

        # Extraction de la zone de la plaque
        zone = result[y1:y2, x1:x2]

        # Flou gaussien : le kernel (51, 51) donne un flou fort et lisible
        # Plus le kernel est grand, plus le flou est prononcé
        blurred_zone = cv2.GaussianBlur(zone, (51, 51), 0)

        # Remplacement de la zone originale par la zone floutée
        result[y1:y2, x1:x2] = blurred_zone

    return result


def load_image(image_bytes: bytes) -> np.ndarray:
    """
    Convertit des bytes (fichier uploadé) en tableau NumPy lisible par OpenCV.

    Args:
        image_bytes : contenu brut du fichier image (jpg, png...)

    Returns:
        Image sous forme de tableau NumPy (BGR)
    """
    np_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    return image


def save_image(image: np.ndarray, output_path: str) -> None:
    """
    Sauvegarde une image NumPy vers un fichier sur le disque.

    Args:
        image       : image sous forme de tableau NumPy (BGR)
        output_path : chemin complet du fichier de sortie (ex: storage/processed/img.jpg)
    """
    cv2.imwrite(output_path, image)