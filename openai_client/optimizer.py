import os
import json
import requests

# Tes clés et le nom du modèle restent intacts
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_MODEL = "deepseek-chat"

def optimize_cv_for_job(cv_json, job_description):
    """
    Optimise par rapport a la description de poste, le JSON du CV pour une offre d'emploi spécifique en gardant
    les informations personnelles et la structure du JSON puis en ajoutant
    un champ 'MyComment' à côté de chaque partie  pour indiquer ce
    qui a été changé et ce que l'utilisateur doit ajuster.
    """
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a professional CV optimization assistant.
You are given a CV in JSON format and a job description.

Your task:
- Keep all personal information (name, email, phone, address) unchanged.
- Keep the same JSON structure and fields.
- Modify ONLY the content of professional summary, experiences, skills, and education
  to better fit the job description.
- Rewrite where necessary to highlight relevant achievements and keywords.
- For each section that you modify, create a new field "MyComment" next to it.
  In "MyComment", explain:
    1) What was optimized automatically
    2) What the user should still adjust or check
- Return ONLY valid JSON, no explanations.

CV JSON:
{json.dumps(cv_json, indent=2)}

Job Description:
{job_description}
"""

    data = {
        "model": DEEPSEEK_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()

    optimized_text = result["choices"][0]["message"]["content"]

    try:
        optimized_json = json.loads(optimized_text)
    except json.JSONDecodeError:
        raise ValueError("DeepSeek did not return valid JSON. Response was:\n" + optimized_text)

    return optimized_json

def save_optimized_cv(cv_json, output_path):
    """
    Sauvegarde le CV optimisé dans le fichier spécifié.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cv_json, f, indent=2, ensure_ascii=False)
