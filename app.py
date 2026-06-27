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

# ---- Page Config ----
st.set_page_config(
    page_title="DocForge – Professional Document Builder",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Custom CSS (AgentForge-inspired design) ----
st.markdown("""
<style>
    /* ===== Font & Reset ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    * {
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }

    /* ===== Custom Cursor ===== */
    body, .stApp {
        cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><circle cx="16" cy="16" r="12" fill="%2333a3dc" stroke="%231a2a3a" stroke-width="2"/><circle cx="16" cy="16" r="5" fill="%231a2a3a"/></svg>') 16 16, auto;
    }
    a, button, .stButton button, .stDownloadButton button, .stRadio label, .doc-card {
        cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><circle cx="16" cy="16" r="12" fill="%2333a3dc" stroke="%231a2a3a" stroke-width="2"/><circle cx="16" cy="16" r="5" fill="%231a2a3a"/><path d="M20 20 L28 28" stroke="%231a2a3a" stroke-width="2"/></svg>') 16 16, pointer;
    }
    input, textarea {
        cursor: text !important;
    }

    /* ===== Theme Variables ===== */
    :root {
        --bg-start: #f0f4f8;
        --bg-end: #d9e2ec;
        --text-color: #102a43;
        --text-light: #486581;
        --card-bg: rgba(255,255,255,0.85);
        --card-border: rgba(51,163,220,0.25);
        --sidebar-bg: #d9e2ec;
        --sidebar-border: #b0c4de;
        --input-bg: #ffffff;
        --input-border: #b0c4de;
        --tab-bg: #e1e8f0;
        --tab-selected: #1e6f9f;
        --header-bg: linear-gradient(135deg, #0b2b44, #1e6f9f);
        --header-text: #ffffff;
        --header-subtext: #d9e2ec;
        --btn-bg: linear-gradient(135deg, #1e6f9f, #33a3dc);
        --btn-text: #ffffff;
        --alert-bg: #e1e8f0;
        --shadow-color: rgba(11,43,68,0.2);
        --placeholder-color: #7a8fa6;
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
        --sidebar-bg: #1a2a3a;
        --sidebar-border: #2a4a6a;
        --input-bg: #1a2a3a;
        --input-border: #2a4a6a;
        --tab-bg: #1a2a3a;
        --tab-selected: #33a3dc;
        --header-bg: linear-gradient(135deg, #0b2b44, #1e6f9f);
        --header-text: #ffffff;
        --header-subtext: #b0c4de;
        --btn-bg: linear-gradient(135deg, #1e6f9f, #33a3dc);
        --btn-text: #ffffff;
        --alert-bg: #1a2a3a;
        --shadow-color: rgba(0,0,0,0.4);
        --placeholder-color: #8aa0b8;
        --primary: #33a3dc;
        --primary-light: #66c2e8;
        --primary-dark: #1a4a6a;
        --section-bg: #1a2a3a;
    }

    /* ===== Global Layout ===== */
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(51,163,220,0.08), transparent 40%),
            linear-gradient(135deg, var(--bg-start), var(--bg-end));
        padding: 0;
    }

    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* ===== Header / Navigation (Sticky) ===== */
    .custom-nav {
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid var(--card-border);
        padding: 0.5rem 2rem;
        border-radius: 0;
        margin-bottom: 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        position: sticky;
        top: 0;
        z-index: 100;
        transition: background 0.3s;
    }
    .custom-nav .logo {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 800;
        font-size: 1.5rem;
        color: var(--text-color);
        text-decoration: none;
    }
    .custom-nav .logo img {
        height: 2rem;
    }
    .custom-nav .nav-links {
        display: flex;
        gap: 1.5rem;
        align-items: center;
        flex-wrap: wrap;
    }
    .custom-nav .nav-links a {
        color: var(--text-light);
        text-decoration: none;
        font-weight: 500;
        font-size: 0.95rem;
        transition: color 0.2s;
    }
    .custom-nav .nav-links a:hover {
        color: var(--primary);
    }
    .custom-nav .nav-links .active {
        color: var(--primary);
        font-weight: 600;
    }
    .custom-nav .theme-toggle {
        background: none;
        border: none;
        color: var(--text-color);
        font-size: 1.2rem;
        cursor: pointer;
        padding: 0.2rem 0.5rem;
        border-radius: 8px;
        transition: background 0.2s;
    }
    .custom-nav .theme-toggle:hover {
        background: var(--card-border);
    }

    /* ===== Hero Section ===== */
    .hero {
        text-align: center;
        padding: 4rem 2rem 3rem;
        animation: fadeInUp 0.8s ease;
    }
    .hero h1 {
        font-size: 3.2rem;
        font-weight: 900;
        line-height: 1.1;
        color: var(--text-color);
        margin-bottom: 1rem;
    }
    .hero h1 span {
        background: linear-gradient(135deg, var(--primary), var(--primary-light));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero p {
        font-size: 1.2rem;
        color: var(--text-light);
        max-width: 700px;
        margin: 0 auto 2rem;
    }
    .hero .buttons {
        display: flex;
        gap: 1rem;
        justify-content: center;
        flex-wrap: wrap;
    }
    .hero .buttons .btn-primary {
        background: var(--btn-bg);
        color: var(--btn-text);
        padding: 0.8rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        border: none;
        box-shadow: 0 10px 25px var(--shadow-color);
        transition: all 0.3s;
        text-decoration: none;
        display: inline-block;
    }
    .hero .buttons .btn-primary:hover {
        transform: translateY(-3px);
        box-shadow: 0 18px 35px var(--shadow-color);
    }
    .hero .buttons .btn-secondary {
        background: transparent;
        color: var(--text-color);
        padding: 0.8rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        border: 1px solid var(--card-border);
        transition: all 0.3s;
        text-decoration: none;
        display: inline-block;
    }
    .hero .buttons .btn-secondary:hover {
        background: var(--card-bg);
        border-color: var(--primary);
    }

    /* ===== Stats ===== */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
        text-align: center;
    }
    .stats-grid .stat {
        background: var(--card-bg);
        backdrop-filter: blur(8px);
        border-radius: 20px;
        padding: 1.5rem 1rem;
        border: 1px solid var(--card-border);
    }
    .stats-grid .stat .number {
        font-size: 2.8rem;
        font-weight: 800;
        color: var(--primary);
        display: block;
    }
    .stats-grid .stat .label {
        color: var(--text-light);
        font-weight: 500;
        font-size: 0.9rem;
    }

    /* ===== Section Headers ===== */
    .section-header {
        text-align: center;
        margin: 3rem 0 2rem;
    }
    .section-header .badge {
        display: inline-block;
        background: var(--card-border);
        color: var(--primary);
        padding: 0.2rem 1rem;
        border-radius: 30px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .section-header h2 {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--text-color);
        margin-top: 0.5rem;
    }
    .section-header p {
        color: var(--text-light);
        max-width: 600px;
        margin: 0.5rem auto 0;
    }

    /* ===== Feature Cards ===== */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    .feature-card {
        background: var(--card-bg);
        backdrop-filter: blur(8px);
        border-radius: 24px;
        padding: 2rem 1.5rem;
        border: 1px solid var(--card-border);
        transition: all 0.3s;
        text-align: center;
    }
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px var(--shadow-color);
        border-color: var(--primary);
    }
    .feature-card .icon {
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    .feature-card h3 {
        color: var(--text-color);
        font-weight: 700;
        font-size: 1.3rem;
    }
    .feature-card p {
        color: var(--text-light);
        font-size: 0.95rem;
        margin-top: 0.5rem;
    }

    /* ===== Testimonials ===== */
    .testimonial-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    .testimonial {
        background: var(--card-bg);
        backdrop-filter: blur(8px);
        border-radius: 20px;
        padding: 1.8rem;
        border: 1px solid var(--card-border);
    }
    .testimonial .stars {
        color: var(--primary);
        font-size: 1.1rem;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
    }
    .testimonial blockquote {
        font-weight: 500;
        color: var(--text-color);
        font-size: 1rem;
        line-height: 1.6;
        margin: 0.5rem 0;
    }
    .testimonial .author {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin-top: 1rem;
    }
    .testimonial .author .avatar {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: var(--primary);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.1rem;
    }
    .testimonial .author .info {
        font-weight: 600;
        color: var(--text-color);
    }
    .testimonial .author .info small {
        display: block;
        font-weight: 400;
        color: var(--text-light);
        font-size: 0.8rem;
    }

    /* ===== FAQ Accordion ===== */
    .faq-item {
        background: var(--card-bg);
        backdrop-filter: blur(8px);
        border-radius: 16px;
        margin-bottom: 1rem;
        border: 1px solid var(--card-border);
        overflow: hidden;
    }
    .faq-item .question {
        padding: 1.2rem 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        cursor: pointer;
        font-weight: 600;
        color: var(--text-color);
        transition: background 0.2s;
    }
    .faq-item .question:hover {
        background: var(--card-border);
    }
    .faq-item .answer {
        padding: 0 1.5rem 1.2rem;
        color: var(--text-light);
        line-height: 1.6;
        display: none;
    }
    .faq-item.active .answer {
        display: block;
    }
    .faq-item .question .icon {
        font-size: 1.4rem;
        transition: transform 0.3s;
    }
    .faq-item.active .question .icon {
        transform: rotate(45deg);
    }

    /* ===== CTA Section ===== */
    .cta-section {
        background: var(--header-bg);
        border-radius: 32px;
        padding: 3rem 2rem;
        text-align: center;
        color: white;
        margin: 3rem 0;
        box-shadow: 0 20px 50px var(--shadow-color);
    }
    .cta-section h2 {
        font-size: 2.5rem;
        font-weight: 800;
    }
    .cta-section p {
        opacity: 0.9;
        max-width: 600px;
        margin: 0.5rem auto 1.5rem;
    }
    .cta-section .btn-cta {
        background: white;
        color: var(--primary-dark);
        padding: 0.8rem 2.5rem;
        border-radius: 12px;
        font-weight: 700;
        border: none;
        transition: all 0.3s;
        text-decoration: none;
        display: inline-block;
    }
    .cta-section .btn-cta:hover {
        transform: scale(1.03);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }

    /* ===== Footer ===== */
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
    .footer .links a:hover {
        color: var(--primary);
    }

    /* ===== Document Pages (resume, cv, etc.) ===== */
    .doc-page {
        max-width: 1200px;
        margin: 0 auto;
        padding: 1.5rem 1rem;
    }
    .doc-page .header {
        margin-bottom: 2rem;
    }
    .doc-page .header h1 {
        font-size: 2.2rem;
        font-weight: 800;
        color: var(--text-color);
    }
    .doc-page .header p {
        color: var(--text-light);
        font-size: 1.1rem;
    }
    .doc-page .preview-box {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid var(--card-border);
        min-height: 200px;
        margin-top: 1rem;
    }

    /* ===== Animations ===== */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeInUp 0.6s ease forwards;
    }
    .delay-1 { animation-delay: 0.1s; }
    .delay-2 { animation-delay: 0.2s; }
    .delay-3 { animation-delay: 0.3s; }
    .delay-4 { animation-delay: 0.4s; }

    /* ===== Responsive tweaks ===== */
    @media (max-width: 768px) {
        .hero h1 { font-size: 2.2rem; }
        .custom-nav { padding: 0.5rem 1rem; }
        .custom-nav .nav-links { gap: 0.8rem; }
        .stats-grid { grid-template-columns: 1fr 1fr; }
        .features-grid { grid-template-columns: 1fr; }
    }
</style>
""", unsafe_allow_html=True)

# ---- JavaScript for Dark/Light Toggle & FAQ Accordion ----
st.markdown("""
<script>
    // Dark mode toggle
    function toggleTheme() {
        const html = document.documentElement;
        const current = html.getAttribute('data-theme');
        const newTheme = current === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    }

    // Apply saved theme
    (function() {
        const saved = localStorage.getItem('theme');
        if (saved) {
            document.documentElement.setAttribute('data-theme', saved);
        } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.setAttribute('data-theme', 'dark');
        }
    })();

    // FAQ toggle
    document.addEventListener('click', function(e) {
        const faqItem = e.target.closest('.faq-item .question');
        if (faqItem) {
            const parent = faqItem.closest('.faq-item');
            parent.classList.toggle('active');
        }
    });
</script>
""", unsafe_allow_html=True)

# ---- Session State ----
if "skills" not in st.session_state:
    st.session_state.skills = []
if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---- Navigation ----
pages = {
    "🏠 Home": "Home",
    "📝 Builder": "Builder",
    "📄 Resume": "Resume",
    "📋 CV": "CV",
    "✉️ Cover Letter": "CoverLetter",
    "📊 Proposal": "Proposal",
    "🏆 Experience": "Experience",
    "🔍 Job Scraper": "JobScraper"
}

# ---- Header / Nav (replaces sidebar) ----
with st.container():
    # We'll use columns to create a custom nav bar
    col_logo, col_nav, col_theme = st.columns([1, 4, 1])
    with col_logo:
        st.markdown("""
        <div class="custom-nav" style="background:transparent; border:none; padding:0;">
            <span class="logo" style="font-size:1.8rem;">📄 DocForge</span>
        </div>
        """, unsafe_allow_html=True)
    with col_nav:
        # We'll use st.radio hidden inside to keep state, but display custom buttons
        # Actually we'll use st.tabs or st.selectbox, but we want a horizontal nav.
        # We can use st.radio with horizontal orientation and custom CSS to make it look like a nav.
        # We'll use a selectbox for mobile friendliness, but we can also use columns.
        # Let's use st.selectbox for simplicity and to avoid extra complexity.
        # But the user wants a nav like the example. We'll use st.radio with horizontal.
        # We'll define a function to render nav.
        pass

# ---- Sidebar alternative: use a selectbox in the main area ----
# We'll actually use a custom navigation with st.radio in a container with horizontal layout.
# But to keep the code simple and working, we'll use a st.selectbox for page selection.
# However, the user wants a visual nav like AgentForge – we can do that with CSS-styled buttons.
# Let's use st.columns to create clickable buttons that set session state.

# We'll render the nav as a set of buttons in columns.
# For simplicity, we'll use st.radio with horizontal option.

# ---- Page Selection ----
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "📝 Builder", "📄 Resume", "📋 CV", "✉️ Cover Letter", "📊 Proposal", "🏆 Experience", "🔍 Job Scraper"],
    index=0,
    label_visibility="collapsed"
)
# But we'll hide the sidebar and use a top nav. Since we can't easily hide sidebar without CSS, we'll keep sidebar minimal.
# Actually we can style sidebar to look like a top nav, but it's easier to use a custom top nav using columns.
# Let's implement a top nav using st.columns and st.button.

# We'll create a function to render the top nav, and use st.session_state.page to track.

# ---- Helper to get user data ----
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

# ---- Render top navigation ----
nav_items = ["🏠 Home", "📝 Builder", "📄 Resume", "📋 CV", "✉️ Cover Letter", "📊 Proposal", "🏆 Experience", "🔍 Job Scraper"]
cols = st.columns(len(nav_items))
for i, item in enumerate(nav_items):
    with cols[i]:
        # Use a button to change page
        if st.button(item, key=f"nav_{item}", use_container_width=True):
            st.session_state.page = item.split(" ")[-1]  # extract page name without emoji
            st.rerun()

# ---- Display content based on page ----
page = st.session_state.get("page", "Home")

# ==================== PAGES ====================

# ---- HOME ----
if page == "Home":
    # Hero Section
    st.markdown("""
    <div class="hero">
        <h1>Create <span>Professional Documents</span><br>Instantly</h1>
        <p>Build resumes, CVs, cover letters, proposals, and experience letters – all from one platform. No design skills needed.</p>
        <div class="buttons">
            <a href="#" class="btn-primary" onclick="document.querySelector('[data-testid=\\"stButton\\"] button').click()">Get Started Free</a>
            <a href="#" class="btn-secondary">Learn More</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    st.markdown("""
    <div class="stats-grid">
        <div class="stat"><span class="number">10K+</span><span class="label">Documents Created</span></div>
        <div class="stat"><span class="number">98%</span><span class="label">User Satisfaction</span></div>
        <div class="stat"><span class="number">50+</span><span class="label">Templates</span></div>
        <div class="stat"><span class="number">4.9★</span><span class="label">Average Rating</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Features
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
    </div>
    """, unsafe_allow_html=True)

    # Testimonials
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

    # FAQ
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

    # CTA
    st.markdown("""
    <div class="cta-section">
        <h2>Ready to Build Your Document?</h2>
        <p>Get started now – it's free and takes less than 5 minutes.</p>
        <a href="#" class="btn-cta" onclick="document.querySelector('[data-testid=\\"stButton\\"] button').click()">Start Building</a>
    </div>
    """, unsafe_allow_html=True)

# ---- BUILDER ----
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
        st.text_area("Professional Summary", key="f_summary", placeholder="Experienced software engineer with 5+ years...", height=100)

    if st.button("💾 Save Information", type="primary", use_container_width=True):
        st.success("✅ All information saved!")

# ---- RESUME ----
elif page == "Resume":
    st.markdown("""
    <div class="doc-page">
        <div class="header">
            <h1>📄 Resume Generator</h1>
            <p>Create an ATS-optimized professional resume.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        theme = st.selectbox("🎨 Theme", ["Classic Green", "Corporate Blue", "Creative Purple"], key="resume_theme")
        summary = st.text_area("Professional Summary", key="resume_summary", placeholder="Write a brief summary...", height=100)
    with col2:
        st.markdown("**Preview Sections**")
        st.markdown("✅ Personal Info\n✅ Summary\n✅ Skills\n✅ Experience\n✅ Education\n✅ Projects")

    if st.button("📥 Generate Resume PDF", type="primary", use_container_width=True):
        data = get_user_data()
        data["summary"] = st.session_state.get("resume_summary", "")
        data["theme"] = st.session_state.get("resume_theme", "Classic Green")
        pdf = generate_resume_pdf(data)
        if pdf:
            st.download_button(
                label="⬇️ Download PDF",
                data=pdf,
                file_name=f"{data['name'].replace(' ', '_')}_Resume.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.error("Failed to generate PDF. Check logs.")

# ---- CV ----
elif page == "CV":
    st.markdown("""
    <div class="doc-page">
        <div class="header">
            <h1>📋 CV Generator</h1>
            <p>Create a comprehensive curriculum vitae.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        cv_theme = st.selectbox("🎨 Theme", ["Classic Green", "Corporate Blue", "Creative Purple"], key="cv_theme")
        publications = st.text_area("Publications (one per line)", key="cv_publications", placeholder="• Smith, J. (2023). 'AI in Healthcare.' Journal of AI, 12(3), 45-67.", height=80)
    with col2:
        st.markdown("**CV Sections**")
        st.markdown("✅ Personal Info\n✅ Summary\n✅ Skills\n✅ Experience\n✅ Education\n✅ Publications\n✅ Projects")

    if st.button("📥 Generate CV PDF", type="primary", use_container_width=True):
        data = get_user_data()
        data["publications"] = st.session_state.get("cv_publications", "")
        data["theme"] = st.session_state.get("cv_theme", "Classic Green")
        pdf = generate_cv_pdf(data)
        if pdf:
            st.download_button(
                label="⬇️ Download PDF",
                data=pdf,
                file_name=f"{data['name'].replace(' ', '_')}_CV.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.error("Failed to generate PDF.")

# ---- COVER LETTER ----
elif page == "CoverLetter":
    st.markdown("""
    <div class="doc-page">
        <div class="header">
            <h1>✉️ Cover Letter Generator</h1>
            <p>Personalized cover letters for job applications.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        col_a, col_b = st.columns(2)
        with col_a:
            cover_company = st.text_input("Company Name *", key="cover_company", placeholder="Google")
            cover_position = st.text_input("Position *", key="cover_position", placeholder="Software Engineer")
        with col_b:
            cover_recruiter = st.text_input("Recruiter Name", key="cover_recruiter", placeholder="Sarah Johnson")
        cover_custom = st.text_area("Additional Message (optional)", key="cover_custom", placeholder="Why you're interested, specific achievements...", height=100)
        cover_theme = st.selectbox("🎨 Theme", ["Classic Green", "Corporate Blue", "Creative Purple"], key="cover_theme")
    with col2:
        st.markdown("**Letter Structure**")
        st.markdown("✅ Sender Info\n✅ Date\n✅ Recipient\n✅ Salutation\n✅ Body\n✅ Closing\n✅ Signature")

    if st.button("📥 Generate Cover Letter PDF", type="primary", use_container_width=True):
        data = get_user_data()
        data["cover_company"] = st.session_state.get("cover_company", "")
        data["cover_position"] = st.session_state.get("cover_position", "")
        data["cover_recruiter"] = st.session_state.get("cover_recruiter", "")
        data["cover_custom"] = st.session_state.get("cover_custom", "")
        data["theme"] = st.session_state.get("cover_theme", "Classic Green")
        pdf = generate_cover_letter_pdf(data)
        if pdf:
            st.download_button(
                label="⬇️ Download PDF",
                data=pdf,
                file_name=f"{data['name'].replace(' ', '_')}_Cover_Letter.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.error("Failed to generate PDF.")

# ---- PROPOSAL ----
elif page == "Proposal":
    st.markdown("""
    <div class="doc-page">
        <div class="header">
            <h1>📊 Proposal Generator</h1>
            <p>Professional project proposals for clients.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        col_a, col_b = st.columns(2)
        with col_a:
            proposal_title = st.text_input("Proposal Title *", key="prop_title", placeholder="AI-Powered Customer Support")
            proposal_client = st.text_input("Client/Organization *", key="prop_client", placeholder="ABC Corp")
        with col_b:
            proposal_budget = st.text_input("Budget", key="prop_budget", placeholder="$50,000 – $75,000")
            proposal_timeline = st.text_input("Timeline", key="prop_timeline", placeholder="3 months")
        proposal_summary = st.text_area("Executive Summary *", key="prop_summary", placeholder="This proposal outlines...", height=100)
        proposal_approach = st.text_area("Approach/Methodology *", key="prop_approach", placeholder="1. Requirement Analysis\n2. Design\n3. Development\n4. Testing", height=80)
        proposal_theme = st.selectbox("🎨 Theme", ["Classic Green", "Corporate Blue", "Creative Purple"], key="prop_theme")
    with col2:
        st.markdown("**Proposal Sections**")
        st.markdown("✅ Title\n✅ Client Info\n✅ Executive Summary\n✅ Approach\n✅ About Us\n✅ Contact")

    if st.button("📥 Generate Proposal PDF", type="primary", use_container_width=True):
        data = get_user_data()
        data["proposal_title"] = st.session_state.get("prop_title", "")
        data["proposal_client"] = st.session_state.get("prop_client", "")
        data["proposal_budget"] = st.session_state.get("prop_budget", "")
        data["proposal_timeline"] = st.session_state.get("prop_timeline", "")
        data["proposal_summary"] = st.session_state.get("prop_summary", "")
        data["proposal_approach"] = st.session_state.get("prop_approach", "")
        data["theme"] = st.session_state.get("prop_theme", "Classic Green")
        pdf = generate_proposal_pdf(data)
        if pdf:
            st.download_button(
                label="⬇️ Download PDF",
                data=pdf,
                file_name=f"{data['name'].replace(' ', '_')}_Proposal.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.error("Failed to generate PDF.")

# ---- EXPERIENCE LETTER ----
elif page == "Experience":
    st.markdown("""
    <div class="doc-page">
        <div class="header">
            <h1>🏆 Experience Letter Generator</h1>
            <p>Employment verification letters.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        col_a, col_b = st.columns(2)
        with col_a:
            exp_company = st.text_input("Company Name *", key="exp_company", placeholder="TechCorp Inc.")
            exp_employee = st.text_input("Employee Name *", key="exp_employee", placeholder="John Doe")
            exp_position = st.text_input("Position Held *", key="exp_position", placeholder="Senior Developer")
        with col_b:
            exp_period = st.text_input("Employment Period *", key="exp_period", placeholder="Jan 2020 – Dec 2023")
            exp_issuer = st.text_input("Issuer Name *", key="exp_issuer", placeholder="Jane Smith")
            exp_issuer_title = st.text_input("Issuer Title *", key="exp_issuer_title", placeholder="HR Manager")
        exp_remarks = st.text_area("Performance Remarks *", key="exp_remarks", placeholder="John was an exceptional employee...", height=80)
        exp_theme = st.selectbox("🎨 Theme", ["Classic Green", "Corporate Blue", "Creative Purple"], key="exp_theme")
    with col2:
        st.markdown("**Letter Sections**")
        st.markdown("✅ Company Header\n✅ Date\n✅ Subject\n✅ Employee Details\n✅ Performance Remarks\n✅ Issuer Info")

    if st.button("📥 Generate Experience Letter PDF", type="primary", use_container_width=True):
        data = {
            "exp_company": st.session_state.get("exp_company", ""),
            "exp_employee": st.session_state.get("exp_employee", ""),
            "exp_position": st.session_state.get("exp_position", ""),
            "exp_period": st.session_state.get("exp_period", ""),
            "exp_remarks": st.session_state.get("exp_remarks", ""),
            "exp_issuer": st.session_state.get("exp_issuer", ""),
            "exp_issuer_title": st.session_state.get("exp_issuer_title", ""),
            "theme": st.session_state.get("exp_theme", "Classic Green"),
        }
        pdf = generate_experience_letter_pdf(data)
        if pdf:
            st.download_button(
                label="⬇️ Download PDF",
                data=pdf,
                file_name=f"{data['exp_employee'].replace(' ', '_')}_Experience_Letter.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.error("Failed to generate PDF.")

# ---- JOB SCRAPER ----
elif page == "JobScraper":
    st.markdown("""
    <div class="doc-page">
        <div class="header">
            <h1>🔍 Job Scraper</h1>
            <p>Find jobs and match your skills.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        role = st.text_input("Job Role", value="Python Developer")
        source = st.selectbox("Source", ["RemoteOK (live)", "Simulated"])
        if st.button("🔍 Scrape Jobs", type="primary", use_container_width=True):
            with st.spinner("Fetching jobs..."):
                jobs = get_jobs(role, source, st.session_state.skills)
                st.session_state.jobs = jobs
            st.success(f"Found {len(jobs)} jobs!")
    with col2:
        st.metric("Total Jobs", len(st.session_state.jobs))
        if st.session_state.jobs:
            avg = sum(j["match"] for j in st.session_state.jobs) / len(st.session_state.jobs)
            st.metric("Avg Match", f"{avg:.1f}%")

    st.markdown("---")
    if st.session_state.jobs:
        st.subheader("📋 Job Listings")
        for job in st.session_state.jobs[:10]:
            with st.container():
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"**{job['emoji']} {job['title']}**")
                    st.markdown(f"🏢 {job['company']} · 📍 {job['loc']} · {job['type']}")
                with col_b:
                    color = "#10b981" if job["match"] >= 70 else "#f59e0b" if job["match"] >= 40 else "#ef4444"
                    st.markdown(f"<h3 style='color:{color};'>{job['match']}%</h3>", unsafe_allow_html=True)
                st.markdown("---")
    else:
        st.info("No jobs found. Click 'Scrape Jobs' to search.")

# ---- Footer (shown on all pages) ----
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
