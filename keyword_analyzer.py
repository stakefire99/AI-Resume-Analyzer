"""
Keyword, Visibility & ATS Format Analyzer
Extends beyond skill-matching to cover JD keyword overlap,
recruiter visibility/standout factors, and ATS format compliance.
"""

import re
from collections import Counter

# Common English stopwords to ignore when extracting keywords
STOPWORDS = set("""
a an the and or but if while is are was were be been being have has had
do does did will would shall should can could may might must to of in on
at by for with about against between into through during before after
above below from up down out off over under again further then once
here there when where why how all any both each few more most other some
such no nor not only own same so than too very s t just don now i you he
she it we they this that these those as
""".split())


# ─────────────────────────────────────────────
# 1. KEYWORD MATCHING (broader than skills)
# ─────────────────────────────────────────────

def extract_keywords(text: str, top_n: int = 30) -> list[str]:
    """
    Extract significant keywords/phrases from text (1-2 word terms),
    ignoring stopwords and common filler.
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s\-+#./]', ' ', text)
    words = text.split()

    # Single words (length > 2, not stopwords)
    unigrams = [w for w in words if len(w) > 2 and w not in STOPWORDS]

    # Bigrams (two consecutive non-stopwords)
    bigrams = []
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        if w1 not in STOPWORDS and w2 not in STOPWORDS and len(w1) > 2 and len(w2) > 2:
            bigrams.append(f"{w1} {w2}")

    counts = Counter(unigrams + bigrams)
    # Filter out very common generic words
    generic = {"experience", "role", "team", "work", "ability", "years", "year",
               "knowledge", "strong", "skills", "skill", "job", "company", "etc"}
    filtered = {k: v for k, v in counts.items() if k not in generic}

    return [w for w, _ in Counter(filtered).most_common(top_n)]


def keyword_match_analysis(resume_text: str, jd_text: str) -> dict:
    """
    Compare JD keywords against resume keywords.
    Returns match %, matched keywords, missing keywords.
    """
    jd_keywords = extract_keywords(jd_text, top_n=40)
    resume_keywords = set(extract_keywords(resume_text, top_n=200))
    resume_text_lower = resume_text.lower()

    matched, missing = [], []
    for kw in jd_keywords:
        if kw in resume_keywords or kw in resume_text_lower:
            matched.append(kw)
        else:
            missing.append(kw)

    score = round(len(matched) / len(jd_keywords) * 100) if jd_keywords else 0

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "total_jd_keywords": len(jd_keywords)
    }


# ─────────────────────────────────────────────
# 2. RECRUITER VISIBILITY / STANDOUT SCORE
# ─────────────────────────────────────────────

def visibility_analysis(resume_text: str) -> dict:
    """
    Evaluate factors that make a resume stand out to a human recruiter
    (6-second scan test). Returns score + checklist.
    """
    text_lower = resume_text.lower()
    checks = []
    score = 0
    max_score = 0

    # 1. Quantified achievements (numbers, %, metrics)
    max_score += 20
    metrics = len(re.findall(r'\d+%|\d+x|\$\d[\d,]*|\b\d{2,}\b', resume_text))
    if metrics >= 5:
        checks.append({"label": "Quantified achievements", "pass": True,
                        "detail": f"Found {metrics} numeric/metric mentions — great for impact."})
        score += 20
    elif metrics >= 2:
        checks.append({"label": "Quantified achievements", "pass": "partial",
                        "detail": f"Only {metrics} metrics found. Add more numbers (%, $, counts)."})
        score += 10
    else:
        checks.append({"label": "Quantified achievements", "pass": False,
                        "detail": "Almost no numbers found. Quantify your impact (e.g. 'improved X by 20%')."})

    # 2. Strong action verbs at line starts
    max_score += 15
    action_verbs = ["built", "developed", "designed", "led", "created", "implemented",
                    "optimized", "automated", "launched", "managed", "improved",
                    "deployed", "analyzed", "engineered", "delivered", "achieved"]
    verb_count = sum(text_lower.count(v) for v in action_verbs)
    if verb_count >= 6:
        checks.append({"label": "Strong action verbs", "pass": True,
                        "detail": f"Found {verb_count} strong action verbs — sounds proactive and impactful."})
        score += 15
    elif verb_count >= 3:
        checks.append({"label": "Strong action verbs", "pass": "partial",
                        "detail": f"Found {verb_count} action verbs. Aim for at least 6-8 across your bullets."})
        score += 8
    else:
        checks.append({"label": "Strong action verbs", "pass": False,
                        "detail": "Few action verbs found. Start bullets with words like 'Built', 'Led', 'Automated'."})

    # 3. Project/portfolio links (GitHub, live demos, portfolio)
    max_score += 15
    link_patterns = ["github.com", "linkedin.com", ".streamlit.app", "vercel.app",
                     "netlify.app", "portfolio", "http://", "https://"]
    has_links = any(p in text_lower for p in link_patterns)
    if has_links:
        checks.append({"label": "Clickable links (GitHub/Portfolio/LinkedIn)", "pass": True,
                        "detail": "Links detected — recruiters can verify your work directly."})
        score += 15
    else:
        checks.append({"label": "Clickable links (GitHub/Portfolio/LinkedIn)", "pass": False,
                        "detail": "No links found. Add GitHub, LinkedIn, or live project URLs to stand out."})

    # 4. Length check (not too short, not too long)
    max_score += 15
    word_count = len(resume_text.split())
    if 350 <= word_count <= 1100:
        checks.append({"label": "Resume length", "pass": True,
                        "detail": f"~{word_count} words — ideal length for a recruiter's 6-second scan."})
        score += 15
    elif word_count < 350:
        checks.append({"label": "Resume length", "pass": "partial",
                        "detail": f"~{word_count} words — feels thin. Add more project/impact details."})
        score += 7
    else:
        checks.append({"label": "Resume length", "pass": "partial",
                        "detail": f"~{word_count} words — may be too long. Trim to 1 page (~500-800 words)."})
        score += 7

    # 5. Unique/standout section (projects, certifications, achievements)
    max_score += 15
    standout_sections = ["project", "certification", "achievement", "award", "publication", "hackathon"]
    found_sections = [s for s in standout_sections if s in text_lower]
    if len(found_sections) >= 2:
        checks.append({"label": "Standout sections present", "pass": True,
                        "detail": f"Found: {', '.join(found_sections)} — these differentiate you from generic resumes."})
        score += 15
    elif found_sections:
        checks.append({"label": "Standout sections present", "pass": "partial",
                        "detail": f"Only found: {', '.join(found_sections)}. Consider adding certifications or hackathon wins."})
        score += 8
    else:
        checks.append({"label": "Standout sections present", "pass": False,
                        "detail": "No projects/certifications/achievements section detected — add one to stand out."})

    # 6. Contact info completeness
    max_score += 10
    has_email = bool(re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', resume_text))
    has_phone = bool(re.search(r'(\+?\d[\d\-\s]{8,}\d)', resume_text))
    if has_email and has_phone:
        checks.append({"label": "Contact information", "pass": True,
                        "detail": "Email and phone number both found."})
        score += 10
    elif has_email or has_phone:
        checks.append({"label": "Contact information", "pass": "partial",
                        "detail": "Only one contact method found. Add both email and phone."})
        score += 5
    else:
        checks.append({"label": "Contact information", "pass": False,
                        "detail": "No email or phone detected — recruiters can't reach you!"})

    # 7. Buzzword overuse check
    max_score += 10
    buzzwords = ["synergy", "go-getter", "team player", "hard worker", "detail-oriented",
                  "self-motivated", "dynamic", "results-driven", "passionate"]
    buzz_count = sum(text_lower.count(b) for b in buzzwords)
    if buzz_count == 0:
        checks.append({"label": "Avoids generic buzzwords", "pass": True,
                        "detail": "No overused buzzwords found — your resume sounds specific and credible."})
        score += 10
    elif buzz_count <= 2:
        checks.append({"label": "Avoids generic buzzwords", "pass": "partial",
                        "detail": f"Found {buzz_count} generic phrase(s). Replace with specific examples."})
        score += 5
    else:
        checks.append({"label": "Avoids generic buzzwords", "pass": False,
                        "detail": f"Found {buzz_count} buzzwords (e.g. 'team player', 'go-getter'). Replace with concrete proof."})

    overall = round((score / max_score) * 100) if max_score else 0
    return {"score": overall, "checks": checks}


# ─────────────────────────────────────────────
# 3. ATS FORMAT COMPLIANCE CHECK
# ─────────────────────────────────────────────

def ats_format_check(resume_text: str, file_extension: str) -> dict:
    """
    Evaluate ATS-friendliness of the resume format.
    Note: structural checks (tables/columns/images) require the raw file,
    so this works primarily on extracted text patterns + file type.
    """
    checks = []
    score = 0
    max_score = 0
    text_lower = resume_text.lower()

    # 1. File format check
    max_score += 20
    if file_extension.lower() in [".docx", ".txt"]:
        checks.append({"label": "File format", "pass": True,
                        "detail": f"{file_extension.upper()} files parse cleanly through most ATS systems."})
        score += 20
    elif file_extension.lower() == ".pdf":
        checks.append({"label": "File format", "pass": "partial",
                        "detail": "PDF is widely accepted, but ensure it's text-based (not a scanned image)."})
        score += 14
    else:
        checks.append({"label": "File format", "pass": False,
                        "detail": "Unusual file format — convert to PDF or DOCX for best ATS compatibility."})

    # 2. Text extraction quality (proxy for tables/columns/images breaking parsing)
    max_score += 25
    word_count = len(resume_text.split())
    char_to_word_ratio = len(resume_text) / max(word_count, 1)
    # Garbled extraction often produces very short or very long "words" / odd ratios
    if word_count > 100 and 3 <= char_to_word_ratio <= 8:
        checks.append({"label": "Clean text extraction", "pass": True,
                        "detail": "Text extracted cleanly — likely a single-column, ATS-friendly layout."})
        score += 25
    elif word_count > 50:
        checks.append({"label": "Clean text extraction", "pass": "partial",
                        "detail": "Text extraction looks slightly irregular — multi-column layouts or text boxes can confuse ATS parsers. Prefer a single-column layout."})
        score += 12
    else:
        checks.append({"label": "Clean text extraction", "pass": False,
                        "detail": "Very little text extracted — likely an image-based/scanned PDF or heavy graphics. ATS cannot read this."})

    # 3. Standard section headers
    max_score += 20
    standard_headers = ["experience", "education", "skills", "projects", "summary", "objective", "certification"]
    found_headers = [h for h in standard_headers if h in text_lower]
    if len(found_headers) >= 4:
        checks.append({"label": "Standard section headers", "pass": True,
                        "detail": f"Found standard headers: {', '.join(found_headers)} — ATS can categorize your content."})
        score += 20
    elif len(found_headers) >= 2:
        checks.append({"label": "Standard section headers", "pass": "partial",
                        "detail": f"Found: {', '.join(found_headers)}. Use clear standard headers like 'Experience', 'Education', 'Skills', 'Projects'."})
        score += 10
    else:
        checks.append({"label": "Standard section headers", "pass": False,
                        "detail": "No standard section headers detected. ATS relies on these to parse your resume correctly."})

    # 4. Special characters / symbols that break parsing
    max_score += 15
    weird_chars = len(re.findall(r'[•◦▪‣⁃➤➢]', resume_text))
    if weird_chars == 0:
        checks.append({"label": "No problematic symbols", "pass": True,
                        "detail": "No unusual bullet/symbol characters that commonly break ATS parsing."})
        score += 15
    else:
        checks.append({"label": "No problematic symbols", "pass": "partial",
                        "detail": f"Found {weird_chars} special bullet symbols. Standard hyphens (-) or round bullets are safer for ATS."})
        score += 8

    # 5. Date format consistency
    max_score += 20
    date_patterns = re.findall(r'\b(19|20)\d{2}\b', resume_text)
    if len(date_patterns) >= 2:
        checks.append({"label": "Dates present and parseable", "pass": True,
                        "detail": f"Found {len(date_patterns)} year references — ATS can extract your timeline."})
        score += 20
    else:
        checks.append({"label": "Dates present and parseable", "pass": "partial",
                        "detail": "Few/no clear years (YYYY) found. Use standard formats like 'Jan 2024 - Present'."})
        score += 8

    overall = round((score / max_score) * 100) if max_score else 0
    return {"score": overall, "checks": checks}
