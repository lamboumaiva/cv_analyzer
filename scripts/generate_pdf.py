import os
import json
import glob
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright

# Dossiers
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # racine du projet
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

def find_latest_json():
    """Trouve le fichier JSON le plus récent qui se termine par _optimized.json dans outputs/"""
    pattern = os.path.join(OUTPUT_DIR, "*_optimized.json")
    json_files = glob.glob(pattern)
    if not json_files:
        raise FileNotFoundError("❌ Aucun fichier *_optimized.json trouvé dans outputs/")
    latest_json = max(json_files, key=os.path.getmtime)  # le plus récent
    print("[INFO] JSON trouvé :", latest_json)
    return latest_json

def load_cv_data():
    """Charge le JSON le plus récent *_optimized.json"""
    latest_json = find_latest_json()
    with open(latest_json, "r", encoding="utf-8") as f:
        return json.load(f), latest_json

def render_html(cv_data):
    """Rend le template HTML avec les données du CV"""
    print("[DEBUG] Rendu du template avec Jinja2")
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("cv_template.html")
    return template.render(cv=cv_data)

def save_html(content, filename):
    """Sauvegarde le HTML généré"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def generate_pdf(html_content, output_path):
    """Génère un PDF à partir d'un HTML via Playwright"""
    print("[DEBUG] Lancement de Playwright pour générer le PDF…")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(html_content, wait_until="networkidle")
        page.pdf(path=output_path, format="A4", print_background=True)
        browser.close()
    print("[OK] PDF généré :", output_path)

def main():
    print("[DEBUG] Script generate_pdf.py lancé")

    # Vérifier les dossiers
    if not os.path.exists(OUTPUT_DIR):
        raise FileNotFoundError(f"❌ Le dossier outputs/ est introuvable : {OUTPUT_DIR}")
    if not os.path.exists(TEMPLATE_DIR):
        raise FileNotFoundError(f"❌ Le dossier templates/ est introuvable : {TEMPLATE_DIR}")

    # Charger le JSON et récupérer le chemin
    cv_data, json_path = load_cv_data()

    # Générer l’HTML
    html_content = render_html(cv_data)

    # Sauvegarder une copie HTML pour debug
    debug_html_path = os.path.join(OUTPUT_DIR, "debug_cv.html")
    save_html(html_content, debug_html_path)
    print("[DEBUG] HTML rendu sauvegardé :", debug_html_path)

    # Nom du PDF basé sur le JSON
    pdf_path = json_path.replace(".json", ".pdf")

    # Générer le PDF
    generate_pdf(html_content, pdf_path)

if __name__ == "__main__":
    main()
