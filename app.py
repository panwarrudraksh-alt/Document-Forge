import streamlit as st
from datetime import datetime

# ---- Page Config ----
st.set_page_config(
    page_title="DocForge – Professional Document Builder",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- THEME: Dark Glassmorphism / Neon Slate ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & Root ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg:        #0b0f1a;
    --bg2:       #111827;
    --bg3:       #1a2235;
    --glass:     rgba(255,255,255,0.04);
    --glass2:    rgba(255,255,255,0.08);
    --border:    rgba(255,255,255,0.08);
    --border2:   rgba(255,255,255,0.14);
    --neon:      #00e5ff;
    --neon2:     #7c3aed;
    --neon3:     #10b981;
    --neon4:     #f59e0b;
    --text:      #f0f4ff;
    --text2:     #94a3b8;
    --text3:     #4b5563;
    --danger:    #f43f5e;
    --r:         12px;
    --r2:        18px;
    --r3:        24px;
}

/* ── Global ── */
html, body, .stApp {
    font-family: 'Space Grotesk', sans-serif;
    background: var(--bg) !important;
    color: var(--text) !important;
}

.block-container {
    padding: 1.5rem 2rem 3rem !important;
    max-width: 1400px !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--bg3); border-radius: 99px; }

/* ───────────────────────────────────────────────
   SIDEBAR
─────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
    width: 240px !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }

/* Sidebar text overrides */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div { color: var(--text2) !important; }

/* Radio nav pills */
section[data-testid="stSidebar"] .stRadio > div {
    gap: 2px !important;
    flex-direction: column;
}
section[data-testid="stSidebar"] .stRadio label {
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    padding: 10px 16px !important;
    border-radius: var(--r) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: var(--text2) !important;
    cursor: pointer !important;
    transition: all .2s !important;
    margin: 1px 8px !important;
    width: calc(100% - 16px) !important;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: var(--glass2) !important;
    color: var(--text) !important;
}
section[data-testid="stSidebar"] .stRadio label[data-selected="true"] {
    background: linear-gradient(135deg, rgba(0,229,255,.12), rgba(124,58,237,.12)) !important;
    color: var(--neon) !important;
    border: 1px solid rgba(0,229,255,.2) !important;
}
/* Hide default radio circles */
section[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] { display: none; }
section[data-testid="stSidebar"] .stRadio > div > label > div:first-child { display: none; }

/* Sidebar metrics */
section[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: var(--glass) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    padding: 12px !important;
}
section[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    color: var(--neon) !important;
    font-size: 22px !important;
}
section[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
    color: var(--text3) !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: .6px !important;
}
section[data-testid="stSidebar"] .stCaption {
    color: var(--text3) !important;
    font-size: 10px !important;
}

/* ───────────────────────────────────────────────
   TYPOGRAPHY HELPERS
─────────────────────────────────────────────── */
.df-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 20px 16px 16px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 8px;
}
.df-logo-icon {
    width: 38px; height: 38px;
    border-radius: 10px;
    background: linear-gradient(135deg, #00e5ff22, #7c3aed33);
    border: 1px solid rgba(0,229,255,.3);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.df-logo-text { line-height: 1; }
.df-logo-name { font-weight: 700; font-size: 16px; color: var(--text) !important; }
.df-logo-sub  { font-size: 10px; color: var(--text3) !important; letter-spacing: .5px; margin-top: 2px; }

/* Page header */
.df-header {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 20px 24px;
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: var(--r3);
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.df-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, rgba(0,229,255,.03), rgba(124,58,237,.03));
    pointer-events: none;
}
.df-header-icon {
    font-size: 2rem;
    width: 52px; height: 52px;
    background: linear-gradient(135deg, rgba(0,229,255,.1), rgba(124,58,237,.15));
    border: 1px solid rgba(0,229,255,.2);
    border-radius: var(--r);
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.df-header h1 {
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
    letter-spacing: -.5px !important;
    margin: 0 !important;
    line-height: 1.2 !important;
}
.df-header p {
    color: var(--text2) !important;
    font-size: .875rem !important;
    margin: 3px 0 0 !important;
}

/* ───────────────────────────────────────────────
   CARDS
─────────────────────────────────────────────── */
.df-card {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: var(--r2);
    padding: 20px;
    transition: border-color .2s, transform .2s;
}
.df-card:hover { border-color: var(--border2); }

/* Doc type cards on home */
.doc-card {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: var(--r2);
    padding: 22px 16px;
    text-align: center;
    transition: all .25s;
    cursor: default;
    height: 100%;
    position: relative;
    overflow: hidden;
}
.doc-card::after {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 60%; height: 1px;
    background: linear-gradient(90deg, transparent, var(--neon), transparent);
    opacity: 0;
    transition: opacity .3s;
}
.doc-card:hover { transform: translateY(-4px); border-color: rgba(0,229,255,.25); }
.doc-card:hover::after { opacity: 1; }

.doc-card .dc-icon { font-size: 2.4rem; display: block; margin-bottom: 10px; }
.doc-card .dc-name {
    font-size: .9rem; font-weight: 700; color: var(--text) !important;
    letter-spacing: -.2px;
}
.doc-card .dc-desc { font-size: .75rem; color: var(--text2) !important; margin-top: 4px; }
.doc-card .dc-badge {
    display: inline-block;
    margin-top: 10px;
    padding: 3px 10px;
    border-radius: 99px;
    font-size: .68rem;
    font-weight: 600;
    letter-spacing: .3px;
}
.badge-cyan   { background: rgba(0,229,255,.1);   color: #00e5ff !important; border: 1px solid rgba(0,229,255,.2);   }
.badge-violet { background: rgba(124,58,237,.12); color: #a78bfa !important; border: 1px solid rgba(124,58,237,.25); }
.badge-emerald{ background: rgba(16,185,129,.1);  color: #34d399 !important; border: 1px solid rgba(16,185,129,.2);  }
.badge-amber  { background: rgba(245,158,11,.1);  color: #fbbf24 !important; border: 1px solid rgba(245,158,11,.2);  }

/* Steps row */
.step-row { display: flex; gap: 12px; margin-top: .5rem; }
.step-box {
    flex: 1;
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: var(--r);
    padding: 16px 14px;
    text-align: center;
}
.step-num {
    width: 30px; height: 30px;
    border-radius: 50%;
    background: linear-gradient(135deg, rgba(0,229,255,.15), rgba(124,58,237,.15));
    border: 1px solid rgba(0,229,255,.2);
    color: var(--neon) !important;
    font-size: .78rem; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 8px;
    font-family: 'JetBrains Mono', monospace;
}
.step-t { font-size: .82rem; font-weight: 600; color: var(--text) !important; }
.step-d { font-size: .72rem; color: var(--text3) !important; margin-top: 3px; }

/* ───────────────────────────────────────────────
   FORM INPUTS
─────────────────────────────────────────────── */
.stTextInput > label,
.stTextArea  > label,
.stSelectbox > label {
    color: var(--text2) !important;
    font-size: .78rem !important;
    font-weight: 600 !important;
    letter-spacing: .3px !important;
    text-transform: uppercase !important;
    margin-bottom: 5px !important;
}
.stTextInput > div > div > input,
.stTextArea  > div > div > textarea,
.stSelectbox > div > div {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: .9rem !important;
    padding: 10px 14px !important;
    transition: border-color .2s, box-shadow .2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea  > div > div > textarea:focus {
    border-color: rgba(0,229,255,.4) !important;
    box-shadow: 0 0 0 3px rgba(0,229,255,.08) !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea  > div > div > textarea::placeholder {
    color: var(--text3) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg3) !important;
    border-radius: var(--r) !important;
    padding: 4px !important;
    gap: 2px !important;
    border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: var(--text2) !important;
    font-size: .82rem !important;
    font-weight: 600 !important;
    padding: 6px 14px !important;
    background: none !important;
    transition: all .2s !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--text) !important; }
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0,229,255,.12), rgba(124,58,237,.12)) !important;
    color: var(--neon) !important;
    border: 1px solid rgba(0,229,255,.2) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* ───────────────────────────────────────────────
   BUTTONS
─────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #00e5ff18, #7c3aed22) !important;
    border: 1px solid rgba(0,229,255,.25) !important;
    color: var(--neon) !important;
    border-radius: var(--r) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: .88rem !important;
    padding: .6rem 1.2rem !important;
    transition: all .2s !important;
    letter-spacing: .2px !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #00e5ff28, #7c3aed35) !important;
    border-color: rgba(0,229,255,.5) !important;
    box-shadow: 0 0 20px rgba(0,229,255,.15) !important;
    transform: translateY(-1px) !important;
}
/* Primary variant (type="primary") */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #00e5ffcc, #7c3aedcc) !important;
    border: none !important;
    color: #0b0f1a !important;
    font-weight: 700 !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 0 30px rgba(0,229,255,.3) !important;
    transform: translateY(-2px) !important;
}

.stDownloadButton > button {
    background: linear-gradient(135deg, rgba(16,185,129,.15), rgba(16,185,129,.25)) !important;
    border: 1px solid rgba(16,185,129,.35) !important;
    color: #34d399 !important;
    border-radius: var(--r) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    width: 100% !important;
}
.stDownloadButton > button:hover {
    box-shadow: 0 0 20px rgba(16,185,129,.2) !important;
    transform: translateY(-1px) !important;
}

/* ───────────────────────────────────────────────
   ALERTS & INFO
─────────────────────────────────────────────── */
.stAlert { border-radius: var(--r) !important; background: var(--bg3) !important; }
.stSuccess { border-left: 3px solid var(--neon3) !important; }
.stInfo    { border-left: 3px solid var(--neon) !important; }
.stError   { border-left: 3px solid var(--danger) !important; }

/* ───────────────────────────────────────────────
   SKILL TAGS
─────────────────────────────────────────────── */
.skill-chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(124,58,237,.12);
    border: 1px solid rgba(124,58,237,.25);
    color: #a78bfa !important;
    padding: 4px 12px;
    border-radius: 99px;
    font-size: .75rem;
    font-weight: 600;
    margin: 3px;
    transition: all .2s;
    cursor: default;
}
.skill-chip:hover { background: rgba(124,58,237,.2); border-color: rgba(124,58,237,.4); }

/* ───────────────────────────────────────────────
   GENERATE PANEL
─────────────────────────────────────────────── */
.gen-box {
    background: linear-gradient(135deg, rgba(0,229,255,.04), rgba(124,58,237,.06));
    border: 1px solid rgba(0,229,255,.15);
    border-radius: var(--r2);
    padding: 18px;
}
.gen-box h4 {
    font-size: .78rem !important;
    font-weight: 600 !important;
    color: var(--text2) !important;
    text-transform: uppercase !important;
    letter-spacing: .6px !important;
    margin-bottom: 10px !important;
}
.check-row {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: .82rem;
    color: var(--text2) !important;
    padding: 4px 0;
}
.check-dot {
    width: 18px; height: 18px;
    border-radius: 5px;
    background: rgba(16,185,129,.2);
    border: 1px solid rgba(16,185,129,.4);
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    font-size: .65rem;
    color: #34d399 !important;
}

/* ───────────────────────────────────────────────
   JOB LISTINGS
─────────────────────────────────────────────── */
.job-row {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: var(--r);
    padding: 14px 16px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    transition: border-color .2s;
}
.job-row:hover { border-color: var(--border2); }
.job-title { font-size: .9rem; font-weight: 600; color: var(--text) !important; }
.job-meta  { font-size: .75rem; color: var(--text2) !important; margin-top: 3px; }
.job-badge {
    font-size: .72rem;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 99px;
    font-family: 'JetBrains Mono', monospace;
    flex-shrink: 0;
    min-width: 52px;
    text-align: center;
}
.match-hi  { background: rgba(16,185,129,.15); color: #34d399 !important; border: 1px solid rgba(16,185,129,.3); }
.match-mid { background: rgba(245,158,11,.12); color: #fbbf24 !important; border: 1px solid rgba(245,158,11,.25); }
.match-lo  { background: rgba(244,63,94,.1);   color: #fb7185 !important; border: 1px solid rgba(244,63,94,.2); }

/* ───────────────────────────────────────────────
   THEME PICKER
─────────────────────────────────────────────── */
.theme-grid { display: flex; gap: 8px; margin-top: 8px; }
.theme-pill {
    display: flex;
    align-items: center;
    gap: 7px;
    padding: 7px 14px;
    border-radius: 99px;
    border: 1px solid var(--border);
    background: var(--glass);
    cursor: pointer;
    font-size: .78rem;
    font-weight: 600;
    color: var(--text2) !important;
    transition: all .2s;
}
.theme-pill:hover { border-color: var(--border2); color: var(--text) !important; }
.theme-dot { width: 10px; height: 10px; border-radius: 50%; }

/* ───────────────────────────────────────────────
   DIVIDER
─────────────────────────────────────────────── */
hr { border: none; border-top: 1px solid var(--border) !important; margin: 1rem 0 !important; }

/* Section label */
.sec-label {
    font-size: .7rem;
    font-weight: 700;
    color: var(--text3) !important;
    text-transform: uppercase;
    letter-spacing: .8px;
    margin-bottom: .6rem;
    margin-top: 1.2rem;
}

/* Stat cards row */
.stat-grid { display: flex; gap: 10px; margin-bottom: 1rem; }
.stat-card {
    flex: 1;
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: var(--r);
    padding: 14px 16px;
}
.stat-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--neon) !important;
    line-height: 1;
}
.stat-lbl { font-size: .72rem; color: var(--text3) !important; margin-top: 4px; text-transform: uppercase; letter-spacing: .5px; }
</style>
""", unsafe_allow_html=True)

# ── Session State ──
if "skills" not in st.session_state:    st.session_state.skills = []
if "jobs"   not in st.session_state:    st.session_state.jobs   = []

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div class="df-logo">
        <div class="df-logo-icon">⚡</div>
        <div class="df-logo-text">
            <div class="df-logo-name">DocForge</div>
            <div class="df-logo-sub">DOCUMENT BUILDER</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("nav", [
        "⚡  Home",
        "✏️  Builder",
        "📄  Resume",
        "📋  CV",
        "✉️  Cover Letter",
        "📊  Proposal",
        "🏆  Experience Letter",
        "🔍  Job Scraper",
    ], label_visibility="collapsed")

    st.markdown("<hr>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.metric("Skills", len(st.session_state.skills))
    c2.metric("Jobs",   len(st.session_state.jobs))
    st.caption("⚡ Powered by Streamlit + ReportLab")


# ── Helpers ──
def header(icon, title, sub):
    st.markdown(f"""
    <div class="df-header">
        <div class="df-header-icon">{icon}</div>
        <div>
            <h1>{title}</h1>
            <p>{sub}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def sec(label):
    st.markdown(f'<div class="sec-label">{label}</div>', unsafe_allow_html=True)

def gen_box(sections):
    rows = "".join(
        f'<div class="check-row"><div class="check-dot">✓</div> {s}</div>'
        for s in sections
    )
    st.markdown(f'<div class="gen-box"><h4>Sections included</h4>{rows}</div>',
                unsafe_allow_html=True)

def get_data():
    return {
        "name":      st.session_state.get("f_name", ""),
        "title":     st.session_state.get("f_title", ""),
        "email":     st.session_state.get("f_email", ""),
        "phone":     st.session_state.get("f_phone", ""),
        "location":  st.session_state.get("f_loc", ""),
        "linkedin":  st.session_state.get("f_linkedin", ""),
        "skills":    st.session_state.skills,
        "company":   st.session_state.get("f_company", ""),
        "role":      st.session_state.get("f_exp_role", ""),
        "duration":  st.session_state.get("f_duration", ""),
        "exp_desc":  st.session_state.get("f_exp_desc", ""),
        "degree":    st.session_state.get("f_degree", ""),
        "institution": st.session_state.get("f_inst", ""),
        "year":      st.session_state.get("f_year", ""),
        "projects":  st.session_state.get("f_projects", ""),
        "summary":   st.session_state.get("f_summary", ""),
        "theme":     "Classic Green",
    }

def theme_picker(key):
    themes = [("Classic Green", "#10b981"), ("Corporate Blue", "#3b82f6"), ("Creative Purple", "#8b5cf6")]
    dots = "".join(
        f'<div class="theme-pill"><div class="theme-dot" style="background:{c}"></div>{n}</div>'
        for n, c in themes
    )
    st.markdown(f'<div class="theme-grid">{dots}</div>', unsafe_allow_html=True)
    return st.selectbox("Theme", [t[0] for t in themes], key=key, label_visibility="collapsed")


# ═══════════════════════════════════════════════
#  HOME
# ═══════════════════════════════════════════════
if page == "⚡  Home":
    header("⚡", "DocForge", "Professional documents — built in seconds, not hours")

    # Doc type grid
    sec("What you can build")
    c1, c2, c3, c4 = st.columns(4)
    tiles = [
        ("📄", "Resume",           "ATS-optimized, one-pager",      "badge-emerald", "Most popular"),
        ("📋", "CV",               "Full academic & career record",  "badge-cyan",    "Comprehensive"),
        ("✉️", "Cover Letter",     "Personalized job pitch",         "badge-amber",   "Tailored"),
        ("📊", "Proposal",         "Client-ready project brief",     "badge-violet",  "Professional"),
    ]
    for col, (icon, name, desc, badge, label) in zip([c1, c2, c3, c4], tiles):
        with col:
            st.markdown(f"""
            <div class="doc-card">
                <span class="dc-icon">{icon}</span>
                <div class="dc-name">{name}</div>
                <div class="dc-desc">{desc}</div>
                <span class="dc-badge {badge}">{label}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5:
        st.markdown("""
        <div class="doc-card">
            <span class="dc-icon">🏆</span>
            <div class="dc-name">Experience Letter</div>
            <div class="dc-desc">Official employment verification</div>
            <span class="dc-badge badge-cyan">Formal</span>
        </div>
        """, unsafe_allow_html=True)
    with c6:
        st.markdown("""
        <div class="doc-card">
            <span class="dc-icon">🔍</span>
            <div class="dc-name">Job Scraper</div>
            <div class="dc-desc">Live job listings matched to your skills</div>
            <span class="dc-badge badge-violet">Live data</span>
        </div>
        """, unsafe_allow_html=True)

    # How it works
    st.markdown("<br>", unsafe_allow_html=True)
    sec("How it works")
    st.markdown("""
    <div class="step-row">
        <div class="step-box">
            <div class="step-num">01</div>
            <div class="step-t">Fill details</div>
            <div class="step-d">Enter your info once in Builder</div>
        </div>
        <div class="step-box">
            <div class="step-num">02</div>
            <div class="step-t">Choose document</div>
            <div class="step-d">Pick from 5 document types</div>
        </div>
        <div class="step-box">
            <div class="step-num">03</div>
            <div class="step-t">Customize</div>
            <div class="step-d">Add specifics & pick a theme</div>
        </div>
        <div class="step-box">
            <div class="step-num">04</div>
            <div class="step-t">Download PDF</div>
            <div class="step-d">Instant professional export</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════
#  BUILDER
# ═══════════════════════════════════════════════
elif page == "✏️  Builder":
    header("✏️", "Document Builder", "Fill your details once — every document pulls from here")

    tabs = st.tabs(["👤 Personal", "💼 Experience", "🎓 Education", "🛠️ Skills", "📝 Summary"])

    with tabs[0]:
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Full name *",          key="f_name",    placeholder="Alex Johnson")
            st.text_input("Email address *",      key="f_email",   placeholder="alex@example.com")
            st.text_input("Phone number",         key="f_phone",   placeholder="+1 234 567 890")
        with c2:
            st.text_input("Professional title",   key="f_title",   placeholder="Senior Software Engineer")
            st.text_input("Location",             key="f_loc",     placeholder="San Francisco, CA")
            st.text_input("LinkedIn URL",         key="f_linkedin",placeholder="linkedin.com/in/alex")

    with tabs[1]:
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Company",  key="f_company",  placeholder="Stripe")
            st.text_input("Your role",key="f_exp_role", placeholder="Backend Engineer")
        with c2:
            st.text_input("Duration", key="f_duration", placeholder="Mar 2021 – Present")
        st.text_area("Key responsibilities",
                     key="f_exp_desc",
                     placeholder="• Built payment APIs handling $2M/day\n• Led infrastructure migrations to AWS\n• Mentored team of 4 engineers",
                     height=130)

    with tabs[2]:
        c1, c2, c3 = st.columns(3)
        with c1: st.text_input("Degree",      key="f_degree", placeholder="B.S. Computer Science")
        with c2: st.text_input("Institution", key="f_inst",   placeholder="MIT")
        with c3: st.text_input("Years",       key="f_year",   placeholder="2016 – 2020")
        st.text_area("Projects",
                     key="f_projects",
                     placeholder="DocForge — AI-powered document builder\nPayAPI — Stripe integration middleware",
                     height=100)

    with tabs[3]:
        cA, cB = st.columns([4, 1])
        with cA:
            new_skill = st.text_input("Add a skill", key="skill_input",
                                      placeholder="e.g. Python, React, Figma...")
        with cB:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Add", use_container_width=True) and new_skill.strip():
                s = new_skill.strip().lower()
                if s not in st.session_state.skills:
                    st.session_state.skills.append(s)
                st.rerun()

        if st.session_state.skills:
            chips = "".join(
                f'<span class="skill-chip">{s.title()}</span>'
                for s in st.session_state.skills
            )
            st.markdown(f'<div style="margin-top:10px">{chips}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            cols = st.columns(min(len(st.session_state.skills), 6))
            for i, sk in enumerate(st.session_state.skills):
                with cols[i % 6]:
                    if st.button(f"✕ {sk.title()}", key=f"rm_{sk}", use_container_width=True):
                        st.session_state.skills.remove(sk)
                        st.rerun()
        else:
            st.info("No skills added yet — type one above and click Add.")

    with tabs[4]:
        st.text_area("Professional summary",
                     key="f_summary",
                     placeholder="Results-driven software engineer with 6+ years building scalable backend systems...",
                     height=120)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾  Save all details", type="primary", use_container_width=True):
        st.success("✅  Details saved — head to any document tab to generate your PDF.")


# ═══════════════════════════════════════════════
#  RESUME
# ═══════════════════════════════════════════════
elif page == "📄  Resume":
    header("📄", "Resume", "ATS-optimized · single page · instant PDF")

    c1, c2 = st.columns([3, 2])
    with c1:
        sec("Customize")
        selected_theme = theme_picker("resume_theme")
        st.text_area("Override summary (optional)",
                     key="resume_summary",
                     placeholder="Leave blank to use your saved summary...",
                     height=100)
    with c2:
        sec("Included sections")
        gen_box(["Personal info", "Professional summary", "Core skills",
                 "Work experience", "Education", "Projects"])

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⚡  Generate Resume PDF", type="primary", use_container_width=True):
        data = get_data()
        data["summary"] = st.session_state.get("resume_summary") or data["summary"]
        data["theme"]   = selected_theme
        try:
            from pdf_generator import generate_resume_pdf
            pdf = generate_resume_pdf(data)
            if pdf:
                st.download_button("⬇️  Download Resume PDF", pdf,
                                   f"{data['name'].replace(' ','_')}_Resume.pdf",
                                   "application/pdf", use_container_width=True)
            else:
                st.error("PDF generation failed — check your pdf_generator.py.")
        except ImportError:
            st.warning("⚠️  pdf_generator.py not found — wire up your generate_resume_pdf() function.")


# ═══════════════════════════════════════════════
#  CV
# ═══════════════════════════════════════════════
elif page == "📋  CV":
    header("📋", "Curriculum Vitae", "Full academic & professional record · multi-page PDF")

    c1, c2 = st.columns([3, 2])
    with c1:
        sec("Customize")
        cv_theme = theme_picker("cv_theme")
        st.text_area("Publications (one per line)",
                     key="cv_publications",
                     placeholder="• Smith, A. (2024). 'Transformer Efficiency.' NeurIPS 2024.",
                     height=100)
    with c2:
        sec("Included sections")
        gen_box(["Personal info", "Summary", "Skills", "Experience",
                 "Education", "Publications", "Projects"])

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⚡  Generate CV PDF", type="primary", use_container_width=True):
        data = get_data()
        data["publications"] = st.session_state.get("cv_publications", "")
        data["theme"] = cv_theme
        try:
            from pdf_generator import generate_cv_pdf
            pdf = generate_cv_pdf(data)
            if pdf:
                st.download_button("⬇️  Download CV PDF", pdf,
                                   f"{data['name'].replace(' ','_')}_CV.pdf",
                                   "application/pdf", use_container_width=True)
            else:
                st.error("PDF generation failed.")
        except ImportError:
            st.warning("⚠️  pdf_generator.py not found.")


# ═══════════════════════════════════════════════
#  COVER LETTER
# ═══════════════════════════════════════════════
elif page == "✉️  Cover Letter":
    header("✉️", "Cover Letter", "Personalized for every application · professional tone")

    c1, c2 = st.columns([3, 2])
    with c1:
        sec("Job details")
        col_a, col_b = st.columns(2)
        with col_a:
            st.text_input("Company name *",   key="cover_company",   placeholder="Google")
            st.text_input("Position *",       key="cover_position",  placeholder="Staff Engineer")
        with col_b:
            st.text_input("Recruiter name",   key="cover_recruiter", placeholder="Sarah Johnson")
        st.text_area("Why you're a great fit (optional)",
                     key="cover_custom",
                     placeholder="Specific achievements, why this company excites you...",
                     height=100)
        sec("Theme")
        cover_theme = theme_picker("cover_theme")
    with c2:
        sec("Letter structure")
        gen_box(["Sender contact info", "Date", "Recipient greeting",
                 "Opening hook", "Body paragraphs", "Strong closing", "Signature"])

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⚡  Generate Cover Letter PDF", type="primary", use_container_width=True):
        data = get_data()
        data.update({
            "cover_company":   st.session_state.get("cover_company", ""),
            "cover_position":  st.session_state.get("cover_position", ""),
            "cover_recruiter": st.session_state.get("cover_recruiter", ""),
            "cover_custom":    st.session_state.get("cover_custom", ""),
            "theme":           cover_theme,
        })
        try:
            from pdf_generator import generate_cover_letter_pdf
            pdf = generate_cover_letter_pdf(data)
            if pdf:
                st.download_button("⬇️  Download Cover Letter PDF", pdf,
                                   f"{data['name'].replace(' ','_')}_Cover_Letter.pdf",
                                   "application/pdf", use_container_width=True)
            else:
                st.error("PDF generation failed.")
        except ImportError:
            st.warning("⚠️  pdf_generator.py not found.")


# ═══════════════════════════════════════════════
#  PROPOSAL
# ═══════════════════════════════════════════════
elif page == "📊  Proposal":
    header("📊", "Project Proposal", "Client-ready · structured · persuasive")

    c1, c2 = st.columns([3, 2])
    with c1:
        sec("Project details")
        col_a, col_b = st.columns(2)
        with col_a:
            st.text_input("Proposal title *",      key="prop_title",    placeholder="AI Customer Support System")
            st.text_input("Client / organization *",key="prop_client",  placeholder="Acme Corp")
        with col_b:
            st.text_input("Budget range",           key="prop_budget",   placeholder="$40,000 – $60,000")
            st.text_input("Delivery timeline",      key="prop_timeline", placeholder="10 weeks")
        st.text_area("Executive summary *",
                     key="prop_summary",
                     placeholder="This proposal outlines a scalable solution for...",
                     height=90)
        st.text_area("Approach & methodology *",
                     key="prop_approach",
                     placeholder="Phase 1: Discovery & architecture\nPhase 2: Development sprints\nPhase 3: QA & deployment",
                     height=90)
        sec("Theme")
        prop_theme = theme_picker("prop_theme")
    with c2:
        sec("Proposal sections")
        gen_box(["Cover page & title", "Client information",
                 "Executive summary", "Methodology", "Timeline",
                 "About us", "Budget breakdown", "Contact"])

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⚡  Generate Proposal PDF", type="primary", use_container_width=True):
        data = get_data()
        data.update({
            "proposal_title":    st.session_state.get("prop_title", ""),
            "proposal_client":   st.session_state.get("prop_client", ""),
            "proposal_budget":   st.session_state.get("prop_budget", ""),
            "proposal_timeline": st.session_state.get("prop_timeline", ""),
            "proposal_summary":  st.session_state.get("prop_summary", ""),
            "proposal_approach": st.session_state.get("prop_approach", ""),
            "theme":             prop_theme,
        })
        try:
            from pdf_generator import generate_proposal_pdf
            pdf = generate_proposal_pdf(data)
            if pdf:
                st.download_button("⬇️  Download Proposal PDF", pdf,
                                   f"{data['name'].replace(' ','_')}_Proposal.pdf",
                                   "application/pdf", use_container_width=True)
            else:
                st.error("PDF generation failed.")
        except ImportError:
            st.warning("⚠️  pdf_generator.py not found.")


# ═══════════════════════════════════════════════
#  EXPERIENCE LETTER
# ═══════════════════════════════════════════════
elif page == "🏆  Experience Letter":
    header("🏆", "Experience Letter", "Official employment verification · company letterhead")

    c1, c2 = st.columns([3, 2])
    with c1:
        sec("Letter details")
        col_a, col_b = st.columns(2)
        with col_a:
            st.text_input("Company name *",      key="exp_company",       placeholder="TechCorp Inc.")
            st.text_input("Employee name *",     key="exp_employee",      placeholder="Alex Johnson")
            st.text_input("Position held *",     key="exp_position",      placeholder="Senior Developer")
        with col_b:
            st.text_input("Employment period *", key="exp_period",        placeholder="Jan 2020 – Dec 2023")
            st.text_input("Issued by *",         key="exp_issuer",        placeholder="Jane Smith")
            st.text_input("Issuer title *",      key="exp_issuer_title",  placeholder="HR Manager")
        st.text_area("Performance remarks *",
                     key="exp_remarks",
                     placeholder="Alex demonstrated outstanding technical leadership and consistently exceeded KPIs...",
                     height=90)
        sec("Theme")
        exp_theme = theme_picker("exp_theme")
    with c2:
        sec("Letter sections")
        gen_box(["Company letterhead", "Issue date",
                 "Subject line", "Employee details", "Period of employment",
                 "Performance remarks", "Issuer signature & seal"])

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⚡  Generate Experience Letter PDF", type="primary", use_container_width=True):
        data = {
            "exp_company":      st.session_state.get("exp_company", ""),
            "exp_employee":     st.session_state.get("exp_employee", ""),
            "exp_position":     st.session_state.get("exp_position", ""),
            "exp_period":       st.session_state.get("exp_period", ""),
            "exp_remarks":      st.session_state.get("exp_remarks", ""),
            "exp_issuer":       st.session_state.get("exp_issuer", ""),
            "exp_issuer_title": st.session_state.get("exp_issuer_title", ""),
            "theme":            exp_theme,
        }
        try:
            from pdf_generator import generate_experience_letter_pdf
            pdf = generate_experience_letter_pdf(data)
            if pdf:
                st.download_button("⬇️  Download Experience Letter PDF", pdf,
                                   f"{data['exp_employee'].replace(' ','_')}_Experience_Letter.pdf",
                                   "application/pdf", use_container_width=True)
            else:
                st.error("PDF generation failed.")
        except ImportError:
            st.warning("⚠️  pdf_generator.py not found.")


# ═══════════════════════════════════════════════
#  JOB SCRAPER
# ═══════════════════════════════════════════════
elif page == "🔍  Job Scraper":
    header("🔍", "Job Scraper", "Live listings matched against your skills")

    c1, c2 = st.columns([3, 1])
    with c1:
        col_a, col_b = st.columns([2, 1])
        with col_a:
            role = st.text_input("Job role", value="Python Developer", label_visibility="visible")
        with col_b:
            source = st.selectbox("Source", ["RemoteOK (live)", "Simulated"])
        search = st.button("🔍  Search jobs", type="primary", use_container_width=True)
    with c2:
        st.markdown(f"""
        <div style="margin-top:4px">
            <div class="stat-card">
                <div class="stat-val">{len(st.session_state.jobs)}</div>
                <div class="stat-lbl">Jobs found</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.session_state.jobs:
            avg = sum(j["match"] for j in st.session_state.jobs) / len(st.session_state.jobs)
            st.markdown(f"""
            <div style="margin-top:8px">
                <div class="stat-card">
                    <div class="stat-val">{avg:.0f}%</div>
                    <div class="stat-lbl">Avg match</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    if search:
        with st.spinner("Scraping jobs..."):
            try:
                from job_scraper import get_jobs
                jobs = get_jobs(role, source, st.session_state.skills)
                st.session_state.jobs = jobs
                st.success(f"Found {len(jobs)} jobs for '{role}'")
            except ImportError:
                st.warning("⚠️  job_scraper.py not found — using demo data.")
                st.session_state.jobs = [
                    {"emoji": "🐍", "title": "Python Backend Engineer",  "company": "Stripe",       "loc": "Remote",    "type": "Full-time",  "match": 92},
                    {"emoji": "🌐", "title": "Django Developer",          "company": "Notion",       "loc": "USA",       "type": "Contract",   "match": 76},
                    {"emoji": "🤖", "title": "ML Engineer (Python)",      "company": "Hugging Face", "loc": "Remote",    "type": "Full-time",  "match": 63},
                    {"emoji": "📊", "title": "Data Engineer",             "company": "Databricks",   "loc": "EU",        "type": "Full-time",  "match": 48},
                    {"emoji": "🔧", "title": "API Developer",             "company": "Twilio",       "loc": "Remote",    "type": "Part-time",  "match": 31},
                ]

    st.markdown("<hr>", unsafe_allow_html=True)

    if st.session_state.jobs:
        sec(f"{len(st.session_state.jobs)} results")
        for job in st.session_state.jobs[:10]:
            m = job["match"]
            cls = "match-hi" if m >= 70 else "match-mid" if m >= 45 else "match-lo"
            st.markdown(f"""
            <div class="job-row">
                <div>
                    <div class="job-title">{job.get('emoji','')} {job['title']}</div>
                    <div class="job-meta">🏢 {job['company']} &nbsp;·&nbsp; 📍 {job['loc']} &nbsp;·&nbsp; {job['type']}</div>
                </div>
                <div class="job-badge {cls}">{m}%</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Enter a role above and click 'Search jobs' to see matching listings.")
