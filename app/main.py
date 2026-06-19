from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="""
## Système d'anonymisation de plaques d'immatriculation

Ce système permet de détecter et flouter automatiquement les plaques
d'immatriculation présentes sur des images, afin de respecter les
exigences du RGPD en matière de protection des données personnelles.

### Pipeline de traitement

1. **Upload** d'une image (JPG, JPEG, PNG)
2. **Détection** des plaques via un modèle YOLOv8 fine-tuné (mAP50 = 98.6%)
3. **Floutage** gaussien des zones détectées via OpenCV
4. **Récupération** de l'image anonymisée

### Acteurs

- **Opérateur** : importe les images et récupère les résultats
- **Administrateur** : supervise les logs et la configuration
    """,
    contact={
        "name": "VisionRoad Solutions",
    },
    license_info={
        "name": "Projet académique - usage interne",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, tags=["Traitement d'images"])


@app.get("/health", tags=["Système"])
def health_check() -> dict[str, str]:
    """
    Vérifie que le serveur est opérationnel.

    Utile pour le monitoring et les health checks automatisés.
    """
    return {"status": "ok"}