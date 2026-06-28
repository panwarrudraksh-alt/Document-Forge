import streamlit as st
from datetime import datetime
import time
import os
from pdf_generator import (
    generate_resume_pdf,
    generate_cv_pdf,
    generate_cover_letter_pdf,
    generate_proposal_pdf,
    generate_experience_letter_pdf
)
from job_scraper import get_jobs
from ai_utils import ai_suggest_improvements, ai_autofill_skills, ai_generate_summary, ai_generate_cover_letter
from chat_utils import chat_with_ai

# ---- Page Config ----
st.set_page_config(
    page_title="DocForge – Professional Document Builder",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Custom CSS with darker backgrounds ----
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    * {
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    html {
        scroll-behavior: smooth;
    }

    :root {
        /* Light theme – now darker */
        --bg-start: #dce3ea;
        --bg-end: #c5d0dd;
        --text-color: #102a43;
        --text-light: #3d5a78;
        --card-bg: rgba(255,255,255,0.88);
        --card-border: rgba(51,163,220,0.25);
        --input-bg: #ffffff;
        --input-border: #b0c4de;
        --tab-bg: #e1e8f0;
        --tab-selected: #1e6f9f;
        --header-bg: linear-gradient(135deg, #0b2b44, #1e6f9f);
        --header-text: #ffffff;
        --header-subtext: #d9e2ec;
        --btn-bg: linear-gradient(135deg, #1e6f9f, #33a3dc);
        --btn-text: #ffffff;
        --shadow-color: rgba(11,43,68,0.2);
        --primary: #1e6f9f;
        --primary-light: #33a3dc;
        --primary-dark: #0b2b44;
        --section-bg: #f0f4f8;
        --support-bg: #dce3ea;
    }

    [data-theme="dark"] {
        /* Dark theme – now darker */
        --bg-start: #0b1a2a;
        --bg-end: #1a2a3a;
        --text-color: #f0f4f8;
        --text-light: #b0c4de;
        --card-bg: rgba(20,35,50,0.88);
        --card-border: rgba(51,163,220,0.25);
        --input-bg: #1a2a3a;
        --input-border: #2a4a6a;
        --tab-bg: #1a2a3a;
        --tab-selected: #33a3dc;
        --header-bg: linear-gradient(135deg, #0b2b44, #1e6f9f);
        --header-text: #ffffff;
        --header-subtext: #b0c4de;
        --btn-bg: linear-gradient(135deg, #1e6f9f, #33a3dc);
        --btn-text: #ffffff;
        --shadow-color: rgba(0,0,0,0.4);
        --primary: #33a3dc;
        --primary-light: #66c2e8;
        --primary-dark: #1a4a6a;
        --section-bg: #1a2a3a;
        --support-bg: #0b1a2a;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(51,163,220,0.08), transparent 40%),
            linear-gradient(135deg, var(--bg-start), var(--bg-end));
        padding: 0;
    }

    section[data-testid="stSidebar"] {
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        border-right: 1px solid var(--card-border);
    }
    section[data-testid="stSidebar"] * {
        color: var(--text-color) !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: var(--text-light) !important;
        font-weight: 500;
        padding: 0.3rem 0.8rem;
        border-radius: 8px;
        transition: background 0.2s;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        background: var(--card-border);
    }
    section[data-testid="stSidebar"] .stRadio label[data-selected="true"] {
        background: var(--primary);
        color: white !important;
        font-weight: 600;
    }
    section[data-testid="stSidebar"] .stMetric {
        background: rgba(255,255,255,0.3);
        border-radius: 12px;
        padding: 0.5rem;
        border: 1px solid var(--card-border);
    }
    section[data-testid="stSidebar"] .stMetric label {
        color: var(--text-light) !important;
    }
    section[data-testid="stSidebar"] .stMetric .stMetricValue {
        color: var(--text-color) !important;
        font-weight: 600;
    }

    .hero { text-align: center; padding: 3rem 1rem; animation: fadeInUp 0.8s ease; }
    .hero h1 { font-size: 2.8rem; font-weight: 900; color: var(--text-color); }
    .hero h1 span { background: linear-gradient(135deg, var(--primary), var(--primary-light)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    .hero p { font-size: 1.2rem; color: var(--text-light); max-width: 700px; margin: 0 auto 2rem; }
    .hero .buttons { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }
    .hero .buttons .btn-primary {
        background: var(--btn-bg); color: var(--btn-text); padding: 0.8rem 2rem; border-radius: 12px; font-weight: 600; border: none; box-shadow: 0 10px 25px var(--shadow-color); transition: all 0.3s; text-decoration: none; display: inline-block;
    }
    .hero .buttons .btn-primary:hover { transform: translateY(-3px); box-shadow: 0 18px 35px var(--shadow-color); }
    .hero .buttons .btn-secondary {
        background: transparent; color: var(--text-color); padding: 0.8rem 2rem; border-radius: 12px; font-weight: 600; border: 1px solid var(--card-border); transition: all 0.3s; text-decoration: none; display: inline-block;
    }
    .hero .buttons .btn-secondary:hover { background: var(--card-bg); border-color: var(--primary); }
    .hero .buttons .btn-support {
        background: #f43f5e; color: white; padding: 0.8rem 2rem; border-radius: 12px; font-weight: 600; border: none; box-shadow: 0 10px 25px rgba(244,63,94,0.3); transition: all 0.3s; text-decoration: none; display: inline-block;
    }
    .hero .buttons .btn-support:hover { transform: translateY(-3px); box-shadow: 0 18px 35px rgba(244,63,94,0.4); background: #e11d48; }

    .about-section {
        background: var(--card-bg);
        backdrop-filter: blur(8px);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 3rem 0;
        border: 1px solid var(--card-border);
        display: flex;
        align-items: center;
        gap: 2rem;
        flex-wrap: wrap;
        scroll-margin-top: 80px;
    }
    .about-section .text { flex: 1; }
    .about-section .text h2 { color: var(--text-color); font-weight: 800; font-size: 2rem; margin-top: 0; }
    .about-section .text p { color: var(--text-light); font-size: 1.05rem; line-height: 1.7; margin: 0.5rem 0; }
    .about-section .avatar {
        width: 120px;
        height: 120px;
        background: var(--primary);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        font-weight: 700;
        box-shadow: 0 10px 30px var(--shadow-color);
        flex-shrink: 0;
    }
    @media (max-width: 768px) {
        .about-section { flex-direction: column; text-align: center; }
        .about-section .avatar { width: 100px; height: 100px; font-size: 2.5rem; }
    }

    .feature-card-btn {
        display: block;
        width: 100%;
        background: var(--card-bg);
        backdrop-filter: blur(8px);
        border: 1px solid var(--card-border);
        border-radius: 24px;
        padding: 2rem 1.5rem;
        text-align: center;
        transition: all 0.3s;
        cursor: pointer;
        font-family: inherit;
        color: var(--text-color);
        font-size: 1rem;
        line-height: 1.5;
        box-shadow: none;
    }
    .feature-card-btn:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px var(--shadow-color);
        border-color: var(--primary);
    }
    .feature-card-btn .icon {
        font-size: 2.8rem;
        display: block;
        margin-bottom: 0.5rem;
    }
    .feature-card-btn h3 {
        font-weight: 700;
        font-size: 1.3rem;
        margin: 0.5rem 0 0.25rem;
    }
    .feature-card-btn p {
        color: var(--text-light);
        font-size: 0.95rem;
        margin: 0;
    }
    .feature-card-btn:active {
        transform: scale(0.98);
    }

    .section-header { text-align: center; margin: 3rem 0 2rem; }
    .section-header .badge { display: inline-block; background: var(--card-border); color: var(--primary); padding: 0.2rem 1rem; border-radius: 30px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .section-header h2 { font-size: 2.5rem; font-weight: 800; color: var(--text-color); margin-top: 0.5rem; }
    .section-header p { color: var(--text-light); max-width: 600px; margin: 0.5rem auto 0; }

    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }

    .cta-section {
        background: var(--header-bg);
        border-radius: 32px;
        padding: 3rem 2rem;
        text-align: center;
        color: white;
        margin: 3rem 0;
        box-shadow: 0 20px 50px var(--shadow-color);
    }
    .cta-section h2 { font-size: 2.5rem; font-weight: 800; }
    .cta-section p { opacity: 0.9; max-width: 600px; margin: 0.5rem auto 1.5rem; }

    button[data-testid="baseButton-cta_start_building"] {
        background: white !important;
        color: var(--primary-dark) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2.5rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;
        transition: all 0.3s !important;
        width: auto !important;
        display: inline-block !important;
    }
    button[data-testid="baseButton-cta_start_building"]:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 15px 40px rgba(0,0,0,0.3) !important;
        background: #f8f9fa !important;
    }

    .footer {
        border-top: 1px solid var(--card-border);
        padding: 2rem 0;
        margin-top: 3rem;
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        color: var(--text-light);
        font-size: 0.9rem;
    }
    .footer .links a {
        color: var(--text-light);
        text-decoration: none;
        margin-left: 1.5rem;
        transition: color 0.2s;
    }
    .footer .links a:hover { color: var(--primary); }

    .support-section {
        background: var(--card-bg);
        backdrop-filter: blur(8px);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 3rem 0;
        border: 1px solid var(--card-border);
        text-align: center;
        scroll-margin-top: 80px;
    }
    .support-section h2 {
        color: var(--text-color);
        font-weight: 800;
        font-size: 2rem;
    }
    .support-section p {
        color: var(--text-light);
        font-size: 1.05rem;
        max-width: 600px;
        margin: 0.5rem auto;
        line-height: 1.7;
    }

    .doc-page { max-width: 1200px; margin: 0 auto; padding: 1.5rem 1rem; }
    .doc-page .header { margin-bottom: 2rem; }
    .doc-page .header h1 { font-size: 2.2rem; font-weight: 800; color: var(--text-color); }
    .doc-page .header p { color: var(--text-light); font-size: 1.1rem; }

    .chat-float {
        position: fixed;
        bottom: 90px;
        right: 20px;
        width: 380px;
        max-width: 90vw;
        max-height: 70vh;
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        border: 1px solid var(--card-border);
        border-radius: 24px;
        box-shadow: 0 20px 60px var(--shadow-color);
        z-index: 999;
        display: none;
        flex-direction: column;
        overflow: hidden;
        padding: 0;
    }
    .chat-float.open { display: flex; }
    .chat-float .chat-header {
        padding: 0.8rem 1.2rem;
        background: var(--header-bg);
        color: white;
        font-weight: 700;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-shrink: 0;
    }
    .chat-float .chat-header button {
        background: none;
        border: none;
        color: white;
        font-size: 1.2rem;
        cursor: pointer;
    }
    .chat-float .chat-body {
        flex: 1;
        overflow-y: auto;
        padding: 1rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    .chat-toggle-btn {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        z-index: 1000;
        background: var(--primary);
        color: white;
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 2rem;
        box-shadow: 0 8px 25px var(--shadow-color);
        cursor: pointer;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .chat-toggle-btn:hover { transform: scale(1.05); }

    @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    .fade-in { animation: fadeInUp 0.6s ease forwards; }

    @media (max-width: 768px) {
        .hero h1 { font-size: 2.2rem; }
        .features-grid { grid-template-columns: 1fr; }
        .chat-float { width: 90vw; right: 5vw; }
        .about-section { flex-direction: column; text-align: center; }
        .support-section { padding: 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)

# ---- JavaScript ----
st.markdown("""
<script>
    function toggleTheme() {
        const html = document.documentElement;
        const current = html.getAttribute('data-theme');
        const newTheme = current === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    }
    (function() {
        const saved = localStorage.getItem('theme');
        if (saved) { document.documentElement.setAttribute('data-theme', saved); }
        else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.setAttribute('data-theme', 'dark');
        }
    })();
    function toggleChat() {
        const chat = document.getElementById('chat-float');
        if (chat) chat.classList.toggle('open');
    }
</script>
""", unsafe_allow_html=True)

# ---- Session State ----
if "skills" not in st.session_state:
    st.session_state.skills = []
if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---- Page navigation helper ----
def go_to_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# ---- Sidebar Navigation ----
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:0.5rem 0;">
        <div style="font-size:2.5rem;">📄</div>
        <div style="font-weight:700; font-size:1.4rem; color:var(--text-color);">DocForge</div>
        <div style="color:var(--text-light); font-size:0.85rem;">Professional Documents</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    page_choices = ["🏠 Home", "📝 Builder", "📄 Resume", "📋 CV", "✉️ Cover Letter", "📊 Proposal", "🏆 Experience", "🔍 Job Scraper", "🤖 AI Assistant"]
    current_index = page_choices.index([p for p in page_choices if p.split(" ")[-1] == st.session_state.page][0]) if any(p.split(" ")[-1] == st.session_state.page for p in page_choices) else 0

    selected = st.radio(
        "Navigate",
        page_choices,
        index=current_index,
        label_visibility="collapsed"
    )
    page_map = {
        "🏠 Home": "Home",
        "📝 Builder": "Builder",
        "📄 Resume": "Resume",
        "📋 CV": "CV",
        "✉️ Cover Letter": "CoverLetter",
        "📊 Proposal": "Proposal",
        "🏆 Experience": "Experience",
        "🔍 Job Scraper": "JobScraper",
        "🤖 AI Assistant": "AIAssistant"
    }
    if selected:
        st.session_state.page = page_map[selected]

    st.markdown("---")
    col1, col2 = st.columns(2)
    col1.metric("🛠️ Skills", len(st.session_state.skills))
    col2.metric("💼 Jobs", len(st.session_state.jobs))
    st.caption("⚡ Streamlit · ReportLab")

    st.markdown("---")
    if st.button("🌓 Toggle Theme", use_container_width=True):
        st.markdown("<script>toggleTheme();</script>", unsafe_allow_html=True)

# ---- Determine current page ----
page = st.session_state.page

# ---- Helper ----
def get_user_data():
    return {
        "name": st.session_state.get("f_name", ""),
        "title": st.session_state.get("f_title", ""),
        "email": st.session_state.get("f_email", ""),
        "phone": st.session_state.get("f_phone", ""),
        "location": st.session_state.get("f_loc", ""),
        "linkedin": st.session_state.get("f_linkedin", ""),
        "skills": st.session_state.skills,
        "company": st.session_state.get("f_company", ""),
        "role": st.session_state.get("f_exp_role", ""),
        "duration": st.session_state.get("f_duration", ""),
        "exp_desc": st.session_state.get("f_exp_desc", ""),
        "degree": st.session_state.get("f_degree", ""),
        "institution": st.session_state.get("f_inst", ""),
        "year": st.session_state.get("f_year", ""),
        "projects": st.session_state.get("f_projects", ""),
        "summary": st.session_state.get("f_summary", ""),
        "theme": "Classic Green",
    }

# ==================== PAGES ====================

if page == "Home":
    st.markdown("""
    <div class="hero">
        <h1>Create <span>Professional Documents</span><br>Instantly</h1>
        <p>Build resumes, CVs, cover letters, proposals, and experience letters – all from one platform. No design skills needed.</p>
        <div class="buttons">
            <a href="#" class="btn-primary" onclick="document.querySelector('[data-testid=\\"stButton\\"] button')?.click()">Get Started Free</a>
            <a href="#about" class="btn-secondary">Learn More</a>
            <a href="#support-section" class="btn-support">Support Me 💖</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Hidden button for "Get Started Free"
    if st.button("Get Started Free (hidden)", key="home_get_started", use_container_width=False, type="primary"):
        go_to_page("Builder")

    # About Me
    st.markdown("""
    <div class="about-section" id="about">
        <div class="text">
            <h2>👋 About Me</h2>
            <p><strong>Rudraksh Panwar</strong><br>
            B.Sc Computer Science student at <strong>IIMT College of Science and Technology</strong>.</p>
            <p><strong>Skills:</strong> MySQL, Python<br>
            <strong>Currently learning:</strong> GUI Development, Operating System concepts.</p>
            <p>I built DocForge as a project to help students and professionals create polished documents effortlessly.
            Passionate about technology, coding, and building things that make life easier.</p>
        </div>
        <div class="avatar">RP</div>
    </div>
    """, unsafe_allow_html=True)

    # Features – clickable cards
    st.markdown("""
    <div class="section-header">
        <span class="badge">Features</span>
        <h2>Everything You Need</h2>
        <p>Click any card to jump directly to that tool.</p>
    </div>
    <div class="features-grid">
    """, unsafe_allow_html=True)

    features = [
        ("📄", "Resume Builder", "ATS-friendly resumes with multiple themes.", "Resume"),
        ("📋", "CV Generator", "Comprehensive curriculum vitae with publications.", "CV"),
        ("✉️", "Cover Letters", "Personalized letters for job applications.", "CoverLetter"),
        ("📊", "Proposal Generator", "Professional project proposals for clients.", "Proposal"),
        ("🏆", "Experience Letters", "Employment verification letters.", "Experience"),
        ("🔍", "Job Scraper", "Find jobs and match your skills.", "JobScraper"),
        ("🤖", "AI Assistant", "Get AI-powered suggestions and help.", "AIAssistant"),
    ]

    cols = st.columns(3)
    for i, (icon, title, desc, page_key) in enumerate(features):
        with cols[i % 3]:
            if st.button(
                f"{icon}\n\n**{title}**\n\n{desc}",
                key=f"home_feature_{page_key}",
                use_container_width=True,
                type="secondary",
            ):
                go_to_page(page_key)

    st.markdown("</div>", unsafe_allow_html=True)

    # CTA
    st.markdown("""
    <div class="cta-section">
        <h2>Ready to Build Your Document?</h2>
        <p>Get started now – it's free and takes less than 5 minutes.</p>
        <div style="display: flex; justify-content: center; margin-top: 1.5rem;">
    """, unsafe_allow_html=True)

    if st.button("Start Building", key="cta_start_building", use_container_width=False, type="primary"):
        go_to_page("Builder")

    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- SUPPORT SECTION with QR code ----
    st.markdown("""
    <div class="support-section" id="support-section">
        <h2>❤️ Support the Developer</h2>
        <p>
            If DocForge has helped you create professional documents, consider supporting my work.
            Every contribution, no matter how small, helps me keep building free tools for students and professionals like you.
            Your support fuels my passion to create more useful tools and improve existing ones.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ---- QR Code – try multiple paths ----
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # List of possible file locations (relative to app root)
        possible_paths = [
            "api_qr.jpeg",
            "./api_qr.jpeg",
            "static/api_qr.jpeg",
            "./static/api_qr.jpeg",
            "api_qr.png",
            "static/api_qr.png",
        ]
        
        found = False
        for path in possible_paths:
            if os.path.exists(path):
                st.image(path, caption="Scan to support", use_container_width=True)
                found = True
                break
        
        if not found:
            st.error("""
            **QR Code not found.**  
            Please ensure the file is named `api_qr.jpeg` and placed in the **root folder** of your repository (same level as `app.py`).
            """)
        
        st.markdown("""
        <div style="text-align: center; padding-bottom: 2rem;">
            <p style="color: var(--text-light); font-size: 0.95rem;">
                Scan the QR code with your UPI app to send a payment. Every contribution counts – thank you! 🙏
            </p>
        </div>
        """, unsafe_allow_html=True)

# ---- BUILDER (unchanged) ----
elif page == "Builder":
    st.markdown("""
    <div class="doc-page">
        <div class="header">
            <h1>📝 Document Builder</h1>
            <p>Fill your information once. All documents will use this data.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["👤 Personal", "💼 Experience", "🎓 Education", "🛠️ Skills", "📝 Extra"])

    with tabs[0]:
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Full Name *", key="f_name", placeholder="John Doe")
            st.text_input("Email *", key="f_email", placeholder="john@example.com")
            st.text_input("Phone", key="f_phone", placeholder="+1 234 567 890")
        with col2:
            st.text_input("Professional Title", key="f_title", placeholder="Software Engineer")
            st.text_input("Location", key="f_loc", placeholder="San Francisco, CA")
            st.text_input("LinkedIn URL", key="f_linkedin", placeholder="linkedin.com/in/john")

    with tabs[1]:
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Company", key="f_company", placeholder="Tech Corp")
            st.text_input("Role", key="f_exp_role", placeholder="Senior Developer")
        with col2:
            st.text_input("Duration", key="f_duration", placeholder="Jan 2020 – Present")
        st.text_area("Job Description", key="f_exp_desc", placeholder="• Built REST APIs serving 10k users/day\n• Led team of 5 developers", height=120)
        col_ai1, col_ai2 = st.columns([4, 1])
        with col_ai2:
            if st.button("✨ Improve", key="improve_exp"):
                improved = ai_suggest_improvements("job description", st.session_state.f_exp_desc)
                if improved and "Error" not in improved:
                    st.session_state.f_exp_desc = improved
                    st.rerun()
                else:
                    st.warning("AI suggestion failed. Please try again.")

    with tabs[2]:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("Degree", key="f_degree", placeholder="B.Tech Computer Science")
        with col2:
            st.text_input("Institution", key="f_inst", placeholder="Stanford University")
        with col3:
            st.text_input("Year", key="f_year", placeholder="2016 – 2020")

    with tabs[3]:
        col1, col2 = st.columns([3, 1])
        with col1:
            new_skill = st.text_input("Add a skill", key="skill_input", placeholder="Python, React, SQL...")
        with col2:
            if st.button("➕ Add", use_container_width=True) and new_skill.strip():
                s = new_skill.strip().lower()
                if s not in st.session_state.skills:
                    st.session_state.skills.append(s)
                st.rerun()

        job_title_for_skills = st.text_input("Job Title for Skill Suggestions", placeholder="e.g., Data Scientist")
        if st.button("🤖 Suggest Skills") and job_title_for_skills:
            suggested = ai_autofill_skills(job_title_for_skills)
            if suggested and "Error" not in suggested:
                skills_list = [s.strip().lower() for s in suggested.split(',') if s.strip()]
                for sk in skills_list:
                    if sk not in st.session_state.skills:
                        st.session_state.skills.append(sk)
                st.rerun()
            else:
                st.warning("Could not get skill suggestions. Please try again.")

        if st.session_state.skills:
            st.markdown("**Your Skills:**")
            cols = st.columns(6)
            for i, sk in enumerate(st.session_state.skills):
                with cols[i % 6]:
                    if st.button(f"✕ {sk.title()}", key=f"rm_{sk}"):
                        st.session_state.skills.remove(sk)
                        st.rerun()
        else:
            st.info("No skills added yet.")

        st.text_area("Projects (one per line)", key="f_projects", placeholder="ResumeForge — AI resume builder\nTaskBot — Slack automation", height=100)

    with tabs[4]:
        summary = st.text_area("Professional Summary", key="f_summary", placeholder="Experienced software engineer with 5+ years...", height=100)
        col_ai1, col_ai2 = st.columns([4, 1])
        with col_ai2:
            if st.button("✨ Improve", key="improve_summary"):
                improved = ai_suggest_improvements("professional summary", st.session_state.f_summary)
                if improved and "Error" not in improved:
                    st.session_state.f_summary = improved
                    st.rerun()
                else:
                    st.warning("AI suggestion failed. Please try again.")

    if st.button("💾 Save Information", type="primary", use_container_width=True):
        st.success("✅ All information saved!")

# ---- Resume, CV, Cover Letter, Proposal, Experience, Job Scraper, AI Assistant (unchanged) ----
# ... (keep all your existing code for these pages) ...

# ---- FOOTER ----
st.markdown("""
<div class="footer">
    <span>© 2026 DocForge – Built with ❤️ by Rudraksh Panwar</span>
    <div class="links">
        <a href="#">Privacy</a>
        <a href="#">Terms</a>
        <a href="#">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- FLOATING CHAT ----
if "show_chat" not in st.session_state:
    st.session_state.show_chat = False

st.markdown("""
<button class="chat-toggle-btn" onclick="toggleChat()">
    💬
</button>
""", unsafe_allow_html=True)

chat_placeholder = st.empty()

if st.session_state.show_chat:
    with chat_placeholder.container():
        st.markdown("""
        <div id="chat-float" class="chat-float open">
            <div class="chat-header">
                <span>🤖 DocForge Assistant</span>
                <button onclick="document.getElementById('chat-float').classList.remove('open'); toggleChat();">✕</button>
            </div>
            <div class="chat-body">
        """, unsafe_allow_html=True)

        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        prompt = st.chat_input("Ask me anything about resumes, careers, or documents...", key="chat_input")
        if prompt:
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            response = chat_with_ai(prompt, st.session_state.chat_messages[:-1])
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.rerun()

        st.markdown("""
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    pass

st.markdown("""
<script>
    function toggleChat() {
        const chat = document.getElementById('chat-float');
        if (chat) {
            chat.classList.toggle('open');
        }
    }
</script>
""", unsafe_allow_html=True)
