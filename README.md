# CV Analyzer

## Pré-requis
- Python 3.10+ installé
- Windows (instructions ci-dessous faites pour Windows), fonctionne sur Linux/Mac aussi.

## Installation
1. Ouvrir PowerShell ou cmd.
2. Créer et activer un virtualenv:
   - PowerShell:
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
   - cmd:
     python -m venv .venv
     .\.venv\Scripts\activate.bat

3. Installer les dépendances:
   pip install -r requirements.txt

## Configuration de la clé OpenAI (Windows)
Tu m'as fourni la clé. Pour la définir comme variable d'environnement (PowerShell) :
  $env:OPENAI_API_KEY = "sk-xxxxx..."
Pour la rendre persistante (PowerShell) :
  setx OPENAI_API_KEY "sk-xxxxx..."

Ou en cmd:
  setx OPENAI_API_KEY "sk-xxxxx..."

**Remplace** "sk-xxxxx..." par ta clé réelle.

## Utilisation
Exemple:
python run_cv_analyzer.py --cv-file samples/sample_cv.docx --job-file samples/sample_job_description.txt --user-name "Jean Dupont" --title "Developpeur" --out-dir data/outputs --blueprint cv_blueprint.json

Le fichier `data/outputs/CV_Jean_Dupont_Developpeur.json` sera généré.

## Tests
python -m pytest -q

## Notes
- Je ne fournis pas la conversion JSON -> Word/PDF (hors scope).
- Si le PDF est scanné (image), il faudra d'abord lancer un OCR (Tesseract) — non inclus ici.
