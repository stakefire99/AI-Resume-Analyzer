"""
Resume Parser — Extracts text from PDF and DOCX files
"""

import io
import re


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from a PDF file using PyPDF2."""
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return clean_text(text)
    except Exception as e:
        raise ValueError(f"Could not read PDF: {e}. Make sure it's not password-protected.")


def extract_text_from_docx(uploaded_file) -> str:
    """Extract text from a DOCX file using python-docx."""
    try:
        from docx import Document
        doc = Document(io.BytesIO(uploaded_file.read()))
        text = "\n".join([para.text for para in doc.paragraphs])
        return clean_text(text)
    except Exception as e:
        raise ValueError(f"Could not read DOCX: {e}")


def extract_text_from_txt(uploaded_file) -> str:
    """Read plain text file."""
    return clean_text(uploaded_file.read().decode("utf-8", errors="ignore"))


def parse_resume(uploaded_file) -> str:
    """
    Auto-detects file type and returns extracted text.
    Supports: PDF, DOCX, TXT
    """
    filename = uploaded_file.name.lower()
    uploaded_file.seek(0)  # Reset pointer

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    elif filename.endswith(".txt"):
        return extract_text_from_txt(uploaded_file)
    else:
        raise ValueError(f"Unsupported file type: {filename}. Please upload PDF, DOCX, or TXT.")


def clean_text(text: str) -> str:
    """Clean and normalize extracted text."""
    # Remove excessive whitespace and special characters
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # remove non-ASCII
    return text.strip()


def extract_sections(text: str) -> dict:
    """
    Attempt to split resume into sections.
    Returns dict with keys like 'experience', 'education', 'skills', 'projects'.
    """
    sections = {
        "experience": "",
        "education": "",
        "skills": "",
        "projects": "",
        "summary": "",
        "full": text
    }

    # Common section headers (case-insensitive)
    patterns = {
        "summary": r"(summary|objective|profile|about me)",
        "experience": r"(experience|employment|work history|internship)",
        "education": r"(education|academic|qualification)",
        "skills": r"(skills|technical skills|core competencies|expertise)",
        "projects": r"(projects|personal projects|academic projects|portfolio)"
    }

    lines = text.split(". ")
    current_section = "full"

    for line in lines:
        line_lower = line.lower().strip()
        matched = False
        for section, pattern in patterns.items():
            if re.search(pattern, line_lower) and len(line_lower) < 50:
                current_section = section
                matched = True
                break
        if not matched:
            sections[current_section] += " " + line

    return sections
