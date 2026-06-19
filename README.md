# systeme-anonymisation-plaques
système qui permet de détecter et flouter les numéros de plaques d'immatriculation présente sur une image

# Système d'anonymisation de plaques d'immatriculation

Système automatique de détection et de floutage de plaques d'immatriculation
sur des images, développé dans le cadre du projet VisionRoad Solutions.

## Fonctionnalités

- Upload d'une image (JPG, JPEG, PNG)
- Détection automatique des plaques via un modèle YOLOv8 fine-tuné
- Floutage gaussien des zones détectées via OpenCV
- Récupération de l'image anonymisée via une route dédiée
- Documentation interactive de l'API générée automatiquement (Swagger UI)

## Architecture
Client (navigateur)

↓ HTTP/HTTPS

Serveur Web (FastAPI)

↓              ↓              ↓

YOLOv8 (détection)  OpenCV (floutage)  Stockage fichiers

## Prérequis

- Python 3.10 ou supérieur
- pip
- Un fichier `best.pt` (modèle YOLOv8 entraîné) placé dans `app/services/models/`

## Installation

**1. Cloner le dépôt :**

```bash
git clone https://github.com/MCBELA21/systeme-anonymisation-plaques.git
cd systeme-anonymisation-plaques
```

**2. Créer et activer l'environnement virtuel :**

```bash
# Créer
python -m venv venv

# Activer (Linux/macOS)
source venv/bin/activate

# Activer (Windows cmd)
venv\Scripts\activate
```

**3. Installer les dépendances :**

```bash
pip install -r requirements.txt
```

**4. Placer le modèle entraîné :**

Copie ton fichier `best.pt` dans :
app/services/models/best.pt

## Lancer le serveur

```bash
uvicorn app.main:app --reload
```

Le serveur démarre sur `http://127.0.0.1:8000`

## Utilisation

### Via Swagger UI (recommandé pour les tests)

Ouvre `http://127.0.0.1:8000/docs` dans ton navigateur.

- **POST /process** : envoie une image, reçois le nom du fichier anonymisé et le nombre de plaques détectées.
- **GET /result/{filename}** : affiche l'image anonymisée dans le navigateur.
- **GET /health** : vérifie que le serveur répond.

### Via curl

```bash
# Envoyer une image
curl -X POST "http://127.0.0.1:8000/process" \
  -F "file=@chemin/vers/image.jpg"

# Récupérer l'image anonymisée
curl "http://127.0.0.1:8000/result/nom_du_fichier_retourné.jpg" \
  --output image_anonymisee.jpg
```

### Exemple de réponse de /process

```json
{
  "filename": "3f7a2c1d8e4b5f6a9c0d1e2f3a4b5c6d.jpg",
  "status": "traité",
  "detections_count": 1
}
```

## Structure du projet
app/

main.py              -> point d'entrée FastAPI

api/

routes.py          -> routes /process, /result, /health

core/

config.py          -> configuration centralisée

models/

schemas.py         -> schémas Pydantic

services/

detection.py       -> détection des plaques (YOLOv8)

blur.py            -> floutage des zones détectées (OpenCV)

models/

best.pt          -> modèle entraîné (non versionné sur GitHub)

storage/

uploads/             -> images reçues (non versionnées)

processed/           -> images anonymisées (non versionnées)

## Modèle YOLOv8

Le modèle a été fine-tuné sur un dataset de ~8000 images de plaques
d'immatriculation (une seule classe : `plate`), avec la répartition suivante :
- 80% entraînement
- 20% validation
- 10% test

Résultat obtenu : **mAP50 = 0.986** (98.6% de précision sur le jeu de validation).

## Technologies utilisées

| Composant | Technologie |
|-----------|-------------|
| Backend API | FastAPI |
| Serveur | Uvicorn |
| Détection IA | YOLOv8 (ultralytics) |
| Traitement image | OpenCV |
| Validation données | Pydantic |

