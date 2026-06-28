import streamlit as st
from datetime import datetime
import time
import requests
import base64
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

# ---- Custom CSS (same as before - kept for brevity) ----
# (I'm keeping the CSS from the previous version, it's identical)
# Please ensure you copy the full CSS from the previous response

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

    # ---- SUPPORT SECTION (with QR code) ----
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

    # ---- QR Code using Streamlit (reliable) ----
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        qr_image_url = "https://raw.githubusercontent.com/panwarrudraksh-alt/Document-Forge/main/static/api_qr.jpeg"
        try:
            st.image(qr_image_url, caption="Scan to support", use_container_width=True)
        except Exception:
            st.error("QR Code could not be loaded. Please try again later.")

    st.markdown("""
    <div style="text-align: center; padding-bottom: 2rem;">
        <p style="color: var(--text-light); font-size: 0.95rem;">
            Scan the QR code with your UPI app to send a payment. Every contribution counts – thank you! 🙏
        </p>
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

# ---- AI ASSISTANT ----
elif page == "AIAssistant":
    st.markdown("""
    <div class="doc-page">
        <div class="header">
            <h1>🤖 AI Document Assistant</h1>
            <p>Get AI‑powered suggestions to improve your documents and career content.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_ai = st.tabs(["✨ Improve Text", "📝 Generate Summary", "🛠️ Suggest Skills", "✉️ Cover Letter"])

    with tab_ai[0]:
        text_to_improve = st.text_area("Paste text to improve", height=150)
        if st.button("Improve Text"):
            if text_to_improve:
                improved = ai_suggest_improvements("text", text_to_improve)
                st.markdown("### Improved Version")
                st.write(improved)
            else:
                st.warning("Please enter some text.")

    with tab_ai[1]:
        if st.button("Generate Professional Summary"):
            skills = ", ".join(st.session_state.skills)
            experience = st.session_state.get("f_exp_desc", "")
            name = st.session_state.get("f_name", "Candidate")
            title = st.session_state.get("f_title", "Professional")
            summary = ai_generate_summary(name, title, skills, experience)
            st.markdown("### Generated Summary")
            st.write(summary)
            if st.button("Use This Summary"):
                st.session_state.f_summary = summary
                st.rerun()

    with tab_ai[2]:
        job_title = st.text_input("Job Title", placeholder="e.g., Data Scientist")
        if st.button("Suggest Skills"):
            if job_title:
                skills = ai_autofill_skills(job_title)
                st.markdown("### Suggested Skills")
                for sk in skills.split(','):
                    if sk.strip():
                        st.write(f"• {sk.strip()}")
                if st.button("Add All to My Skills"):
                    for sk in skills.split(','):
                        s = sk.strip().lower()
                        if s and s not in st.session_state.skills:
                            st.session_state.skills.append(s)
                    st.rerun()
            else:
                st.warning("Enter a job title.")

    with tab_ai[3]:
        col1, col2 = st.columns(2)
        with col1:
            company = st.text_input("Company Name", placeholder="Google")
            position = st.text_input("Position", placeholder="Software Engineer")
        with col2:
            recruiter = st.text_input("Recruiter Name (optional)", placeholder="Sarah Johnson")
        if st.button("Generate Cover Letter"):
            if company and position:
                skills = ", ".join(st.session_state.skills)
                experience = st.session_state.get("f_exp_desc", "")
                name = st.session_state.get("f_name", "Candidate")
                letter = ai_generate_cover_letter(name, position, company, skills, experience)
                st.markdown("### Generated Cover Letter")
                st.write(letter)
                if st.button("Use This Cover Letter"):
                    st.session_state.cover_letter_ai = letter
                    st.info("Cover letter saved. Go to Cover Letter page to use it.")
            else:
                st.warning("Please fill in company and position.")

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
