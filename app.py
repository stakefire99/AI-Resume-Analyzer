"""
ResumeScope AI — ATS Resume Analyzer
Built with Streamlit | Python | OpenAI API
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
from resume_parser import parse_resume
from analyzer import (
    extract_skills, calculate_match_score,
    generate_suggestions, generate_resume_headline, score_label
)
from ai_feedback import get_ai_feedback, is_api_key_valid

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ResumeScope AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600&family=DM+Mono:wght@400;600&display=swap');

    /* Base */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Main background */
    .stApp {
        background-color: #0a0d14;
        color: #e8eaf0;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f1320;
        border-right: 1px solid #1e2435;
    }

    /* Headings */
    h1, h2, h3 {
        font-family: 'Syne', sans-serif !important;
        color: #e8eaf0 !important;
    }

    /* Cards */
    .metric-card {
        background: #111827;
        border: 1px solid #1e2435;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        margin-bottom: 12px;
    }

    .skill-matched {
        background: rgba(0,229,160,0.12);
        color: #00e5a0;
        border: 1px solid rgba(0,229,160,0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-family: 'DM Mono', monospace;
        font-size: 12px;
        font-weight: 600;
        margin: 3px;
        display: inline-block;
    }

    .skill-missing {
        background: rgba(255,94,94,0.10);
        color: #ff7b7b;
        border: 1px solid rgba(255,94,94,0.25);
        padding: 4px 12px;
        border-radius: 20px;
        font-family: 'DM Mono', monospace;
        font-size: 12px;
        font-weight: 600;
        margin: 3px;
        display: inline-block;
    }

    .skill-extra {
        background: rgba(100,130,255,0.12);
        color: #8fa8ff;
        border: 1px solid rgba(100,130,255,0.25);
        padding: 4px 12px;
        border-radius: 20px;
        font-family: 'DM Mono', monospace;
        font-size: 12px;
        font-weight: 600;
        margin: 3px;
        display: inline-block;
    }

    .verdict-box {
        background: rgba(0,229,160,0.06);
        border: 1px solid rgba(0,229,160,0.2);
        border-radius: 12px;
        padding: 16px 20px;
        margin: 12px 0;
    }

    .suggestion-card {
        background: #0d1117;
        border: 1px solid #1e2435;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 10px;
    }

    .headline-box {
        background: linear-gradient(135deg, rgba(0,229,160,0.08), rgba(0,191,255,0.08));
        border: 1px solid rgba(0,229,160,0.3);
        border-radius: 12px;
        padding: 16px 20px;
        font-family: 'DM Mono', monospace;
        font-size: 14px;
        color: #e8eaf0;
        margin: 12px 0;
    }

    .section-label {
        font-family: 'DM Mono', monospace;
        font-size: 11px;
        color: #4a5568;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00e5a0, #00bfff);
        color: #0a0d14;
        border: none;
        border-radius: 10px;
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 15px;
        padding: 12px 32px;
        width: 100%;
        transition: all 0.2s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0,229,160,0.3);
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #111827;
        border: 2px dashed #2a3148;
        border-radius: 14px;
        padding: 8px;
    }

    /* Text area */
    textarea {
        background: #111827 !important;
        color: #e8eaf0 !important;
        border: 1px solid #2a3148 !important;
        border-radius: 10px !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* Text input */
    input[type="text"], input[type="password"] {
        background: #111827 !important;
        color: #e8eaf0 !important;
        border: 1px solid #2a3148 !important;
        border-radius: 8px !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #111827;
        border-radius: 12px;
        padding: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        color: #8892a4;
        font-family: 'DM Sans', sans-serif;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background: #1e2435;
        color: #00e5a0;
        border-radius: 8px;
    }

    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00e5a0, #00bfff);
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #111827;
        border: 1px solid #1e2435;
        border-radius: 10px;
        color: #e8eaf0;
    }

    /* Divider */
    hr {
        border-color: #1e2435;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def render_score_gauge(score: int) -> go.Figure:
    """Render an animated gauge chart for ATS score."""
    label, color = score_label(score)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": "%", "font": {"size": 48, "color": color, "family": "Syne"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#4a5568", "tickfont": {"color": "#4a5568"}},
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": "#1e2435",
            "bordercolor": "#0a0d14",
            "steps": [
                {"range": [0, 35], "color": "rgba(244,67,54,0.15)"},
                {"range": [35, 65], "color": "rgba(255,193,7,0.12)"},
                {"range": [65, 100], "color": "rgba(0,229,160,0.10)"},
            ],
            "threshold": {
                "line": {"color": color, "width": 3},
                "thickness": 0.75,
                "value": score
            }
        },
        title={"text": f"<b>{label}</b>", "font": {"size": 16, "color": "#8892a4", "family": "DM Sans"}}
    ))
    fig.update_layout(
        height=260,
        margin=dict(t=40, b=10, l=20, r=20),
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="#e8eaf0"
    )
    return fig


def render_bar_chart(breakdown: dict) -> go.Figure:
    """Render horizontal bar chart for score breakdown."""
    if not breakdown:
        return None

    categories = list(breakdown.keys())
    scores = list(breakdown.values())
    colors = ["#00e5a0" if s >= 75 else "#FFC107" if s >= 50 else "#F44336" for s in scores]

    fig = go.Figure(go.Bar(
        x=scores, y=categories,
        orientation='h',
        marker_color=colors,
        marker_line_width=0,
        text=[f"{s}%" for s in scores],
        textposition="outside",
        textfont=dict(color="#e8eaf0", size=12, family="DM Mono")
    ))
    fig.update_layout(
        height=max(200, len(categories) * 45),
        margin=dict(t=10, b=10, l=10, r=60),
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        xaxis=dict(range=[0, 120], showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(tickfont=dict(color="#8892a4", size=12, family="DM Sans")),
        bargap=0.3,
        showlegend=False
    )
    return fig


def render_skills_venn_data(matched, missing, extra):
    """Render a simple skills overlap summary chart."""
    fig = go.Figure(go.Bar(
        x=["✓ Matched", "✗ Missing", "➕ Extra (Bonus)"],
        y=[len(matched), len(missing), len(extra)],
        marker_color=["#00e5a0", "#ff7b7b", "#8fa8ff"],
        marker_line_width=0,
        text=[len(matched), len(missing), len(extra)],
        textposition="outside",
        textfont=dict(color="#e8eaf0", size=16, family="Syne", weight="bold")
    ))
    fig.update_layout(
        height=220,
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        xaxis=dict(tickfont=dict(color="#8892a4", size=13, family="DM Sans")),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        showlegend=False,
        bargap=0.4
    )
    return fig


def skills_html(skills_list, skill_type):
    """Render skills as HTML pills."""
    if not skills_list:
        return "<span style='color:#4a5568; font-size:13px;'>None found</span>"
    pills = " ".join([f'<span class="skill-{skill_type}">{s}</span>' for s in skills_list])
    return pills


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0;'>
        <div style='font-size:36px;'>⚡</div>
        <div style='font-family:Syne,sans-serif; font-weight:800; font-size:22px; color:#e8eaf0;'>
            ResumeScope <span style='color:#00e5a0;'>AI</span>
        </div>
        <div style='font-family:DM Mono,monospace; font-size:11px; color:#4a5568; margin-top:4px;'>
            ATS Intelligence Engine v1.0
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Step 1: Upload Resume
    st.markdown("**01 — Upload Resume**")
    uploaded_file = st.file_uploader(
        "PDF, DOCX, or TXT",
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        st.success(f"✓ {uploaded_file.name}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Step 2: Job Description
    st.markdown("**02 — Paste Job Description**")
    jd_text = st.text_area(
        "JD",
        height=180,
        placeholder="Paste the full job description here...",
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Step 3: Optional AI Key
    with st.expander("🤖 AI Feedback (Optional)"):
        st.markdown("""
        <div style='font-size:12px; color:#8892a4; margin-bottom:8px;'>
        Add your OpenAI API key for deep AI-powered coaching beyond rule-based analysis.
        </div>
        """, unsafe_allow_html=True)
        api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
        st.markdown(
            "<div style='font-size:11px; color:#4a5568;'>Get a key at platform.openai.com</div>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("⚡ Analyze My Resume", use_container_width=True)
    
    st.divider()
    st.markdown("""
    <div style='font-size:11px; color:#4a5568; font-family:DM Mono,monospace; text-align:center;'>
    Built with Python · Streamlit · OpenAI<br>
    Skill DB: 150+ tech & data skills
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────

# Hero header (shown before analysis)
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "results" not in st.session_state:
    st.session_state.results = None

if not st.session_state.analysis_done:
    st.markdown("""
    <div style='text-align:center; padding: 60px 20px 40px;'>
        <h1 style='font-family:Syne,sans-serif; font-size:clamp(32px,5vw,52px); font-weight:800;
            line-height:1.1; letter-spacing:-1px; margin-bottom:16px;'>
            Know exactly why you're<br>
            <span style='color:#00e5a0;'>not getting shortlisted.</span>
        </h1>
        <p style='color:#8892a4; font-size:16px; max-width:520px; margin:0 auto 32px;'>
            Upload your resume + paste any job description.<br>
            Get your ATS score, missing skills, and an AI-powered improvement plan.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size:28px; margin-bottom:10px;'>🔍</div>
            <div style='font-family:Syne,sans-serif; font-weight:700; font-size:15px; margin-bottom:6px;'>Skill Extraction</div>
            <div style='color:#8892a4; font-size:13px;'>Detects 150+ tech & data skills from your resume and the JD</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size:28px; margin-bottom:10px;'>🎯</div>
            <div style='font-family:Syne,sans-serif; font-weight:700; font-size:15px; margin-bottom:6px;'>ATS Scoring</div>
            <div style='color:#8892a4; font-size:13px;'>Calculates your match % with visual breakdown by skill category</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size:28px; margin-bottom:10px;'>🤖</div>
            <div style='font-family:Syne,sans-serif; font-weight:700; font-size:15px; margin-bottom:6px;'>AI Coaching</div>
            <div style='color:#8892a4; font-size:13px;'>Specific, actionable improvement suggestions powered by GPT</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; padding: 32px 0 16px; color:#4a5568; font-family:DM Mono,monospace; font-size:12px;'>
        ← Upload your resume and paste a JD in the sidebar to get started
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ANALYSIS LOGIC
# ─────────────────────────────────────────────

if analyze_btn:
    if not uploaded_file:
        st.error("⚠️ Please upload your resume (PDF, DOCX, or TXT).")
    elif not jd_text.strip():
        st.error("⚠️ Please paste the job description.")
    else:
        with st.spinner("🔍 Analyzing your resume..."):
            try:
                # Step 1: Parse resume
                resume_text = parse_resume(uploaded_file)
                if len(resume_text) < 100:
                    st.error("Could not extract enough text from your resume. Try a different format.")
                    st.stop()

                # Step 2: Extract skills
                resume_skills = extract_skills(resume_text)
                jd_skills = extract_skills(jd_text)

                # Step 3: Score
                result = calculate_match_score(resume_skills, jd_skills)
                matched = result["matched"]
                missing = result["missing"]
                score = result["overall"]
                breakdown = result["breakdown"]

                # Extra skills (on resume but not in JD)
                matched_lower = {s.lower() for s in matched}
                extra = [s for s in resume_skills if s.lower() not in matched_lower][:15]

                # Step 4: Suggestions
                suggestions = generate_suggestions(resume_text, jd_text, missing, score)

                # Step 5: Headline
                headline = generate_resume_headline(resume_skills, jd_text)

                # Step 6: AI Feedback (optional)
                ai_result = None
                if api_key and is_api_key_valid(api_key):
                    with st.spinner("🤖 Getting AI feedback..."):
                        ai_result = get_ai_feedback(
                            resume_text, jd_text, matched, missing, score, api_key
                        )

                # Save to session
                st.session_state.results = {
                    "resume_text": resume_text,
                    "jd_text": jd_text,
                    "resume_skills": resume_skills,
                    "jd_skills": jd_skills,
                    "matched": matched,
                    "missing": missing,
                    "extra": extra,
                    "score": score,
                    "breakdown": breakdown,
                    "suggestions": suggestions,
                    "headline": headline,
                    "ai_result": ai_result,
                    "filename": uploaded_file.name
                }
                st.session_state.analysis_done = True
                st.rerun()

            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")


# ─────────────────────────────────────────────
# RESULTS DISPLAY
# ─────────────────────────────────────────────

if st.session_state.analysis_done and st.session_state.results:
    r = st.session_state.results
    score = r["score"]
    label, color = score_label(score)

    # Reset button
    col_title, col_reset = st.columns([4, 1])
    with col_title:
        st.markdown(f"""
        <h2 style='font-family:Syne,sans-serif; font-size:28px; font-weight:800;'>
            Analysis Results
            <span style='font-size:14px; color:#4a5568; font-weight:400; font-family:DM Mono,monospace;'>
            — {r['filename']}
            </span>
        </h2>
        """, unsafe_allow_html=True)
    with col_reset:
        if st.button("🔄 New Analysis"):
            st.session_state.analysis_done = False
            st.session_state.results = None
            st.rerun()

    # ── TOP ROW: Gauge + Quick Stats ──
    col_gauge, col_stats = st.columns([1, 2])

    with col_gauge:
        st.plotly_chart(render_score_gauge(score), use_container_width=True, config={"displayModeBar": False})

    with col_stats:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size:32px; font-weight:800; font-family:Syne,sans-serif; color:#00e5a0;'>{len(r['matched'])}</div>
                <div style='color:#8892a4; font-size:12px; font-family:DM Mono,monospace;'>SKILLS MATCHED</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size:32px; font-weight:800; font-family:Syne,sans-serif; color:#ff7b7b;'>{len(r['missing'])}</div>
                <div style='color:#8892a4; font-size:12px; font-family:DM Mono,monospace;'>SKILLS MISSING</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size:32px; font-weight:800; font-family:Syne,sans-serif; color:#8fa8ff;'>{len(r['jd_skills'])}</div>
                <div style='color:#8892a4; font-size:12px; font-family:DM Mono,monospace;'>JD SKILLS TOTAL</div>
            </div>""", unsafe_allow_html=True)

        # Headline
        st.markdown(f"""
        <div style='margin-top:8px;'>
            <div class='section-label'>💡 Suggested Resume Headline</div>
            <div class='headline-box'>"{r['headline']}"</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── TABS ──
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Skills Analysis",
        "🎯 Action Plan",
        "🤖 AI Feedback",
        "📄 Raw Text"
    ])

    # ─── TAB 1: Skills Analysis ───
    with tab1:
        col_l, col_r = st.columns(2)

        with col_l:
            st.markdown('<div class="section-label">✓ Matched Skills</div>', unsafe_allow_html=True)
            st.markdown(skills_html(r["matched"], "matched"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-label">✗ Missing Skills (From JD)</div>', unsafe_allow_html=True)
            st.markdown(skills_html(r["missing"], "missing"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-label">➕ Other Skills on Your Resume</div>', unsafe_allow_html=True)
            st.markdown(skills_html(r["extra"], "extra"), unsafe_allow_html=True)

        with col_r:
            # Skills overview chart
            st.markdown('<div class="section-label">Skills Overview</div>', unsafe_allow_html=True)
            st.plotly_chart(
                render_skills_venn_data(r["matched"], r["missing"], r["extra"]),
                use_container_width=True,
                config={"displayModeBar": False}
            )

            # Breakdown by category
            if r["breakdown"]:
                st.markdown('<div class="section-label">Score Breakdown by Category</div>', unsafe_allow_html=True)
                fig = render_bar_chart(r["breakdown"])
                if fig:
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ─── TAB 2: Action Plan ───
    with tab2:
        st.markdown(f"""
        <div class='verdict-box'>
            <div class='section-label' style='margin-bottom:6px;'>Overall Assessment</div>
            <div style='font-size:15px; color:#c8ccd8; line-height:1.6;'>
            Your resume has a <strong style='color:{color};'>{score}% ATS match</strong> — {label.lower()}.
            {"Great position to apply!" if score >= 65 else "Focus on the action plan below to improve your chances."}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">Action Plan</div>', unsafe_allow_html=True)

        for i, sug in enumerate(r["suggestions"]):
            with st.expander(f"{sug['icon']} {sug['title']}"):
                st.markdown(sug["detail"])

    # ─── TAB 3: AI Feedback ───
    with tab3:
        ai = r.get("ai_result")
        if not ai:
            st.markdown("""
            <div style='text-align:center; padding:40px 20px;'>
                <div style='font-size:40px; margin-bottom:16px;'>🤖</div>
                <div style='font-family:Syne,sans-serif; font-size:20px; font-weight:700; margin-bottom:10px;'>
                    AI Feedback Not Enabled
                </div>
                <div style='color:#8892a4; font-size:14px; max-width:400px; margin:0 auto;'>
                    Add your OpenAI API key in the sidebar and re-run the analysis to get deep AI-powered coaching.
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif "error" in ai:
            st.error(f"AI Error: {ai['error']}")
        else:
            # Verdict
            if "verdict" in ai:
                st.markdown(f"""
                <div class='verdict-box'>
                    <div class='section-label' style='margin-bottom:6px;'>🤖 AI Verdict</div>
                    <div style='font-size:15px; color:#c8ccd8; line-height:1.6;'>{ai['verdict']}</div>
                </div>
                """, unsafe_allow_html=True)

            col_l, col_r = st.columns(2)

            with col_l:
                # Strengths
                if "strengths" in ai:
                    st.markdown('<div class="section-label">💪 Your Strengths</div>', unsafe_allow_html=True)
                    for i, s in enumerate(ai["strengths"]):
                        st.markdown(f"""
                        <div style='display:flex; gap:10px; align-items:flex-start; margin-bottom:8px;'>
                            <span style='color:#00e5a0; font-family:DM Mono,monospace; font-size:12px; min-width:20px;'>0{i+1}</span>
                            <span style='font-size:13px; color:#c8ccd8;'>{s}</span>
                        </div>
                        """, unsafe_allow_html=True)

                # Keywords to add
                if "keywords_to_add" in ai:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown('<div class="section-label">🔑 Keywords to Add</div>', unsafe_allow_html=True)
                    st.markdown(skills_html(ai["keywords_to_add"], "extra"), unsafe_allow_html=True)

            with col_r:
                # AI Score Breakdown
                if "score_breakdown" in ai:
                    st.markdown('<div class="section-label">📊 AI Score Breakdown</div>', unsafe_allow_html=True)
                    for cat, val in ai["score_breakdown"].items():
                        color_bar = "#00e5a0" if val >= 75 else "#FFC107" if val >= 50 else "#F44336"
                        st.markdown(f"""
                        <div style='margin-bottom:12px;'>
                            <div style='display:flex; justify-content:space-between; margin-bottom:4px;'>
                                <span style='color:#8892a4; font-size:12px;'>{cat}</span>
                                <span style='color:{color_bar}; font-family:DM Mono,monospace; font-size:12px; font-weight:600;'>{val}%</span>
                            </div>
                            <div style='height:6px; background:#1e2435; border-radius:4px; overflow:hidden;'>
                                <div style='width:{val}%; height:100%; background:{color_bar}; border-radius:4px;'></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                # AI Suggestions
                if "ai_suggestions" in ai:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown('<div class="section-label">🎯 AI Recommendations</div>', unsafe_allow_html=True)
                    for sug in ai["ai_suggestions"]:
                        st.markdown(f"""
                        <div class='suggestion-card'>
                            <div style='font-family:Syne,sans-serif; font-weight:700; font-size:13px; color:#00bfff; margin-bottom:6px;'>→ {sug['title']}</div>
                            <div style='font-size:12px; color:#8892a4; line-height:1.6;'>{sug['detail']}</div>
                        </div>
                        """, unsafe_allow_html=True)

    # ─── TAB 4: Raw Text ───
    with tab4:
        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown('<div class="section-label">Extracted Resume Text</div>', unsafe_allow_html=True)
            st.text_area("", r["resume_text"][:3000], height=400, label_visibility="collapsed")
        with col_r:
            st.markdown('<div class="section-label">Job Description</div>', unsafe_allow_html=True)
            st.text_area("", r["jd_text"][:3000], height=400, label_visibility="collapsed")
