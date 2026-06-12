# ⚡ ResumeScope AI — ATS Resume Analyzer

An intelligent resume analyzer that extracts skills, calculates ATS compatibility scores, and generates personalized improvement suggestions using NLP and OpenAI API.

---

## 🚀 Features

- **Resume Parsing** — Supports PDF, DOCX, and TXT formats
- **Skill Extraction** — Detects 150+ tech & data skills using NLP keyword matching
- **ATS Score** — Calculates match percentage against any job description
- **Score Breakdown** — Category-wise breakdown (Programming, ML, BI, Cloud, etc.)
- **Action Plan** — Rule-based improvement suggestions (quantification, keywords, format)
- **AI Feedback** — Deep coaching via OpenAI GPT (optional, requires API key)
- **Resume Headline** — Auto-generates a strong resume headline based on your skills

---

## 📁 Project Structure

```
resume_analyzer/
├── app.py              ← Main Streamlit application
├── analyzer.py         ← Skill extraction, ATS scoring, suggestions engine
├── resume_parser.py    ← PDF/DOCX/TXT text extraction
├── ai_feedback.py      ← OpenAI API integration for AI coaching
├── skills_db.py        ← Skills database (150+ skills across 10 categories)
├── requirements.txt    ← Python dependencies
└── README.md           ← This file
```

---

## ⚙️ Setup & Installation

### 1. Clone or download this project

```bash
cd resume_analyzer
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` in your browser.


### 5. Live Demo

Click here:- "[https://ai-resume-analyzer-l4jf3yefxf3wbp6msxq43o.streamlit.app/](url)"
---

## 🔑 OpenAI API Key (Optional)

AI Feedback is optional. Without it, the app still gives you:
- Full ATS score and breakdown
- Matched/missing skills
- Rule-based action plan
- Resume headline suggestion

To enable AI Feedback:
1. Get a key at [platform.openai.com](https://platform.openai.com)
2. Paste it in the sidebar under **AI Feedback (Optional)**

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Charts | Plotly |
| PDF Parsing | PyPDF2 |
| DOCX Parsing | python-docx |
| NLP / Matching | Custom keyword engine |
| AI Feedback | OpenAI GPT-3.5-turbo |
| Language | Python 3.10+ |

---

## 📌 How It Works

1. **Upload** your resume (PDF/DOCX/TXT)
2. **Paste** the job description
3. App **extracts** skills from both using the skills database
4. **Calculates** ATS match score = matched_skills / total_jd_skills × 100
5. **Generates** rule-based suggestions (quantification, missing keywords, format)
6. (Optional) **Calls OpenAI** for deeper analysis and AI coaching
7. Displays results across 4 tabs: Skills Analysis, Action Plan, AI Feedback, Raw Text

---

## 📊 Resume Highlight (for your own resume)

> *"Built NLP-powered Resume Analyzer with ATS compatibility scoring, real-time skill gap detection across 150+ technologies, and GPT-powered improvement plans — parsing PDF/DOCX resumes against live job descriptions."*

---

## 👩‍💻 Author

Built as a Month 4 PGC Data Science capstone project.
