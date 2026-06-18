from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Paramètres de configuration de l'application.

    Les valeurs peuvent être surchargées via un fichier .env à la racine
    du projet (ex: UPLOAD_DIR=/data/uploads).
    """

    app_name: str = "Système d'anonymisation de plaques d'immatriculation"
    version: str = "0.1.0"

    upload_dir: str = "./storage/uploads"
    processed_dir: str = "./storage/processed"

    allowed_extensions: set[str] = {".jpg", ".jpeg", ".png"}

    class Config:
        env_file = ".env"


settings = Settings()