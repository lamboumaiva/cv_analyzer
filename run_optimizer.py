import argparse
import json
from pathlib import Path
from openai_client.optimizer import optimize_cv_for_job

def read_docx(file_path):
    try:
        from docx import Document
    except ImportError:
        print("Le module python-docx est requis pour lire les fichiers .docx. Installez-le avec 'pip install python-docx'.")
        exit(1)
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

def main():
    parser = argparse.ArgumentParser(description="Optimize CV for a job offer")
    parser.add_argument("--cv-json", required=True, help="Chemin du CV structuré (json)")
    parser.add_argument("--job-file", required=True, help="Chemin du fichier offre d'emploi (txt ou docx)")
    parser.add_argument("--out-dir", required=True, help="Dossier de sortie")
    args = parser.parse_args()

    with open(args.cv_json, encoding="utf-8") as f:
        structured_cv = json.load(f)

    job_path = Path(args.job_file)
    ext = job_path.suffix.lower()
    if ext == '.docx':
        job_text = read_docx(args.job_file)
    else:
        job_text = job_path.read_text(encoding="utf-8")

    print("Optimisation du CV...")
    optimized_cv = optimize_cv_for_job(structured_cv, job_text)

    # Extraire le poste depuis la description (première ligne ou mot-clé)
    def extract_job_title(job_text):
        lines = [l.strip() for l in job_text.splitlines() if l.strip()]
        keywords = ["poste", "intitulé", "job title", "intitule", "position"]
        for line in lines:
            for kw in keywords:
                if kw.lower() in line.lower():
                    # Prend la partie après le mot-clé ou toute la ligne si pas de ':'
                    if ':' in line:
                        return line.split(':', 1)[1].strip().replace(' ', '_')
                    else:
                        return line.replace(kw, '', 1).strip().replace(' ', '_')
        # Sinon, prend la première ligne non générique
        for line in lines:
            if not any(x in line.lower() for x in ["offre d'emploi", "description", "profil", "mission"]):
                return line.replace(' ', '_')
        return "Poste"

    job_title = extract_job_title(job_text)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    base_name = Path(args.cv_json).stem.replace('structured', job_title)
    out_path = out_dir / f"{base_name}_optimized.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(optimized_cv, f, ensure_ascii=False, indent=2)
    print(f"CV optimisé sauvegardé dans {out_path}")

if __name__ == "__main__":
    main()
