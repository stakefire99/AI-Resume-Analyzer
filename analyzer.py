"""
Analyzer — Skill extraction, ATS scoring, and suggestions engine
"""

import re
from skills_db import ALL_SKILLS, SKILLS, ALIASES


# ─────────────────────────────────────────────
# SKILL EXTRACTION
# ─────────────────────────────────────────────

def extract_skills(text: str) -> list[str]:
    """
    Extract skills from text using skill database + aliases.
    Returns sorted list of unique matched skills.
    """
    text_lower = text.lower()
    found = set()

    # Check aliases first (e.g., "sklearn" → "Scikit-learn")
    for alias, canonical in ALIASES.items():
        if alias in text_lower:
            found.add(canonical)

    # Check all skills
    for skill in ALL_SKILLS:
        skill_lower = skill.lower()
        # Use word boundary matching for short skills to avoid false positives
        if len(skill_lower) <= 3:
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            if re.search(pattern, text_lower):
                found.add(skill)
        else:
            if skill_lower in text_lower:
                found.add(skill)

    return sorted(found)


def get_skills_by_category(skills_list: list[str]) -> dict:
    """Group a list of skills by their category."""
    categorized = {}
    for category, skills in SKILLS.items():
        matched = [s for s in skills if s in skills_list]
        if matched:
            categorized[category] = matched
    return categorized


# ─────────────────────────────────────────────
# SCORING
# ─────────────────────────────────────────────

def calculate_match_score(resume_skills: list, jd_skills: list) -> dict:
    """
    Calculate ATS compatibility score with breakdown.
    Returns: overall score + category breakdown
    """
    if not jd_skills:
        return {"overall": 0, "breakdown": {}, "matched": [], "missing": []}

    resume_set = {s.lower() for s in resume_skills}
    jd_set = {s.lower() for s in jd_skills}

    matched = [s for s in jd_skills if s.lower() in resume_set]
    missing = [s for s in jd_skills if s.lower() not in resume_set]

    overall = round(len(matched) / len(jd_skills) * 100)

    # Category breakdown
    breakdown = {}
    for category, skills in SKILLS.items():
        cat_jd = [s for s in jd_skills if s in skills]
        if cat_jd:
            cat_matched = [s for s in cat_jd if s.lower() in resume_set]
            breakdown[category] = round(len(cat_matched) / len(cat_jd) * 100)

    return {
        "overall": overall,
        "breakdown": breakdown,
        "matched": matched,
        "missing": missing
    }


def score_label(score: int) -> tuple[str, str]:
    """Returns (label, color_hex) for a given score."""
    if score >= 80:
        return "Excellent Match", "#00e5a0"
    elif score >= 65:
        return "Good Match", "#4CAF50"
    elif score >= 50:
        return "Fair Match", "#FFC107"
    elif score >= 35:
        return "Weak Match", "#FF9800"
    else:
        return "Poor Match", "#F44336"


# ─────────────────────────────────────────────
# SUGGESTIONS ENGINE
# ─────────────────────────────────────────────

def generate_suggestions(
    resume_text: str,
    jd_text: str,
    missing_skills: list,
    score: int
) -> list[dict]:
    """
    Generate rule-based improvement suggestions.
    Returns list of dicts with title + detail.
    """
    suggestions = []

    # 1. Missing skills suggestion
    if missing_skills:
        top_missing = missing_skills[:5]
        suggestions.append({
            "icon": "🎯",
            "title": "Add Missing Skills to Your Resume",
            "detail": f"Your resume is missing these key JD skills: **{', '.join(top_missing)}**. "
                      f"Add them to your Skills section and support each with a project or experience example."
        })

    # 2. Quantification check
    numbers_in_resume = len(re.findall(r'\d+%|\d+x|\$\d+|\d+ (users|records|projects|models|datasets)', resume_text.lower()))
    if numbers_in_resume < 3:
        suggestions.append({
            "icon": "📊",
            "title": "Quantify Your Achievements",
            "detail": "Your resume has few measurable results. Replace vague statements with numbers: "
                      "'Improved model accuracy by 15%', 'Analyzed 500K+ records', 'Reduced processing time by 40%'."
        })

    # 3. Action verbs check
    weak_words = ["worked on", "helped with", "assisted", "was responsible for", "did"]
    found_weak = [w for w in weak_words if w in resume_text.lower()]
    if found_weak:
        suggestions.append({
            "icon": "✍️",
            "title": "Replace Weak Verbs with Power Verbs",
            "detail": f"Avoid passive phrases like '{found_weak[0]}'. Use strong action verbs: "
                      "'Built', 'Developed', 'Designed', 'Optimized', 'Deployed', 'Led', 'Automated'."
        })

    # 4. Projects section check
    if "project" not in resume_text.lower():
        suggestions.append({
            "icon": "🛠️",
            "title": "Add a Projects Section",
            "detail": "No projects found on your resume. For data/tech roles, projects are critical. "
                      "Include 2-3 relevant projects with: Tech Stack Used → Problem Solved → Impact/Result."
        })

    # 5. Keywords density
    if score < 50:
        suggestions.append({
            "icon": "🔑",
            "title": "Mirror the Job Description Language",
            "detail": "Your resume language doesn't closely match the JD. ATS systems scan for exact keyword matches. "
                      "Use the same terminology the JD uses (e.g., if JD says 'data pipeline', don't say 'data workflow')."
        })

    # 6. Certifications
    cert_keywords = ["certified", "certification", "certificate", "course", "training"]
    has_certs = any(k in resume_text.lower() for k in cert_keywords)
    if not has_certs:
        suggestions.append({
            "icon": "🏅",
            "title": "Add Relevant Certifications",
            "detail": "No certifications detected. Even short online certifications boost ATS scores. "
                      "Consider: Google Data Analytics, IBM Data Science, AWS Cloud Practitioner, or Microsoft Power BI."
        })

    # 7. Summary/objective
    summary_keywords = ["summary", "objective", "profile", "about"]
    has_summary = any(k in resume_text.lower() for k in summary_keywords)
    if not has_summary:
        suggestions.append({
            "icon": "👤",
            "title": "Add a Professional Summary",
            "detail": "No summary section found. A 2-3 line summary at the top dramatically improves ATS ranking. "
                      "Format: [Role] with [X years] experience in [key skills], seeking [target role] at [company type]."
        })

    return suggestions[:6]  # Return top 6


# ─────────────────────────────────────────────
# RESUME HEADLINE GENERATOR
# ─────────────────────────────────────────────

def generate_resume_headline(resume_skills: list, jd_text: str) -> str:
    """Generate a suggested resume headline based on matched skills."""
    top_skills = resume_skills[:4]

    # Detect role from JD
    role_keywords = {
        "Data Analyst": ["data analyst", "analytics", "reporting", "dashboards"],
        "Data Scientist": ["data scientist", "machine learning", "predictive model"],
        "Python Developer": ["python developer", "backend", "api", "django", "flask"],
        "ML Engineer": ["ml engineer", "mlops", "model deployment", "pipeline"],
        "BI Analyst": ["bi analyst", "business intelligence", "power bi", "tableau"],
        "Data Engineer": ["data engineer", "etl", "pipeline", "spark", "airflow"],
        "AI Engineer": ["ai engineer", "llm", "generative ai", "langchain"],
    }

    detected_role = "Data & Analytics Professional"
    jd_lower = jd_text.lower()
    for role, keywords in role_keywords.items():
        if any(k in jd_lower for k in keywords):
            detected_role = role
            break

    skills_str = " | ".join(top_skills[:3]) if top_skills else "Python | SQL | Data Analysis"
    return f"{detected_role} — {skills_str}"
