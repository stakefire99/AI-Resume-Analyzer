"""
AI Feedback Module — Uses OpenAI API for deep resume analysis
"""

import os
import json


def get_ai_feedback(
    resume_text: str,
    jd_text: str,
    matched_skills: list,
    missing_skills: list,
    score: int,
    api_key: str
) -> dict:
    """
    Call OpenAI API for advanced AI-powered resume feedback.
    Returns structured JSON with strengths, suggestions, and keywords.
    """
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        prompt = f"""You are an expert ATS consultant and resume coach for tech/data roles.

RESUME (truncated):
{resume_text[:3000]}

JOB DESCRIPTION:
{jd_text[:2000]}

ANALYSIS DATA:
- ATS Match Score: {score}%
- Matched Skills: {', '.join(matched_skills[:15])}
- Missing Skills: {', '.join(missing_skills[:15])}

Respond ONLY with a valid JSON object (no markdown, no extra text):
{{
  "verdict": "One sentence overall assessment of fit",
  "strengths": ["strength 1", "strength 2", "strength 3"],
  "ai_suggestions": [
    {{"title": "Short action title", "detail": "Specific advice"}},
    {{"title": "Short action title", "detail": "Specific advice"}},
    {{"title": "Short action title", "detail": "Specific advice"}}
  ],
  "keywords_to_add": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
  "score_breakdown": {{
    "Skills Match": {score},
    "Keywords": 0,
    "Experience Relevance": 0,
    "Resume Format": 0
  }}
}}

Fill in realistic estimates for Keywords, Experience Relevance, and Resume Format based on the resume content."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1000
        )

        raw = response.choices[0].message.content.strip()
        # Remove markdown code fences if present
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)

    except ImportError:
        return {"error": "openai package not installed. Run: pip install openai"}
    except json.JSONDecodeError:
        return {"error": "AI returned invalid response. Please try again."}
    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower() or "auth" in error_msg.lower():
            return {"error": "Invalid API key. Please check your OpenAI API key."}
        elif "quota" in error_msg.lower() or "billing" in error_msg.lower():
            return {"error": "OpenAI quota exceeded. Check your billing at platform.openai.com"}
        return {"error": f"AI feedback unavailable: {error_msg}"}


def is_api_key_valid(api_key: str) -> bool:
    """Quick check if API key format looks valid."""
    return api_key and api_key.startswith("sk-") and len(api_key) > 20
