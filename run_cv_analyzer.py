
import argparse
import json
from pathlib import Path
import sys

from extractor.file_text_extractor import extract_text
from openai_client.structurer import structure_cv_to_blueprint


def read_docx(file_path):
    try:
        from docx import Document
    except ImportError:
        print("Le module python-docx est requis pour lire les fichiers .docx. Installez-le avec 'pip install python-docx'.")
        sys.exit(1)
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

def main():
    parser = argparse.ArgumentParser(description="CV Analyzer")
    parser.add_argument("--cv-file", required=True, help="Chemin du fichier CV (pdf, docx, txt)")
    parser.add_argument("--job-file", required=True, help="Chemin du fichier offre d'emploi (pdf, docx, txt)")
    parser.add_argument("--output", help="Chemin du fichier de sortie (json)")
    args = parser.parse_args()

    cv_text = extract_text(args.cv_file)

    # Lecture de l'offre d'emploi
    job_path = Path(args.job_file)
    ext = job_path.suffix.lower()
    if ext == '.docx':
        job_text = read_docx(args.job_file)
    elif ext == '.pdf':
        job_text = extract_text(args.job_file)
    else:
        job_text = job_path.read_text(encoding="utf-8")

    # Charger le blueprint par défaut
    blueprint_path = Path("cv_blueprint.json")
    if blueprint_path.exists():
        with open(blueprint_path, "r", encoding="utf-8") as f:
            blueprint = json.load(f)
    else:
        blueprint = None

    print("Structuration du CV...")
    structured_cv = structure_cv_to_blueprint(cv_text, job_text, blueprint)

    output_path = args.output or f"outputs/{Path(args.cv_file).stem}_structured.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(structured_cv, f, ensure_ascii=False, indent=2)
    print(f"CV structuré sauvegardé dans {output_path}")


if __name__ == "__main__":
    main()
