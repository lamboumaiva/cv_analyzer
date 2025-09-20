# utils/file_utils.py
from pathlib import Path
import re

def safe_filename(s: str) -> str:
    # remplace les caractères dangereux
    s = re.sub(r"[^\w\-_\. ]", "_", s)
    return s.strip().replace(" ", "_")

def build_output_filename(name: str, title: str) -> str:
    name_safe = safe_filename(name)
    title_safe = safe_filename(title)
    return f"CV_{name_safe}_{title_safe}.json"
