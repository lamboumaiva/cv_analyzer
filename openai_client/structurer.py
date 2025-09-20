import os
import json
import requests

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))

if not DEEPSEEK_API_KEY:
    raise EnvironmentError("DEEPSEEK_API_KEY not set. See README.")

HEADERS = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json"
}

API_URL = "https://api.deepseek.com/v1/chat/completions"


def structure_cv_to_blueprint(cv_text, job_description, blueprint=None):
    """
    Envoie le CV et la description du job à DeepSeek
    et reçoit un JSON structuré incluant suggestions et recommandations.
    """
    prompt = f"""
Analyze the CV against this job description and respond ONLY with valid JSON.
Follow the given blueprint strictly without renaming or reordering sections.

Blueprint :
{json.dumps(blueprint, indent=2, ensure_ascii=False)}

Ta tâche :
- Remplace chaque champ "string", "number", "list" etc. par les informations extraites du CV ci-dessous.
- Si une info n’existe pas dans le CV, laisse la valeur vide ("") ou une liste vide [].


CV: {cv_text}

Job Description: {job_description}

⚠️ IMPORTANT: 
- Do NOT include explanations outside JSON
- Do NOT add markdown, ```json, or comments
- Respond ONLY with valid JSON
"""

    data = {
        "model": DEEPSEEK_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": MAX_TOKENS,
        "temperature": 0.0
    }

    response = requests.post(API_URL, headers=HEADERS, json=data)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("❌ Erreur API DeepSeek:", response.text)
        raise e

    result = response.json()

    # 🔍 Debug : afficher la réponse brute
    structured_text = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    print("---- API RAW RESPONSE ----")
    print(structured_text[:500])  # affiche les 500 premiers caractères
    print("--------------------------")

    if not structured_text:
        raise ValueError("❌ Réponse vide reçue de l'API DeepSeek")

    try:
        structured_json = json.loads(structured_text)
    except json.JSONDecodeError:
        raise ValueError("❌ La réponse de l'API n'est pas un JSON valide.\n" + structured_text)

    return structured_json

def save_structured_cv(structured_json, out_dir="outputs"):
    """
    Sauvegarde le CV structuré dans un fichier JSON.
    Le nom du fichier est basé sur le nom trouvé dans le CV et
    l’intitulé du poste trouvé dans la job description.
    """
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # 🔍 Récupérer nom & poste depuis le JSON structuré
    user_name = structured_json.get("personal_info", {}).get("name", "UnknownName")
    job_title = structured_json.get("job_info", {}).get("title", "UnknownJob")

    # 🔧 Nettoyer pour un nom de fichier valide
    safe_name = user_name.replace(" ", "_")
    safe_title = job_title.replace(" ", "_")

    filename = f"CV_{safe_name}_{safe_title}.json"
    filepath = os.path.join(out_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(structured_json, f, indent=2, ensure_ascii=False)

    print(f"✅ CV structuré sauvegardé dans {filepath}")
    return filepath
