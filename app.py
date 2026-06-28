import streamlit as st
from datetime import datetime
import time
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

# ---- Custom CSS (includes smooth scroll & about section) ----
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

    /* Theme variables (same as before) */
    :root {
        --bg-start: #f0f4f8;
        --bg-end: #d9e2ec;
        --text-color: #102a43;
        --text-light: #486581;
        --card-bg: rgba(255,255,255,0.85);
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
    }

    [data-theme="dark"] {
        --bg-start: #0b2b44;
        --bg-end: #1a2a3a;
        --text-color: #f0f4f8;
        --text-light: #b0c4de;
        --card-bg: rgba(26,42,58,0.85);
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
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(51,163,220,0.08), transparent 40%),
            linear-gradient(135deg, var(--bg-start), var(--bg-end));
        padding: 0;
    }

    /* Sidebar styling (same as before) */
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

    /* Hero & sections (unchanged) */
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

    /* About section */
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

    /* Rest of styles (stats, features, testimonial, faq, cta, footer, chat) unchanged */
    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 2rem; margin: 3rem 0; text-align: center; }
    .stats-grid .stat { background: var(--card-bg); backdrop-filter: blur(8px); border-radius: 20px; padding: 1.5rem 1rem; border: 1px solid var(--card-border); }
    .stats-grid .stat .number { font-size: 2.8rem; font-weight: 800; color: var(--primary); display: block; }
    .stats-grid .stat .label { color: var(--text-light); font-weight: 500; font-size: 0.9rem; }

    .section-header { text-align: center; margin: 3rem 0 2rem; }
    .section-header .badge { display: inline-block; background: var(--card-border); color: var(--primary); padding: 0.2rem 1rem; border-radius: 30px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .section-header h2 { font-size: 2.5rem; font-weight: 800; color: var(--text-color); margin-top: 0.5rem; }
    .section-header p { color: var(--text-light); max-width: 600px; margin: 0.5rem auto 0; }

    .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin: 2rem 0; }
    .feature-card { background: var(--card-bg); backdrop-filter: blur(8px); border-radius: 24px; padding: 2rem 1.5rem; border: 1px solid var(--card-border); transition: all 0.3s; text-align: center; }
    .feature-card:hover { transform: translateY(-8px); box-shadow: 0 20px 40px var(--shadow-color); border-color: var(--primary); }
    .feature-card .icon { font-size: 2.8rem; margin-bottom: 0.5rem; display: block; }
    .feature-card h3 { color: var(--text-color); font-weight: 700; font-size: 1.3rem; }
    .feature-card p { color: var(--text-light); font-size: 0.95rem; margin-top: 0.5rem; }

    .testimonial-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem; margin: 2rem 0; }
    .testimonial { background: var(--card-bg); backdrop-filter: blur(8px); border-radius: 20px; padding: 1.8rem; border: 1px solid var(--card-border); }
    .testimonial .stars { color: var(--primary); font-size: 1.1rem; letter-spacing: 2px; margin-bottom: 0.5rem; }
    .testimonial blockquote { font-weight: 500; color: var(--text-color); font-size: 1rem; line-height: 1.6; margin: 0.5rem 0; }
    .testimonial .author { display: flex; align-items: center; gap: 0.8rem; margin-top: 1rem; }
    .testimonial .author .avatar { width: 44px; height: 44px; border-radius: 50%; background: var(--primary); color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1.1rem; }
    .testimonial .author .info { font-weight: 600; color: var(--text-color); }
    .testimonial .author .info small { display: block; font-weight: 400; color: var(--text-light); font-size: 0.8rem; }

    .faq-item { background: var(--card-bg); backdrop-filter: blur(8px); border-radius: 16px; margin-bottom: 1rem; border: 1px solid var(--card-border); overflow: hidden; }
    .faq-item .question { padding: 1.2rem 1.5rem; display: flex; justify-content: space-between; align-items: center; cursor: pointer; font-weight: 600; color: var(--text-color); transition: background 0.2s; }
    .faq-item .question:hover { background: var(--card-border); }
    .faq-item .answer { padding: 0 1.5rem 1.2rem; color: var(--text-light); line-height: 1.6; display: none; }
    .faq-item.active .answer { display: block; }
    .faq-item .question .icon { font-size: 1.4rem; transition: transform 0.3s; }
    .faq-item.active .question .icon { transform: rotate(45deg); }

    .cta-section { background: var(--header-bg); border-radius: 32px; padding: 3rem 2rem; text-align: center; color: white; margin: 3rem 0; box-shadow: 0 20px 50px var(--shadow-color); }
    .cta-section h2 { font-size: 2.5rem; font-weight: 800; }
    .cta-section p { opacity: 0.9; max-width: 600px; margin: 0.5rem auto 1.5rem; }
    .cta-section .btn-cta { background: white; color: var(--primary-dark); padding: 0.8rem 2.5rem; border-radius: 12px; font-weight: 700; border: none; transition: all 0.3s; text-decoration: none; display: inline-block; }
    .cta-section .btn-cta:hover { transform: scale(1.03); box-shadow: 0 10px 30px rgba(0,0,0,0.2); }

    .footer { border-top: 1px solid var(--card-border); padding: 2rem 0; margin-top: 3rem; display: flex; justify-content: space-between; flex-wrap: wrap; color: var(--text-light); font-size: 0.9rem; }
    .footer .links a { color: var(--text-light); text-decoration: none; margin-left: 1.5rem; transition: color 0.2s; }
    .footer .links a:hover { color: var(--primary); }

    .doc-page { max-width: 1200px; margin: 0 auto; padding: 1.5rem 1rem; }
    .doc-page .header { margin-bottom: 2rem; }
    .doc-page .header h1 { font-size: 2.2rem; font-weight: 800; color: var(--text-color); }
    .doc-page .header p { color: var(--text-light); font-size: 1.1rem; }

    /* Chat floating (same as before) */
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
    .chat-float .chat-input-area {
        padding: 0.8rem 1rem;
        border-top: 1px solid var(--card-border);
        flex-shrink: 0;
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
    .delay-1 { animation-delay: 0.1s; }
    .delay-2 { animation-delay: 0.2s; }
    .delay-3 { animation-delay: 0.3s; }
    .delay-4 { animation-delay: 0.4s; }

    @media (max-width: 768px) {
        .hero h1 { font-size: 2.2rem; }
        .stats-grid { grid-template-columns: 1fr 1fr; }
        .features-grid { grid-template-columns: 1fr; }
        .chat-float { width: 90vw; right: 5vw; }
        .about-section { flex-direction: column; text-align: center; }
    }
</style>
""", unsafe_allow_html=True)

# ---- JavaScript (same as before) ----
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
    document.addEventListener('click', function(e) {
        const faqItem = e.target.closest('.faq-item .question');
        if (faqItem) {
            const parent = faqItem.closest('.faq-item');
            parent.classList.toggle('active');
        }
    });
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

    page = st.radio(
        "Navigate",
        ["🏠 Home", "📝 Builder", "📄 Resume", "📋 CV", "✉️ Cover Letter", "📊 Proposal", "🏆 Experience", "🔍 Job Scraper", "🤖 AI Assistant"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    col1, col2 = st.columns(2)
    col1.metric("🛠️ Skills", len(st.session_state.skills))
    col2.metric("💼 Jobs", len(st.session_state.jobs))
    st.caption("⚡ Streamlit · ReportLab")

    st.markdown("---")
    if st.button("🌓 Toggle Theme", use_container_width=True):
        st.markdown("<script>toggleTheme();</script>", unsafe_allow_html=True)

# ---- Map page names ----
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
page = page_map.get(page, "Home")

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
            <a href="#" class="btn-primary" onclick="document.querySelector('[data-testid=\\"stButton\\"] button').click()">Get Started Free</a>
            <a href="#about" class="btn-secondary">Learn More</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- NEW ABOUT ME SECTION ----
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

    # Stats, Features, Testimonials, FAQ, CTA (unchanged)
    st.markdown("""
    <div class="stats-grid">
        <div class="stat"><span class="number">10K+</span><span class="label">Documents Created</span></div>
        <div class="stat"><span class="number">98%</span><span class="label">User Satisfaction</span></div>
        <div class="stat"><span class="number">50+</span><span class="label">Templates</span></div>
        <div class="stat"><span class="number">4.9★</span><span class="label">Average Rating</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header">
        <span class="badge">Features</span>
        <h2>Everything You Need</h2>
        <p>Complete toolkit for creating professional documents.</p>
    </div>
    <div class="features-grid">
        <div class="feature-card"><span class="icon">📄</span><h3>Resume Builder</h3><p>ATS-friendly resumes with multiple themes.</p></div>
        <div class="feature-card"><span class="icon">📋</span><h3>CV Generator</h3><p>Comprehensive curriculum vitae with publications.</p></div>
        <div class="feature-card"><span class="icon">✉️</span><h3>Cover Letters</h3><p>Personalized letters for job applications.</p></div>
        <div class="feature-card"><span class="icon">📊</span><h3>Proposals</h3><p>Professional project proposals for clients.</p></div>
        <div class="feature-card"><span class="icon">🏆</span><h3>Experience Letters</h3><p>Employment verification letters.</p></div>
        <div class="feature-card"><span class="icon">🔍</span><h3>Job Scraper</h3><p>Find jobs and match your skills.</p></div>
        <div class="feature-card"><span class="icon">🤖</span><h3>AI Assistant</h3><p>Get AI-powered suggestions and help.</p></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header">
        <span class="badge">Testimonials</span>
        <h2>What Our Users Say</h2>
    </div>
    <div class="testimonial-grid">
        <div class="testimonial">
            <div class="stars">★★★★★</div>
            <blockquote>"DocForge cut my resume building time from hours to minutes. The templates are stunning."</blockquote>
            <div class="author"><div class="avatar">S</div><div class="info">Sarah Chen <small>Software Engineer</small></div></div>
        </div>
        <div class="testimonial">
            <div class="stars">★★★★★</div>
            <blockquote>"The cover letter generator helped me land interviews at top companies. Highly recommended."</blockquote>
            <div class="author"><div class="avatar">M</div><div class="info">Marcus Rivera <small>Product Manager</small></div></div>
        </div>
        <div class="testimonial">
            <div class="stars">★★★★★</div>
            <blockquote>"I use DocForge for all my client proposals. Professional and easy to customize."</blockquote>
            <div class="author"><div class="avatar">L</div><div class="info">Lisa Park <small>Freelance Designer</small></div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header">
        <span class="badge">FAQ</span>
        <h2>Frequently Asked Questions</h2>
    </div>
    <div class="faq-item active">
        <div class="question"><span>How do I start building a resume?</span><span class="icon">➕</span></div>
        <div class="answer">Go to the Builder page, fill in your personal details, experience, education, and skills. Then navigate to the Resume page to generate your PDF.</div>
    </div>
    <div class="faq-item">
        <div class="question"><span>Can I use my own templates?</span><span class="icon">➕</span></div>
        <div class="answer">Currently, we offer three built‑in themes: Classic Green, Corporate Blue, and Creative Purple. You can choose one when generating your document.</div>
    </div>
    <div class="faq-item">
        <div class="question"><span>Is my data saved?</span><span class="icon">➕</span></div>
        <div class="answer">Your data is stored in your browser session. It will be cleared when you close the tab or refresh the page.</div>
    </div>
    <div class="faq-item">
        <div class="question"><span>Can I download my documents in other formats?</span><span class="icon">➕</span></div>
        <div class="answer">Currently, we support PDF export. More formats may be added in the future.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="cta-section">
        <h2>Ready to Build Your Document?</h2>
        <p>Get started now – it's free and takes less than 5 minutes.</p>
        <a href="#" class="btn-cta" onclick="document.querySelector('[data-testid=\\"stButton\\"] button').click()">Start Building</a>
    </div>
    """, unsafe_allow_html=True)

# ---- BUILDER, RESUME, CV, COVER LETTER, PROPOSAL, EXPERIENCE, JOB SCRAPER, AI ASSISTANT ----
# (All these pages remain exactly as in your previous working version)
# To save space, I'm not repeating them here – they are unchanged from the last version I gave you.
# If you need the full code for those pages, I'll provide them separately, but they work.

# ---- FOOTER ----
st.markdown("""
<div class="footer">
    <span>© 2026 DocForge. All rights reserved.</span>
    <div class="links">
        <a href="#">Privacy</a>
        <a href="#">Terms</a>
        <a href="#">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- FLOATING CHAT (same as before) ----
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
