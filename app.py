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

# ---- UI theme (light / dark) ----
# Presentation-only state: which colour set the stylesheet below uses.
if "ui_theme" not in st.session_state:
    st.session_state.ui_theme = "light"

_THEMES = {
    "light": """
        color-scheme: light;
        --ground: #eef1f7; --surface: #ffffff; --surface-2: #e9edf2; --field: #ffffff;
        --ink: #101318; --ink-2: #3f4856; --ink-3: #5b6573;
        --line: #d3d8e0; --line-strong: #7d8798;
        --acc: #c4006a; --acc-hover: #a30058; --on-acc: #ffffff; --acc-text: #c4006a;
        --cyan: #00b4d8; --cyan-text: #00647f; --cyan-tint: #dff4fa;
        --yellow: #ffd60a;
        --ok: #0b7a3e; --warn: #8a5300; --bad: #b42318;
        --rail: #0d0f13; --rail-ink: #f2f4f7; --rail-muted: #aeb6c3; --rail-line: #2a2f38; --rail-hover: #1a1e25;
        --ambient-1: rgba(124,92,255,0.30); --ambient-2: rgba(0,180,216,0.26); --ambient-3: rgba(255,79,160,0.22);
        --glass-bg: rgba(255,255,255,0.55); --glass-bg-2: rgba(255,255,255,0.38);
        --glass-field: rgba(255,255,255,0.72); --glass-border: rgba(255,255,255,0.85);
        --glass-edge: rgba(255,255,255,0.95); --glass-pill: rgba(255,255,255,0.82);
        --glass-ink: rgba(16,19,24,0.86); --glass-shadow: 0 10px 34px rgba(31,38,80,0.12);
        --rail-glass: rgba(13,15,19,0.72);
    """,
    "dark": """
        color-scheme: dark;
        --ground: #0b0e14; --surface: #171a20; --surface-2: #1f232b; --field: #1f232b;
        --ink: #eef1f5; --ink-2: #b4bcc9; --ink-3: #98a1af;
        --line: #2b313b; --line-strong: #66707f;
        --acc: #ff4fa0; --acc-hover: #ff75b5; --on-acc: #0f1115; --acc-text: #ff6fb3;
        --cyan: #00b4d8; --cyan-text: #4fd3ef; --cyan-tint: #10303a;
        --yellow: #ffd60a;
        --ok: #4cd68a; --warn: #f2b84b; --bad: #ff8a80;
        --rail: #06070a; --rail-ink: #f2f4f7; --rail-muted: #aeb6c3; --rail-line: #2a2f38; --rail-hover: #1a1e25;
        --ambient-1: rgba(124,92,255,0.32); --ambient-2: rgba(0,212,255,0.24); --ambient-3: rgba(255,79,160,0.22);
        --glass-bg: rgba(255,255,255,0.075); --glass-bg-2: rgba(255,255,255,0.05);
        --glass-field: rgba(255,255,255,0.09); --glass-border: rgba(255,255,255,0.16);
        --glass-edge: rgba(255,255,255,0.28); --glass-pill: rgba(255,255,255,0.14);
        --glass-ink: rgba(238,241,245,0.9); --glass-shadow: 0 10px 34px rgba(0,0,0,0.45);
        --rail-glass: rgba(6,7,10,0.62);
    """,
}

# One consistent line-icon set (24px grid, 1.75 stroke) for the sidebar navigation.
_NAV_ICONS = [
    "M3 11.5 12 4l9 7.5M5.5 10v10h13V10M10 20v-5.5h4V20",                                  # Home
    "M4 20h4L19 9l-4-4L4 16v4zM13.5 6.5l4 4",                                                # Builder
    "M6 3h8l4 4v14H6zM14 3v4h4M12 11.5a1.8 1.8 0 1 0 .01 0M9 18c.5-2 1.7-3 3-3s2.5 1 3 3",   # Resume
    "M6 3h12v18H6zM9 8h6M9 12h6M9 16h4",                                                     # CV
    "M3 6h18v12H3zM3 7l9 7 9-7",                                                             # Cover Letter
    "M8 4h8v3H8zM6 5.5H5v15h14v-15h-1M9 17v-4M12 17v-6M15 17v-2.5",                          # Proposal
    "M12 14a5 5 0 1 0 0-10 5 5 0 0 0 0 10zM8.5 13l-1.5 8 5-2.5 5 2.5-1.5-8",                 # Experience
    "M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14zM16.5 16.5 21 21",                                 # Job Scraper
    "M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8zM18.5 15.5l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8z",  # AI Assistant
]
_ICON_CHECK = "M5 12.5 10 17.5 19 7"
_ICON_ARROW = "M5 12h14M13 6l6 6-6 6"
_ICON_SPARK = _NAV_ICONS[8]


def _icon_uri(path_d, stroke="black"):
    svg = (
        "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='" + stroke + "' "
        "stroke-width='1.75' stroke-linecap='round' stroke-linejoin='round'%3E"
        "%3Cpath d='" + path_d + "'/%3E%3C/svg%3E"
    )
    return 'url("data:image/svg+xml,' + svg + '")'


def _nav_icon_css():
    # Each icon is a ::before that exists only where its selector matches the option row. If Streamlit's markup differs
    # from what is expected, the nav falls back to plain text (no empty boxes). Both a direct and a wrapped <label> form
    # are listed because Streamlit versions differ.
    rg = '[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"]'
    rules = []
    for i, d in enumerate(_NAV_ICONS, start=1):
        muted, bright = _icon_uri(d, "%23aeb6c3"), _icon_uri(d, "%23ffffff")
        sel = ["%s > label:nth-child(%d)" % (rg, i), "%s > :nth-child(%d) > label" % (rg, i)]
        rules.append(
            ", ".join(s + "::before" for s in sel)
            + " { content: ''; flex: none; width: 20px; height: 20px; background: %s center / contain no-repeat; }" % muted
        )
        rules.append(
            ", ".join(s + ":hover::before, " + s + ":has(input:checked)::before" for s in sel)
            + " { background-image: %s; }" % bright
        )
    return "\n".join(rules)


_CSS_BASE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&display=swap');

:root {
    __VARS__
    --ico-check: __ICO_CHECK__;
    --ico-arrow: __ICO_ARROW__;
    --ico-spark: __ICO_SPARK__;
}

/* ---------- base ---------- */
html { scroll-behavior: smooth; }
html, body { background-color: var(--ground); }
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background: transparent; color: var(--ink); }
.stApp {
    background-color: var(--ground);
    background-image:
        radial-gradient(1100px 760px at 6% -12%, var(--ambient-1), transparent 62%),
        radial-gradient(980px 700px at 104% 4%, var(--ambient-2), transparent 60%),
        radial-gradient(900px 860px at 48% 118%, var(--ambient-3), transparent 62%);
    background-repeat: no-repeat;
    background-attachment: fixed;
}
.stApp, .stApp :is(p, li, h1, h2, h3, h4, h5, h6, label, input, textarea, button, a, td, th, summary, small, strong, em) {
    font-family: 'Archivo', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
}
.stApp ::selection { background: var(--yellow); color: #101318; }
.stApp * { scrollbar-width: thin; scrollbar-color: var(--line-strong) transparent; }
.stApp :focus-visible { outline: 2px solid var(--acc-text); outline-offset: 2px; }
.stApp [data-testid="stElementContainer"]:has(style), .stApp .element-container:has(style) { display: none; }

[data-testid="stHeader"] { background: transparent; }
[data-testid="stHeader"] :is(button, svg, a, span), [data-testid="stSidebarCollapsedControl"] :is(button, svg), [data-testid="stExpandSidebarButton"] :is(button, svg) { color: var(--ink-2); }

.stApp [data-testid="stMainBlockContainer"], .stApp .block-container {
    max-width: 1120px; margin-inline: auto; padding: 3.5rem 2rem 4rem;
}
.stApp h1, .stApp h2, .stApp h3 { color: var(--ink); letter-spacing: -0.02em; text-wrap: balance; }
.stApp h3 { font-size: 1.25rem; font-weight: 700; }
.stApp p, .stApp li { line-height: 1.6; }
.stApp a { color: var(--cyan-text); text-underline-offset: 0.2em; }
.stApp hr { border: 0; border-top: 1px solid var(--line); margin: 1rem 0; height: 0; background: none; }

/* ---------- sidebar rail ---------- */
[data-testid="stSidebar"] {
    background: var(--rail-glass);
    -webkit-backdrop-filter: blur(26px) saturate(180%);
    backdrop-filter: blur(26px) saturate(180%);
    border-right: 1px solid var(--glass-border);
    box-shadow: inset -1px 0 0 rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] > div:first-child { background: transparent; }
[data-testid="stSidebar"], [data-testid="stSidebar"] :is(p, label, span, div, li, h1, h2, h3, h4) { color: var(--rail-ink); }
[data-testid="stSidebar"] hr { border-top-color: var(--rail-line); }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"], [data-testid="stSidebar"] [data-testid="stCaptionContainer"] * { color: var(--rail-muted); font-size: 0.8125rem; }
[data-testid="stSidebarCollapseButton"] :is(button, svg), [data-testid="stSidebar"] [data-testid="stSidebarHeader"] :is(button, svg) { color: var(--rail-muted); }

.stApp .brand { display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0.25rem 0.25rem; }
.stApp .brand svg { flex: none; }
.stApp .brand-name { font-weight: 800; font-size: 1.3rem; line-height: 1.1; letter-spacing: -0.02em; color: var(--rail-ink); }
.stApp .brand-sub { font-size: 0.8125rem; color: var(--rail-muted); margin-top: 2px; }

[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] { gap: 2px; }
/* Only the option rows (label:not([data-testid="stWidgetLabel"])) are styled, never the widget's own hidden "Navigate" label. */
[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-testid="stWidgetLabel"]) {
    display: flex; align-items: center; gap: 0.75rem; width: 100%; margin: 0;
    padding: 0.6rem 0.75rem; border-radius: 6px; cursor: pointer;
    transition: background-color 0.15s ease, color 0.15s ease;
}
/* Hide only the round radio dot: a direct child that does not hold the option text (the text may or may not be wrapped). */
[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-testid="stWidgetLabel"]) > :is(div, span):not([data-testid="stMarkdownContainer"]):not(:has([data-testid="stMarkdownContainer"])) { display: none; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-testid="stWidgetLabel"]) p { margin: 0; font-size: 0.95rem; font-weight: 500; color: var(--rail-muted); line-height: 1.3; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-testid="stWidgetLabel"]):hover { background: var(--rail-hover); }
[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-testid="stWidgetLabel"]):hover p { color: var(--rail-ink); }
[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-testid="stWidgetLabel"]):has(input:checked) { background: #c4006a; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-testid="stWidgetLabel"]):has(input:checked) p { color: #ffffff; font-weight: 700; }
__NAV_ICONS__

[data-testid="stSidebar"] [data-testid="stMetric"] { background: transparent; border: 1px solid var(--rail-line); border-radius: 8px; padding: 0.6rem 0.75rem; }
[data-testid="stSidebar"] [data-testid="stMetricLabel"] :is(p, div, span) { color: var(--rail-muted); font-size: 0.8125rem; font-weight: 600; }
[data-testid="stSidebar"] [data-testid="stMetricValue"] { color: var(--rail-ink); font-size: 1.5rem; font-weight: 700; font-variant-numeric: tabular-nums; }
.stApp [data-testid="stSidebar"] .stButton > button { background: transparent; border: 1px solid var(--rail-line); color: var(--rail-ink); }
.stApp [data-testid="stSidebar"] .stButton > button:hover { background: var(--rail-hover); border-color: var(--rail-muted); color: var(--rail-ink); }
.stApp [data-testid="stSidebar"] .stButton > button p { color: var(--rail-ink); }

/* ---------- page head ---------- */
.stApp .page-head { margin: 0 0 1.5rem; }
.stApp .page-head h1 { font-size: 2.125rem; line-height: 1.12; font-weight: 800; margin: 0 0 0.5rem; padding: 0; }
.stApp .page-head p { margin: 0 0 1rem; color: var(--ink-2); font-size: 1.0625rem; max-width: 62ch; }
.stApp .bar { display: flex; width: 112px; height: 4px; }
.stApp .bar i { flex: 1; display: block; }
.stApp .bar i:nth-child(1) { background: var(--cyan); }
.stApp .bar i:nth-child(2) { background: var(--acc); }
.stApp .bar i:nth-child(3) { background: var(--yellow); }
.stApp .bar i:nth-child(4) { background: var(--ink); }

/* ---------- home ---------- */
.stApp .hero { padding: 1.5rem 0 0.5rem; }
.stApp .hero h1 { font-size: clamp(2.25rem, 5vw, 3.5rem); line-height: 1.04; font-weight: 800; letter-spacing: -0.03em; margin: 0 0 1.25rem; padding: 0; }
.stApp .hero .hl { background: var(--yellow); color: #101318; padding: 0 0.12em; -webkit-box-decoration-break: clone; box-decoration-break: clone; }
.stApp .hero p { font-size: 1.1875rem; color: var(--ink-2); max-width: 52ch; margin: 0 0 0.5rem; }
.stApp .hero-links { display: flex; gap: 1.5rem; flex-wrap: wrap; margin-top: 0.25rem; }
.stApp .hero-links a { font-weight: 600; font-size: 0.9375rem; }

.stApp .slip { position: relative; background: var(--surface); border: 1px solid var(--line); padding: 1.5rem 1.5rem 1.25rem; margin: 1.5rem 0.75rem 0.75rem; }
.stApp .slip .cm { position: absolute; width: 14px; height: 14px; border: 0 solid var(--ink); }
.stApp .slip .cm.tl { top: -9px; left: -9px; border-right-width: 1px; border-bottom-width: 1px; }
.stApp .slip .cm.tr { top: -9px; right: -9px; border-left-width: 1px; border-bottom-width: 1px; }
.stApp .slip .cm.bl { bottom: -9px; left: -9px; border-right-width: 1px; border-top-width: 1px; }
.stApp .slip .cm.br { bottom: -9px; right: -9px; border-left-width: 1px; border-top-width: 1px; }
.stApp .slip h2 { font-size: 1.25rem; font-weight: 800; line-height: 1.2; margin: 0 0 1rem; padding: 0; }
.stApp .slip-list { list-style: none; margin: 0; padding: 0; border-top: 2px solid var(--ink); }
.stApp .slip-list li { display: flex; flex-direction: column; gap: 2px; padding: 0.7rem 0; border-bottom: 1px solid var(--line); animation: feed 0.55s cubic-bezier(0.16, 1, 0.3, 1) backwards; animation-delay: calc(var(--i, 0) * 70ms); }
.stApp .slip-list b { font-weight: 700; color: var(--ink); }
.stApp .slip-list span { font-size: 0.875rem; color: var(--ink-2); }
.stApp .slip-foot { margin: 0.9rem 0 0; font-size: 0.8125rem; color: var(--ink-3); }
@keyframes feed { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }

.stApp .about { display: grid; grid-template-columns: auto 1fr; gap: 1.75rem; align-items: start; background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 2rem; margin: 2.5rem 0 0; scroll-margin-top: 80px; }
.stApp .about .mono { width: 72px; height: 72px; background: var(--ink); color: var(--ground); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.5rem; letter-spacing: 0.02em; border-radius: 4px; }
.stApp .about h2 { font-size: 1.5rem; font-weight: 800; margin: 0 0 0.5rem; padding: 0; }
.stApp .about p { color: var(--ink-2); margin: 0.5rem 0; max-width: 68ch; }
.stApp .about p strong { color: var(--ink); }

.stApp .sec-head { margin: 3rem 0 0.75rem; }
.stApp .sec-head h2 { font-size: 1.75rem; font-weight: 800; margin: 0 0 0.35rem; padding: 0; }
.stApp .sec-head p { color: var(--ink-2); margin: 0; }

.stApp [class*="st-key-home_feature_"] { margin-bottom: -1rem; }
.stApp [class*="st-key-home_feature_"] .stButton > button {
    display: flex !important; align-items: center; justify-content: space-between !important; gap: 1rem; width: 100%;
    min-height: 4.25rem; padding: 0.9rem 0.5rem; text-align: left;
    background: transparent; color: var(--ink); border: 0; border-bottom: 1px solid var(--line); border-radius: 0;
}
.stApp [class*="st-key-home_feature_"] .stButton > button > div { flex: 1; width: 100%; justify-content: flex-start; text-align: left; }
.stApp [class*="st-key-home_feature_"] .stButton > button p { margin: 0; text-align: left; color: var(--ink-2); font-size: 0.9375rem; font-weight: 400; }
.stApp [class*="st-key-home_feature_"] .stButton > button strong { display: block; color: var(--ink); font-size: 1.0625rem; font-weight: 700; }
.stApp [class*="st-key-home_feature_"] .stButton > button::after {
    content: ""; flex: none; width: 20px; height: 20px; background-color: var(--ink-3);
    -webkit-mask: var(--ico-arrow) center / contain no-repeat; mask: var(--ico-arrow) center / contain no-repeat;
    transition: transform 0.2s ease, background-color 0.2s ease;
}
.stApp [class*="st-key-home_feature_"] .stButton > button:hover { background: var(--surface-2); }
.stApp [class*="st-key-home_feature_"] .stButton > button:hover::after { background-color: var(--acc-text); transform: translateX(4px); }

.stApp .cta { border-top: 2px solid var(--ink); margin: 3rem 0 0; padding: 1.5rem 0 0; }
.stApp .cta h2 { font-size: 1.75rem; font-weight: 800; margin: 0 0 0.35rem; padding: 0; }
.stApp .cta p { color: var(--ink-2); margin: 0; }
.stApp .support { border-top: 1px solid var(--line); margin: 3rem 0 0; padding: 1.5rem 0 0; scroll-margin-top: 80px; }
.stApp .support h2 { font-size: 1.5rem; font-weight: 800; margin: 0 0 0.5rem; padding: 0; }
.stApp .support p { color: var(--ink-2); max-width: 68ch; margin: 0; }
.stApp .support-note { text-align: center; padding-bottom: 1rem; }
.stApp .support-note p { color: var(--ink-3); font-size: 0.9375rem; margin: 0; }
.stApp [data-testid="stImage"] img { max-width: 260px; margin: 0 auto; display: block; background: #ffffff; padding: 12px; border: 1px solid var(--line); border-radius: 6px; }
.stApp [data-testid="stImageCaption"], .stApp [data-testid="stImageCaption"] * { color: var(--ink-3); text-align: center; }

.stApp .footer { border-top: 1px solid var(--line); padding: 1.5rem 0 0; margin-top: 3rem; display: flex; justify-content: space-between; gap: 0.75rem 1.5rem; flex-wrap: wrap; color: var(--ink-3); font-size: 0.875rem; }
.stApp .footer span { color: var(--ink-3); }
.stApp .footer .links { display: flex; gap: 1.25rem; }
.stApp .footer .links a { color: var(--ink-2); text-decoration: none; }
.stApp .footer .links a:hover { color: var(--acc-text); text-decoration: underline; }

/* ---------- document pages ---------- */
.stApp .incl { background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 1rem 1.1rem; }
.stApp .incl h4 { font-size: 0.9375rem; font-weight: 700; margin: 0 0 0.5rem; padding: 0; color: var(--ink); }
.stApp .incl ul { list-style: none; margin: 0; padding: 0; }
.stApp .incl li { display: flex; align-items: center; gap: 0.6rem; padding: 0.3rem 0; color: var(--ink-2); font-size: 0.9375rem; }
.stApp .incl li::before { content: ""; flex: none; width: 16px; height: 16px; background-color: var(--cyan-text); -webkit-mask: var(--ico-check) center / contain no-repeat; mask: var(--ico-check) center / contain no-repeat; }

.stApp .match { text-align: right; font-size: 1.75rem; font-weight: 800; font-variant-numeric: tabular-nums; line-height: 1; }
.stApp .match span { display: block; font-size: 0.75rem; font-weight: 600; color: var(--ink-3); margin-top: 4px; }
.stApp .match.ok { color: var(--ok); }
.stApp .match.warn { color: var(--warn); }
.stApp .match.bad { color: var(--bad); }

/* ---------- native widgets ---------- */
.stApp [data-testid="stWidgetLabel"] :is(p, label, span) { color: var(--ink); font-weight: 600; font-size: 0.875rem; }
/* Text fields. Written so it does not depend on Streamlit's internal markup (data-baseweb, emotion class names): the
   <input>/<textarea> element ITSELF paints both the box and the text colour, so the two can never end up light-on-light
   or dark-on-dark, whatever Streamlit's own theme paints underneath. */
.stApp :is(input, textarea):not([type="checkbox"]):not([type="radio"]):not([type="range"]):not([role="combobox"]):not([aria-autocomplete]) {
    background: var(--field) !important; color: var(--ink) !important; -webkit-text-fill-color: var(--ink) !important;
    caret-color: var(--acc-text); border: 1px solid var(--line-strong) !important; border-radius: 6px !important;
    box-shadow: none !important; outline: none !important;
}
.stApp :is(input, textarea):not([type="checkbox"]):not([type="radio"]):not([type="range"]):not([role="combobox"]):not([aria-autocomplete]):focus {
    border-color: var(--acc-text) !important; box-shadow: 0 0 0 1px var(--acc-text) !important;
}
.stApp :is(input, textarea):-webkit-autofill { -webkit-box-shadow: 0 0 0 1000px var(--field) inset !important; -webkit-text-fill-color: var(--ink) !important; caret-color: var(--acc-text); }
.stApp :is(input, textarea)::placeholder { color: var(--ink-3) !important; -webkit-text-fill-color: var(--ink-3) !important; opacity: 1; }
/* Whatever Streamlit wraps around a text field (its own box, inner layer, focus ring) is made invisible so only our field shows. */
.stApp :is([data-testid="stTextInput"], [data-testid="stTextArea"], [data-testid="stNumberInput"]) :is(div, span):has(> :is(input, textarea)),
.stApp :is([data-testid="stTextInput"], [data-testid="stTextArea"], [data-testid="stNumberInput"]) :is(div, span):has(> :is(div, span) > :is(input, textarea)) {
    background: transparent !important; border-color: transparent !important; box-shadow: none !important;
}
/* Selectbox: the control (the box after the label) is repainted as one piece, box and text together. If the markup is
   not recognised nothing here matches and Streamlit's own selectbox stays fully native and readable. */
.stApp [data-testid="stSelectbox"] label ~ div { background: var(--field) !important; border: 1px solid var(--line-strong) !important; border-radius: 6px !important; }
.stApp [data-testid="stSelectbox"] label ~ div :is(div, span, input, p) { background: transparent !important; color: var(--ink) !important; -webkit-text-fill-color: var(--ink) !important; border-color: transparent !important; box-shadow: none !important; }
.stApp [data-testid="stSelectbox"] label ~ div svg { fill: var(--ink-2) !important; color: var(--ink-2) !important; }
/* Dropdown list: one dark panel, every layer inside transparent, every text ink-coloured, so no layer can be light-on-light. */
div[data-baseweb="popover"], div[data-baseweb="popover"] > div { background: var(--surface) !important; }
div[data-baseweb="popover"] * { background: transparent !important; color: var(--ink) !important; -webkit-text-fill-color: var(--ink) !important; }
div[data-baseweb="popover"] :is(li, [role="option"]):is(:hover, [aria-selected="true"]) { background: var(--surface-2) !important; }

.stApp :is(.stButton, .stDownloadButton) > button {
    min-height: 2.75rem; border-radius: 6px; font-weight: 600; box-shadow: none;
    background: transparent; color: var(--ink); border: 1px solid var(--ink);
    transition: background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease;
}
.stApp :is(.stButton, .stDownloadButton) > button p { color: inherit; font-weight: 600; margin: 0; }
.stApp :is(.stButton, .stDownloadButton) > button:hover { background: var(--surface-2); border-color: var(--ink); color: var(--ink); }
.stApp :is(.stButton, .stDownloadButton) > button:disabled { opacity: 0.5; cursor: not-allowed; }
.stApp :is(.stButton, .stDownloadButton) > button:is([kind="primary"], [data-testid="stBaseButton-primary"], [data-testid="baseButton-primary"]) {
    background: var(--acc); color: var(--on-acc); border-color: var(--acc);
}
.stApp :is(.stButton, .stDownloadButton) > button:is([kind="primary"], [data-testid="stBaseButton-primary"], [data-testid="baseButton-primary"]):hover {
    background: var(--acc-hover); border-color: var(--acc-hover); color: var(--on-acc);
}
.stApp .stDownloadButton > button { background: var(--ink); color: var(--ground); border-color: var(--ink); }
.stApp .stDownloadButton > button:hover { background: var(--ink-2); border-color: var(--ink-2); color: var(--ground); }
.stApp [class*="st-key-home_get_started"] button, .stApp [class*="st-key-cta_start_building"] button { min-height: 3.25rem; padding: 0 1.75rem; font-size: 1.0625rem; }
.stApp [class*="st-key-improve_"] button { min-height: 2.5rem; background: var(--cyan-tint); border-color: var(--cyan-text); color: var(--cyan-text); gap: 0.4rem; }
.stApp [class*="st-key-improve_"] button p { color: var(--cyan-text); }
.stApp [class*="st-key-improve_"] button::before { content: ""; width: 16px; height: 16px; background-color: var(--cyan-text); -webkit-mask: var(--ico-spark) center / contain no-repeat; mask: var(--ico-spark) center / contain no-repeat; }
.stApp [class*="st-key-improve_"] button:hover { background: var(--cyan); border-color: var(--cyan); color: #101318; }
.stApp [class*="st-key-improve_"] button:hover p { color: #101318; }
.stApp [class*="st-key-improve_"] button:hover::before { background-color: #101318; }
.stApp [class*="st-key-rm_"] button { min-height: 2.25rem; padding: 0.25rem 0.6rem; background: var(--cyan-tint); border-color: transparent; color: var(--cyan-text); font-size: 0.875rem; }
.stApp [class*="st-key-rm_"] button p { color: var(--cyan-text); font-size: 0.875rem; }
.stApp [class*="st-key-rm_"] button:hover { background: var(--cyan); color: #101318; }
.stApp [class*="st-key-rm_"] button:hover p { color: #101318; }

/* Tabs, matched by ARIA role (stable across Streamlit versions) rather than internal attributes. */
.stApp [role="tablist"] { gap: 0.25rem; }
.stApp [role="tab"] { background: transparent !important; padding: 0.75rem 1rem; }
.stApp [role="tab"], .stApp [role="tab"] :is(p, span, div) { color: var(--ink-2) !important; font-weight: 600; }
.stApp [role="tab"]:hover, .stApp [role="tab"]:hover :is(p, span, div) { color: var(--ink) !important; }
.stApp [role="tab"][aria-selected="true"], .stApp [role="tab"][aria-selected="true"] :is(p, span, div) { color: var(--ink) !important; }
/* the moving underline and the rule under the tab row: found by position because their class names vary */
.stApp :is([data-baseweb="tab-highlight"], [role="tablist"] > :not([role="tab"]):nth-last-child(2)) { background: var(--acc) !important; height: 3px !important; }
.stApp :is([data-baseweb="tab-border"], [role="tablist"] > :not([role="tab"]):last-child) { background: var(--line) !important; }

.stApp [data-testid="stExpander"] { margin-bottom: 0.5rem; }
.stApp [data-testid="stExpander"] details { background: var(--surface); border: 1px solid var(--line); border-radius: 8px; }
.stApp [data-testid="stExpander"] summary { padding: 0.85rem 1rem; color: var(--ink); }
.stApp [data-testid="stExpander"] summary p { font-weight: 700; color: var(--ink); }
.stApp [data-testid="stExpander"] summary:hover p { color: var(--acc-text); }

.stApp [data-testid="stAlert"] > div { background: var(--surface) !important; border: 1px solid var(--line-strong); border-radius: 6px; color: var(--ink) !important; }
.stApp [data-testid="stAlert"] :is(p, div, span) { color: var(--ink); }
.stApp [data-testid="stAlert"]:has([data-testid="stAlertContentError"]) > div { background: color-mix(in srgb, var(--bad) 9%, var(--surface)) !important; border-color: var(--bad); }
.stApp [data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) > div { background: color-mix(in srgb, var(--warn) 10%, var(--surface)) !important; border-color: var(--warn); }
.stApp [data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]) > div { background: color-mix(in srgb, var(--ok) 9%, var(--surface)) !important; border-color: var(--ok); }
.stApp [data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]) > div { background: var(--cyan-tint) !important; border-color: var(--cyan-text); }

.stApp [data-testid="stMain"] [data-testid="stMetric"] { background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 0.75rem 1rem; }
.stApp [data-testid="stMain"] [data-testid="stMetricLabel"] :is(p, div, span) { color: var(--ink-2); font-size: 0.8125rem; font-weight: 600; }
.stApp [data-testid="stMain"] [data-testid="stMetricValue"] { color: var(--ink); font-weight: 700; font-variant-numeric: tabular-nums; }

.stApp [data-testid="stChatMessage"] { background: var(--surface); border: 1px solid var(--line); border-radius: 8px; }
.stApp [data-testid="stChatInput"] { border-radius: 6px; }

/* floating assistant panel (only shown when show_chat is turned on) */
.stApp .chat-float { position: fixed; bottom: 90px; right: 20px; width: 380px; max-width: 90vw; max-height: 70vh; background: var(--surface); border: 1px solid var(--line-strong); border-radius: 8px; z-index: 999; display: none; flex-direction: column; overflow: hidden; }
.stApp .chat-float.open { display: flex; }
.stApp .chat-float .chat-header { padding: 0.8rem 1.2rem; background: var(--ink); color: var(--ground); font-weight: 700; display: flex; justify-content: space-between; align-items: center; flex-shrink: 0; }
.stApp .chat-float .chat-header button { background: none; border: none; color: var(--ground); font-size: 1.2rem; cursor: pointer; }
.stApp .chat-float .chat-body { flex: 1; overflow-y: auto; padding: 1rem; display: flex; flex-direction: column; gap: 0.5rem; }

/* ================= iOS liquid glass layer ================= */
/* Frosted panels. Placed after the component rules so they win at equal
   specificity. Pure paint: no widget behaviour is touched. */
.stApp .slip,
.stApp .about,
.stApp .incl,
.stApp [data-testid="stMain"] [data-testid="stMetric"],
.stApp [data-testid="stExpander"] details,
.stApp [data-testid="stAlert"] > div,
.stApp [data-testid="stChatMessage"] {
    background: var(--glass-bg) !important;
    -webkit-backdrop-filter: blur(22px) saturate(180%);
    backdrop-filter: blur(22px) saturate(180%);
    border: 1px solid var(--glass-border) !important;
    border-radius: 18px !important;
    box-shadow: var(--glass-shadow), inset 0 1px 0 var(--glass-edge);
}

/* Slip registration marks stay legible on glass. */
.stApp .slip .cm { border-color: color-mix(in srgb, var(--ink) 42%, transparent); }

/* Sidebar metric chips: darker glass so rail text stays readable. */
[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: rgba(255,255,255,0.06) !important;
    -webkit-backdrop-filter: blur(16px) saturate(160%);
    backdrop-filter: blur(16px) saturate(160%);
    border: 1px solid var(--glass-border) !important;
    border-radius: 14px !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.12);
}

/* Fields: the element itself paints box + text, so glass can't create a
   light-on-light (or dark-on-dark) pair. */
.stApp :is(input, textarea):not([type="checkbox"]):not([type="radio"]):not([type="range"]):not([role="combobox"]):not([aria-autocomplete]) {
    background: var(--glass-field) !important;
    -webkit-backdrop-filter: blur(14px) saturate(160%);
    backdrop-filter: blur(14px) saturate(160%);
    border: 1px solid var(--glass-border) !important;
    border-radius: 14px !important;
    box-shadow: inset 0 1px 0 var(--glass-edge);
}
.stApp :is(input, textarea):not([type="checkbox"]):not([type="radio"]):not([type="range"]):not([role="combobox"]):not([aria-autocomplete]):focus {
    border-color: var(--acc-text) !important;
    box-shadow: 0 0 0 3px color-mix(in srgb, var(--acc-text) 26%, transparent), inset 0 1px 0 var(--glass-edge) !important;
}
.stApp :is(input, textarea):-webkit-autofill {
    -webkit-box-shadow: 0 0 0 1000px var(--glass-field) inset !important;
    -webkit-text-fill-color: var(--ink) !important;
}

/* Selectbox control + dropdown as one glass piece. */
.stApp [data-testid="stSelectbox"] label ~ div {
    background: var(--glass-field) !important;
    -webkit-backdrop-filter: blur(14px) saturate(160%);
    backdrop-filter: blur(14px) saturate(160%);
    border: 1px solid var(--glass-border) !important;
    border-radius: 14px !important;
    box-shadow: inset 0 1px 0 var(--glass-edge);
}
div[data-baseweb="popover"], div[data-baseweb="popover"] > div {
    background: var(--glass-bg) !important;
    -webkit-backdrop-filter: blur(24px) saturate(180%);
    backdrop-filter: blur(24px) saturate(180%);
    border: 1px solid var(--glass-border) !important;
    border-radius: 16px !important;
    box-shadow: var(--glass-shadow) !important;
}

/* Buttons: soft glass pills. Feature rows keep their list design. */
.stApp :is(.stButton, .stDownloadButton) > button {
    border-radius: 999px;
    -webkit-backdrop-filter: blur(18px) saturate(160%);
    backdrop-filter: blur(18px) saturate(160%);
    box-shadow: inset 0 1px 0 var(--glass-edge), 0 4px 14px rgba(0,0,0,0.08);
}
.stApp [class*="st-key-home_feature_"] .stButton > button {
    -webkit-backdrop-filter: none;
    backdrop-filter: none;
    box-shadow: none;
}
.stApp :is(.stButton, .stDownloadButton) > button:is([kind="primary"], [data-testid="stBaseButton-primary"], [data-testid="baseButton-primary"]) {
    background: color-mix(in srgb, var(--acc) 88%, transparent) !important;
    border-color: color-mix(in srgb, var(--acc) 58%, white) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.45), 0 10px 26px color-mix(in srgb, var(--acc) 36%, transparent) !important;
}
.stApp .stDownloadButton > button {
    background: var(--glass-ink) !important;
    color: var(--ground) !important;
    border-color: transparent !important;
}
.stApp .stDownloadButton > button:hover {
    background: color-mix(in srgb, var(--ink) 88%, transparent) !important;
    color: var(--ground) !important;
}

/* Tabs become an iOS-style segmented glass control. */
.stApp [role="tablist"] {
    background: var(--glass-bg-2) !important;
    -webkit-backdrop-filter: blur(18px) saturate(180%);
    backdrop-filter: blur(18px) saturate(180%);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 0.3rem;
    gap: 0.3rem !important;
}
.stApp [role="tab"] { border-radius: 12px; }
.stApp [role="tab"][aria-selected="true"] {
    background: var(--glass-pill) !important;
    box-shadow: inset 0 1px 0 var(--glass-edge), 0 3px 10px rgba(0,0,0,0.14);
}
.stApp :is([data-baseweb="tab-highlight"], [role="tablist"] > :not([role="tab"]):nth-last-child(2)) {
    background: transparent !important;
    height: 0 !important;
}
.stApp :is([data-baseweb="tab-border"], [role="tablist"] > :not([role="tab"]):last-child) {
    background: transparent !important;
}

/* Floating assistant panel. */
.stApp .chat-float {
    background: var(--glass-bg) !important;
    -webkit-backdrop-filter: blur(26px) saturate(180%);
    backdrop-filter: blur(26px) saturate(180%);
    border: 1px solid var(--glass-border) !important;
    border-radius: 20px !important;
    box-shadow: var(--glass-shadow), inset 0 1px 0 var(--glass-edge);
}
.stApp .chat-float .chat-header {
    background: color-mix(in srgb, var(--ink) 72%, transparent) !important;
    -webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);
}

@media (max-width: 768px) {
    .stApp .about { grid-template-columns: 1fr; padding: 1.25rem; }
    .stApp .slip { margin: 1.25rem 0.5rem 0.5rem; }
    .stApp .page-head h1 { font-size: 1.75rem; }
    .stApp .footer { flex-direction: column; }
    .stApp .chat-float { width: 90vw; right: 5vw; }
}
@media (prefers-reduced-motion: reduce) {
    .stApp .slip-list li { animation: none; }
    .stApp * { transition-duration: 0.01ms !important; scroll-behavior: auto !important; }
}
</style>
"""

st.markdown(
    _CSS_BASE.replace("__VARS__", _THEMES[st.session_state.ui_theme])
    .replace("__ICO_CHECK__", _icon_uri(_ICON_CHECK))
    .replace("__ICO_ARROW__", _icon_uri(_ICON_ARROW))
    .replace("__ICO_SPARK__", _icon_uri(_ICON_SPARK))
    .replace("__NAV_ICONS__", _nav_icon_css()),
    unsafe_allow_html=True,
)


def _included(title, items):
    """Small 'what's in this document' checklist shown beside each form."""
    lis = "".join("<li>%s</li>" % item for item in items)
    return '<div class="incl"><h4>%s</h4><ul>%s</ul></div>' % (title, lis)


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
if "pending_improve_exp" not in st.session_state:
    st.session_state.pending_improve_exp = None
if "pending_improve_summary" not in st.session_state:
    st.session_state.pending_improve_summary = None

# ---- Page navigation helper ----
def go_to_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# ---- Safe AI response helper ----
def safe_ai_response(response, fallback=None):
    if response is None:
        return fallback
    if not isinstance(response, str):
        return fallback
    error_indicators = ["error", "failed", "⚠️", "unavailable", "timeout", "rate limit"]
    if any(indicator in response.lower() for indicator in error_indicators):
        return fallback
    return response

# ---- Sidebar Navigation ----
with st.sidebar:
    st.markdown("""
<div class="brand">
<svg width="30" height="34" viewBox="0 0 30 34" fill="none" aria-hidden="true"><path d="M3 1.5h15l9 9V32.5H3z" stroke="#f2f4f7" stroke-width="1.75" stroke-linejoin="round"/><path d="M18 1.5v9h9" stroke="#f2f4f7" stroke-width="1.75" stroke-linejoin="round"/><rect x="7" y="24" width="4" height="4" fill="#00b4d8"/><rect x="12" y="24" width="4" height="4" fill="#ff4fa0"/><rect x="17" y="24" width="4" height="4" fill="#ffd60a"/><rect x="22" y="24" width="2" height="4" fill="#f2f4f7"/></svg>
<div><div class="brand-name">DocForge</div><div class="brand-sub">Professional Documents</div></div>
</div>
""", unsafe_allow_html=True)
    st.markdown("---")

    page_choices = ["Home", "Builder", "Resume", "CV", "Cover Letter", "Proposal", "Experience", "Job Scraper", "AI Assistant"]
    page_map = {
        "Home": "Home",
        "Builder": "Builder",
        "Resume": "Resume",
        "CV": "CV",
        "Cover Letter": "CoverLetter",
        "Proposal": "Proposal",
        "Experience": "Experience",
        "Job Scraper": "JobScraper",
        "AI Assistant": "AIAssistant"
    }

    # Navigation fix: the radio now has a fixed key, so Streamlit no longer treats it as a brand-new widget (and drops
    # the click) every time the page changes. A click updates the page through the callback; when the page was changed
    # by go_to_page() (the Home cards), the radio is brought in line before it is drawn.
    def _on_nav_change():
        st.session_state.page = page_map[st.session_state.nav_radio]

    _page_labels = {v: k for k, v in page_map.items()}
    if st.session_state.get("nav_radio") != _page_labels.get(st.session_state.page):
        st.session_state.nav_radio = _page_labels.get(st.session_state.page, "Home")

    selected = st.radio(
        "Navigate",
        page_choices,
        key="nav_radio",
        on_change=_on_nav_change,
        label_visibility="collapsed"
    )
    if selected:
        st.session_state.page = page_map[selected]

    st.markdown("---")
    col1, col2 = st.columns(2)
    col1.metric("Skills", len(st.session_state.skills))
    col2.metric("Jobs", len(st.session_state.jobs))
    st.caption("Streamlit · ReportLab")

    st.markdown("---")
    _is_dark = st.session_state.ui_theme == "dark"
    if st.button("Switch to light mode" if _is_dark else "Switch to dark mode", key="ui_theme_toggle", use_container_width=True):
        st.session_state.ui_theme = "light" if _is_dark else "dark"
        st.rerun()

# ---- Determine current page ----
page = st.session_state.page

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
        "add_exp": st.session_state.get("f_add_exp", ""),
        "degree": st.session_state.get("f_degree", ""),
        "institution": st.session_state.get("f_inst", ""),
        "year": st.session_state.get("f_year", ""),
        "projects": st.session_state.get("f_projects", ""),
        "summary": st.session_state.get("f_summary", ""),
        "languages": st.session_state.get("f_languages", ""),
        "certifications": st.session_state.get("f_certs", ""),
        "theme": "Classic Green",
    }

# ---- Function to render the common info fields (used on each document page) ----
def render_common_info():
    """Render collapsible common information fields."""
    with st.expander("Your Information (edit here)", expanded=False):
        st.markdown("Fill in your details. These will be used for all documents.")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Full Name *", key="f_name", placeholder="John Doe")
            st.text_input("Email *", key="f_email", placeholder="john@example.com")
            st.text_input("Phone", key="f_phone", placeholder="+1 234 567 890")
        with col2:
            st.text_input("Professional Title", key="f_title", placeholder="Software Engineer")
            st.text_input("Location", key="f_loc", placeholder="San Francisco, CA")
            st.text_input("LinkedIn URL", key="f_linkedin", placeholder="linkedin.com/in/john")

        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Company", key="f_company", placeholder="Tech Corp")
            st.text_input("Role", key="f_exp_role", placeholder="Senior Developer")
            st.text_input("Duration", key="f_duration", placeholder="Jan 2020 – Present")
        with col2:
            st.text_area("Job Description", key="f_exp_desc", placeholder="• Built REST APIs serving 10k users/day\n• Led team of 5 developers", height=120)
            col_ai1, col_ai2 = st.columns([4, 1])
            with col_ai2:
                if st.button("Improve", key="improve_exp_common"):
                    try:
                        improved = ai_suggest_improvements("job description", st.session_state.f_exp_desc)
                        valid = safe_ai_response(improved)
                        if valid is not None:
                            st.session_state.pending_improve_exp = valid
                            st.rerun()
                        else:
                            st.warning("AI suggestion failed.")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("Degree", key="f_degree", placeholder="B.Tech Computer Science")
        with col2:
            st.text_input("Institution", key="f_inst", placeholder="Stanford University")
        with col3:
            st.text_input("Year", key="f_year", placeholder="2016 – 2020")

        st.text_area("Professional Summary", key="f_summary", placeholder="Experienced software engineer with 5+ years...", height=100)
        col_ai1, col_ai2 = st.columns([4, 1])
        with col_ai2:
            if st.button("Improve", key="improve_summary_common"):
                try:
                    improved = ai_suggest_improvements("professional summary", st.session_state.f_summary)
                    valid = safe_ai_response(improved)
                    if valid is not None:
                        st.session_state.pending_improve_summary = valid
                        st.rerun()
                    else:
                        st.warning("AI suggestion failed.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

        st.text_area("Projects (one per line)", key="f_projects", placeholder="ResumeForge — AI resume builder\nTaskBot — Slack automation", height=100)

        # Skills management
        col1, col2 = st.columns([3, 1])
        with col1:
            new_skill = st.text_input("Add a skill", key="skill_input_common", placeholder="Python, React, SQL...")
        with col2:
            if st.button("Add", use_container_width=True) and new_skill.strip():
                s = new_skill.strip().lower()
                if s not in st.session_state.skills:
                    st.session_state.skills.append(s)
                st.rerun()

        if st.session_state.skills:
            st.markdown("**Your Skills:**")
            cols = st.columns(6)
            for i, sk in enumerate(st.session_state.skills):
                with cols[i % 6]:
                    if st.button(f"✕ {sk.title()}", key=f"rm_{sk}_common"):
                        st.session_state.skills.remove(sk)
                        st.rerun()
        else:
            st.info("No skills added yet.")

        if st.button("Save Information", type="primary", use_container_width=True):
            st.success("Information saved!")

# ---- PAGES ----

if page == "AIAssistant":
    st.markdown("""
<style>
.stApp [data-testid="stMain"] .stButton > button:not([kind="primary"]):not([data-testid="stBaseButton-primary"]) { background: var(--cyan-tint); border-color: var(--cyan-text); color: var(--cyan-text); }
.stApp [data-testid="stMain"] .stButton > button:not([kind="primary"]):not([data-testid="stBaseButton-primary"]):hover { background: var(--cyan); border-color: var(--cyan); color: #101318; }
</style>
""", unsafe_allow_html=True)

if page == "Home":
    hero_left, hero_right = st.columns([3, 2], gap="large")
    with hero_left:
        st.markdown("""
<div class="hero">
<h1>Create <span class="hl">Professional Documents</span> Instantly</h1>
<p>Build resumes, CVs, cover letters, proposals, and experience letters – all from one platform. No design skills needed.</p>
</div>
""", unsafe_allow_html=True)

        if st.button("Get Started Free", key="home_get_started", use_container_width=False, type="primary"):
            go_to_page("Builder")

        st.markdown("""
<div class="hero-links">
<a href="#about">Learn More</a>
<a href="#support-section">Support Me</a>
</div>
""", unsafe_allow_html=True)

    with hero_right:
        st.markdown("""
<div class="slip">
<i class="cm tl"></i><i class="cm tr"></i><i class="cm bl"></i><i class="cm br"></i>
<h2>Five documents, one set of details</h2>
<ul class="slip-list">
<li style="--i:0"><b>Resume</b><span>ATS-friendly, with multiple themes</span></li>
<li style="--i:1"><b>CV</b><span>Curriculum vitae with publications</span></li>
<li style="--i:2"><b>Cover Letter</b><span>Personalized for each application</span></li>
<li style="--i:3"><b>Proposal</b><span>Project proposals for clients</span></li>
<li style="--i:4"><b>Experience Letter</b><span>Employment verification</span></li>
</ul>
<p class="slip-foot">PDF themes: Classic Green · Corporate Blue · Creative Purple</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="about" id="about">
<div class="mono" aria-hidden="true">RP</div>
<div class="about-text">
<h2>About Me</h2>
<p><strong>Rudraksh Panwar</strong><br>B.Sc Computer Science student at <strong>IIMT College of Science and Technology</strong>.</p>
<p><strong>Skills:</strong> MySQL, Python<br><strong>Currently learning:</strong> GUI Development, Operating System concepts.</p>
<p>I built DocForge as a project to help students and professionals create polished documents effortlessly. Passionate about technology, coding, and building things that make life easier.</p>
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="sec-head">
<h2>Everything You Need</h2>
<p>Click any row to jump directly to that tool.</p>
</div>
""", unsafe_allow_html=True)

    features = [
        ("Resume Builder", "ATS-friendly resumes with multiple themes.", "Resume"),
        ("CV Generator", "Comprehensive curriculum vitae with publications.", "CV"),
        ("Cover Letters", "Personalized letters for job applications.", "CoverLetter"),
        ("Proposal Generator", "Professional project proposals for clients.", "Proposal"),
        ("Experience Letters", "Employment verification letters.", "Experience"),
        ("Job Scraper", "Find jobs and match your skills.", "JobScraper"),
        ("AI Assistant", "Get AI-powered suggestions and help.", "AIAssistant"),
    ]

    for title, desc, page_key in features:
        if st.button(
            f"**{title}**\n\n{desc}",
            key=f"home_feature_{page_key}",
            use_container_width=True,
            type="secondary",
        ):
            go_to_page(page_key)

    st.markdown("""
<div class="cta">
<h2>Ready to Build Your Document?</h2>
<p>Get started now – it's free and takes less than 5 minutes.</p>
</div>
""", unsafe_allow_html=True)

    if st.button("Start Building", key="cta_start_building", use_container_width=False, type="primary"):
        go_to_page("Builder")

    # Support section
    st.markdown("""
<div class="support" id="support-section">
<h2>Support the Developer</h2>
<p>If DocForge has helped you create professional documents, consider supporting my work. Every contribution, no matter how small, helps me keep building free tools for students and professionals like you. Your support fuels my passion to create more useful tools and improve existing ones.</p>
</div>
""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
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
<div class="support-note">
<p>Scan the QR code with your UPI app to send a payment. Every contribution counts – thank you!</p>
</div>
""", unsafe_allow_html=True)

# ---- BUILDER (kept for users who prefer a dedicated page) ----
elif page == "Builder":
    st.markdown("""
<div class="page-head">
<h1>Document Builder</h1>
<p>Fill your information once. All documents will use this data.</p>
<div class="bar"><i></i><i></i><i></i><i></i></div>
</div>
""", unsafe_allow_html=True)

    # Apply pending improvements
    if st.session_state.pending_improve_exp is not None:
        st.session_state.f_exp_desc = st.session_state.pending_improve_exp
        st.session_state.pending_improve_exp = None
    if st.session_state.pending_improve_summary is not None:
        st.session_state.f_summary = st.session_state.pending_improve_summary
        st.session_state.pending_improve_summary = None

    tabs = st.tabs(["Personal", "Experience", "Education", "Skills", "Extra"])

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
            if st.button("Improve", key="improve_exp"):
                try:
                    improved = ai_suggest_improvements("job description", st.session_state.f_exp_desc)
                    valid = safe_ai_response(improved)
                    if valid is not None:
                        st.session_state.pending_improve_exp = valid
                        st.rerun()
                    else:
                        st.warning("AI suggestion returned an error.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

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
            if st.button("Add", use_container_width=True) and new_skill.strip():
                s = new_skill.strip().lower()
                if s not in st.session_state.skills:
                    st.session_state.skills.append(s)
                st.rerun()

        job_title_for_skills = st.text_input("Job Title for Skill Suggestions", placeholder="e.g., Data Scientist")
        if st.button("Suggest Skills") and job_title_for_skills:
            try:
                suggested = ai_autofill_skills(job_title_for_skills)
                valid = safe_ai_response(suggested)
                if valid is not None:
                    skills_list = [s.strip().lower() for s in valid.split(',') if s.strip()]
                    for sk in skills_list:
                        if sk not in st.session_state.skills:
                            st.session_state.skills.append(sk)
                    st.rerun()
                else:
                    st.warning("Could not get skill suggestions.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

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
        col_ai1, col_ai2 = st.columns([4, 1])
        with col_ai2:
            if st.button("Improve", key="improve_summary"):
                try:
                    improved = ai_suggest_improvements("professional summary", st.session_state.f_summary)
                    valid = safe_ai_response(improved)
                    if valid is not None:
                        st.session_state.pending_improve_summary = valid
                        st.rerun()
                    else:
                        st.warning("AI suggestion returned an error.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    if st.button("Save Information", type="primary", use_container_width=True):
        st.success("All information saved!")

# ---- RESUME ----
elif page == "Resume":
    st.markdown("""
<div class="page-head">
<h1>Resume Generator</h1>
<p>Create an ATS-optimized professional resume.</p>
<div class="bar"><i></i><i></i><i></i><i></i></div>
</div>
""", unsafe_allow_html=True)

    # Common info section
    render_common_info()

    col1, col2 = st.columns([2, 1])
    with col1:
        theme = st.selectbox("PDF theme", ["Classic Green", "Corporate Blue", "Creative Purple"], key="resume_theme")
        summary = st.text_area("Professional Summary", key="resume_summary", placeholder="Write a brief summary...", height=100)
    with col2:
        st.markdown(_included("Preview Sections", ["Personal Info", "Summary", "Skills", "Experience", "Education", "Projects"]), unsafe_allow_html=True)

    if st.button("Generate Resume PDF", type="primary", use_container_width=True):
        name = st.session_state.get("f_name", "").strip()
        if not name:
            st.error("Please fill in your Full Name in the 'Your Information' section above.")
        else:
            data = get_user_data()
            data["summary"] = st.session_state.get("resume_summary", "")
            data["theme"] = st.session_state.get("resume_theme", "Classic Green")
            pdf = generate_resume_pdf(data)
            if pdf:
                st.download_button(
                    label="Download PDF",
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
<div class="page-head">
<h1>CV Generator</h1>
<p>Create a comprehensive curriculum vitae.</p>
<div class="bar"><i></i><i></i><i></i><i></i></div>
</div>
""", unsafe_allow_html=True)

    render_common_info()

    col1, col2 = st.columns([2, 1])
    with col1:
        cv_theme = st.selectbox("PDF theme", ["Classic Green", "Corporate Blue", "Creative Purple"], key="cv_theme")
        publications = st.text_area("Publications (one per line)", key="cv_publications", placeholder="• Smith, J. (2023). 'AI in Healthcare.' Journal of AI, 12(3), 45-67.", height=80)
    with col2:
        st.markdown(_included("CV Sections", ["Personal Info", "Summary", "Skills", "Experience", "Education", "Publications", "Projects"]), unsafe_allow_html=True)

    if st.button("Generate CV PDF", type="primary", use_container_width=True):
        name = st.session_state.get("f_name", "").strip()
        if not name:
            st.error("Please fill in your Full Name above.")
        else:
            data = get_user_data()
            data["publications"] = st.session_state.get("cv_publications", "")
            data["theme"] = st.session_state.get("cv_theme", "Classic Green")
            pdf = generate_cv_pdf(data)
            if pdf:
                st.download_button(
                    label="Download PDF",
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
<div class="page-head">
<h1>Cover Letter Generator</h1>
<p>Personalized cover letters for job applications.</p>
<div class="bar"><i></i><i></i><i></i><i></i></div>
</div>
""", unsafe_allow_html=True)

    render_common_info()

    col1, col2 = st.columns([2, 1])
    with col1:
        col_a, col_b = st.columns(2)
        with col_a:
            cover_company = st.text_input("Company Name *", key="cover_company", placeholder="Google")
            cover_position = st.text_input("Position *", key="cover_position", placeholder="Software Engineer")
        with col_b:
            cover_recruiter = st.text_input("Recruiter Name", key="cover_recruiter", placeholder="Sarah Johnson")
        cover_custom = st.text_area("Additional Message (optional)", key="cover_custom", placeholder="Why you're interested, specific achievements...", height=100)
        cover_theme = st.selectbox("PDF theme", ["Classic Green", "Corporate Blue", "Creative Purple"], key="cover_theme")
    with col2:
        st.markdown(_included("Letter Structure", ["Sender Info", "Date", "Recipient", "Salutation", "Body", "Closing", "Signature"]), unsafe_allow_html=True)

    if st.button("Generate Cover Letter PDF", type="primary", use_container_width=True):
        name = st.session_state.get("f_name", "").strip()
        if not name:
            st.error("Please fill in your Full Name above.")
        else:
            data = get_user_data()
            data["cover_company"] = st.session_state.get("cover_company", "")
            data["cover_position"] = st.session_state.get("cover_position", "")
            data["cover_recruiter"] = st.session_state.get("cover_recruiter", "")
            data["cover_custom"] = st.session_state.get("cover_custom", "")
            data["theme"] = st.session_state.get("cover_theme", "Classic Green")
            pdf = generate_cover_letter_pdf(data)
            if pdf:
                st.download_button(
                    label="Download PDF",
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
<div class="page-head">
<h1>Proposal Generator</h1>
<p>Professional project proposals for clients.</p>
<div class="bar"><i></i><i></i><i></i><i></i></div>
</div>
""", unsafe_allow_html=True)

    render_common_info()

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
        proposal_theme = st.selectbox("PDF theme", ["Classic Green", "Corporate Blue", "Creative Purple"], key="prop_theme")
    with col2:
        st.markdown(_included("Proposal Sections", ["Title", "Client Info", "Executive Summary", "Approach", "About Us", "Contact"]), unsafe_allow_html=True)

    if st.button("Generate Proposal PDF", type="primary", use_container_width=True):
        name = st.session_state.get("f_name", "").strip()
        if not name:
            st.error("Please fill in your Full Name above.")
        else:
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
                    label="Download PDF",
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
<div class="page-head">
<h1>Experience Letter Generator</h1>
<p>Employment verification letters.</p>
<div class="bar"><i></i><i></i><i></i><i></i></div>
</div>
""", unsafe_allow_html=True)

    render_common_info()

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
        exp_theme = st.selectbox("PDF theme", ["Classic Green", "Corporate Blue", "Creative Purple"], key="exp_theme")
    with col2:
        st.markdown(_included("Letter Sections", ["Company Header", "Date", "Subject", "Employee Details", "Performance Remarks", "Issuer Info"]), unsafe_allow_html=True)

    if st.button("Generate Experience Letter PDF", type="primary", use_container_width=True):
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
                label="Download PDF",
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
<div class="page-head">
<h1>Job Scraper</h1>
<p>Find jobs and match your skills.</p>
<div class="bar"><i></i><i></i><i></i><i></i></div>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        role = st.text_input("Job Role", value="Python Developer")
        source = st.selectbox("Source", ["RemoteOK (live)", "Simulated"])
        if st.button("Scrape Jobs", type="primary", use_container_width=True):
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
        st.subheader("Job Listings")
        for job in st.session_state.jobs[:10]:
            with st.container():
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"**{job['title']}**")
                    st.markdown(f"{job['company']} · {job['loc']} · {job['type']}")
                with col_b:
                    tone = "ok" if job["match"] >= 70 else "warn" if job["match"] >= 40 else "bad"
                    st.markdown(f"<div class='match {tone}'>{job['match']}%<span>match</span></div>", unsafe_allow_html=True)
                st.markdown("---")
    else:
        st.info("No jobs found. Click 'Scrape Jobs' to search.")

# ---- AI ASSISTANT ----
elif page == "AIAssistant":
    st.markdown("""
<div class="page-head">
<h1>AI Document Assistant</h1>
<p>Get AI‑powered suggestions to improve your documents and career content.</p>
<div class="bar"><i></i><i></i><i></i><i></i></div>
</div>
""", unsafe_allow_html=True)

    tab_ai = st.tabs(["Improve Text", "Generate Summary", "Suggest Skills", "Cover Letter"])

    with tab_ai[0]:
        text_to_improve = st.text_area("Paste text to improve", height=150)
        if st.button("Improve Text"):
            if text_to_improve:
                improved = ai_suggest_improvements("text", text_to_improve)
                valid = safe_ai_response(improved)
                if valid is not None:
                    st.markdown("### Improved Version")
                    st.write(valid)
                else:
                    st.warning("AI suggestion returned an error. Please try again.")
            else:
                st.warning("Please enter some text.")

    with tab_ai[1]:
        if st.button("Generate Professional Summary"):
            skills = ", ".join(st.session_state.skills)
            experience = st.session_state.get("f_exp_desc", "")
            name = st.session_state.get("f_name", "Candidate")
            title = st.session_state.get("f_title", "Professional")
            summary = ai_generate_summary(name, title, skills, experience)
            valid = safe_ai_response(summary)
            if valid is not None:
                st.markdown("### Generated Summary")
                st.write(valid)
                if st.button("Use This Summary"):
                    st.session_state.f_summary = valid
                    st.rerun()
            else:
                st.warning("Could not generate summary. Please try again.")

    with tab_ai[2]:
        job_title = st.text_input("Job Title", placeholder="e.g., Data Scientist")
        if st.button("Suggest Skills"):
            if job_title:
                skills = ai_autofill_skills(job_title)
                valid = safe_ai_response(skills)
                if valid is not None:
                    st.markdown("### Suggested Skills")
                    for sk in valid.split(','):
                        if sk.strip():
                            st.write(f"• {sk.strip()}")
                    if st.button("Add All to My Skills"):
                        for sk in valid.split(','):
                            s = sk.strip().lower()
                            if s and s not in st.session_state.skills:
                                st.session_state.skills.append(s)
                        st.rerun()
                else:
                    st.warning("Could not get skill suggestions. Please try again.")
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
                valid = safe_ai_response(letter)
                if valid is not None:
                    st.markdown("### Generated Cover Letter")
                    st.write(valid)
                    if st.button("Use This Cover Letter"):
                        st.session_state.cover_letter_ai = valid
                        st.info("Cover letter saved. Go to Cover Letter page to use it.")
                else:
                    st.warning("Could not generate cover letter. Please try again.")
            else:
                st.warning("Please fill in company and position.")

# ---- FOOTER ----
st.markdown("""
<div class="footer">
<span>© 2026 DocForge – Built by Rudraksh Panwar</span>
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
