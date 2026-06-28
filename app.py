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

# ---- (Keep all CSS and JavaScript exactly as before) ----
# ... I'm omitting the CSS/JS for brevity, but it's the same as the previous version ...

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
if "show_support_modal" not in st.session_state:
    st.session_state.show_support_modal = False

# ---- Page navigation helper ----
def go_to_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# ---- Sidebar Navigation (same as before) ----
with st.sidebar:
    # ... (same as before) ...

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
            <button class="btn-primary" onclick="document.querySelector('[data-testid=\\"stButton\\"] button')?.click()">Get Started Free</button>
            <a href="#about" class="btn-secondary">Learn More</a>
            <button class="btn-support" onclick="document.querySelector('[data-testid=\\"stButton\\"] button')?.click()">Support Me 💖</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Hidden buttons to handle clicks
    if st.button("Get Started Free (hidden)", key="home_get_started", use_container_width=False, type="primary"):
        go_to_page("Builder")

    if st.button("Support Me (hidden)", key="home_support", use_container_width=False, type="secondary"):
        st.session_state.show_support_modal = not st.session_state.show_support_modal
        st.rerun()

    # Support Modal with Fireworks – fetch image at runtime
    if st.session_state.show_support_modal:
        # ── Your correct raw URL ──
        qr_image_url = "https://raw.githubusercontent.com/panwarrudraksh-alt/Document-Forge/main/static/api_qr.jpeg"
        
        # Fetch and encode to base64
        try:
            response = requests.get(qr_image_url, timeout=10)
            if response.status_code == 200:
                img_base64 = base64.b64encode(response.content).decode("utf-8")
                img_src = f"data:image/jpeg;base64,{img_base64}"
            else:
                img_src = ""  # will trigger fallback
        except Exception:
            img_src = ""

        support_html = f"""
        <div id="support-modal" style="position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(0,0,0,0.7); backdrop-filter:blur(8px); z-index:9999; display:flex; align-items:center; justify-content:center; animation:fadeIn 0.5s ease;">
            <div style="background:white; border-radius:24px; padding:2rem; max-width:90vw; max-height:90vh; overflow:auto; position:relative; box-shadow:0 30px 80px rgba(0,0,0,0.5);">
                <button onclick="document.getElementById('support-modal').style.display='none'; window.parent.postMessage({{type:'streamlit:setComponentValue', value:false}}, '*');" style="position:absolute; top:12px; right:16px; background:none; border:none; font-size:1.8rem; cursor:pointer; color:#333;">✕</button>
                <h2 style="text-align:center; color:#1a2a3a; margin-bottom:1rem;">Support the Developer ❤️</h2>
                <div style="text-align:center;">
                    <img src="{img_src}" alt="UPI QR Code" style="max-width:300px; width:100%; height:auto; border-radius:12px; box-shadow:0 8px 24px rgba(0,0,0,0.1);" onerror="this.style.display='none'; document.getElementById('fallback-text').style.display='block';">
                    <p id="fallback-text" style="display:none; color:#666; font-size:1.1rem; margin-top:1rem;">QR Code could not be loaded.<br>Please try again later.</p>
                    <p style="margin-top:0.5rem; color:#666;">Scan to support – every contribution helps! 🙏</p>
                </div>
                <canvas id="fireworks-canvas" style="position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; border-radius:24px;"></canvas>
            </div>
        </div>
        <style>
            @keyframes fadeIn {{ from {{ opacity:0; transform:scale(0.9); }} to {{ opacity:1; transform:scale(1); }} }}
        </style>
        <script>
            (function() {{
                const canvas = document.getElementById('fireworks-canvas');
                if (!canvas) return;
                const ctx = canvas.getContext('2d');
                let width, height;
                const particles = [];
                const colors = ['#ff6b6b', '#ffd93d', '#6bcb77', '#4d96ff', '#ff6bff', '#ffb347'];

                function resize() {{
                    const rect = canvas.parentElement.getBoundingClientRect();
                    canvas.width = rect.width;
                    canvas.height = rect.height;
                    width = canvas.width;
                    height = canvas.height;
                }}
                resize();
                window.addEventListener('resize', resize);

                class Particle {{
                    constructor(x, y) {{
                        this.x = x;
                        this.y = y;
                        const angle = Math.random() * 2 * Math.PI;
                        const speed = Math.random() * 6 + 2;
                        this.vx = Math.cos(angle) * speed;
                        this.vy = Math.sin(angle) * speed;
                        this.life = 1;
                        this.decay = Math.random() * 0.015 + 0.005;
                        this.radius = Math.random() * 4 + 2;
                        this.color = colors[Math.floor(Math.random() * colors.length)];
                        this.trail = [];
                    }}
                    update() {{
                        this.trail.push({{x: this.x, y: this.y}});
                        if (this.trail.length > 8) this.trail.shift();
                        this.x += this.vx;
                        this.y += this.vy;
                        this.vy += 0.05;
                        this.vx *= 0.99;
                        this.vy *= 0.99;
                        this.life -= this.decay;
                    }}
                    draw() {{
                        for (let i = 0; i < this.trail.length; i++) {{
                            const alpha = (i / this.trail.length) * 0.8;
                            ctx.beginPath();
                            ctx.arc(this.trail[i].x, this.trail[i].y, this.radius * (i / this.trail.length), 0, Math.PI * 2);
                            ctx.fillStyle = this.color + Math.floor(alpha * 255).toString(16).padStart(2, '0');
                            ctx.fill();
                        }}
                        ctx.beginPath();
                        ctx.arc(this.x, this.y, this.radius * this.life, 0, Math.PI * 2);
                        ctx.fillStyle = this.color;
                        ctx.globalAlpha = this.life;
                        ctx.fill();
                        ctx.globalAlpha = 1;
                    }}
                }}

                function launchFirework() {{
                    const x = Math.random() * width * 0.8 + width * 0.1;
                    const y = Math.random() * height * 0.6 + height * 0.1;
                    const count = 80 + Math.floor(Math.random() * 60);
                    for (let i = 0; i < count; i++) {{
                        particles.push(new Particle(x, y));
                    }}
                }}

                function animate() {{
                    ctx.clearRect(0, 0, width, height);
                    for (let i = particles.length - 1; i >= 0; i--) {{
                        const p = particles[i];
                        p.update();
                        p.draw();
                        if (p.life <= 0) {{
                            particles.splice(i, 1);
                        }}
                    }}
                    if (particles.length < 200) {{
                        if (Math.random() < 0.05) launchFirework();
                    }}
                    requestAnimationFrame(animate);
                }}

                for (let i = 0; i < 5; i++) {{
                    setTimeout(launchFirework, i * 200);
                }}
                setInterval(launchFirework, 800);
                animate();

                const modal = document.getElementById('support-modal');
                const observer = new MutationObserver(() => {{
                    if (modal.style.display === 'none') {{ /* no-op */ }}
                }});
                observer.observe(modal, {{ attributes: true, attributeFilter: ['style'] }});
            }})();
        </script>
        """
        st.components.v1.html(support_html, height=0)

    # About Me (same as before)
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

    # Features – clickable cards (same as before)
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

# ---- All other pages (Builder, Resume, CV, etc.) are unchanged from the previous version ----
# I'm not repeating them here for space, but they must be included in your final app.py.

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

# ---- FLOATING CHAT (unchanged) ----
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
