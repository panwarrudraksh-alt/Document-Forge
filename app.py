import streamlit as st
from datetime import datetime
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

# ---- Custom CSS ----
st.markdown("""
<style>
    /* Global styles */
    .main {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Header */
    .app-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.8rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    .app-header h1 {
        font-weight: 700;
        font-size: 2.5rem;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .app-header p {
        margin: 0.3rem 0 0;
        opacity: 0.85;
        font-size: 1.05rem;
    }
    /* Cards */
    .doc-card {
        background: white;
        border-radius: 14px;
        padding: 1.8rem 1.2rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: all 0.25s ease;
        border: 1px solid #e9ecef;
        height: 100%;
        cursor: pointer;
    }
    .doc-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 28px rgba(0,0,0,0.1);
        border-color: #2a5298;
    }
    .doc-card .icon {
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
    }
    .doc-card .title {
        font-weight: 600;
        font-size: 1.1rem;
        color: #1e3c72;
    }
    .doc-card .desc {
        font-size: 0.85rem;
        color: #6c757d;
        margin-top: 0.3rem;
    }
    /* Buttons */
    .stButton button {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 500;
        padding: 0.5rem 1.2rem;
        transition: all 0.2s;
        width: 100%;
    }
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 14px rgba(42, 82, 152, 0.4);
    }
    /* Sidebar */
    .css-1d391kg {
        background: #1e3c72;
    }
    .css-1d391kg .stRadio label {
        color: white;
    }
    .css-1d391kg .stMetric {
        background: rgba(255,255,255,0.08);
        border-radius: 8px;
        padding: 0.5rem;
    }
    /* Inputs */
    .stTextInput, .stTextArea, .stSelectbox {
        border-radius: 8px;
    }
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.4rem 1rem;
        font-weight: 500;
        background: #f1f3f5;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: #2a5298;
        color: white;
    }
    /* Preview box */
    .preview-box {
        background: white;
        border: 1px solid #dee2e6;
        border-radius: 12px;
        padding: 1.2rem;
        min-height: 180px;
        font-size: 0.9rem;
        line-height: 1.6;
        white-space: pre-wrap;
        overflow-y: auto;
        max-height: 400px;
    }
    .skill-tag {
        display: inline-block;
        background: #e7f3ff;
        color: #1e3c72;
        padding: 0.15rem 0.6rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
        margin: 0.15rem;
    }
</style>
""", unsafe_allow_html=True)

# ---- Session State ----
if "skills" not in st.session_state:
    st.session_state.skills = []
if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# ---- Sidebar Navigation ----
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1rem 0;">
        <div style="font-size:2.5rem;">📄</div>
        <div style="font-weight:700; font-size:1.4rem; color:white;">DocForge</div>
        <div style="color:#b0c4de; font-size:0.8rem;">Professional Documents</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["🏠 Home", "📝 Builder", "📄 Resume", "📋 CV", "✉️ Cover Letter", "📊 Proposal", "🏆 Experience", "🔍 Job Scraper"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    col1, col2 = st.columns(2)
    col1.metric("🛠️ Skills", len(st.session_state.skills))
    col2.metric("💼 Jobs", len(st.session_state.jobs))
    st.caption("⚡ Built with Streamlit · ReportLab")

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

# ==================== PAGES ====================

# ---- HOME ----
if page == "🏠 Home":
    st.markdown("""
    <div class="app-header">
        <h1>✨ Create Professional Documents Instantly</h1>
        <p>Build resumes, CVs, cover letters, proposals, and experience letters – all from one place.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    docs = [
        ("📄", "Resume", "ATS-friendly"),
        ("📋", "CV", "Comprehensive"),
        ("✉️", "Cover Letter", "Personalized"),
        ("📊", "Proposal", "Client-ready"),
        ("🏆", "Experience", "Employment verification"),
    ]
    # Show first four in row, fifth on next row
    for i, (icon, title, desc) in enumerate(docs[:4]):
        col = [col1, col2, col3, col4][i]
        with col:
            st.markdown(f"""
            <div class="doc-card">
                <div class="icon">{icon}</div>
                <div class="title">{title}</div>
                <div class="desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    # Fifth card
    with st.container():
        st.markdown(f"""
        <div style="max-width:300px; margin:0 auto;">
            <div class="doc-card">
                <div class="icon">🏆</div>
                <div class="title">Experience</div>
                <div class="desc">Employment verification</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:white; border-radius:14px; padding:1.5rem; margin-top:2rem; box-shadow:0 4px 12px rgba(0,0,0,0.05);">
        <h3 style="color:#1e3c72;">🚀 How It Works</h3>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(150px,1fr)); gap:1.5rem; margin-top:1rem;">
            <div style="text-align:center;">
                <div style="font-size:2rem;">1️⃣</div>
                <div><strong>Enter Details</strong></div>
                <div style="color:#6c757d; font-size:0.85rem;">Fill once</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:2rem;">2️⃣</div>
                <div><strong>Choose Document</strong></div>
                <div style="color:#6c757d; font-size:0.85rem;">Select type</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:2rem;">3️⃣</div>
                <div><strong>Customize</strong></div>
                <div style="color:#6c757d; font-size:0.85rem;">Add specifics</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:2rem;">4️⃣</div>
                <div><strong>Download PDF</strong></div>
                <div style="color:#6c757d; font-size:0.85rem;">Instant professional PDF</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---- BUILDER (unified input) ----
elif page == "📝 Builder":
    st.markdown("""
    <div class="app-header" style="padding:1.2rem 2rem;">
        <h1 style="font-size:1.8rem;">📝 Document Builder</h1>
        <p>Fill your information once. All documents will use this data.</p>
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
elif page == "📄 Resume":
    st.markdown("""
    <div class="app-header" style="padding:1.2rem 2rem; background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);">
        <h1 style="font-size:1.8rem;">📄 Resume Generator</h1>
        <p>Create an ATS-optimized professional resume.</p>
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
elif page == "📋 CV":
    st.markdown("""
    <div class="app-header" style="padding:1.2rem 2rem; background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);">
        <h1 style="font-size:1.8rem;">📋 CV Generator</h1>
        <p>Create a comprehensive curriculum vitae.</p>
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
elif page == "✉️ Cover Letter":
    st.markdown("""
    <div class="app-header" style="padding:1.2rem 2rem; background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);">
        <h1 style="font-size:1.8rem;">✉️ Cover Letter Generator</h1>
        <p>Personalized cover letters for job applications.</p>
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
elif page == "📊 Proposal":
    st.markdown("""
    <div class="app-header" style="padding:1.2rem 2rem; background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);">
        <h1 style="font-size:1.8rem;">📊 Proposal Generator</h1>
        <p>Professional project proposals for clients.</p>
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
elif page == "🏆 Experience":
    st.markdown("""
    <div class="app-header" style="padding:1.2rem 2rem; background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);">
        <h1 style="font-size:1.8rem;">🏆 Experience Letter Generator</h1>
        <p>Employment verification letters.</p>
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
elif page == "🔍 Job Scraper":
    st.markdown("""
    <div class="app-header" style="padding:1.2rem 2rem; background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);">
        <h1 style="font-size:1.8rem;">🔍 Job Scraper</h1>
        <p>Find jobs and match your skills.</p>
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