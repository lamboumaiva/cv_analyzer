# tests/test_extractor.py
from extractor.file_text_extractor import extract_text
from pathlib import Path

def test_extract_docx():
    sample = Path(__file__).parent.parent / "samples" / "sample_cv.docx"
    text = extract_text(str(sample))
    assert isinstance(text, str)
    assert len(text) > 10
