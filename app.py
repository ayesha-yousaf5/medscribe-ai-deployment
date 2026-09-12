# import streamlit as st
# import os
# from vision import generate_heatmap, detect_abnormalities
# from orchestrator import run_agent
# from settings import SUPPORTED_LANGUAGES

# # ---------- Page config ----------
# st.set_page_config(
#     page_title="MedScribe AI",
#     page_icon="🩺",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

# # ---------- Custom CSS ----------
# st.markdown("""
# <style>
#     /* Global font */
#     html, body, [class*="css"] {
#         font-family: 'Segoe UI', 'Inter', sans-serif;
#     }

#     /* Header */
#     .main-header {
#         background: linear-gradient(90deg, #0f766e 0%, #0891b2 100%);
#         padding: 1.2rem 1.5rem;
#         border-radius: 12px;
#         color: white;
#         margin-bottom: 1rem;
#     }
#     .main-header h1 {
#         margin: 0; font-size: 1.8rem; font-weight: 700;
#     }
#     .main-header p {
#         margin: 0.2rem 0 0 0; opacity: 0.9; font-size: 0.95rem;
#     }

#     /* Card */
#     .card {
#         background: #f8fafc;
#         border: 1px solid #e2e8f0;
#         border-radius: 12px;
#         padding: 1rem 1.2rem;
#         margin-bottom: 1rem;
#     }

#     /* Urgency badges */
#     .badge {
#         display: inline-block;
#         padding: 0.4rem 1rem;
#         border-radius: 999px;
#         font-weight: 600;
#         font-size: 0.95rem;
#     }
#     .badge-routine  { background: #d1fae5; color: #065f46; }
#     .badge-urgent   { background: #fef3c7; color: #92400e; }
#     .badge-critical { background: #fee2e2; color: #991b1b; }

#     /* Agent trace step */
#     .trace-step {
#         background: #eef2ff;
#         border-left: 4px solid #6366f1;
#         padding: 0.6rem 0.9rem;
#         border-radius: 6px;
#         margin-bottom: 0.5rem;
#         font-family: 'Consolas', monospace;
#         font-size: 0.9rem;
#     }

#     /* RTL for Urdu/Arabic */
#     .rtl {
#         direction: rtl;
#         text-align: right;
#         font-family: 'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq', sans-serif;
#         font-size: 1.1rem;
#         line-height: 2.2;
#         background: #f0fdf4;
#         padding: 1rem 1.2rem;
#         border-radius: 12px;
#         border: 1px solid #bbf7d0;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ---------- Header ----------
# st.markdown("""
# <div class="main-header">
#     <h1>🩺 MedScribe AI</h1>
#     <p>Agentic radiology assistant — detects, explains, reports, translates.</p>
# </div>
# """, unsafe_allow_html=True)

# # ---------- Session state ----------
# if "result" not in st.session_state:
#     st.session_state.result = None
# if "image_path" not in st.session_state:
#     st.session_state.image_path = None
# if "heatmap" not in st.session_state:
#     st.session_state.heatmap = None
# if "language" not in st.session_state:
#     st.session_state.language = "English"

# # ---------- Upload panel (always visible on top) ----------
# with st.container():
#     col_u1, col_u2, col_u3 = st.columns([2, 1, 1])
#     with col_u1:
#         uploaded = st.file_uploader("Upload chest X-ray", type=["png", "jpg", "jpeg"])
#     with col_u2:
#         st.session_state.language = st.selectbox(
#             "Patient language", SUPPORTED_LANGUAGES,
#             index=SUPPORTED_LANGUAGES.index(st.session_state.language),
#         )
#     with col_u3:
#         st.write("")
#         st.write("")
#         run = st.button("🚀 Analyze", type="primary", use_container_width=True)

# if run and uploaded:
#     os.makedirs("outputs", exist_ok=True)
#     path = f"outputs/{uploaded.name}"
#     with open(path, "wb") as f:
#         f.write(uploaded.read())

#     with st.spinner("🧠 Agent is reasoning..."):
#         result = run_agent(path, st.session_state.language)
#         _, img_tensor = detect_abnormalities(path)
#         heatmap = generate_heatmap(path, img_tensor)

#     st.session_state.result = result
#     st.session_state.image_path = path
#     st.session_state.heatmap = heatmap

# # ---------- Tabs (navbar) ----------
# tab_diag, tab_trace, tab_patient, tab_about = st.tabs(
#     ["🩺 Diagnosis", "🧠 Agent Trace", "💬 Patient View", "ℹ️ About"]
# )

# # ============================================================
# # TAB 1 — DIAGNOSIS
# # ============================================================
# with tab_diag:
#     if st.session_state.result is None:
#         st.info("⬆️ Upload an X-ray and click **Analyze** to begin.")
#     else:
#         result = st.session_state.result
#         language = st.session_state.language

#         # Row 1: Scan + Heatmap
#         st.subheader("📸 Imaging")
#         c1, c2 = st.columns(2)
#         c1.image(st.session_state.image_path, caption="Original Scan", use_container_width=True)
#         c2.image(st.session_state.heatmap, caption="AI Attention (Grad-CAM)", use_container_width=True)

#         # Row 2: Urgency + Findings
#         st.subheader("🚨 Urgency")
#         urgency = result["urgency"].strip().lower()
#         badge_class = {
#             "routine": "badge-routine",
#             "urgent": "badge-urgent",
#             "critical": "badge-critical",
#         }.get(urgency, "badge-routine")
#         st.markdown(
#             f'<span class="badge {badge_class}">{urgency.upper()}</span>',
#             unsafe_allow_html=True,
#         )
#         if result["escalated"]:
#             st.error("⚠️ Critical finding — alert escalated to on-call radiologist.")

#         # Row 3: Clinical Report
#         st.subheader("📋 Clinical Report")
#         with st.container():
#             st.markdown('<div class="card">', unsafe_allow_html=True)
#             st.write(result["clinical_report"])
#             st.markdown('</div>', unsafe_allow_html=True)

# # ============================================================
# # TAB 2 — AGENT TRACE
# # ============================================================
# with tab_trace:
#     if st.session_state.result is None:
#         st.info("No trace yet. Run an analysis first.")
#     else:
#         result = st.session_state.result
#         st.subheader("🧠 Agent Reasoning — Step by Step")
#         st.caption("This shows exactly which tools the agent decided to call, in what order, and with what inputs.")

#         for i, step in enumerate(result["agent_trace"], 1):
#             st.markdown(
#                 f'<div class="trace-step">'
#                 f'<b>Step {i}:</b> <code>{step["tool"]}</code>'
#                 f'</div>',
#                 unsafe_allow_html=True,
#             )
#             with st.expander(f"Inputs for step {i}"):
#                 st.json(step["args"])

#         with st.expander("🤖 Final agent message"):
#             st.write(result.get("final_message", "—"))

# # ============================================================
# # TAB 3 — PATIENT VIEW
# # ============================================================
# with tab_patient:
#     if st.session_state.result is None:
#         st.info("No patient summary yet. Run an analysis first.")
#     else:
#         result = st.session_state.result
#         language = st.session_state.language

#         st.subheader(f"💬 آپ کے نتائج کا خلاصہ — {language}" if language == "Urdu"
#                      else f"💬 Your Results — {language}")
#         st.caption("A plain-language summary of your scan, written for you.")

#         summary = result["patient_summary"]
#         if language in ["Urdu", "Arabic", "Persian"]:
#             st.markdown(f'<div class="rtl">{summary}</div>', unsafe_allow_html=True)
#         else:
#             st.success(summary)

# # ============================================================
# # TAB 4 — ABOUT
# # ============================================================
# with tab_about:
#     st.subheader("ℹ️ About MedScribe AI")

#     st.markdown("""
# **What it does:** Takes a chest X-ray and produces two reports — a structured clinical
# report for the radiologist, and a plain-language summary for the patient in their own language.

# **How it works:**
# 1. A pretrained **DenseNet121** (TorchXRayVision, 18 pathologies) detects abnormalities
# 2. **Grad-CAM** shows which regions the model focused on
# 3. An **agentic LLM** (openai/gpt-oss-120b via Groq) decides which tools to call:
#    detect → report → assess urgency → escalate if critical → translate for patient

# **Tech stack:**
# - Frontend: Streamlit
# - CV model: TorchXRayVision (`densenet121-res224-all`)
# - Explainability: Grad-CAM
# - Agent: LangGraph + Groq (`openai/gpt-oss-120b`)
# - Language: Python 3.11
#     """)

#     st.warning("⚠️ **Disclaimer:** This is a proof of concept built for a hackathon. "
#                "It is **not a medical device** and must not be used for real clinical diagnosis. "
#                "Always consult a qualified radiologist.")






from __future__ import annotations

import html
import io
import json
import os
import re
import uuid
import urllib.request
import importlib.resources as importlib_resources
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image as PILImage, ImageDraw, ImageFont, features as PILFeatures

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import (
        HRFlowable,
        Image as RLImage,
        KeepTogether,
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )
    PDF_EXPORT_AVAILABLE = True
except ImportError:
    PDF_EXPORT_AVAILABLE = False

try:
    import arabic_reshaper
    from bidi.algorithm import get_display as bidi_get_display
except ImportError:
    arabic_reshaper = None
    bidi_get_display = None

try:
    from groq import Groq
except ImportError:
    Groq = None

from orchestrator import run_agent
from settings import SUPPORTED_LANGUAGES
from vision import detect_abnormalities, generate_heatmap


# -----------------------------------------------------------------------------
# Page configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="MedScribe AI | Radiology Intelligence",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# -----------------------------------------------------------------------------
# Luxury / royal visual system
# -----------------------------------------------------------------------------
ROYAL_CSS = r"""
<style>
:root {
    --bg-0: #050b14;
    --bg-1: #07111f;
    --bg-2: #0b1728;
    --surface-1: #0d1928;
    --surface-2: #101d30;
    --surface-3: #17263b;
    --line: rgba(151, 169, 191, 0.18);
    --line-strong: rgba(215, 194, 154, 0.30);
    --ivory: #f5f1e8;
    --ivory-soft: #ddd7ca;
    --muted: #9aa8b9;
    --muted-2: #6f7d90;
    --gold: #b79a5b;
    --champagne: #d7c29a;
    --sapphire: #4169a8;
    --sapphire-2: #2f527f;
    --success: #58a889;
    --warning: #c79a54;
    --urgent: #d88155;
    --critical: #c75b64;
    --shadow: 0 20px 70px rgba(0, 0, 0, 0.30);
}

html, body, [class*="css"] {
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
        "Segoe UI", sans-serif;
}

body {
    color: var(--ivory);
}

.stApp {
    background:
        radial-gradient(circle at 82% 8%, rgba(65, 105, 168, 0.11), transparent 31rem),
        radial-gradient(circle at 17% 72%, rgba(183, 154, 91, 0.055), transparent 29rem),
        linear-gradient(145deg, #050b14 0%, #07111f 43%, #081523 100%);
    color: var(--ivory);
    overflow-x: hidden;
}

.stApp::before,
.stApp::after {
    content: "";
    position: fixed;
    pointer-events: none;
    z-index: 0;
    border-radius: 999px;
    filter: blur(18px);
    opacity: 0.8;
}

.stApp::before {
    width: 34rem;
    height: 34rem;
    right: -15rem;
    top: 9rem;
    background: radial-gradient(circle, rgba(65,105,168,.08), rgba(65,105,168,0) 68%);
    animation: medscribeDriftA 24s ease-in-out infinite alternate;
}

.stApp::after {
    width: 28rem;
    height: 28rem;
    left: -13rem;
    bottom: 2rem;
    background: radial-gradient(circle, rgba(215,194,154,.045), rgba(215,194,154,0) 68%);
    animation: medscribeDriftB 30s ease-in-out infinite alternate;
}

@keyframes medscribeDriftA {
    from { transform: translate3d(0, -12px, 0) scale(1); }
    to   { transform: translate3d(-55px, 50px, 0) scale(1.08); }
}

@keyframes medscribeDriftB {
    from { transform: translate3d(0, 0, 0) scale(1.04); }
    to   { transform: translate3d(70px, -38px, 0) scale(.96); }
}

@keyframes medscribePulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(88, 168, 137, .28); }
    50% { box-shadow: 0 0 0 7px rgba(88, 168, 137, 0); }
}

@keyframes medscribeLine {
    from { transform: translateX(-110%); }
    to   { transform: translateX(290%); }
}

@keyframes medscribeReveal {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes medscribeBar {
    from { transform: scaleX(0); }
    to   { transform: scaleX(1); }
}

/* Streamlit chrome */
#MainMenu, footer, header[data-testid="stHeader"] {
    visibility: hidden;
}

[data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {
    display: none !important;
}

.block-container {
    position: relative;
    z-index: 2;
    max-width: 1480px;
    padding-top: 1.1rem;
    padding-bottom: 3.5rem;
}

/* Global typography */
h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: inherit;
}

h1, h2, h3 {
    letter-spacing: -0.025em;
}

p {
    color: var(--muted);
}

/* Grid overlay */
.royal-grid {
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    opacity: .19;
    background-image:
        linear-gradient(rgba(140,157,180,.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(140,157,180,.035) 1px, transparent 1px);
    background-size: 62px 62px;
    mask-image: linear-gradient(to bottom, rgba(0,0,0,.6), transparent 88%);
}

/* Top bar */
.ms-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: .72rem .15rem 1.15rem .15rem;
    border-bottom: 1px solid rgba(215,194,154,.12);
    animation: medscribeReveal .55s ease both;
}

.ms-brand {
    display: flex;
    align-items: center;
    gap: .85rem;
}

.ms-monogram {
    width: 2.55rem;
    height: 2.55rem;
    display: grid;
    place-items: center;
    border: 1px solid rgba(215,194,154,.48);
    background: linear-gradient(145deg, rgba(215,194,154,.08), rgba(65,105,168,.045));
    box-shadow: inset 0 0 0 1px rgba(255,255,255,.012), 0 9px 30px rgba(0,0,0,.20);
    color: var(--champagne);
    font-family: "Iowan Old Style", "Palatino Linotype", Georgia, serif;
    font-size: 1rem;
    letter-spacing: .08em;
}

.ms-brand-name {
    font-family: "Iowan Old Style", "Palatino Linotype", Georgia, serif;
    color: var(--ivory);
    font-size: 1.17rem;
    letter-spacing: .035em;
    line-height: 1.05;
}

.ms-brand-meta {
    margin-top: .22rem;
    color: var(--muted-2);
    font-size: .62rem;
    letter-spacing: .18em;
    text-transform: uppercase;
}

.ms-system {
    display: flex;
    align-items: center;
    gap: .58rem;
    color: #aab6c5;
    font-size: .68rem;
    letter-spacing: .12em;
    text-transform: uppercase;
}

.ms-system-dot {
    width: .48rem;
    height: .48rem;
    border-radius: 50%;
    background: var(--success);
    animation: medscribePulse 2.4s ease-in-out infinite;
}

/* Hero */
.ms-hero {
    position: relative;
    overflow: hidden;
    margin: 1.2rem 0 1.6rem;
    min-height: 23rem;
    display: grid;
    grid-template-columns: minmax(0, 1.25fr) minmax(20rem, .75fr);
    gap: 2rem;
    align-items: center;
    padding: 3.4rem 3.4rem;
    border: 1px solid rgba(215,194,154,.15);
    background:
        linear-gradient(110deg, rgba(13,25,40,.96), rgba(9,19,32,.87)),
        radial-gradient(circle at 80% 25%, rgba(65,105,168,.12), transparent 55%);
    box-shadow: var(--shadow);
    animation: medscribeReveal .7s ease .06s both;
}

.ms-hero::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(215,194,154,.55), transparent);
}

.ms-hero::after {
    content: "";
    position: absolute;
    width: 19rem;
    height: 1px;
    top: 0;
    left: 0;
    background: linear-gradient(90deg, transparent, rgba(245,241,232,.7), transparent);
    animation: medscribeLine 8s linear infinite;
    opacity: .45;
}

.ms-eyebrow,
.ms-section-index,
.ms-mini-label {
    color: var(--champagne);
    font-size: .68rem;
    font-weight: 650;
    letter-spacing: .18em;
    text-transform: uppercase;
}

.ms-hero h1 {
    margin: .7rem 0 1rem;
    max-width: 820px;
    color: var(--ivory);
    font-family: "Iowan Old Style", "Palatino Linotype", Georgia, serif;
    font-size: clamp(3.25rem, 6vw, 6.7rem);
    line-height: .91;
    font-weight: 500;
    letter-spacing: -.055em;
}

.ms-hero h1 .gold {
    color: var(--champagne);
}

.ms-hero-copy {
    max-width: 680px;
    margin: 0;
    color: #9eacbd;
    font-size: .98rem;
    line-height: 1.75;
}

.ms-hero-tags {
    margin-top: 1.7rem;
    display: flex;
    flex-wrap: wrap;
    gap: .6rem;
}

.ms-tag {
    padding: .48rem .7rem;
    border: 1px solid rgba(151,169,191,.15);
    background: rgba(255,255,255,.018);
    color: #a9b4c2;
    font-size: .64rem;
    letter-spacing: .08em;
    text-transform: uppercase;
}

.ms-visual {
    position: relative;
    min-height: 17rem;
    display: grid;
    place-items: center;
}

.ms-orbit {
    position: relative;
    width: min(17rem, 72vw);
    aspect-ratio: 1;
    border: 1px solid rgba(215,194,154,.18);
    border-radius: 50%;
    box-shadow:
        inset 0 0 90px rgba(65,105,168,.055),
        0 0 80px rgba(65,105,168,.045);
}

.ms-orbit::before,
.ms-orbit::after {
    content: "";
    position: absolute;
    border-radius: 50%;
    inset: 14%;
    border: 1px solid rgba(151,169,191,.12);
}

.ms-orbit::after {
    inset: 31%;
    border-color: rgba(215,194,154,.22);
    background: radial-gradient(circle, rgba(215,194,154,.06), rgba(65,105,168,.02), transparent 70%);
}

.ms-cross-h,
.ms-cross-v {
    position: absolute;
    background: rgba(151,169,191,.10);
}

.ms-cross-h { left: 7%; right: 7%; top: 50%; height: 1px; }
.ms-cross-v { top: 7%; bottom: 7%; left: 50%; width: 1px; }

.ms-core {
    position: absolute;
    inset: 0;
    display: grid;
    place-items: center;
    z-index: 2;
    text-align: center;
}

.ms-core strong {
    display: block;
    color: var(--ivory);
    font-family: "Iowan Old Style", "Palatino Linotype", Georgia, serif;
    font-size: 2rem;
    font-weight: 500;
}

.ms-core span {
    color: var(--muted-2);
    font-size: .58rem;
    letter-spacing: .18em;
    text-transform: uppercase;
}

.ms-float-label {
    position: absolute;
    padding: .5rem .65rem;
    border: 1px solid rgba(151,169,191,.14);
    background: rgba(7,17,31,.84);
    color: #aab7c6;
    font-size: .58rem;
    letter-spacing: .13em;
    text-transform: uppercase;
    backdrop-filter: blur(9px);
}

.ms-float-label.one { right: -1.2rem; top: 18%; }
.ms-float-label.two { left: -1.5rem; bottom: 25%; }
.ms-float-label.three { right: -.2rem; bottom: 5%; }

/* Section headers */
.ms-section-head {
    margin: 2.0rem 0 .95rem;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 1rem;
}

.ms-section-title {
    margin-top: .3rem;
    color: var(--ivory);
    font-family: "Iowan Old Style", "Palatino Linotype", Georgia, serif;
    font-size: 1.65rem;
    letter-spacing: -.025em;
}

.ms-section-copy {
    color: var(--muted-2);
    font-size: .72rem;
    line-height: 1.6;
    text-align: right;
    max-width: 460px;
}

/* Native Streamlit controls */
[data-testid="stFileUploader"],
[data-testid="stSelectbox"],
[data-testid="stTextInput"] {
    margin-bottom: .6rem;
}

[data-testid="stFileUploader"] > label,
[data-testid="stSelectbox"] > label {
    color: #a7b2c0 !important;
    font-size: .70rem !important;
    letter-spacing: .10em;
    text-transform: uppercase;
    font-weight: 620;
}

[data-testid="stFileUploaderDropzone"] {
    position: relative;
    min-height: 13.6rem;
    padding: 3.5rem 1.25rem 1.65rem !important;
    border: 1px solid rgba(215,194,154,.18) !important;
    border-radius: 7px !important;
    background:
        linear-gradient(rgba(13,25,40,.67), rgba(10,20,33,.72)) !important;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    transition: border-color .25s ease, transform .25s ease, box-shadow .25s ease;
    overflow: hidden;
}

/* Top-left gold label */
[data-testid="stFileUploaderDropzone"]::before {
    content: "RADIOGRAPH INPUT";
    position: absolute;
    left: 1.15rem;
    top: .95rem;
    z-index: 4;
    color: rgba(215,194,154,.74);
    font-size: .56rem;
    font-weight: 650;
    letter-spacing: .18em;
    line-height: 1;
    pointer-events: none;
}

/* Move the divider lower */
[data-testid="stFileUploaderDropzone"]::after {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    top: 68%;
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent 0%,
        rgba(65,105,168,.17) 12%,
        rgba(65,105,168,.28) 50%,
        rgba(65,105,168,.17) 88%,
        transparent 100%
    );
    pointer-events: none;
}

/* Center the whole native uploader content */
[data-testid="stFileUploaderDropzone"] > div {
    width: 100% !important;
    min-height: 8.1rem !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    gap: .7rem !important;
}

/* Center the Upload button itself */
[data-testid="stFileUploaderDropzone"] button {
    position: absolute !important;
    z-index: 3;
    left: 50% !important;
    top: 44% !important;
    transform: translate(-50%, -50%) !important;
    margin: 0 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-width: 8.8rem;
    background: rgba(245,241,232,.95) !important;
    color: #07111f !important;
    border: 1px solid rgba(215,194,154,.50) !important;
    border-radius: 4px !important;
    font-weight: 700 !important;
}

/* Prevent native uploader wrappers from left-aligning the centered button */
[data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"] {
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
}

/* Push helper / file-size text below the divider */
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] [data-testid="stFileUploaderDropzoneInstructions"] {
    position: absolute !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 1.15rem !important;
    width: 100% !important;
    margin: 0 !important;
    text-align: center !important;
    color: rgba(111,125,144,.58) !important;
    z-index: 2;
}

/* Some Streamlit versions wrap the instructions in a paragraph/span */
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] span {
    text-align: center;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(215,194,154,.42) !important;
    box-shadow: 0 18px 55px rgba(0,0,0,.20), inset 0 0 80px rgba(65,105,168,.028);
    transform: translateY(-1px);
}


div[data-baseweb="select"] > div {
    min-height: 3.15rem;
    background: linear-gradient(145deg, rgba(16,29,48,.72), rgba(11,23,40,.76)) !important;
    backdrop-filter: blur(9px);
    -webkit-backdrop-filter: blur(9px);
    border: 1px solid rgba(151,169,191,.17) !important;
    border-radius: 5px !important;
    color: var(--ivory) !important;
    box-shadow: none !important;
}

ul[role="listbox"] {
    background: #0d1928 !important;
}

li[role="option"] {
    color: #e6e1d8 !important;
}

.stButton > button,
.stDownloadButton > button {
    width: 100%;
    min-height: 3.15rem;
    border-radius: 4px !important;
    border: 1px solid rgba(215,194,154,.42) !important;
    background: linear-gradient(100deg, #f3eee4 0%, #ded1b8 100%) !important;
    color: #07111f !important;
    font-weight: 760 !important;
    letter-spacing: .08em;
    text-transform: uppercase;
    font-size: .72rem !important;
    box-shadow: 0 12px 30px rgba(0,0,0,.18);
    transition: transform .22s ease, box-shadow .22s ease, filter .22s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform: translateY(-2px);
    filter: brightness(1.035);
    box-shadow: 0 18px 44px rgba(0,0,0,.28);
}

.stButton > button:disabled {
    opacity: .44;
    transform: none;
}

/* Dark secondary download button when inside export area */
.ms-dark-action + div .stDownloadButton > button {
    background: rgba(255,255,255,.024) !important;
    color: var(--ivory-soft) !important;
    border-color: rgba(151,169,191,.18) !important;
}

/* Panels */
.ms-panel,
.ms-info-panel,
.ms-metric,
.ms-urgency,
.ms-report-shell,
.ms-summary-shell,
.ms-trace-shell {
    border: 1px solid rgba(151,169,191,.14);
    background: linear-gradient(145deg, rgba(16,29,48,.66), rgba(10,21,36,.72));
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: 0 14px 55px rgba(0,0,0,.15);
}

.ms-panel {
    padding: 1.3rem 1.35rem;
    min-height: 100%;
}

.ms-panel.gold-edge,
.ms-report-shell {
    border-top-color: rgba(215,194,154,.42);
}

.ms-panel-title {
    color: var(--ivory);
    font-size: .83rem;
    font-weight: 690;
    letter-spacing: .06em;
    text-transform: uppercase;
}

.ms-panel-copy {
    margin-top: .5rem;
    color: var(--muted);
    font-size: .76rem;
    line-height: 1.65;
}

.ms-workflow-list {
    margin-top: 1rem;
    display: grid;
    gap: .62rem;
}

.ms-workflow-row {
    display: grid;
    grid-template-columns: 2.25rem 1fr auto;
    align-items: center;
    gap: .75rem;
    padding: .67rem 0;
    border-bottom: 1px solid rgba(151,169,191,.09);
}

.ms-workflow-row:last-child { border-bottom: 0; }

.ms-workflow-no {
    color: var(--champagne);
    font-family: "Iowan Old Style", "Palatino Linotype", Georgia, serif;
    font-size: .92rem;
}

.ms-workflow-main {
    color: #cbd2dc;
    font-size: .70rem;
    letter-spacing: .055em;
    text-transform: uppercase;
}

.ms-workflow-state {
    color: var(--muted-2);
    font-size: .55rem;
    letter-spacing: .12em;
    text-transform: uppercase;
}

.ms-note {
    margin-top: .85rem;
    padding: .8rem .9rem;
    border-left: 2px solid rgba(183,154,91,.58);
    background: rgba(183,154,91,.045);
    color: #9ba7b6;
    font-size: .68rem;
    line-height: 1.62;
}

/* Image styling */
[data-testid="stImage"] {
    overflow: hidden;
    border: 1px solid rgba(151,169,191,.14);
    background: #04080d;
    box-shadow: 0 18px 55px rgba(0,0,0,.23);
}

[data-testid="stImage"] img {
    filter: saturate(.93) contrast(1.01);
}

[data-testid="stImageCaption"] {
    color: #7f8da0 !important;
    font-size: .62rem !important;
    letter-spacing: .11em;
    text-transform: uppercase;
}

/* Result metrics */
.ms-metrics {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: .8rem;
    margin: .9rem 0 1.4rem;
}

.ms-metric {
    position: relative;
    padding: 1rem 1.05rem;
    overflow: hidden;
}

.ms-metric::after {
    content: "";
    position: absolute;
    inset: auto 0 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(215,194,154,.22), transparent);
}

.ms-metric-label {
    color: var(--muted-2);
    font-size: .58rem;
    letter-spacing: .15em;
    text-transform: uppercase;
}

.ms-metric-value {
    margin-top: .35rem;
    color: var(--ivory);
    font-family: "Iowan Old Style", "Palatino Linotype", Georgia, serif;
    font-size: 1.65rem;
}

.ms-metric-sub {
    margin-top: .15rem;
    color: #758398;
    font-size: .62rem;
}

/* Findings */
.ms-findings-shell {
    padding: 1.25rem 1.35rem 1.1rem;
    border: 1px solid rgba(151,169,191,.14);
    background: linear-gradient(145deg, rgba(13,25,40,.64), rgba(8,18,31,.70));
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
}

.ms-finding-row {
    padding: .82rem 0 .88rem;
    border-bottom: 1px solid rgba(151,169,191,.08);
}

.ms-finding-row:last-child { border-bottom: 0; }

.ms-finding-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: .53rem;
}

.ms-finding-name {
    color: #dce1e8;
    font-size: .76rem;
    font-weight: 620;
}

.ms-finding-score {
    color: var(--champagne);
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: .68rem;
}

.ms-track {
    height: 4px;
    background: rgba(151,169,191,.09);
    overflow: hidden;
}

.ms-fill {
    height: 100%;
    transform-origin: left center;
    background: linear-gradient(90deg, #345c94, #708db7 68%, #b79a5b 100%);
    animation: medscribeBar 1s cubic-bezier(.2,.8,.2,1) both;
}

.ms-empty-findings {
    padding: 1rem 0 .25rem;
    color: #8795a8;
    font-size: .74rem;
    line-height: 1.65;
}

/* Urgency */
.ms-urgency {
    padding: 1.05rem 1.1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}

.ms-urgency-left {
    display: flex;
    align-items: center;
    gap: .8rem;
}

.ms-urgency-dot {
    width: .62rem;
    height: .62rem;
    border-radius: 50%;
}

.ms-urgency-dot.routine { background: var(--success); }
.ms-urgency-dot.urgent { background: var(--warning); }
.ms-urgency-dot.critical { background: var(--critical); }

.ms-urgency-name {
    color: var(--ivory);
    font-size: .78rem;
    font-weight: 700;
    letter-spacing: .11em;
    text-transform: uppercase;
}

.ms-urgency-caption {
    color: var(--muted-2);
    font-size: .62rem;
    margin-top: .16rem;
}

.ms-urgency-code {
    color: #7f8da0;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: .61rem;
}

.ms-critical-alert {
    margin-top: .72rem;
    border: 1px solid rgba(199,91,100,.30);
    border-left: 3px solid rgba(199,91,100,.80);
    background: rgba(199,91,100,.055);
    padding: .85rem .95rem;
    color: #cbb1b4;
    font-size: .70rem;
    line-height: 1.6;
}

/* Report / summary */
.ms-report-shell,
.ms-summary-shell,
.ms-trace-shell {
    padding: 1.25rem 1.35rem;
}

.ms-report-shell + div,
.ms-summary-shell + div {
    margin-top: -.25rem;
}

.ms-report-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding-bottom: .75rem;
    margin-bottom: .35rem;
    border-bottom: 1px solid rgba(151,169,191,.09);
}

.ms-report-title {
    color: var(--ivory);
    font-family: "Iowan Old Style", "Palatino Linotype", Georgia, serif;
    font-size: 1.28rem;
}

.ms-report-meta {
    color: var(--muted-2);
    font-size: .57rem;
    letter-spacing: .14em;
    text-transform: uppercase;
}

.ms-summary-text {
    color: #c8d0da;
    font-size: .82rem;
    line-height: 1.86;
    white-space: pre-wrap;
}

.ms-summary-text[dir="rtl"] {
    font-family: "Noto Nastaliq Urdu", "Noto Naskh Arabic", "Segoe UI", sans-serif;
    font-size: 1rem;
    line-height: 2.05;
    text-align: right;
}

/* markdown report appearance */
.ms-report-marker + div [data-testid="stMarkdownContainer"] {
    color: #c9d1da;
    font-size: .83rem;
    line-height: 1.78;
}

.ms-report-marker + div [data-testid="stMarkdownContainer"] h1,
.ms-report-marker + div [data-testid="stMarkdownContainer"] h2,
.ms-report-marker + div [data-testid="stMarkdownContainer"] h3 {
    font-family: "Iowan Old Style", "Palatino Linotype", Georgia, serif;
    color: var(--ivory);
}

/* Trace */
.ms-trace-item {
    display: grid;
    grid-template-columns: 2.4rem 1fr;
    gap: .85rem;
    position: relative;
    padding: .15rem 0 1.05rem;
}

.ms-trace-item:not(:last-child)::after {
    content: "";
    position: absolute;
    left: 1.16rem;
    top: 2.15rem;
    bottom: .1rem;
    width: 1px;
    background: linear-gradient(to bottom, rgba(215,194,154,.30), rgba(151,169,191,.08));
}

.ms-trace-no {
    width: 2.35rem;
    height: 2.35rem;
    display: grid;
    place-items: center;
    border: 1px solid rgba(215,194,154,.22);
    color: var(--champagne);
    font-family: "Iowan Old Style", "Palatino Linotype", Georgia, serif;
    font-size: .78rem;
    background: rgba(183,154,91,.025);
}

.ms-trace-tool {
    color: #d7dde5;
    font-size: .72rem;
    font-weight: 690;
    letter-spacing: .06em;
    text-transform: uppercase;
}

.ms-trace-desc {
    margin-top: .2rem;
    color: #7f8da0;
    font-size: .65rem;
    line-height: 1.55;
}

.ms-trace-args {
    margin-top: .38rem;
    color: #8492a4;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: .57rem;
    line-height: 1.52;
    word-break: break-word;
}

/* Tabs */
[data-baseweb="tab-list"] {
    gap: .35rem !important;
    border-bottom: 1px solid rgba(151,169,191,.10);
}

button[data-baseweb="tab"] {
    min-height: 2.8rem;
    padding: 0 1rem !important;
    border-radius: 0 !important;
    color: #7f8da0 !important;
    font-size: .66rem !important;
    font-weight: 680 !important;
    letter-spacing: .10em !important;
    text-transform: uppercase;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--ivory) !important;
}

[data-baseweb="tab-highlight"] {
    background: var(--champagne) !important;
    height: 1px !important;
}

/* Streamlit alerts and spinner */
[data-testid="stAlert"] {
    border-radius: 4px !important;
    border: 1px solid rgba(151,169,191,.16) !important;
    background: rgba(13,25,40,.70) !important;
    backdrop-filter: blur(9px);
    -webkit-backdrop-filter: blur(9px);
    color: #cbd3dd !important;
}

[data-testid="stSpinner"] > div {
    color: var(--champagne) !important;
}

/* Progress */
[data-testid="stProgress"] > div > div > div > div {
    background: linear-gradient(90deg, var(--sapphire), var(--champagne)) !important;
}

/* Divider */
hr {
    border-color: rgba(151,169,191,.10) !important;
}

/* Footer */
.ms-footer {
    margin-top: 2.7rem;
    padding-top: 1.15rem;
    border-top: 1px solid rgba(215,194,154,.11);
    display: flex;
    justify-content: space-between;
    gap: 1.3rem;
    color: #627186;
    font-size: .60rem;
    line-height: 1.65;
    letter-spacing: .035em;
}

.ms-footer strong {
    color: #8794a6;
    font-weight: 650;
}

/* Responsive */
@media (max-width: 900px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
    .ms-hero {
        grid-template-columns: 1fr;
        padding: 2.4rem 1.5rem;
    }
    .ms-hero h1 { font-size: clamp(3rem, 15vw, 5rem); }
    .ms-visual { min-height: 15rem; }
    .ms-orbit { width: 14rem; }
    .ms-float-label.one { right: .2rem; }
    .ms-float-label.two { left: .2rem; }
    .ms-section-head { align-items: flex-start; flex-direction: column; }
    .ms-section-copy { text-align: left; }
    .ms-metrics { grid-template-columns: 1fr; }
    .ms-footer { flex-direction: column; }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: .001ms !important;
        animation-iteration-count: 1 !important;
        scroll-behavior: auto !important;
    }
}





/* Primary clinical action — royal gold */
.stButton > button[kind="primary"],
button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(
        100deg,
        #A98642 0%,
        #B79A5B 42%,
        #D7C29A 100%
    ) !important;
    color: #07111F !important;
    border: 1px solid rgba(231, 208, 158, .78) !important;
    box-shadow:
        0 12px 30px rgba(183,154,91,.18),
        inset 0 1px 0 rgba(255,255,255,.16) !important;
}

.stButton > button[kind="primary"]:hover,
button[data-testid="stBaseButton-primary"]:hover {
    background: linear-gradient(
        100deg,
        #B18E49 0%,
        #C1A464 45%,
        #DEC99F 100%
    ) !important;
    color: #07111F !important;
    filter: none !important;
    box-shadow:
        0 16px 38px rgba(183,154,91,.28),
        inset 0 1px 0 rgba(255,255,255,.20) !important;
}

/* Keep the gold identity visible before an image is uploaded */
.stButton > button[kind="primary"]:disabled,
button[data-testid="stBaseButton-primary"]:disabled {
    background: linear-gradient(
        100deg,
        rgba(169,134,66,.88) 0%,
        rgba(183,154,91,.88) 42%,
        rgba(215,194,154,.88) 100%
    ) !important;
    color: rgba(7,17,31,.82) !important;
    opacity: .72 !important;
    border-color: rgba(215,194,154,.58) !important;
    box-shadow: 0 8px 22px rgba(183,154,91,.10) !important;
}



/* Run Clinical Analysis — force high-contrast text on gold */
.stButton > button[kind="primary"],
button[data-testid="stBaseButton-primary"] {
    color: #07111F !important;
    font-weight: 800 !important;
}

.stButton > button[kind="primary"] *,
button[data-testid="stBaseButton-primary"] * {
    color: #07111F !important;
    fill: #07111F !important;
    opacity: 1 !important;
    font-weight: 800 !important;
    text-shadow: none !important;
}

/* Disabled state: still readable, just slightly muted */
.stButton > button[kind="primary"]:disabled,
button[data-testid="stBaseButton-primary"]:disabled {
    color: rgba(7,17,31,.82) !important;
}

.stButton > button[kind="primary"]:disabled *,
button[data-testid="stBaseButton-primary"]:disabled * {
    color: rgba(7,17,31,.82) !important;
    fill: rgba(7,17,31,.82) !important;
    opacity: 1 !important;
}



/* Language + analysis action row */
.ms-control-label {
    min-height: 1.55rem;
    display: flex;
    align-items: flex-end;
    margin: 0 0 .52rem .05rem;
    color: #a7b2c0;
    font-size: .70rem;
    font-weight: 620;
    letter-spacing: .10em;
    text-transform: uppercase;
}

.ms-control-label-spacer {
    visibility: hidden;
}

/* Both controls use exactly the same height */
.ms-analysis-control-row + div div[data-baseweb="select"] > div,
.ms-analysis-control-row + div .stButton > button {
    min-height: 3.35rem !important;
    height: 3.35rem !important;
}

/* Remove extra native spacing inside the row */
.ms-analysis-control-row + div [data-testid="stSelectbox"],
.ms-analysis-control-row + div [data-testid="stButton"] {
    margin-bottom: 0 !important;
}

/* Keep select and primary action visually balanced */
.ms-analysis-control-row + div div[data-baseweb="select"] > div {
    width: 100% !important;
}

.ms-analysis-control-row + div .stButton > button {
    width: 100% !important;
    padding-left: 1.15rem !important;
    padding-right: 1.15rem !important;
    white-space: nowrap !important;
}



/* Doctor-facing vs patient-facing visual hierarchy */
.ms-audience-kicker {
    display: inline-flex;
    align-items: center;
    gap: .48rem;
    margin-bottom: .8rem;
    padding: .42rem .58rem;
    border: 1px solid rgba(151,169,191,.14);
    font-size: .58rem;
    font-weight: 720;
    letter-spacing: .15em;
    text-transform: uppercase;
}

.ms-audience-kicker.doctor {
    color: #b8c9df;
    background: rgba(65,105,168,.075);
    border-left: 2px solid rgba(65,105,168,.78);
}

.ms-audience-kicker.patient {
    color: var(--champagne);
    background: rgba(183,154,91,.06);
    border-left: 2px solid rgba(183,154,91,.80);
}

/* The Streamlit markdown block immediately following the report marker becomes
   a real doctor-facing document surface rather than loose text. */
.ms-report-marker + div [data-testid="stMarkdownContainer"] {
    margin-top: -.02rem;
    padding: 1.35rem 1.45rem 1.45rem;
    border: 1px solid rgba(151,169,191,.14);
    border-top: 0;
    border-left: 2px solid rgba(65,105,168,.66);
    background: linear-gradient(145deg, rgba(12,25,42,.43), rgba(7,17,30,.52));
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}

.ms-report-marker + div [data-testid="stMarkdownContainer"] strong {
    color: var(--ivory);
}

.ms-summary-shell.patient-facing {
    border-left: 2px solid rgba(183,154,91,.70);
    background: linear-gradient(145deg, rgba(30,27,20,.26), rgba(8,18,31,.50));
}

.ms-audit-shell-intro {
    margin-bottom: .9rem;
    padding: .75rem .9rem;
    border-left: 2px solid rgba(151,169,191,.30);
    background: rgba(151,169,191,.035);
    color: #8795a8;
    font-size: .68rem;
    line-height: 1.62;
}

.ms-export-feature {
    height: 100%;
    padding: 1rem 1.05rem;
    border: 1px solid rgba(215,194,154,.16);
    background: linear-gradient(145deg, rgba(17,29,46,.42), rgba(8,18,31,.50));
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}

.ms-export-feature strong {
    color: var(--ivory);
    font-size: .75rem;
    letter-spacing: .04em;
}

.ms-export-feature p {
    margin: .38rem 0 0;
    color: #8492a4;
    font-size: .66rem;
    line-height: 1.58;
}



/* ------------------------------------------------------------------
   Urdu / RTL output
   ------------------------------------------------------------------ */
.ms-section-head.ms-rtl {
    flex-direction: row-reverse !important;
    direction: rtl !important;
}

.ms-section-head.ms-rtl > div:first-child,
.ms-section-head.ms-rtl .ms-section-index,
.ms-section-head.ms-rtl .ms-section-title,
.ms-section-head.ms-rtl .ms-section-copy {
    text-align: right !important;
    direction: rtl !important;
}

.ms-section-head.ms-rtl .ms-section-copy {
    margin-left: auto;
    margin-right: 0;
}

.ms-report-shell.ms-rtl,
.ms-summary-shell.ms-rtl,
.ms-findings-shell.ms-rtl,
.ms-urgency.ms-rtl,
.ms-metrics.ms-rtl {
    direction: rtl !important;
    text-align: right !important;
}

.ms-report-shell.ms-rtl .ms-report-heading,
.ms-summary-shell.ms-rtl .ms-report-heading {
    flex-direction: row-reverse !important;
}

.ms-report-shell.ms-rtl .ms-report-title,
.ms-report-shell.ms-rtl .ms-mini-label,
.ms-report-shell.ms-rtl .ms-report-meta,
.ms-summary-shell.ms-rtl .ms-report-title,
.ms-summary-shell.ms-rtl .ms-mini-label,
.ms-summary-shell.ms-rtl .ms-report-meta {
    text-align: right !important;
    direction: rtl !important;
}

.ms-urdu-report {
    direction: rtl !important;
    text-align: right !important;
    unicode-bidi: plaintext;
    font-family: "Noto Naskh Arabic", "Noto Nastaliq Urdu", "Segoe UI", Tahoma, sans-serif;
    color: #c9d1da;
    font-size: .92rem;
    line-height: 2.05;
    padding: .35rem .1rem .2rem;
}

.ms-urdu-report h3 {
    direction: rtl !important;
    text-align: right !important;
    color: var(--champagne);
    font-family: "Noto Naskh Arabic", "Noto Nastaliq Urdu", "Segoe UI", Tahoma, sans-serif;
    font-size: 1.02rem;
    font-weight: 760;
    line-height: 1.7;
    margin: 1.35rem 0 .45rem;
}

.ms-urdu-report h3:first-child {
    margin-top: .25rem;
}

.ms-urdu-report p,
.ms-urdu-report .ms-urdu-bullet,
.ms-urdu-report .ms-urdu-numbered {
    direction: rtl !important;
    text-align: right !important;
    unicode-bidi: plaintext;
    margin: .36rem 0;
}

.ms-urdu-report .ms-urdu-bullet,
.ms-urdu-report .ms-urdu-numbered {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    gap: .55rem;
}

.ms-urdu-report .ms-urdu-marker {
    flex: 0 0 auto;
    color: var(--champagne);
}

.ms-summary-text[dir="rtl"] {
    direction: rtl !important;
    text-align: right !important;
    unicode-bidi: plaintext !important;
    font-family: "Noto Naskh Arabic", "Noto Nastaliq Urdu", "Segoe UI", Tahoma, sans-serif !important;
    line-height: 2.05 !important;
}

.ms-findings-shell.ms-rtl .ms-finding-head {
    flex-direction: row-reverse;
}

.ms-findings-shell.ms-rtl .ms-finding-name,
.ms-findings-shell.ms-rtl .ms-mini-label,
.ms-findings-shell.ms-rtl .ms-panel-title {
    text-align: right !important;
}

.ms-urgency.ms-rtl {
    flex-direction: row-reverse;
}

.ms-urgency.ms-rtl .ms-urgency-left {
    flex-direction: row-reverse;
}

.ms-urgency.ms-rtl .ms-urgency-name,
.ms-urgency.ms-rtl .ms-urgency-caption,
.ms-urgency.ms-rtl .ms-urgency-code {
    direction: rtl !important;
    text-align: right !important;
}



/* ------------------------------------------------------------------
   Export actions — same royal-gold identity as Run Clinical Analysis
   ------------------------------------------------------------------ */
.stDownloadButton > button {
    background: linear-gradient(
        100deg,
        #A98642 0%,
        #B79A5B 42%,
        #D7C29A 100%
    ) !important;
    color: #07111F !important;
    border: 1px solid rgba(231, 208, 158, .78) !important;
    box-shadow:
        0 12px 30px rgba(183,154,91,.18),
        inset 0 1px 0 rgba(255,255,255,.16) !important;
    font-weight: 800 !important;
}

.stDownloadButton > button *,
.stDownloadButton > button p,
.stDownloadButton > button span,
.stDownloadButton > button svg {
    color: #07111F !important;
    fill: #07111F !important;
    opacity: 1 !important;
    font-weight: 800 !important;
    text-shadow: none !important;
}

.stDownloadButton > button:hover {
    background: linear-gradient(
        100deg,
        #B18E49 0%,
        #C1A464 45%,
        #DEC99F 100%
    ) !important;
    color: #07111F !important;
    filter: none !important;
    transform: translateY(-2px);
    box-shadow:
        0 16px 38px rgba(183,154,91,.28),
        inset 0 1px 0 rgba(255,255,255,.20) !important;
}

.stDownloadButton > button:disabled {
    background: linear-gradient(
        100deg,
        rgba(169,134,66,.88) 0%,
        rgba(183,154,91,.88) 42%,
        rgba(215,194,154,.88) 100%
    ) !important;
    color: rgba(7,17,31,.82) !important;
    border-color: rgba(215,194,154,.58) !important;
    opacity: .72 !important;
}

.stDownloadButton > button:disabled * {
    color: rgba(7,17,31,.82) !important;
    fill: rgba(7,17,31,.82) !important;
    opacity: 1 !important;
}

.ms-export-feature.ms-rtl {
    direction: rtl !important;
    text-align: right !important;
}

.ms-export-feature.ms-rtl strong,
.ms-export-feature.ms-rtl p {
    direction: rtl !important;
    text-align: right !important;
    font-family: "Noto Naskh Arabic", "Noto Nastaliq Urdu", "Segoe UI", Tahoma, sans-serif;
}

</style>
"""

st.markdown(ROYAL_CSS, unsafe_allow_html=True)
st.markdown('<div class="royal-grid"></div>', unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value))


def normalize_urgency(value: Any) -> str:
    raw = str(value or "routine").strip().lower().replace('"', "").replace("'", "")
    if "critical" in raw:
        return "critical"
    if "urgent" in raw:
        return "urgent"
    return "routine"


def safe_suffix(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix not in {".png", ".jpg", ".jpeg"}:
        return ".png"
    return suffix


def top_confidence(findings: list[dict[str, Any]]) -> float:
    if not findings:
        return 0.0
    return max(float(item.get("confidence", 0) or 0) for item in findings)


def trace_description(tool_name: str) -> str:
    descriptions = {
        "detect_findings": "Vision inference · DenseNet121 pathology screening",
        "write_clinical_report": "Clinical synthesis · structured radiology report",
        "assess_urgency": "Triage layer · routine / urgent / critical classification",
        "write_patient_summary": "Communication layer · patient-friendly language output",
        "escalate_to_doctor": "Escalation layer · on-call radiologist alert",
    }
    return descriptions.get(tool_name, "Agent tool execution")


def compact_args(args: Any, limit: int = 220) -> str:
    try:
        text = json.dumps(args, ensure_ascii=False, default=str)
    except Exception:
        text = str(args)
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1] + "…"



def render_golden_dust_background() -> None:
    """
    Inject a full-viewport golden shimmer plume behind the Streamlit UI.

    The effect is inspired by floating glitter / energy-smoke particles:
    a concentrated sinuous gold stream runs from top to bottom, surrounded
    by sparse drifting dust. Nearby particles move away from the cursor and
    spring back toward the plume.
    """
    components.html(
        """
        <script>
        (function () {
          let parentWin;
          let parentDoc;

          try {
            parentWin = window.parent;
            parentDoc = parentWin.document;
          } catch (err) {
            return;
          }

          if (!parentDoc || !parentDoc.body) return;

          const oldRoot =
            parentDoc.getElementById("ms-gold-plume-root") ||
            parentDoc.getElementById("ms-dna-gold-root") ||
            parentDoc.getElementById("ms-golden-dust-root");
          if (oldRoot) oldRoot.remove();

          const oldStyle =
            parentDoc.getElementById("ms-gold-plume-style") ||
            parentDoc.getElementById("ms-dna-gold-style") ||
            parentDoc.getElementById("ms-golden-dust-style");
          if (oldStyle) oldStyle.remove();

          const style = parentDoc.createElement("style");
          style.id = "ms-gold-plume-style";
          style.textContent = `
            #ms-gold-plume-root {
              position: fixed;
              inset: 0;
              z-index: 1;
              pointer-events: none;
              overflow: hidden;
            }

            #ms-gold-plume-canvas {
              position: absolute;
              inset: 0;
              width: 100%;
              height: 100%;
              display: block;
              pointer-events: none;
              opacity: 1;
              filter: none;
            }

            @media (prefers-reduced-motion: reduce) {
              #ms-gold-plume-canvas { opacity: .42; }
            }
          `;
          parentDoc.head.appendChild(style);

          const root = parentDoc.createElement("div");
          root.id = "ms-gold-plume-root";

          const canvas = parentDoc.createElement("canvas");
          canvas.id = "ms-gold-plume-canvas";
          root.appendChild(canvas);
          parentDoc.body.appendChild(root);

          const ctx = canvas.getContext("2d", { alpha: true });
          if (!ctx) return;

          let width = 1;
          let height = 1;
          let dpr = 1;

          let targetMouseX = -10000;
          let targetMouseY = -10000;
          let mouseX = -10000;
          let mouseY = -10000;

          let scrollY = parentWin.scrollY || 0;
          let smoothScrollY = scrollY;

          const plumeParticles = [];
          const ambientParticles = [];
          const totalPlume = 820;
          const totalAmbient = 265;

          function rand(seed) {
            const x = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
            return x - Math.floor(x);
          }

          function resetParticles() {
            plumeParticles.length = 0;
            ambientParticles.length = 0;

            for (let i = 0; i < totalPlume; i++) {
              const t = rand(i * 2.17 + 5.1);

              // Most particles live close to the bright core,
              // with a smaller number forming the outer smoke halo.
              const coreBias = Math.pow(rand(i * 3.91 + 8.2), 2.15);
              const side = rand(i * 7.33 + 4.6) > .5 ? 1 : -1;

              plumeParticles.push({
                t,
                side,
                radial: 7 + coreBias * 118,
                verticalJitter: (rand(i * 5.27 + 1.8) - .5) * 28,
                phase: rand(i * 9.1 + 3.2) * Math.PI * 2,
                size: .34 + rand(i * 4.51 + 7.4) * 1.72,
                alpha: .075 + rand(i * 8.77 + 2.1) * .48,
                warmth: rand(i * 6.12 + 6.4),
                ox: 0,
                oy: 0,
                vx: 0,
                vy: 0
              });
            }

            for (let i = 0; i < totalAmbient; i++) {
              ambientParticles.push({
                x: rand(i * 3.7 + 1.1),
                y: rand(i * 5.4 + 2.8),
                phase: rand(i * 7.9 + 9.4) * Math.PI * 2,
                size: .24 + rand(i * 9.2 + 4.3) * 1.16,
                alpha: .040 + rand(i * 6.7 + 7.5) * .20,
                driftX: (rand(i * 4.9 + 3.6) - .5) * 16,
                driftY: 8 + rand(i * 2.8 + 5.9) * 26,
                ox: 0,
                oy: 0,
                vx: 0,
                vy: 0
              });
            }
          }

          function resize() {
            width = Math.max(
              1,
              parentWin.innerWidth || parentDoc.documentElement.clientWidth || 1
            );
            height = Math.max(
              1,
              parentWin.innerHeight || parentDoc.documentElement.clientHeight || 1
            );

            dpr = Math.min(2, parentWin.devicePixelRatio || 1);
            canvas.width = Math.floor(width * dpr);
            canvas.height = Math.floor(height * dpr);
            canvas.style.width = width + "px";
            canvas.style.height = height + "px";
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
          }

          resetParticles();
          resize();

          function onMouseMove(e) {
            targetMouseX = e.clientX;
            targetMouseY = e.clientY;
          }

          function onMouseLeave() {
            targetMouseX = -10000;
            targetMouseY = -10000;
          }

          function onScroll() {
            scrollY =
              parentWin.scrollY ||
              parentDoc.documentElement.scrollTop ||
              0;
          }

          parentWin.addEventListener("mousemove", onMouseMove, { passive: true });
          parentWin.addEventListener("mouseleave", onMouseLeave, { passive: true });
          parentWin.addEventListener("scroll", onScroll, { passive: true });
          parentWin.addEventListener("resize", resize, { passive: true });

          function plumeCenter(t, time) {
            // A graceful S-shaped vertical plume, rather than a literal DNA helix.
            const scrollPhase = smoothScrollY * .00055;

            const centerX =
              width * .53 +
              Math.sin(t * Math.PI * 2.25 + time * .00011 + scrollPhase) *
                Math.min(width * .095, 120) +
              Math.sin(t * Math.PI * 5.1 - time * .00007) *
                Math.min(width * .028, 38);

            const y =
              -height * .10 +
              t * height * 1.20 +
              Math.sin(t * Math.PI * 3.8 + time * .00016) * 10;

            return { x: centerX, y };
          }

          function plumeTangent(t, time) {
            const eps = .002;
            const a = plumeCenter(Math.max(0, t - eps), time);
            const b = plumeCenter(Math.min(1, t + eps), time);

            let tx = b.x - a.x;
            let ty = b.y - a.y;
            const len = Math.sqrt(tx * tx + ty * ty) || 1;

            tx /= len;
            ty /= len;

            return {
              tx,
              ty,
              nx: -ty,
              ny: tx
            };
          }

          function repel(p, homeX, homeY, radius, strength) {
            const px = homeX + p.ox;
            const py = homeY + p.oy;

            const dx = px - mouseX;
            const dy = py - mouseY;
            const d2 = dx * dx + dy * dy;
            const r2 = radius * radius;

            if (d2 < r2 && d2 > .001) {
              const d = Math.sqrt(d2);
              const f = (1 - d / radius) * strength;
              p.vx += (dx / d) * f;
              p.vy += (dy / d) * f;
            }

            // Elastic return to the original plume.
            p.vx += (-p.ox) * .017;
            p.vy += (-p.oy) * .017;
            p.vx *= .90;
            p.vy *= .90;
            p.ox += p.vx;
            p.oy += p.vy;
          }

          function glow(x, y, radius, alpha) {
            const g = ctx.createRadialGradient(x, y, 0, x, y, radius);
            g.addColorStop(0, `rgba(215,194,154,${alpha})`);
            g.addColorStop(.30, `rgba(183,154,91,${alpha * .62})`);
            g.addColorStop(.72, `rgba(183,154,91,${alpha * .16})`);
            g.addColorStop(1, "rgba(183,154,91,0)");

            ctx.fillStyle = g;
            ctx.beginPath();
            ctx.arc(x, y, radius, 0, Math.PI * 2);
            ctx.fill();
          }

          function drawPlumeParticle(p, time) {
            const center = plumeCenter(p.t, time);
            const tangent = plumeTangent(p.t, time);

            const wave =
              Math.sin(time * .00065 + p.phase + p.t * 18) * 8;

            const homeX =
              center.x +
              tangent.nx * (p.radial * p.side + wave);

            const homeY =
              center.y +
              tangent.ny * (p.radial * p.side + wave * .35) +
              p.verticalJitter +
              Math.cos(time * .00042 + p.phase) * 6;

            repel(p, homeX, homeY, 135, 2.45);

            const x = homeX + p.ox;
            const y = homeY + p.oy;

            const shimmer =
              .18 +
              .82 * (
                .5 +
                .5 * Math.sin(
                  time * .0031 +
                  p.phase +
                  p.t * 31
                )
              );

            const alpha =
              Math.min(
                .82,
                p.alpha *
                (.34 + shimmer * 1.72) *
                (1 - Math.min(1, p.radial / 160) * .28)
              );

            const size = p.size * (.96 + shimmer * .08);

            const colorMix = p.warmth;
            const r = Math.round(183 + (215 - 183) * colorMix);
            const g = Math.round(154 + (194 - 154) * colorMix);
            const b = Math.round(91 + (154 - 91) * colorMix);

            ctx.fillStyle = `rgba(${r},${g},${b},${alpha})`;
            ctx.beginPath();
            ctx.arc(x, y, Math.max(.28, size), 0, Math.PI * 2);
            ctx.fill();

          }

          function drawAmbient(p, time) {
            const baseX =
              p.x * width +
              Math.sin(time * .00022 + p.phase) * p.driftX;

            const baseY =
              ((p.y * height +
                time * .006 * p.driftY -
                smoothScrollY * .07) %
                (height + 70)) -
              35;

            repel(p, baseX, baseY, 105, 1.6);

            const x = baseX + p.ox;
            const y = baseY + p.oy;

            const shimmer =
              .20 +
              .80 * (
                .5 +
                .5 * Math.sin(time * .0020 + p.phase)
              );

            const alpha = Math.min(.42, p.alpha * (.30 + shimmer * 1.55));
            const size = p.size * (.97 + shimmer * .06);

            ctx.fillStyle = `rgba(183,154,91,${alpha})`;
            ctx.beginPath();
            ctx.arc(x, y, size, 0, Math.PI * 2);
            ctx.fill();
          }

          function drawSoftSmoke(time) {
            // Very soft golden illumination along the same path.
            ctx.save();
            ctx.globalCompositeOperation = "screen";

            for (let i = 0; i < 22; i++) {
              const t = i / 21;
              const c = plumeCenter(t, time);
              const pulse =
                .78 +
                .22 * Math.sin(time * .0007 + i * .77);

              const radius =
                52 +
                Math.sin(t * Math.PI) * 42 +
                pulse * 15;

              const grad = ctx.createRadialGradient(
                c.x, c.y, 0,
                c.x, c.y, radius
              );

              grad.addColorStop(
                0,
                `rgba(183,154,91,${.014 + pulse * .012})`
              );
              grad.addColorStop(
                .40,
                `rgba(183,154,91,${.008 + pulse * .008})`
              );
              grad.addColorStop(1, "rgba(203,138,26,0)");

              ctx.fillStyle = grad;
              ctx.beginPath();
              ctx.arc(c.x, c.y, radius, 0, Math.PI * 2);
              ctx.fill();
            }

            ctx.restore();
          }

          function render(time) {
            mouseX += (targetMouseX - mouseX) * .17;
            mouseY += (targetMouseY - mouseY) * .17;
            smoothScrollY += (scrollY - smoothScrollY) * .08;

            ctx.clearRect(0, 0, width, height);

            drawSoftSmoke(time);

            // Ambient dust first.
            for (const p of ambientParticles) {
              drawAmbient(p, time);
            }

            // Main concentrated glitter plume.
            for (const p of plumeParticles) {
              drawPlumeParticle(p, time);
            }

            parentWin.requestAnimationFrame(render);
          }

          parentWin.requestAnimationFrame(render);
        })();
        </script>
        """,
        height=0,
        scrolling=False,
    )


def render_topbar() -> None:
    st.markdown(
        """
        <div class="ms-topbar">
            <div class="ms-brand">
                <div class="ms-monogram">MS</div>
                <div>
                    <div class="ms-brand-name">MedScribe AI</div>
                    <div class="ms-brand-meta">Radiology Intelligence</div>
                </div>
            </div>
            <div class="ms-system">
                <span class="ms-system-dot"></span>
                System operational
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    """Render the luxury hero with a real interactive 3D adult-male chest model.

    The model is embedded from Sketchfab (CC BY) and remains confined to the
    right-hand hero viewer. It auto-rotates slowly and supports mouse/touch drag.
    """
    hero_html = r"""
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <style>
        :root {
          --bg: #07111f;
          --surface: #0b1728;
          --surface-2: #101d30;
          --ivory: #f5f1e8;
          --muted: #91a0b2;
          --muted-2: #657488;
          --gold: #b79a5b;
          --champagne: #d7c29a;
          --success: #58a889;
          --line: rgba(151,169,191,.14);
        }

        * { box-sizing: border-box; }
        html, body {
          margin: 0;
          width: 100%;
          height: 100%;
          overflow: hidden;
          background: transparent;
          color: var(--ivory);
          font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        .hero {
          position: relative;
          height: 410px;
          display: grid;
          grid-template-columns: minmax(0, 1.08fr) minmax(420px, .92fr);
          gap: 26px;
          align-items: center;
          padding: 34px 36px;
          overflow: hidden;
          border: 1px solid rgba(215,194,154,.15);
          background:
            radial-gradient(circle at 84% 48%, rgba(65,105,168,.10), transparent 31%),
            linear-gradient(110deg, rgba(13,25,40,.84), rgba(8,18,31,.78));
          box-shadow: 0 24px 70px rgba(0,0,0,.25);
        }

        .hero::before {
          content: "";
          position: absolute;
          inset: 0;
          pointer-events: none;
          background-image:
            linear-gradient(rgba(140,157,180,.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(140,157,180,.025) 1px, transparent 1px);
          background-size: 62px 62px;
          mask-image: linear-gradient(to right, rgba(0,0,0,.68), rgba(0,0,0,.12));
        }

        .hero::after {
          content: "";
          position: absolute;
          left: 0;
          top: 0;
          width: 100%;
          height: 1px;
          background: linear-gradient(90deg, transparent, rgba(215,194,154,.55), transparent);
        }

        .copy {
          position: relative;
          z-index: 3;
          padding-left: 3px;
        }

        .eyebrow {
          color: var(--champagne);
          font-size: 10px;
          font-weight: 700;
          letter-spacing: .19em;
          text-transform: uppercase;
        }

        h1 {
          margin: 14px 0 14px;
          max-width: 760px;
          color: var(--ivory);
          font-family: "Iowan Old Style", "Palatino Linotype", Georgia, serif;
          font-size: clamp(46px, 5vw, 68px);
          line-height: .94;
          font-weight: 500;
          letter-spacing: -.052em;
        }

        h1 span { color: var(--champagne); }

        .copy p {
          margin: 0;
          max-width: 650px;
          color: #96a5b6;
          font-size: 14px;
          line-height: 1.72;
        }

        .caps {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 9px;
          margin-top: 25px;
          max-width: 650px;
        }

        .cap {
          min-height: 69px;
          padding: 11px 12px 10px;
          border-top: 1px solid rgba(215,194,154,.26);
          background: rgba(255,255,255,.008);
        }

        .cap .no {
          display: block;
          color: var(--gold);
          font-family: Georgia, serif;
          font-size: 12px;
        }

        .cap b {
          display: block;
          margin-top: 4px;
          color: #d8dee6;
          font-size: 10px;
          letter-spacing: .13em;
          text-transform: uppercase;
        }

        .cap small {
          display: block;
          margin-top: 4px;
          color: #68798d;
          font-size: 8px;
          letter-spacing: .12em;
          text-transform: uppercase;
        }

        .viewer {
          position: relative;
          z-index: 3;
          height: 340px;
          overflow: hidden;
          border: 1px solid rgba(151,169,191,.12);
          background:
            radial-gradient(circle at 50% 46%, rgba(72,112,157,.14), transparent 44%),
            linear-gradient(180deg, rgba(4,13,23,.85), rgba(3,10,17,.65));
          box-shadow: inset 0 0 50px rgba(61,96,137,.05);
        }

        .viewer::before,
        .viewer::after {
          content: "";
          position: absolute;
          z-index: 4;
          pointer-events: none;
          border-radius: 50%;
          left: 50%;
          top: 50%;
          transform: translate(-50%, -50%);
        }

        .viewer::before {
          width: 250px;
          height: 250px;
          border: 1px solid rgba(163,185,209,.08);
          box-shadow: 0 0 42px rgba(75,115,159,.05);
          animation: ringSpin 22s linear infinite;
        }

        .viewer::after {
          width: 190px;
          height: 190px;
          border: 1px dashed rgba(215,194,154,.10);
          animation: ringSpinReverse 18s linear infinite;
        }

        .viewer-top {
          position: absolute;
          z-index: 7;
          left: 15px;
          right: 15px;
          top: 12px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          pointer-events: none;
        }

        .viewer-label {
          color: #7b8c9f;
          font-size: 8px;
          letter-spacing: .17em;
          text-transform: uppercase;
        }

        .viewer-label b { color: #b8c4d0; font-weight: 700; }

        .live {
          display: flex;
          align-items: center;
          gap: 6px;
          color: #7b8c9f;
          font-size: 7px;
          letter-spacing: .16em;
          text-transform: uppercase;
        }

        .live i {
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background: var(--success);
          box-shadow: 0 0 0 5px rgba(88,168,137,.07);
        }

        .model-frame {
          position: absolute;
          inset: 0;
          z-index: 2;
          width: 100%;
          height: 100%;
          border: 0;
          background: transparent;
          filter: saturate(.72) contrast(1.08) brightness(.95) hue-rotate(182deg);
        }

        .model-vignette {
          position: absolute;
          inset: 0;
          z-index: 5;
          pointer-events: none;
          background:
            linear-gradient(to bottom, rgba(4,13,23,.22), transparent 18%, transparent 80%, rgba(4,13,23,.34)),
            linear-gradient(90deg, rgba(4,13,23,.18), transparent 15%, transparent 85%, rgba(4,13,23,.18));
        }

        .scan {
          position: absolute;
          z-index: 6;
          left: 13%;
          right: 13%;
          top: 50%;
          height: 1px;
          pointer-events: none;
          background: linear-gradient(90deg, transparent, rgba(169,215,255,.38), transparent);
          box-shadow: 0 0 15px rgba(86,150,206,.14);
          animation: scan 6.8s ease-in-out infinite alternate;
        }

        .node {
          position: absolute;
          z-index: 6;
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background: #eff6ff;
          box-shadow: 0 0 14px rgba(215,234,255,.34);
          pointer-events: none;
        }

        .n1 { right: 84px; top: 76px; animation: nodeA 5.5s ease-in-out infinite; }
        .n2 { left: 70px; bottom: 77px; animation: nodeB 6.4s ease-in-out infinite; }

        .viewer-bottom {
          position: absolute;
          z-index: 7;
          left: 15px;
          right: 15px;
          bottom: 9px;
          display: flex;
          justify-content: space-between;
          gap: 14px;
          pointer-events: none;
          color: #607186;
          font-size: 7px;
          letter-spacing: .12em;
          text-transform: uppercase;
        }

        .viewer-bottom b { color: #96a8ba; font-weight: 650; }

        .credit {
          position: absolute;
          z-index: 8;
          right: 13px;
          bottom: 27px;
          color: rgba(147,164,183,.62);
          font-size: 7px;
          letter-spacing: .05em;
          pointer-events: none;
        }

        @keyframes ringSpin {
          from { transform: translate(-50%, -50%) rotate(0deg); }
          to { transform: translate(-50%, -50%) rotate(360deg); }
        }
        @keyframes ringSpinReverse {
          from { transform: translate(-50%, -50%) rotate(360deg); }
          to { transform: translate(-50%, -50%) rotate(0deg); }
        }
        @keyframes scan {
          from { transform: translateY(-86px); }
          to { transform: translateY(86px); }
        }
        @keyframes nodeA {
          0%, 100% { transform: translate(0,0); }
          50% { transform: translate(-12px,10px); }
        }
        @keyframes nodeB {
          0%, 100% { transform: translate(0,0); }
          50% { transform: translate(12px,-8px); }
        }

        @media (max-width: 960px) {
          .hero {
            height: 680px;
            grid-template-columns: 1fr;
            padding: 28px 22px;
            gap: 22px;
          }
          h1 { font-size: 50px; }
          .viewer { height: 310px; }
        }

        @media (max-width: 620px) {
          .hero { height: 745px; padding: 24px 16px; }
          h1 { font-size: 41px; }
          .copy p { font-size: 12px; }
          .caps { grid-template-columns: 1fr; gap: 4px; margin-top: 16px; }
          .cap { min-height: 52px; padding: 8px 10px; }
          .viewer { height: 280px; }
        }

        @media (prefers-reduced-motion: reduce) {
          .viewer::before, .viewer::after, .scan, .node { animation: none !important; }
        }
      </style>
    </head>
    <body>
      <section class="hero">
        <div class="copy">
          <div class="eyebrow">Clinical intelligence / multimodal analysis</div>
          <h1>Precision at the point of <span>interpretation.</span></h1>
          <p>
            An agentic chest-radiograph workspace combining pathology detection,
            explainability, structured reporting, urgency triage and multilingual
            patient communication in one controlled workflow.
          </p>
          <div class="caps">
            <div class="cap"><span class="no">01</span><b>Vision</b><small>18 pathologies</small></div>
            <div class="cap"><span class="no">02</span><b>Explainability</b><small>Grad-CAM</small></div>
            <div class="cap"><span class="no">03</span><b>Synthesis</b><small>Clinical agent</small></div>
          </div>
        </div>

        <div class="viewer">
          <div class="viewer-top">
            <div class="viewer-label"><b>Interactive 3D chest</b></div>
          </div>

          <iframe
            class="model-frame"
            title="Adult male human thorax 3D model"
            frameborder="0"
            allow="autoplay; fullscreen; xr-spatial-tracking"
            allowfullscreen
            mozallowfullscreen="true"
            webkitallowfullscreen="true"
            src="https://sketchfab.com/models/4aba9b2ced344bdf8f09656c6a298b50/embed?autostart=1&autospin=0.18&ui_theme=dark&ui_infos=0&ui_help=0&ui_settings=0&ui_inspector=0&ui_stop=0&ui_hint=0&dnt=1">
          </iframe>

          <div class="model-vignette"></div>
          <div class="scan"></div>
          <div class="node n1"></div>
          <div class="node n2"></div>
        </div>
      </section>
    </body>
    </html>
    """
    components.html(hero_html, height=430, scrolling=False)


def section_header(index: str, title: str, copy: str, rtl: bool = False) -> None:
    rtl_class = " ms-rtl" if rtl else ""
    direction = "rtl" if rtl else "ltr"
    st.markdown(
        f"""
        <div class="ms-section-head{rtl_class}" dir="{direction}">
            <div>
                <div class="ms-section-index">{esc(index)}</div>
                <div class="ms-section-title">{esc(title)}</div>
            </div>
            <div class="ms-section-copy">{esc(copy)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_workflow_panel() -> None:
    rows = [
        ("01", "Image ingestion", "Local input"),
        ("02", "Vision inference", "DenseNet121"),
        ("03", "Attention mapping", "Grad-CAM"),
        ("04", "Clinical synthesis", "Agent / LLM"),
        ("05", "Urgency + summary", "Final output"),
    ]
    rows_html = "".join(
        f"""
        <div class="ms-workflow-row">
            <div class="ms-workflow-no">{n}</div>
            <div class="ms-workflow-main">{name}</div>
            <div class="ms-workflow-state">{state}</div>
        </div>
        """
        for n, name, state in rows
    )
    st.markdown(
        f"""
        <div class="ms-panel gold-edge">
            <div class="ms-mini-label">Analysis architecture</div>
            <div class="ms-panel-title" style="margin-top:.45rem;">Controlled clinical workflow</div>
            <div class="ms-panel-copy">
                Each scan moves through the MedScribe clinical intelligence pipeline from image
                ingestion through explainability, synthesis, urgency assessment and patient communication.
            </div>
            <div class="ms-workflow-list">{rows_html}</div>
            <div class="ms-note">
                AI-assisted output requires qualified clinical review and must not be used as a standalone diagnosis.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _screen_inline_markup(value: Any) -> str:
    safe = esc(_pdf_normalize_text(value))
    safe = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", safe)
    return safe


def render_clinical_report_screen(report_text: str, language: str) -> None:
    """Render Urdu report content as true RTL HTML; English keeps native Markdown."""
    report_text = _pdf_normalize_text(report_text or "")

    if not _is_urdu(language):
        st.markdown(report_text or "_No clinical report was returned by the agent._")
        return

    if not report_text:
        st.markdown(
            '<div class="ms-urdu-report" dir="rtl">طبی رپورٹ دستیاب نہیں ہے۔</div>',
            unsafe_allow_html=True,
        )
        return

    parts: list[str] = []
    for raw_line in report_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        clean = _clean_markdown_heading(line)

        if _looks_like_report_heading(line):
            parts.append(
                f'<h3 dir="rtl">{_screen_inline_markup(clean)}</h3>'
            )
            continue

        bullet = re.match(r"^(?:[-*•]\\s+)(.+)$", line)
        if bullet:
            parts.append(
                '<div class="ms-urdu-bullet" dir="rtl">'
                '<span class="ms-urdu-marker">•</span>'
                f'<span>{_screen_inline_markup(bullet.group(1))}</span>'
                '</div>'
            )
            continue

        numbered = re.match(r"^(\\d+)[.)]\\s*(.+)$", line)
        if numbered:
            parts.append(
                '<div class="ms-urdu-numbered" dir="rtl">'
                f'<span class="ms-urdu-marker">{numbered.group(1)}.</span>'
                f'<span>{_screen_inline_markup(numbered.group(2))}</span>'
                '</div>'
            )
            continue

        parts.append(
            f'<p dir="rtl">{_screen_inline_markup(line)}</p>'
        )

    st.markdown(
        '<div class="ms-urdu-report" dir="rtl">'
        + "".join(parts)
        + "</div>",
        unsafe_allow_html=True,
    )


def render_findings(
    findings: list[dict[str, Any]],
    language: str = "English",
) -> None:
    """Render model findings and confidence bars."""
    urdu = _is_urdu(language)
    rtl_class = " ms-rtl" if urdu else ""

    if not findings:
        empty_text = (
            "ماڈل کی مقررہ حد سے اوپر کوئی نمایاں نتیجہ نہیں ملا۔ "
            "اس کا مطلب یہ نہیں کہ اسکین مکمل طور پر نارمل ہے؛ ڈاکٹر کا جائزہ ضروری ہے۔"
            if urdu
            else
            "No pathology exceeded the current model display threshold for this scan. "
            "This does not establish a normal study; clinical review remains required."
        )
        rows_html = f'<div class="ms-empty-findings">{esc(empty_text)}</div>'
    else:
        sorted_findings = sorted(
            findings,
            key=lambda item: float(item.get("confidence", 0) or 0),
            reverse=True,
        )

        row_parts: list[str] = []
        for item in sorted_findings:
            label = esc(_localized_finding_label(item.get("label", "Finding"), language))
            confidence = max(
                0.0,
                min(1.0, float(item.get("confidence", 0) or 0)),
            )
            pct = confidence * 100

            row_parts.append(
                '<div class="ms-finding-row">'
                '<div class="ms-finding-head">'
                f'<div class="ms-finding-name">{label}</div>'
                f'<div class="ms-finding-score">{pct:.1f}%</div>'
                '</div>'
                '<div class="ms-track">'
                f'<div class="ms-fill" style="width:{pct:.1f}%"></div>'
                '</div>'
                '</div>'
            )

        rows_html = "".join(row_parts)

    mini_label = "ماڈل کا مشاہدہ" if urdu else "Model observations"
    title = "نمایاں نتائج" if urdu else "Detected findings"

    findings_html = (
        f'<div class="ms-findings-shell{rtl_class}" dir="{"rtl" if urdu else "ltr"}">'
        f'<div class="ms-mini-label">{esc(mini_label)}</div>'
        f'<div class="ms-panel-title" style="margin-top:.45rem;">{esc(title)}</div>'
        f'{rows_html}'
        '</div>'
    )

    st.markdown(findings_html, unsafe_allow_html=True)


def render_urgency(
    urgency: str,
    escalated: bool,
    language: str = "English",
) -> None:
    urdu = _is_urdu(language)
    rtl_class = " ms-rtl" if urdu else ""

    if urdu:
        captions = {
            "routine": "فوری خطرے کی درجہ بندی سامنے نہیں آئی۔",
            "urgent": "ترجیحی طبی جائزہ جلد کرنے کی سفارش کی گئی ہے۔",
            "critical": "نتیجہ انتہائی فوری طبی جائزے کا تقاضا کرتا ہے۔",
        }
        urgency_name = _localized_urgency(urgency, language)
        code = f"درجہ بندی / {urgency_name}"
    else:
        captions = {
            "routine": "No critical escalation was returned by the agent.",
            "urgent": "Prioritized clinical review is recommended by the agent output.",
            "critical": "Critical classification returned by the agent workflow.",
        }
        urgency_name = urgency
        code = f"TRIAGE / {urgency.upper()}"

    st.markdown(
        f"""
        <div class="ms-urgency{rtl_class}" dir="{"rtl" if urdu else "ltr"}">
            <div class="ms-urgency-left">
                <span class="ms-urgency-dot {esc(urgency)}"></span>
                <div>
                    <div class="ms-urgency-name">{esc(urgency_name)}</div>
                    <div class="ms-urgency-caption">{esc(captions.get(urgency, captions['routine']))}</div>
                </div>
            </div>
            <div class="ms-urgency-code">{esc(code)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if escalated:
        alert = (
            "یہ تجزیہ فوری طبی جائزے کے لیے نشان زد کیا گیا ہے۔"
            if urdu
            else
            "The analysis was flagged for escalation and requires prioritized clinical review."
        )
        st.markdown(
            f'<div class="ms-critical-alert" dir="{"rtl" if urdu else "ltr"}">{esc(alert)}</div>',
            unsafe_allow_html=True,
        )


def render_trace(
    trace: list[dict[str, Any]],
    language: str = "English",
) -> None:
    """Render the agent workflow; Urdu mode stays fully Urdu and RTL."""
    urdu = _is_urdu(language)
    if not trace:
        message = "اس تجزیے کے لیے کوئی مرحلہ دستیاب نہیں ہے۔" if urdu else "No agent tool trace was returned for this run."
        st.markdown(
            f'<div class="ms-empty-findings" dir="{"rtl" if urdu else "ltr"}" style="text-align:{"right" if urdu else "left"};">{esc(message)}</div>',
            unsafe_allow_html=True,
        )
        return

    item_parts: list[str] = []
    for idx, step in enumerate(trace, start=1):
        tool_name = str(step.get("tool", "agent_step"))
        if urdu:
            title = _localized_audit_step(tool_name, language)
            desc = "تجزیے کا مرحلہ مکمل کیا گیا۔"
            args_html = ""
        else:
            title = tool_name.replace("_", " ")
            desc = trace_description(tool_name)
            args_html = f'<div class="ms-trace-args">{esc(compact_args(step.get("args", {})))}</div>'

        item_parts.append(
            '<div class="ms-trace-item">'
            f'<div class="ms-trace-no">{idx:02d}</div>'
            '<div>'
            f'<div class="ms-trace-tool">{esc(title)}</div>'
            f'<div class="ms-trace-desc">{esc(desc)}</div>'
            f'{args_html}'
            '</div>'
            '</div>'
        )

    rtl_class = " ms-rtl" if urdu else ""
    st.markdown(
        f'<div class="ms-trace-shell{rtl_class}" dir="{"rtl" if urdu else "ltr"}">' + ''.join(item_parts) + '</div>',
        unsafe_allow_html=True,
    )


def export_text(
    scan_name: str,
    language: str,
    findings: list[dict[str, Any]],
    result: dict[str, Any],
) -> str:
    localized_result = _localize_result_for_language(result, language)
    urgency = normalize_urgency(localized_result.get("urgency"))

    finding_lines = []
    for item in sorted(
        findings,
        key=lambda x: float(x.get("confidence", 0) or 0),
        reverse=True,
    ):
        label = _localized_finding_label(item.get("label", "Finding"), language)
        pct = float(item.get("confidence", 0) or 0) * 100
        finding_lines.append(f"- {label}: {pct:.1f}%")

    if not finding_lines:
        finding_lines = [
            "- ماڈل کی مقررہ حد سے اوپر کوئی نمایاں نتیجہ نہیں ملا۔"
            if _is_urdu(language)
            else "- No displayed finding exceeded the model threshold."
        ]

    if _is_urdu(language):
        return f"""میڈ اسکرائب اے آئی — ریڈیولوجی انٹیلیجنس
اے آئی معاون ریڈیولوجی تجزیہ

اسکین
فائل: {scan_name}
مریض کی زبان: اردو

ماڈل کے نتائج
{chr(10).join(finding_lines)}

طبی رپورٹ
{localized_result.get('clinical_report') or 'طبی رپورٹ دستیاب نہیں ہے۔'}

فوری نوعیت
{_localized_urgency(urgency, language)}

مریض کے لیے آسان خلاصہ
{localized_result.get('patient_summary') or 'مریض کا خلاصہ دستیاب نہیں ہے۔'}

اہم نوٹ
یہ اے آئی معاون رپورٹ صرف طبی فیصلہ سازی میں مدد کے لیے ہے۔ حتمی تشخیص کے لیے مستند ڈاکٹر کا جائزہ ضروری ہے۔
"""

    return f"""MEDSCRIBE AI — RADIOLOGY INTELLIGENCE
AI-assisted radiology analysis

SCAN
File: {scan_name}
Patient output language: {language}

MODEL FINDINGS
{chr(10).join(finding_lines)}

CLINICAL REPORT
{localized_result.get('clinical_report') or 'No report returned.'}

URGENCY
{urgency.upper()}

PATIENT SUMMARY
{localized_result.get('patient_summary') or 'No patient summary returned.'}

DISCLAIMER
This AI-assisted output requires qualified clinical review and is not a standalone diagnosis.
"""



def _pdf_normalize_text(value: Any) -> str:
    """Normalize report text and restore escaped line breaks for readable output."""
    value = "" if value is None else str(value)

    # Some agent payloads arrive with literal "\\n" sequences. They are data
    # serialization artifacts, not content the end user should ever see.
    value = (
        value.replace("\\r\\n", "\n")
        .replace("\\n", "\n")
        .replace("\\t", " ")
    )

    replacements = {
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
        "\u2022": "-",
        "\u2713": "[OK]",
        "\u2714": "[OK]",
        "\u26a0": "اہم:",
        "\u2757": "اہم:",
        "\u2705": "[OK]",
        "\u2139": "معلومات:",
        "\U0001f4cb": "",
        "\U0001f4a1": "",
        "\U0001f6a8": "اہم:",
        "\u00a0": " ",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
    }
    for source, target in replacements.items():
        value = value.replace(source, target)

    # ReportLab does not provide font fallback inside a Paragraph. Remove
    # remaining emoji and pictographs that Noto Naskh Arabic cannot render.
    value = re.sub(
        r"[\U0001F000-\U0001FAFF\U00002600-\U000027BF\uFE0F\u20E3]",
        "",
        value,
    )

    # Remove invisible Unicode formatting controls that some PDF renderers
    # display as empty rectangular glyphs ("tofu").
    value = re.sub(
        r"[\u200b-\u200f\u202a-\u202e\u2066-\u2069\ufeff]",
        "",
        value,
    )

    # Replace replacement/tofu-style characters instead of exporting boxes.
    value = value.replace("\ufffd", "")
    value = value.replace("\u25a1", "")
    value = value.replace("\u25a0", "")

    # Tidy excessive whitespace while preserving paragraph boundaries.
    value = re.sub(r"[ \t]+\n", "\n", value)
    value = re.sub(r"\n[ \t]+", "\n", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()



def _is_urdu(language: Any) -> bool:
    return str(language or "").strip().lower() == "urdu"


def _contains_urdu(value: Any) -> bool:
    return bool(re.search(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]", str(value or "")))


def _has_latin_letters(value: Any) -> bool:
    return bool(re.search(r"[A-Za-z]", str(value or "")))


@st.cache_data(show_spinner=False, ttl=86400)
def _translate_medical_text_to_urdu(text_value: str, purpose: str) -> str:
    """
    Faithfully translate generated report text into clear Urdu.
    This uses the same Groq service already used by the MedScribe pipeline.
    """
    source = _pdf_normalize_text(text_value)
    if not source:
        return source

    if Groq is None:
        raise RuntimeError("Groq package is required for complete Urdu report translation.")

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is required for complete Urdu report translation.")

    client = Groq(api_key=api_key)
    model = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")

    system_prompt = (
        "You are a professional medical translator for a radiology reporting system. "
        "Translate the supplied content into clear, natural Urdu written in Urdu script. "
        "Preserve the medical meaning exactly. Do not add, remove, diagnose beyond, or reinterpret facts. "
        "Keep all percentages and numbers unchanged. "
        "Translate or transliterate ALL English medical terms and abbreviations into Urdu script "
        "(for example X-ray -> ایکس رے, CT -> سی ٹی, CBC -> سی بی سی, CRP -> سی آر پی). "
        "Do not leave Latin/English words in the answer. "
        "Keep report section headings on separate lines. "
        "Use these Urdu headings when applicable: "
        "FINDINGS=نتائج, IMPRESSION=تاثر, RECOMMENDATION=تجویز, "
        "URGENCY=فوری نوعیت, REASONING=وجہ اور تشریح. "
        "Return only the translated Urdu text with no commentary."
    )

    response = client.chat.completions.create(
        model=model,
        temperature=0.1,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"مواد کی قسم: {purpose}\n\n{source}",
            },
        ],
    )
    translated = _pdf_normalize_text(response.choices[0].message.content or "")

    # One strict retry if the model leaves Latin text behind.
    if _has_latin_letters(translated):
        retry = client.chat.completions.create(
            model=model,
            temperature=0.0,
            messages=[
                {
                    "role": "system",
                    "content": (
                        system_prompt
                        + " IMPORTANT: Your previous answer still contained Latin/English letters. "
                          "Rewrite it so there are ZERO A-Z or a-z letters anywhere."
                    ),
                },
                {"role": "user", "content": translated},
            ],
        )
        translated = _pdf_normalize_text(retry.choices[0].message.content or translated)

    return translated


def _translate_result_bundle_to_urdu(result: dict[str, Any]) -> dict[str, str]:
    """
    Translate the two user-visible report bodies in one request.

    This is a fallback used only if the normal per-section localization path fails.
    The medical analysis itself is already complete in English at this point.
    """
    if Groq is None:
        raise RuntimeError("Groq is unavailable for Urdu localization.")

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is unavailable for Urdu localization.")

    clinical_report = _pdf_normalize_text(result.get("clinical_report") or "")
    patient_summary = _pdf_normalize_text(result.get("patient_summary") or "")

    client = Groq(api_key=api_key)
    model = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")

    system_prompt = (
        "You are the Urdu localization layer of a radiology reporting application. "
        "The medical analysis is already finished and MUST NOT be changed. "
        "Translate both supplied fields into clear, natural Urdu script. "
        "Preserve every diagnosis, confidence percentage, recommendation, urgency level, "
        "number and clinical fact exactly. Do not add or remove medical information. "
        "Do not leave English prose. Transliterate necessary medical terms into Urdu script. "
        "Use clear section headings on separate lines. "
        "Return ONLY valid JSON with exactly these keys: clinical_report, patient_summary."
    )

    payload = json.dumps(
        {
            "clinical_report": clinical_report,
            "patient_summary": patient_summary,
        },
        ensure_ascii=False,
    )

    response = client.chat.completions.create(
        model=model,
        temperature=0.0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": payload},
        ],
    )

    content = response.choices[0].message.content or "{}"
    parsed = json.loads(content)

    localized_clinical = _pdf_normalize_text(parsed.get("clinical_report") or "")
    localized_patient = _pdf_normalize_text(parsed.get("patient_summary") or "")

    if not localized_clinical or not _contains_urdu(localized_clinical):
        raise RuntimeError("Urdu clinical report localization returned no usable Urdu text.")
    if not localized_patient or not _contains_urdu(localized_patient):
        raise RuntimeError("Urdu patient summary localization returned no usable Urdu text.")

    return {
        "clinical_report": localized_clinical,
        "patient_summary": localized_patient,
    }


def _localize_result_for_language_safe(
    result: dict[str, Any],
    language: str,
) -> dict[str, Any]:
    """
    Never send Urdu into the clinical reasoning pipeline.

    The core result is generated first in English; this function then converts only
    the presentation text to Urdu. Two localization strategies are attempted before
    reporting a failure.
    """
    if not _is_urdu(language):
        return dict(result)

    try:
        localized = _localize_result_for_language(result, language)
        clinical = _pdf_normalize_text(localized.get("clinical_report") or "")
        patient = _pdf_normalize_text(localized.get("patient_summary") or "")

        if clinical and patient and _contains_urdu(clinical) and _contains_urdu(patient):
            return localized
    except Exception as first_error:
        print(
            "[MedScribe AI] Primary Urdu localization failed: "
            f"{type(first_error).__name__}: {first_error}"
        )

    # One combined fallback request is often more reliable than two independent
    # translation calls and avoids rerunning the medical agent.
    bundle = _translate_result_bundle_to_urdu(result)

    localized = dict(result)
    localized["clinical_report"] = bundle["clinical_report"]
    localized["patient_summary"] = bundle["patient_summary"]
    localized["display_language"] = "Urdu"
    return localized


def _extract_patient_summary(result: dict[str, Any], language: str) -> str:
    """Prefer an Urdu-native patient summary when the backend already returned one."""
    if _is_urdu(language):
        candidates = [
            result.get("patient_summary_urdu"),
            result.get("urdu_patient_summary"),
            result.get("patient_summary"),
        ]

        final_message = result.get("final_message")
        if isinstance(final_message, dict):
            candidates.extend([
                final_message.get("patient_summary_urdu"),
                final_message.get("urdu_patient_summary"),
                final_message.get("patient_summary"),
            ])
        elif isinstance(final_message, str):
            try:
                parsed = json.loads(final_message)
                if isinstance(parsed, dict):
                    candidates.extend([
                        parsed.get("patient_summary_urdu"),
                        parsed.get("urdu_patient_summary"),
                        parsed.get("patient_summary"),
                    ])
            except Exception:
                pass

        for candidate in candidates:
            if candidate and _contains_urdu(candidate):
                # Even if it is mostly Urdu, remove any remaining English/Latin fragments.
                if _has_latin_letters(candidate):
                    return _translate_medical_text_to_urdu(
                        str(candidate),
                        "مریض کے لیے آسان خلاصہ",
                    )
                return _pdf_normalize_text(candidate)

        fallback = result.get("patient_summary") or ""
        return _translate_medical_text_to_urdu(
            fallback,
            "مریض کے لیے آسان خلاصہ",
        )

    return _pdf_normalize_text(result.get("patient_summary") or "")


def _localize_result_for_language(
    result: dict[str, Any],
    language: str,
) -> dict[str, Any]:
    """For Urdu, localize the entire generated clinical content before display/export."""
    localized = dict(result)

    if not _is_urdu(language):
        return localized

    clinical_report = (
        result.get("clinical_report_urdu")
        or result.get("urdu_clinical_report")
        or result.get("clinical_report")
        or ""
    )
    if clinical_report:
        if not _contains_urdu(clinical_report) or _has_latin_letters(clinical_report):
            clinical_report = _translate_medical_text_to_urdu(
                clinical_report,
                "مکمل طبی ریڈیولوجی رپورٹ",
            )
        else:
            clinical_report = _pdf_normalize_text(clinical_report)

    localized["clinical_report"] = clinical_report
    localized["patient_summary"] = _extract_patient_summary(result, language)
    return localized


URDU_FINDING_LABELS = {
    "NORMAL": "معمول کے مطابق",
    "PNEUMONIA": "نمونیا",
    "ATELECTASIS": "پھیپھڑے کا سکڑاؤ",
    "CONSOLIDATION": "پھیپھڑے میں کثافت",
    "INFILTRATION": "پھیپھڑے میں سوزشی تبدیلیاں",
    "PNEUMOTHORAX": "نیوموتھوریکس",
    "EDEMA": "پھیپھڑوں میں ورم",
    "EMPHYSEMA": "ایمفیسیما",
    "FIBROSIS": "فائبروسس",
    "EFFUSION": "پھیپھڑوں کے گرد سیال",
    "PLEURAL THICKENING": "پلورا کی موٹائی",
    "PLEURAL_THICKENING": "پلورا کی موٹائی",
    "CARDIOMEGALY": "دل کا بڑھ جانا",
    "NODULE": "چھوٹی گلٹی",
    "MASS": "گلٹی",
    "HERNIA": "ہرنیا",
    "LUNG LESION": "پھیپھڑے کا زخم",
    "LUNG LESION": "پھیپھڑے کا زخم",
    "FRACTURE": "ہڈی کا فریکچر",
    "LUNG OPACITY": "پھیپھڑوں میں دھندلا پن",
    "ENLARGED CARDIOMEDIASTINUM": "دل اور وسطی سینے کا پھیلاؤ",
}


def _localized_finding_label(label: Any, language: str) -> str:
    raw = _pdf_normalize_text(label or "Finding")
    if not _is_urdu(language):
        return raw
    key = raw.strip().upper()
    return URDU_FINDING_LABELS.get(key, raw)


def _localized_urgency(urgency: str, language: str) -> str:
    if not _is_urdu(language):
        return urgency.upper()
    return {
        "routine": "معمول",
        "urgent": "فوری",
        "critical": "انتہائی فوری",
    }.get(urgency, "معمول")


def _urdu_datetime_now() -> str:
    month_names = {
        1: "جنوری", 2: "فروری", 3: "مارچ", 4: "اپریل",
        5: "مئی", 6: "جون", 7: "جولائی", 8: "اگست",
        9: "ستمبر", 10: "اکتوبر", 11: "نومبر", 12: "دسمبر",
    }
    now = datetime.now()
    return f"{now.day} {month_names[now.month]} {now.year}، {now:%H:%M}"


def _pdf_display(value: Any, language: str) -> str:
    """Escape and shape Urdu for ReportLab; preserve ordinary text otherwise."""
    value = _pdf_normalize_text(value)
    if _is_urdu(language):
        return html.escape(_shape_rtl_text(value))
    return html.escape(value)


def _localized_audit_step(tool_name: str, language: str) -> str:
    if not _is_urdu(language):
        return _friendly_audit_step(tool_name)
    labels = {
        "detect_findings": "ایکس رے میں ممکنہ غیر معمولی تبدیلیوں کا جائزہ لیا گیا",
        "write_clinical_report": "طبی رپورٹ تیار کی گئی",
        "assess_urgency": "نتیجے کی فوری نوعیت کا جائزہ لیا گیا",
        "write_patient_summary": "مریض کے لیے آسان وضاحت تیار کی گئی",
        "escalate_to_doctor": "معاملہ ڈاکٹر کے فوری جائزے کے لیے نشان زد کیا گیا",
    }
    return labels.get(tool_name, "تجزیے کا ایک مرحلہ مکمل کیا گیا")


def _ensure_runtime_urdu_font() -> tuple[str | None, str | None]:
    """
    Obtain Noto Naskh Arabic without bundling font files in the project.
    Deployment environments with fonts-noto-core installed use the system font;
    otherwise the font is cached at runtime from the official Noto repository.
    """
    cache_dir = Path("/tmp/medscribe_fonts")
    cache_dir.mkdir(parents=True, exist_ok=True)

    regular_dest = cache_dir / "NotoSansArabic-Regular.ttf"
    bold_dest = cache_dir / "NotoSansArabic-Bold.ttf"

    urls = {
        regular_dest: [
            "https://raw.githubusercontent.com/notofonts/noto-fonts/main/hinted/ttf/NotoSansArabic/NotoSansArabic-Regular.ttf",
            "https://raw.githubusercontent.com/googlefonts/noto-fonts/main/hinted/ttf/NotoSansArabic/NotoSansArabic-Regular.ttf",
        ],
        bold_dest: [
            "https://raw.githubusercontent.com/notofonts/noto-fonts/main/hinted/ttf/NotoSansArabic/NotoSansArabic-Bold.ttf",
            "https://raw.githubusercontent.com/googlefonts/noto-fonts/main/hinted/ttf/NotoSansArabic/NotoSansArabic-Bold.ttf",
        ],
    }

    for destination, candidates in urls.items():
        if destination.exists() and destination.stat().st_size > 50_000:
            continue

        for url in candidates:
            try:
                request = urllib.request.Request(
                    url,
                    headers={"User-Agent": "MedScribe-AI/1.0"},
                )
                with urllib.request.urlopen(request, timeout=12) as response:
                    payload = response.read()

                if len(payload) > 50_000:
                    destination.write_bytes(payload)
                    break
            except Exception:
                continue

    regular = str(regular_dest) if regular_dest.exists() and regular_dest.stat().st_size > 50_000 else None
    bold = str(bold_dest) if bold_dest.exists() and bold_dest.stat().st_size > 50_000 else None
    return regular, bold


def _register_pdf_fonts(language: str = "English") -> tuple[str, str]:
    """Register Unicode fonts. Urdu export requires a real Urdu-capable Noto font."""

    def first_existing(candidates: list[str | None]) -> str | None:
        for candidate in candidates:
            if candidate and Path(candidate).exists():
                return candidate
        return None

    if _is_urdu(language):
        # Noto Naskh Arabic contains the Urdu glyphs that generic DejaVu fallback
        # is missing (for example ہ, ے and ۓ).
        regular_candidates: list[str | None] = [
            "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf",
            "/usr/share/fonts/opentype/noto/NotoNaskhArabic-Regular.ttf",
            "/usr/local/share/fonts/NotoNaskhArabic-Regular.ttf",
        ]
        bold_candidates: list[str | None] = [
            "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf",
            "/usr/share/fonts/opentype/noto/NotoNaskhArabic-Bold.ttf",
            "/usr/local/share/fonts/NotoNaskhArabic-Bold.ttf",
        ]

        windows_font_dirs = [
            Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "Windows" / "Fonts",
            Path(os.environ.get("WINDIR", "C:\\Windows")) / "Fonts",
        ]
        regular_candidates.extend(
            str(font_dir / filename)
            for font_dir in windows_font_dirs
            for filename in ("NotoNaskhArabic.ttf", "NotoNaskhArabic-Regular.ttf")
        )
        bold_candidates.extend(
            str(font_dir / filename)
            for font_dir in windows_font_dirs
            for filename in ("NotoNaskhArabic-Bold.ttf",)
        )

        regular_path = first_existing(regular_candidates)
        bold_path = first_existing(bold_candidates)

        if not regular_path:
            runtime_regular, runtime_bold = _ensure_runtime_urdu_font()
            regular_path = runtime_regular
            bold_path = runtime_bold or bold_path

        if not regular_path:
            raise RuntimeError(
                "Urdu PDF font could not be loaded. Install the system package "
                "'fonts-noto-core' or allow the app to download Noto Naskh Arabic."
            )

        if "MedScribeUrdu" not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont("MedScribeUrdu", regular_path))

        bold_name = "MedScribeUrdu"
        if bold_path:
            if "MedScribeUrdu-Bold" not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont("MedScribeUrdu-Bold", bold_path))
            bold_name = "MedScribeUrdu-Bold"
            pdfmetrics.registerFontFamily(
                "MedScribeUrdu",
                normal="MedScribeUrdu",
                bold=bold_name,
                italic="MedScribeUrdu",
                boldItalic=bold_name,
            )

        return "MedScribeUrdu", bold_name

    # English/non-Urdu export.
    regular_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    ]
    bold_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    ]

    regular_path = first_existing(regular_candidates)
    bold_path = first_existing(bold_candidates)

    if regular_path:
        if "MedScribeSans" not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont("MedScribeSans", regular_path))
        if bold_path and "MedScribeSans-Bold" not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont("MedScribeSans-Bold", bold_path))
        if bold_path:
            pdfmetrics.registerFontFamily(
                "MedScribeSans",
                normal="MedScribeSans",
                bold="MedScribeSans-Bold",
                italic="MedScribeSans",
                boldItalic="MedScribeSans-Bold",
            )
            return "MedScribeSans", "MedScribeSans-Bold"
        return "MedScribeSans", "MedScribeSans"

    return "Helvetica", "Helvetica-Bold"


def _pdf_inline_markup(value: Any) -> str:
    """Convert a restrained subset of Markdown bold syntax to ReportLab markup."""
    safe = html.escape(_pdf_normalize_text(value))
    safe = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", safe)
    return safe


def _shape_rtl_text(value: Any) -> str:
    """Shape Urdu/Arabic/Persian when optional dependencies are available."""
    text_value = _pdf_normalize_text(value)
    if arabic_reshaper is not None and bidi_get_display is not None:
        try:
            return bidi_get_display(arabic_reshaper.reshape(text_value))
        except Exception:
            return text_value
    return text_value


def _image_source_to_png_bytes(source: Any) -> bytes:
    """Convert path, PIL image, or numpy-like heatmap to RGB PNG bytes."""
    if isinstance(source, (str, Path)):
        image = PILImage.open(source)
    elif isinstance(source, PILImage.Image):
        image = source.copy()
    else:
        array = np.asarray(source)
        if array.size == 0:
            raise ValueError("Image source is empty")

        if np.issubdtype(array.dtype, np.floating):
            finite = array[np.isfinite(array)]
            max_value = float(finite.max()) if finite.size else 1.0
            if max_value <= 1.0:
                array = array * 255.0
            array = np.nan_to_num(array, nan=0.0, posinf=255.0, neginf=0.0)

        array = np.clip(array, 0, 255).astype(np.uint8)
        if array.ndim == 2:
            image = PILImage.fromarray(array, mode="L")
        elif array.ndim == 3 and array.shape[-1] in (3, 4):
            image = PILImage.fromarray(array)
        else:
            raise ValueError(f"Unsupported image shape for PDF export: {array.shape}")

    if image.mode in {"RGBA", "LA"}:
        rgba = image.convert("RGBA")
        background = PILImage.new("RGB", rgba.size, (7, 17, 31))
        background.paste(rgba, mask=rgba.getchannel("A"))
        image = background
    elif image.mode != "RGB":
        image = image.convert("RGB")

    output = io.BytesIO()
    image.save(output, format="PNG", optimize=True)
    return output.getvalue()


def _pdf_image(source: Any, max_width: float, max_height: float) -> Any:
    png_bytes = _image_source_to_png_bytes(source)
    probe = PILImage.open(io.BytesIO(png_bytes))
    width_px, height_px = probe.size
    scale = min(max_width / width_px, max_height / height_px)
    scale = max(scale, 0.01)
    return RLImage(
        io.BytesIO(png_bytes),
        width=width_px * scale,
        height=height_px * scale,
    )


def _clean_markdown_heading(value: str) -> str:
    value = re.sub(r"^[#\s]+", "", value.strip())
    value = value.strip("* _:-")
    return re.sub(r"\s+", " ", value).strip()


def _looks_like_report_heading(line: str) -> bool:
    """Identify short report headings without treating normal sentences as headings."""
    clean = _clean_markdown_heading(line)
    if not clean:
        return False

    if line.lstrip().startswith("#"):
        return True

    if line.startswith("**") and line.endswith("**") and len(clean) <= 80:
        return True

    canonical = {
        "FINDINGS",
        "IMPRESSION",
        "RECOMMENDATION",
        "RECOMMENDATIONS",
        "URGENCY",
        "REASONING",
        "CLINICAL FINDINGS",
        "CLINICAL IMPRESSION",
        "NEXT STEPS",
        "WHAT THIS MEANS",
        "WHAT THIS MEANS FOR YOU",
        "WHAT THE SCAN SHOWS",
        "WHY THIS MATTERS",
    }
    urdu_headings = {
        "نتائج",
        "تاثر",
        "تجویز",
        "تجاویز",
        "فوری نوعیت",
        "وجہ",
        "وجہ اور تشریح",
        "طبی نتائج",
        "طبی تاثر",
        "اگلے اقدامات",
        "اس کا کیا مطلب ہے",
        "اسکین کیا دکھاتا ہے",
        "یہ کیوں اہم ہے",
    }
    if clean.upper() in canonical or clean in urdu_headings:
        return True

    return (
        len(clean) <= 55
        and clean.upper() == clean
        and any(ch.isalpha() for ch in clean)
        and not clean.endswith(".")
    )


def _markdown_report_flowables(
    report_text: str,
    styles: dict[str, Any],
    language: str = "English",
) -> list[Any]:
    """Convert the structured report into headings, bullets, and paragraphs."""
    flowables: list[Any] = []
    normalized = _pdf_normalize_text(report_text or "No clinical report was returned.")
    lines = normalized.splitlines()

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            flowables.append(Spacer(1, 1.8 * mm))
            continue

        if _looks_like_report_heading(line):
            heading = _clean_markdown_heading(line)
            if not _is_urdu(language):
                heading = heading.title()
            flowables.append(
                Paragraph(_pdf_display(heading, language), styles["report_heading"])
            )
            continue

        bullet_match = re.match(r"^(?:[-*•]\s+)(.+)$", line)
        if bullet_match:
            body = bullet_match.group(1).strip()
            display = f"- {body}"
            if _is_urdu(language):
                flowables.append(
                    Paragraph(_pdf_display(display, language), styles["bullet"])
                )
            else:
                flowables.append(
                    Paragraph("- " + _pdf_inline_markup(body), styles["bullet"])
                )
            continue

        number_match = re.match(r"^(\d+)[.)]\s*(.+)$", line)
        if number_match:
            display = f"{number_match.group(1)}. {number_match.group(2)}"
            if _is_urdu(language):
                flowables.append(
                    Paragraph(_pdf_display(display, language), styles["bullet"])
                )
            else:
                flowables.append(
                    Paragraph(
                        f"{number_match.group(1)}. "
                        + _pdf_inline_markup(number_match.group(2)),
                        styles["bullet"],
                    )
                )
            continue

        if _is_urdu(language):
            flowables.append(
                Paragraph(_pdf_display(line, language), styles["body"])
            )
        else:
            flowables.append(Paragraph(_pdf_inline_markup(line), styles["body"]))

    return flowables


def _patient_summary_flowables(
    patient_text: str,
    language: str,
    styles: dict[str, Any],
) -> list[Any]:
    """Render patient communication as readable headings and short blocks."""
    is_rtl = _is_urdu(language) or (language or "").strip().lower() in {"arabic", "persian"}
    normalized = _pdf_normalize_text(
        patient_text or "No patient summary was returned."
    )

    flowables: list[Any] = []
    for raw_line in normalized.splitlines():
        line = raw_line.strip()
        if not line:
            flowables.append(Spacer(1, 1.8 * mm))
            continue

        clean = _clean_markdown_heading(line)
        is_heading = (
            (line.startswith("**") and line.endswith("**") and len(clean) <= 90)
            or clean in {
                "اسکین کیا دکھاتا ہے",
                "اس کا آپ کے لیے کیا مطلب ہے",
                "اگلے اقدامات",
                "یہ کتنا فوری ہے؟",
                "یہ کتنا فوری ہے",
                "اب آگے کیا ہوگا",
            }
            or (
                not is_rtl
                and (
                    (len(clean) <= 70 and clean.upper() == clean and any(ch.isalpha() for ch in clean))
                    or clean.lower() in {
                        "what the scan shows",
                        "what this means for you",
                        "next steps",
                        "how urgent is this?",
                        "how urgent is this",
                        "what happens next",
                    }
                )
            )
        )

        if is_heading:
            flowables.append(
                Paragraph(_pdf_display(clean, language), styles["patient_heading"])
            )
            continue

        bullet_match = re.match(r"^(?:[-*•]\s+)(.+)$", line)
        number_match = re.match(r"^(\d+)[.)]\s*(.+)$", line)

        if bullet_match:
            body = f"- {bullet_match.group(1).strip()}"
            flowables.append(
                Paragraph(
                    _pdf_display(body, language) if is_rtl else _pdf_inline_markup(body),
                    styles["patient_bullet"],
                )
            )
            continue

        if number_match:
            body = f"{number_match.group(1)}. {number_match.group(2).strip()}"
            flowables.append(
                Paragraph(
                    _pdf_display(body, language) if is_rtl else _pdf_inline_markup(body),
                    styles["patient_bullet"],
                )
            )
            continue

        flowables.append(
            Paragraph(
                _pdf_display(clean, language) if is_rtl else _pdf_inline_markup(clean),
                styles["patient"],
            )
        )

    return flowables


def _friendly_audit_step(tool_name: str) -> str:
    """Human-readable processing step for the exported report."""
    labels = {
        "detect_findings": "Reviewed the X-ray for visible abnormalities",
        "write_clinical_report": "Prepared the clinician-facing report",
        "assess_urgency": "Checked how urgently the result should be reviewed",
        "write_patient_summary": "Prepared the patient-friendly explanation",
        "escalate_to_doctor": "Flagged the study for clinician review",
    }
    return labels.get(tool_name, "Completed an analysis step")


def _resolve_urdu_raster_font() -> str:
    """
    Resolve an Urdu-capable font for Pillow/RAQM.

    Prefer Noto Sans Arabic because it covers Urdu letters plus ordinary report
    punctuation. Noto Naskh remains a fallback after punctuation sanitization.
    """
    system_candidates = [
        "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansArabic-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansArabicUI-Regular.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansArabicUI-Regular.ttf",
        "/usr/local/share/fonts/NotoSansArabic-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf",
        "/usr/share/fonts/opentype/noto/NotoNaskhArabic-Regular.ttf",
        "/usr/local/share/fonts/NotoNaskhArabic-Regular.ttf",
    ]
    for candidate in system_candidates:
        if Path(candidate).exists():
            return candidate

    # Portable Python-package fallback. `khatt` bundles open-source Arabic fonts.
    try:
        root = importlib_resources.files("khatt")
        stack = [root]
        naskh_fallback = None
        other_fallback = None

        while stack:
            node = stack.pop()
            try:
                children = list(node.iterdir())
            except Exception:
                continue

            for child in children:
                try:
                    if child.is_dir():
                        stack.append(child)
                        continue
                except Exception:
                    pass

                name = getattr(child, "name", "").lower()
                if not name.endswith((".ttf", ".otf")):
                    continue

                path = str(child)

                if "noto" in name and "sans" in name and "arabic" in name:
                    return path

                if (
                    naskh_fallback is None
                    and "noto" in name
                    and "naskh" in name
                    and "arabic" in name
                ):
                    naskh_fallback = path

                if other_fallback is None and (
                    "arabic" in name or "amiri" in name or "cairo" in name
                ):
                    other_fallback = path

        if naskh_fallback:
            return naskh_fallback
        if other_fallback:
            return other_fallback
    except Exception:
        pass

    regular, _ = _ensure_runtime_urdu_font()
    if regular and Path(regular).exists():
        return regular

    raise RuntimeError(
        "Urdu PDF font is unavailable. Redeploy with the updated requirements.txt."
    )


def _pil_urdu_font(font_path: str, size: int) -> Any:
    layout = getattr(ImageFont, "Layout", None)
    kwargs = {"layout_engine": layout.RAQM} if layout is not None and PILFeatures.check("raqm") else {}
    return ImageFont.truetype(font_path, size=size, **kwargs)


def _pil_rtl_text(value: str) -> tuple[str, bool]:
    """Return text and whether Pillow must use RAQM for shaping."""
    if PILFeatures.check("raqm"):
        return value, True
    return _shape_rtl_text(value), False


def _strip_report_markup(value: Any) -> str:
    """
    Prepare Urdu for raster rendering without missing-glyph rectangles.
    """
    value = _pdf_normalize_text(value)
    value = re.sub(r"^#{1,6}\s*", "", value.strip())
    value = value.replace("**", "").replace("__", "")
    value = value.replace("%", "٪")

    # Natural Urdu rendering of numeric ranges: 48-72 -> 48 تا 72.
    value = re.sub(
        r"(?<=\d)\s*[-‐‑‒–—−]\s*(?=\d)",
        " تا ",
        value,
    )

    # Sentence dashes become an Urdu comma. Several Arabic-only fonts do not
    # contain the decorative dash glyphs and render them as empty rectangles.
    value = re.sub(r"[-‐‑‒–—−]+", "،", value)

    # Decorative bullets/squares/diamonds are removed. Layout provides the list
    # structure, so these symbols are unnecessary and were another source of boxes.
    value = re.sub(r"[•▪●◦‣∙·■□◆◇►▶◀◼◻]+", " ", value)

    value = re.sub(
        r"[\u200b-\u200f\u202a-\u202e\u2066-\u2069\ufeff]",
        "",
        value,
    )
    value = value.replace("\ufffd", "")
    value = re.sub(r"[ \t]{2,}", " ", value)
    return value.strip()


def _build_urdu_raster_pdf_report(
    scan_name: str,
    findings: list[dict[str, Any]],
    result: dict[str, Any],
    scan_path: str | Path,
    heatmap: Any,
) -> bytes:
    """
    Build the Urdu PDF as high-resolution page images.

    ReportLab itself does not perform OpenType Urdu shaping. The previous approach
    reshaped text into presentation-form code points, and missing presentation-form
    glyphs produced the rectangular boxes the user saw. This path instead lets
    Pillow + RAQM (HarfBuzz/FriBidi) shape the original Urdu Unicode text correctly,
    then places the finished page pixels into the PDF. This removes font-subset/tofu
    failures while preserving a polished clinical-document layout.
    """
    clinical_text = _pdf_normalize_text(result.get("clinical_report") or "")
    patient_text = _pdf_normalize_text(result.get("patient_summary") or "")
    if not clinical_text or not _contains_urdu(clinical_text):
        raise RuntimeError("Urdu clinical report is missing. Run the analysis again with Urdu selected.")
    if not patient_text or not _contains_urdu(patient_text):
        raise RuntimeError("Urdu patient summary is missing. Run the analysis again with Urdu selected.")

    font_path = _resolve_urdu_raster_font()

    DPI = 180
    PAGE_W, PAGE_H = 1488, 2105  # A4-ish at 180 dpi
    MARGIN_X = 105
    CONTENT_TOP = 120
    CONTENT_BOTTOM = 112
    CONTENT_W = PAGE_W - 2 * MARGIN_X

    NAVY = (7, 17, 31)
    NAVY_2 = (11, 23, 40)
    GOLD = (183, 154, 91)
    CHAMPAGNE = (215, 194, 154)
    SLATE = (86, 101, 119)
    TEXT = (39, 51, 66)
    LINE = (218, 224, 232)
    SOFT_BLUE = (238, 243, 248)
    SOFT_GOLD = (247, 242, 232)
    WHITE = (255, 255, 255)
    RED = (184, 79, 89)

    font_cache: dict[int, Any] = {}

    def font(size: int) -> Any:
        if size not in font_cache:
            font_cache[size] = _pil_urdu_font(font_path, size)
        return font_cache[size]

    pages: list[PILImage.Image] = []
    page: PILImage.Image
    draw: Any
    y: int

    def measure(text_value: str, fnt: Any) -> tuple[int, int]:
        probe = ImageDraw.Draw(PILImage.new("RGB", (10, 10), WHITE))
        shaped, use_raqm = _pil_rtl_text(text_value or " ")
        kwargs = {"direction": "rtl", "language": "ur"} if use_raqm else {}
        bbox = probe.textbbox((0, 0), shaped, font=fnt, **kwargs)
        return max(1, bbox[2] - bbox[0]), max(1, bbox[3] - bbox[1])

    def draw_rtl_line(
        canvas: Any,
        text_value: str,
        x_right: int,
        y_top: int,
        fnt: Any,
        fill: tuple[int, int, int],
    ) -> int:
        text_value = _strip_report_markup(text_value)
        if not text_value:
            return 0
        shaped, use_raqm = _pil_rtl_text(text_value)
        kwargs = {"direction": "rtl", "language": "ur"} if use_raqm else {}
        bbox = canvas.textbbox((0, 0), shaped, font=fnt, **kwargs)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        x = x_right - width - bbox[0]
        yy = y_top - bbox[1]
        canvas.text(
            (x, yy),
            shaped,
            font=fnt,
            fill=fill,
            **kwargs,
        )
        return max(height, int(getattr(fnt, "size", 20) * 1.15))

    def wrap_rtl(text_value: str, fnt: Any, max_width: int) -> list[str]:
        text_value = _strip_report_markup(text_value)
        if not text_value:
            return []
        words = text_value.split()
        if not words:
            return []
        lines: list[str] = []
        current = words[0]
        for word in words[1:]:
            candidate = current + " " + word
            width, _ = measure(candidate, fnt)
            if width <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
        return lines

    def add_page() -> None:
        nonlocal page, draw, y
        page = PILImage.new("RGB", (PAGE_W, PAGE_H), WHITE)
        draw = ImageDraw.Draw(page)
        draw.rectangle((0, 0, PAGE_W, 78), fill=NAVY)
        draw_rtl_line(draw, "میڈ اسکرائب اے آئی", PAGE_W - MARGIN_X, 20, font(24), CHAMPAGNE)
        draw_rtl_line(draw, "ریڈیولوجی انٹیلیجنس", MARGIN_X + 260, 24, font(17), (183, 193, 207))
        pages.append(page)
        y = CONTENT_TOP

    def ensure_space(height: int) -> None:
        nonlocal y
        if y + height > PAGE_H - CONTENT_BOTTOM:
            add_page()

    def add_paragraph(
        text_value: str,
        size: int = 25,
        color: tuple[int, int, int] = TEXT,
        max_width: int = CONTENT_W,
        indent: int = 0,
        gap_after: int = 12,
    ) -> None:
        nonlocal y
        fnt = font(size)
        line_gap = max(9, int(size * 0.42))
        lines = wrap_rtl(text_value, fnt, max_width - indent)
        if not lines:
            y += gap_after
            return
        for line in lines:
            _, h = measure(line, fnt)
            line_h = max(int(size * 1.42), h + line_gap)
            ensure_space(line_h + 4)
            draw_rtl_line(draw, line, PAGE_W - MARGIN_X - indent, y, fnt, color)
            y += line_h
        y += gap_after

    def add_heading(text_value: str, size: int = 31, color: tuple[int, int, int] = NAVY, gap_before: int = 12) -> None:
        nonlocal y
        ensure_space(size * 2 + 18)
        y += gap_before
        add_paragraph(text_value, size=size, color=color, gap_after=8)

    def add_structured_text(text_value: str, patient: bool = False) -> None:
        nonlocal y
        for raw in _pdf_normalize_text(text_value).splitlines():
            line = raw.strip()
            if not line:
                y += 8
                continue
            clean = _clean_markdown_heading(line)
            if _looks_like_report_heading(line) or (
                patient
                and clean in {
                    "اسکین کیا دکھاتا ہے",
                    "اس کا آپ کے لیے کیا مطلب ہے",
                    "اگلے اقدامات",
                    "یہ کتنا فوری ہے؟",
                    "اب آگے کیا ہوگا",
                    "آپ کی رپورٹ کا خلاصہ (آسان الفاظ میں)",
                    "آپ کے لیے کیا مطلب ہے؟",
                }
            ):
                add_heading(clean, size=28, color=GOLD if patient else NAVY_2, gap_before=9)
                continue

            bullet = re.match(r"^(?:[-*•]\\s+)(.+)$", line)
            if bullet:
                add_paragraph(
                    bullet.group(1).strip(),
                    size=24,
                    indent=24,
                    gap_after=5,
                )
                continue

            numbered = re.match(r"^(\\d+)[.)]\\s*(.+)$", line)
            if numbered:
                add_paragraph(f"{numbered.group(1)}. {numbered.group(2).strip()}", size=24, indent=18, gap_after=5)
                continue

            add_paragraph(clean, size=24 if not patient else 25, gap_after=8)

    def paste_fit(source: Any, box: tuple[int, int, int, int]) -> None:
        x1, yy1, x2, yy2 = box
        img = PILImage.open(io.BytesIO(_image_source_to_png_bytes(source))).convert("RGB")
        max_w = max(1, x2 - x1 - 18)
        max_h = max(1, yy2 - yy1 - 18)
        scale = min(max_w / img.width, max_h / img.height)
        nw = max(1, int(img.width * scale))
        nh = max(1, int(img.height * scale))
        img = img.resize((nw, nh), PILImage.Resampling.LANCZOS)
        px = x1 + (x2 - x1 - nw) // 2
        py = yy1 + (yy2 - yy1 - nh) // 2
        page.paste(img, (px, py))

    add_page()

    # Title / subtitle
    add_paragraph("اے آئی معاون ریڈیولوجی رپورٹ", size=45, color=NAVY, gap_after=2)
    add_paragraph(
        "ڈاکٹر کے لیے منظم طبی تشریح، تصویری وضاحت، اور مریض کے لیے آسان معلومات۔",
        size=22,
        color=SLATE,
        gap_after=20,
    )

    # Metadata card
    ensure_space(150)
    meta_top = y
    meta_h = 126
    draw.rectangle((MARGIN_X, meta_top, PAGE_W - MARGIN_X, meta_top + meta_h), fill=(249, 250, 252), outline=LINE, width=2)
    mid_x = PAGE_W // 2
    mid_y = meta_top + meta_h // 2
    draw.line((mid_x, meta_top, mid_x, meta_top + meta_h), fill=LINE, width=2)
    draw.line((MARGIN_X, mid_y, PAGE_W - MARGIN_X, mid_y), fill=LINE, width=2)

    urgency = normalize_urgency(result.get("urgency"))
    meta_items = [
        ("اسکین", "اپ لوڈ شدہ تصویر", PAGE_W - MARGIN_X - 18, meta_top + 13),
        ("تیار کردہ", _urdu_datetime_now(), mid_x - 18, meta_top + 13),
        ("مریض کی زبان", "اردو", PAGE_W - MARGIN_X - 18, mid_y + 13),
        ("فوری نوعیت", _localized_urgency(urgency, "Urdu"), mid_x - 18, mid_y + 13),
    ]
    for label, value, xr, yt in meta_items:
        draw_rtl_line(draw, label, xr, yt, font(18), SLATE)
        draw_rtl_line(draw, str(value), xr - 145, yt, font(20), NAVY)
    y = meta_top + meta_h + 22

    # Imaging
    add_heading("امیجنگ اور وضاحت", size=30, color=NAVY, gap_before=0)
    ensure_space(430)
    image_top = y
    gap = 22
    card_w = (CONTENT_W - gap) // 2
    card_h = 350
    left_box = (MARGIN_X, image_top, MARGIN_X + card_w, image_top + card_h)
    right_box = (MARGIN_X + card_w + gap, image_top, PAGE_W - MARGIN_X, image_top + card_h)
    for box in (left_box, right_box):
        draw.rectangle(box, fill=(250, 251, 252), outline=LINE, width=2)
    # RTL visual order: original X-ray on the right, Grad-CAM on the left.
    paste_fit(heatmap, left_box)
    paste_fit(scan_path, right_box)
    draw_rtl_line(draw, "ماڈل کی توجہ کا نقشہ", left_box[2] - 18, image_top + card_h + 8, font(18), SLATE)
    draw_rtl_line(draw, "اصل سینے کا ایکس رے", right_box[2] - 18, image_top + card_h + 8, font(18), SLATE)
    y = image_top + card_h + 50

    # Findings table
    add_heading("ماڈل کے نتائج", size=30, color=NAVY, gap_before=0)
    sorted_findings = sorted(findings, key=lambda item: float(item.get("confidence", 0) or 0), reverse=True)
    row_h = 54
    table_h = row_h * (max(1, len(sorted_findings)) + 1)
    ensure_space(table_h + 20)
    table_top = y
    confidence_w = 220
    draw.rectangle((MARGIN_X, table_top, PAGE_W - MARGIN_X, table_top + row_h), fill=NAVY)
    draw_rtl_line(draw, "نتیجہ", PAGE_W - MARGIN_X - 18, table_top + 9, font(19), WHITE)
    draw_rtl_line(draw, "اعتماد", MARGIN_X + confidence_w - 18, table_top + 9, font(19), WHITE)
    rows = sorted_findings or [{"label": "کوئی نمایاں نتیجہ نہیں", "confidence": 0.0}]
    for i, item in enumerate(rows, start=1):
        yy = table_top + i * row_h
        draw.rectangle((MARGIN_X, yy, PAGE_W - MARGIN_X, yy + row_h), fill=WHITE, outline=LINE, width=1)
        draw.line((MARGIN_X + confidence_w, yy, MARGIN_X + confidence_w, yy + row_h), fill=LINE, width=1)
        label = _localized_finding_label(item.get("label", "Finding"), "Urdu")
        pct = max(0.0, min(1.0, float(item.get("confidence", 0) or 0))) * 100
        draw_rtl_line(draw, label, PAGE_W - MARGIN_X - 18, yy + 9, font(20), TEXT)
        draw_rtl_line(draw, f"{pct:.1f}٪", MARGIN_X + confidence_w - 18, yy + 9, font(20), TEXT)
    y = table_top + row_h * (len(rows) + 1) + 20

    # Clinical report
    add_heading("ڈاکٹر کے لیے طبی رپورٹ", size=32, color=NAVY, gap_before=4)
    ensure_space(62)
    banner_top = y
    draw.rectangle((MARGIN_X, banner_top, PAGE_W - MARGIN_X, banner_top + 52), fill=SOFT_BLUE, outline=(207, 220, 232), width=2)
    draw_rtl_line(draw, "منظم طبی ریڈیولوجی تشریح", PAGE_W - MARGIN_X - 18, banner_top + 8, font(20), (69, 100, 134))
    y = banner_top + 68
    add_structured_text(clinical_text, patient=False)

    # Patient summary
    add_heading("مریض کے لیے آسان خلاصہ", size=32, color=GOLD, gap_before=16)
    add_paragraph(
        "یہ حصہ مریض کے لیے آسان زبان میں اسکین کی وضاحت کرتا ہے۔ علاج سے متعلق فیصلے اپنے ڈاکٹر سے مشورے کے بعد کریں۔",
        size=23,
        color=SLATE,
        gap_after=10,
    )
    add_structured_text(patient_text, patient=True)

    # Audit trail
    trace = result.get("agent_trace") or []
    if trace:
        add_heading("اے آئی نے اسکین پر کیسے کام کیا", size=30, color=NAVY, gap_before=14)
        for idx, step in enumerate(trace, start=1):
            tool_name = str(step.get("tool", "agent_step"))
            add_paragraph(f"{idx:02d}  {_localized_audit_step(tool_name, 'Urdu')}", size=22, gap_after=4)

    # Disclaimer
    ensure_space(130)
    y += 10
    box_top = y
    box_h = 118
    draw.rectangle((MARGIN_X, box_top, PAGE_W - MARGIN_X, box_top + box_h), fill=(255, 247, 247), outline=(232, 201, 204), width=2)
    draw_rtl_line(draw, "طبی جائزہ ضروری ہے", PAGE_W - MARGIN_X - 18, box_top + 12, font(21), RED)
    disclaimer = (
        "یہ اے آئی معاون رپورٹ صرف طبی فیصلہ سازی میں مدد کے لیے ہے اور اسے اکیلے حتمی تشخیص نہیں سمجھا جا سکتا۔ "
        "ایک مستند ڈاکٹر کو اصل تصاویر، ماڈل کی توجہ کا نقشہ، اور تیار کردہ تشریح کا جائزہ لینا ضروری ہے۔"
    )
    # Fit disclaimer inside the box using manual wrapped lines.
    disc_font = font(19)
    disc_lines = wrap_rtl(disclaimer, disc_font, CONTENT_W - 36)
    yy = box_top + 48
    for line in disc_lines[:3]:
        draw_rtl_line(draw, line, PAGE_W - MARGIN_X - 18, yy, disc_font, TEXT)
        yy += 26
    y = box_top + box_h + 10

    # Header/footer page numbers after pagination is complete.
    for page_index, page_img in enumerate(pages, start=1):
        pd = ImageDraw.Draw(page_img)
        pd.line((MARGIN_X, PAGE_H - 72, PAGE_W - MARGIN_X, PAGE_H - 72), fill=LINE, width=2)
        draw_rtl_line(
            pd,
            "اے آئی معاون ریڈیولوجی رپورٹ - طبی ماہر کا جائزہ ضروری ہے",
            PAGE_W - MARGIN_X,
            PAGE_H - 58,
            font(15),
            SLATE,
        )
        draw_rtl_line(pd, f"صفحہ {page_index}", MARGIN_X + 100, PAGE_H - 58, font(15), SLATE)

    out = io.BytesIO()
    pages[0].save(
        out,
        format="PDF",
        save_all=True,
        append_images=pages[1:],
        resolution=DPI,
        quality=92,
    )
    out.seek(0)
    return out.getvalue()


# PDF language contract:
# - English selection: the complete report is English.
# - Urdu selection: the complete report, from title to footer, is Urdu.
# - Dynamic clinical content is translated faithfully to Urdu before export.

def build_pdf_report(
    scan_name: str,
    language: str,
    findings: list[dict[str, Any]],
    result: dict[str, Any],
    scan_path: str | Path,
    heatmap: Any,
) -> bytes:
    """Build a polished, fully localized clinical PDF."""
    is_urdu = _is_urdu(language)

    # Urdu is rendered through Pillow + RAQM/HarfBuzz as page pixels. This avoids
    # ReportLab's missing Urdu presentation-form glyphs and eliminates tofu boxes.
    if is_urdu:
        return _build_urdu_raster_pdf_report(
            scan_name=scan_name,
            findings=findings,
            result=result,
            scan_path=scan_path,
            heatmap=heatmap,
        )

    if not PDF_EXPORT_AVAILABLE:
        raise RuntimeError("PDF export requires the 'reportlab' package.")

    font_regular, font_bold = _register_pdf_fonts(language)

    navy = colors.HexColor("#07111F")
    navy_2 = colors.HexColor("#0B1728")
    gold = colors.HexColor("#B79A5B")
    champagne = colors.HexColor("#D7C29A")
    ivory = colors.HexColor("#F5F1E8")
    slate = colors.HexColor("#5F6D7F")
    light_line = colors.HexColor("#D8DEE7")
    soft_blue = colors.HexColor("#EEF3F8")
    soft_gold = colors.HexColor("#F7F2E8")
    success = colors.HexColor("#3E8B70")
    warning = colors.HexColor("#A9742F")
    critical = colors.HexColor("#B84F59")

    localized_result = dict(result)

    # The analysis stage already localizes Urdu output. PDF creation is intentionally
    # offline/deterministic so the download does not fail because of a second API call.
    if is_urdu:
        clinical_text = _pdf_normalize_text(localized_result.get("clinical_report") or "")
        patient_text = _pdf_normalize_text(localized_result.get("patient_summary") or "")
        if not clinical_text or not _contains_urdu(clinical_text):
            raise RuntimeError(
                "Urdu clinical report is not present in the current analysis result. "
                "Run the analysis again with Urdu selected."
            )
        if not patient_text or not _contains_urdu(patient_text):
            raise RuntimeError(
                "Urdu patient summary is not present in the current analysis result. "
                "Run the analysis again with Urdu selected."
            )

    labels = {
        "title": "اے آئی معاون ریڈیولوجی رپورٹ" if is_urdu else "AI-Assisted Radiology Report",
        "subtitle": (
            "ڈاکٹر کے لیے منظم طبی تشریح، تصویری وضاحت، اور مریض کے لیے آسان معلومات۔"
            if is_urdu
            else "Structured doctor-facing interpretation, explainability evidence, and patient-facing communication."
        ),
        "study": "اسکین" if is_urdu else "STUDY",
        "generated": "تیار کردہ" if is_urdu else "GENERATED",
        "patient_language": "مریض کی زبان" if is_urdu else "PATIENT LANGUAGE",
        "urgency": "فوری نوعیت" if is_urdu else "URGENCY",
        "language_value": "اردو" if is_urdu else (language or "English"),
        "imaging": "امیجنگ اور وضاحت" if is_urdu else "Imaging & Explainability",
        "original_image": "اصل سینے کا ایکس رے" if is_urdu else "Original chest radiograph",
        "attention_image": "ماڈل کی توجہ کا نقشہ" if is_urdu else "Grad-CAM model attention",
        "model_findings": "ماڈل کے نتائج" if is_urdu else "Model Findings",
        "finding": "نتیجہ" if is_urdu else "Finding",
        "confidence": "اعتماد" if is_urdu else "Confidence",
        "no_findings": (
            "ماڈل کی مقررہ حد سے اوپر کوئی نمایاں نتیجہ نہیں ملا۔"
            if is_urdu
            else "No displayed finding exceeded the model threshold."
        ),
        "doctor_report": "ڈاکٹر کے لیے طبی رپورٹ" if is_urdu else "Doctor-Facing Clinical Report",
        "doctor_banner": "منظم طبی ریڈیولوجی تشریح" if is_urdu else "RADIOLOGY OUTPUT - STRUCTURED CLINICAL INTERPRETATION",
        "patient_summary": "مریض کے لیے آسان خلاصہ" if is_urdu else "Patient-Friendly Summary",
        "patient_intro": (
            "یہ حصہ مریض کے لیے آسان زبان میں اسکین کی وضاحت کرتا ہے۔ "
            "علاج سے متعلق فیصلے اپنے ڈاکٹر سے مشورے کے بعد کریں۔"
            if is_urdu
            else "This section explains the scan in plain language for the patient. "
                 "Please discuss treatment decisions with your clinician."
        ),
        "processing": "اے آئی نے اسکین پر کیسے کام کیا" if is_urdu else "How the AI Processed the Scan",
        "step": "مرحلہ" if is_urdu else "Step",
        "what_happened": "کیا کیا گیا" if is_urdu else "What happened",
        "review_required": "طبی جائزہ ضروری ہے" if is_urdu else "CLINICAL REVIEW REQUIRED",
        "disclaimer": (
            "یہ اے آئی معاون رپورٹ صرف طبی فیصلہ سازی میں مدد کے لیے ہے اور اسے اکیلے حتمی تشخیص نہیں سمجھا جا سکتا۔ "
            "ایک مستند ڈاکٹر کو اصل تصاویر، ماڈل کی توجہ کا نقشہ، اور تیار کردہ تشریح کا جائزہ لینا ضروری ہے۔"
            if is_urdu
            else "This AI-assisted output is decision support only and must not be used as a standalone diagnosis. "
                 "A qualified clinician must review the source images, model attention map, and generated interpretation."
        ),
        "header_brand": "میڈ اسکرائب اے آئی" if is_urdu else "MEDSCRIBE AI",
        "header_meta": "ریڈیولوجی انٹیلیجنس" if is_urdu else "RADIOLOGY INTELLIGENCE",
        "footer": (
            "اے آئی معاون ریڈیولوجی رپورٹ — طبی ماہر کا جائزہ ضروری ہے"
            if is_urdu
            else "AI-assisted radiology report - clinical review required"
        ),
        "page": "صفحہ" if is_urdu else "Page",
    }

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=27 * mm,
        bottomMargin=19 * mm,
        title=_pdf_normalize_text(labels["title"]),
        author="MedScribe AI",
        subject=_pdf_normalize_text(labels["subtitle"]),
    )

    styles = getSampleStyleSheet()
    rtl_align = TA_RIGHT if is_urdu else TA_LEFT

    pdf_styles = {
        "title": ParagraphStyle(
            "MS_Title",
            parent=styles["Title"],
            fontName=font_bold,
            fontSize=21 if not is_urdu else 18,
            leading=27 if is_urdu else 25,
            textColor=navy,
            spaceAfter=3 * mm,
            alignment=rtl_align,
        ),
        "subtitle": ParagraphStyle(
            "MS_Subtitle",
            parent=styles["BodyText"],
            fontName=font_regular,
            fontSize=8.7,
            leading=15 if is_urdu else 13,
            textColor=slate,
            spaceAfter=4 * mm,
            alignment=rtl_align,
        ),
        "section": ParagraphStyle(
            "MS_Section",
            parent=styles["Heading2"],
            fontName=font_bold,
            fontSize=11.2,
            leading=16 if is_urdu else 14,
            textColor=navy,
            spaceBefore=4 * mm,
            spaceAfter=2.2 * mm,
            alignment=rtl_align,
        ),
        "section_gold": ParagraphStyle(
            "MS_SectionGold",
            parent=styles["Heading2"],
            fontName=font_bold,
            fontSize=11.2,
            leading=16 if is_urdu else 14,
            textColor=gold,
            spaceBefore=4 * mm,
            spaceAfter=2.2 * mm,
            alignment=rtl_align,
        ),
        "body": ParagraphStyle(
            "MS_Body",
            parent=styles["BodyText"],
            fontName=font_regular,
            fontSize=9.1 if is_urdu else 8.8,
            leading=16 if is_urdu else 13.2,
            textColor=colors.HexColor("#273342"),
            spaceAfter=1.7 * mm,
            alignment=rtl_align,
        ),
        "bullet": ParagraphStyle(
            "MS_Bullet",
            parent=styles["BodyText"],
            fontName=font_regular,
            fontSize=9.0 if is_urdu else 8.7,
            leading=15.5 if is_urdu else 12.8,
            textColor=colors.HexColor("#273342"),
            leftIndent=0 if is_urdu else 4 * mm,
            rightIndent=3 * mm if is_urdu else 0,
            firstLineIndent=0 if is_urdu else -2.5 * mm,
            spaceAfter=1.35 * mm,
            alignment=rtl_align,
        ),
        "report_heading": ParagraphStyle(
            "MS_ReportHeading",
            parent=styles["Heading3"],
            fontName=font_bold,
            fontSize=10.0 if is_urdu else 9.4,
            leading=15 if is_urdu else 12,
            textColor=navy_2,
            spaceBefore=2.5 * mm,
            spaceAfter=1.3 * mm,
            alignment=rtl_align,
        ),
        "caption": ParagraphStyle(
            "MS_Caption",
            parent=styles["BodyText"],
            fontName=font_bold,
            fontSize=7.4,
            leading=11 if is_urdu else 9.5,
            textColor=slate,
            alignment=TA_CENTER,
        ),
        "meta_label": ParagraphStyle(
            "MS_MetaLabel",
            parent=styles["BodyText"],
            fontName=font_bold,
            fontSize=7.3,
            leading=11 if is_urdu else 9,
            textColor=slate,
            alignment=rtl_align,
        ),
        "meta_value": ParagraphStyle(
            "MS_MetaValue",
            parent=styles["BodyText"],
            fontName=font_regular,
            fontSize=8.3,
            leading=12 if is_urdu else 10.2,
            textColor=navy,
            alignment=rtl_align,
        ),
        "patient": ParagraphStyle(
            "MS_Patient",
            parent=styles["BodyText"],
            fontName=font_regular,
            fontSize=9.5,
            leading=16 if is_urdu else 14.6,
            textColor=colors.HexColor("#2B3542"),
            alignment=rtl_align,
            spaceAfter=1.7 * mm,
        ),
        "patient_heading": ParagraphStyle(
            "MS_PatientHeading",
            parent=styles["Heading3"],
            fontName=font_bold,
            fontSize=10.2,
            leading=15 if is_urdu else 13.5,
            textColor=gold,
            alignment=rtl_align,
            spaceBefore=2.2 * mm,
            spaceAfter=1.4 * mm,
        ),
        "patient_bullet": ParagraphStyle(
            "MS_PatientBullet",
            parent=styles["BodyText"],
            fontName=font_regular,
            fontSize=9.3,
            leading=15.5 if is_urdu else 14.2,
            textColor=colors.HexColor("#2B3542"),
            alignment=rtl_align,
            leftIndent=0 if is_urdu else 4 * mm,
            rightIndent=3 * mm if is_urdu else 0,
            firstLineIndent=0 if is_urdu else -2.5 * mm,
            spaceAfter=1.4 * mm,
        ),
        "small": ParagraphStyle(
            "MS_Small",
            parent=styles["BodyText"],
            fontName=font_regular,
            fontSize=7.3,
            leading=12 if is_urdu else 10,
            textColor=slate,
            alignment=rtl_align,
        ),
    }

    urgency = normalize_urgency(localized_result.get("urgency"))
    urgency_color = {
        "routine": success,
        "urgent": warning,
        "critical": critical,
    }.get(urgency, success)

    generated_at = _urdu_datetime_now() if is_urdu else datetime.now().strftime("%d %b %Y, %H:%M")
    story: list[Any] = []

    story.append(Paragraph(_pdf_display(labels["title"], language), pdf_styles["title"]))
    story.append(Paragraph(_pdf_display(labels["subtitle"], language), pdf_styles["subtitle"]))

    overview_data = [
        [
            Paragraph(_pdf_display(labels["study"], language), pdf_styles["meta_label"]),
            Paragraph(html.escape(scan_name), pdf_styles["meta_value"]),
            Paragraph(_pdf_display(labels["generated"], language), pdf_styles["meta_label"]),
            Paragraph(_pdf_display(generated_at, language), pdf_styles["meta_value"]),
        ],
        [
            Paragraph(_pdf_display(labels["patient_language"], language), pdf_styles["meta_label"]),
            Paragraph(_pdf_display(labels["language_value"], language), pdf_styles["meta_value"]),
            Paragraph(_pdf_display(labels["urgency"], language), pdf_styles["meta_label"]),
            Paragraph(
                _pdf_display(_localized_urgency(urgency, language), language),
                pdf_styles["meta_value"],
            ),
        ],
    ]

    overview = Table(overview_data, colWidths=[28*mm, 61*mm, 30*mm, 55*mm], hAlign="LEFT")
    overview.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ("BOX", (0,0), (-1,-1), .55, light_line),
        ("INNERGRID", (0,0), (-1,-1), .35, colors.HexColor("#E6EAF0")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN", (0,0), (-1,-1), "RIGHT" if is_urdu else "LEFT"),
        ("LEFTPADDING", (0,0), (-1,-1), 7),
        ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("TEXTCOLOR", (2,1), (3,1), urgency_color),
    ]))
    story.append(overview)
    story.append(Spacer(1, 4 * mm))

    # Imaging / explainability
    story.append(Paragraph(_pdf_display(labels["imaging"], language), pdf_styles["section"]))
    original_img = _pdf_image(scan_path, 76 * mm, 67 * mm)
    heatmap_img = _pdf_image(heatmap, 76 * mm, 67 * mm)
    image_table = Table(
        [
            [original_img, heatmap_img],
            [
                Paragraph(_pdf_display(labels["original_image"], language), pdf_styles["caption"]),
                Paragraph(_pdf_display(labels["attention_image"], language), pdf_styles["caption"]),
            ],
        ],
        colWidths=[86 * mm, 86 * mm],
        hAlign="CENTER",
    )
    image_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#FAFBFC")),
        ("BOX", (0,0), (-1,-1), .55, light_line),
        ("INNERGRID", (0,0), (-1,-1), .35, colors.HexColor("#E7EBF0")),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,0), 8),
        ("BOTTOMPADDING", (0,0), (-1,0), 6),
        ("TOPPADDING", (0,1), (-1,1), 5),
        ("BOTTOMPADDING", (0,1), (-1,1), 7),
    ]))
    story.append(KeepTogether([image_table]))
    story.append(Spacer(1, 3.5 * mm))

    # Model findings
    story.append(Paragraph(_pdf_display(labels["model_findings"], language), pdf_styles["section"]))
    sorted_findings = sorted(
        findings,
        key=lambda item: float(item.get("confidence", 0) or 0),
        reverse=True,
    )

    if sorted_findings:
        finding_rows = [[
            Paragraph(_pdf_display(labels["finding"], language), pdf_styles["meta_label"]),
            Paragraph(_pdf_display(labels["confidence"], language), pdf_styles["meta_label"]),
        ]]
        for item in sorted_findings:
            label = _localized_finding_label(item.get("label", "Finding"), language)
            pct = max(0.0, min(1.0, float(item.get("confidence", 0) or 0))) * 100
            finding_rows.append([
                Paragraph(_pdf_display(label, language), pdf_styles["body"]),
                Paragraph(_pdf_display(f"{pct:.1f}%", language), pdf_styles["body"]),
            ])

        finding_table = Table(
            finding_rows,
            colWidths=[135 * mm, 37 * mm],
            repeatRows=1,
        )
        finding_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), navy),
            ("TEXTCOLOR", (0,0), (-1,0), ivory),
            ("BOX", (0,0), (-1,-1), .5, light_line),
            ("INNERGRID", (0,1), (-1,-1), .3, colors.HexColor("#E7EBF0")),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("ALIGN", (0,0), (-1,-1), "RIGHT" if is_urdu else "LEFT"),
            ("LEFTPADDING", (0,0), (-1,-1), 7),
            ("RIGHTPADDING", (0,0), (-1,-1), 7),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ]))
        story.append(finding_table)
    else:
        story.append(Paragraph(_pdf_display(labels["no_findings"], language), pdf_styles["body"]))

    # Clinical report
    story.append(Spacer(1, 2 * mm))
    story.append(HRFlowable(
        width="100%",
        thickness=1.3,
        color=colors.HexColor("#6D89AD"),
        spaceBefore=3*mm,
        spaceAfter=2*mm,
    ))
    story.append(Paragraph(_pdf_display(labels["doctor_report"], language), pdf_styles["section"]))

    doctor_banner_style = ParagraphStyle(
        "DoctorBanner",
        fontName=font_bold,
        fontSize=7.6 if not is_urdu else 8.4,
        leading=12 if is_urdu else 9.5,
        textColor=colors.HexColor("#456486"),
        alignment=rtl_align,
    )
    doctor_banner = Table(
        [[Paragraph(_pdf_display(labels["doctor_banner"], language), doctor_banner_style)]],
        colWidths=[172*mm],
    )
    doctor_banner.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), soft_blue),
        ("BOX", (0,0), (-1,-1), .6, colors.HexColor("#CFDCE8")),
        ("ALIGN", (0,0), (-1,-1), "RIGHT" if is_urdu else "LEFT"),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(doctor_banner)
    story.append(Spacer(1, 2.5 * mm))
    story.extend(
        _markdown_report_flowables(
            localized_result.get("clinical_report") or "",
            pdf_styles,
            language,
        )
    )

    # Patient-facing summary
    story.append(Spacer(1, 2 * mm))
    story.append(HRFlowable(width="100%", thickness=1.3, color=gold, spaceBefore=3*mm, spaceAfter=2*mm))
    story.append(Paragraph(_pdf_display(labels["patient_summary"], language), pdf_styles["section_gold"]))

    patient_content: list[Any] = [
        Paragraph(_pdf_display(labels["patient_intro"], language), pdf_styles["patient"]),
        Spacer(1, 1.2 * mm),
    ]
    patient_content.extend(
        _patient_summary_flowables(
            localized_result.get("patient_summary") or "",
            language,
            pdf_styles,
        )
    )

    patient_box = Table([[patient_content]], colWidths=[172 * mm])
    patient_box.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), soft_gold),
        ("BOX", (0,0), (-1,-1), .7, colors.HexColor("#E2D5B8")),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 9),
        ("BOTTOMPADDING", (0,0), (-1,-1), 9),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ALIGN", (0,0), (-1,-1), "RIGHT" if is_urdu else "LEFT"),
    ]))
    story.append(patient_box)

    # Processing summary
    trace = localized_result.get("agent_trace") or []
    if trace:
        story.append(Paragraph(_pdf_display(labels["processing"], language), pdf_styles["section"]))
        audit_rows = [[
            Paragraph(_pdf_display(labels["step"], language), pdf_styles["meta_label"]),
            Paragraph(_pdf_display(labels["what_happened"], language), pdf_styles["meta_label"]),
        ]]
        for idx, step in enumerate(trace, start=1):
            tool_name = str(step.get("tool", "agent_step"))
            audit_rows.append([
                Paragraph(_pdf_display(f"{idx:02d}", language), pdf_styles["small"]),
                Paragraph(
                    _pdf_display(_localized_audit_step(tool_name, language), language),
                    pdf_styles["small"],
                ),
            ])

        audit_table = Table(audit_rows, colWidths=[18*mm, 154*mm], repeatRows=1)
        audit_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#F0F3F7")),
            ("BOX", (0,0), (-1,-1), .45, light_line),
            ("INNERGRID", (0,1), (-1,-1), .25, colors.HexColor("#E7EBF0")),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("ALIGN", (0,0), (-1,-1), "RIGHT" if is_urdu else "LEFT"),
            ("LEFTPADDING", (0,0), (-1,-1), 6),
            ("RIGHTPADDING", (0,0), (-1,-1), 6),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ]))
        story.append(audit_table)

    story.append(Spacer(1, 4 * mm))
    disclaimer_title_style = ParagraphStyle(
        "DisclaimerTitle",
        fontName=font_bold,
        fontSize=7.7 if not is_urdu else 8.4,
        leading=12 if is_urdu else 9,
        textColor=critical,
        alignment=rtl_align,
    )
    disclaimer = Table([[
        Paragraph(_pdf_display(labels["review_required"], language), disclaimer_title_style),
        Paragraph(_pdf_display(labels["disclaimer"], language), pdf_styles["small"]),
    ]], colWidths=[38*mm, 134*mm])
    disclaimer.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#FFF7F7")),
        ("BOX", (0,0), (-1,-1), .6, colors.HexColor("#E8C9CC")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ALIGN", (0,0), (-1,-1), "RIGHT" if is_urdu else "LEFT"),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ]))
    story.append(disclaimer)

    def draw_page(canvas, document):
        canvas.saveState()
        page_width, page_height = A4

        canvas.setFillColor(navy)
        canvas.rect(0, page_height - 18*mm, page_width, 18*mm, fill=1, stroke=0)

        canvas.setFillColor(champagne)
        canvas.setFont(font_bold, 10.5)
        header_brand = _shape_rtl_text(labels["header_brand"]) if is_urdu else labels["header_brand"]

        canvas.setFillColor(colors.HexColor("#B7C1CF"))
        canvas.setFont(font_regular, 7.2)
        header_meta = _shape_rtl_text(labels["header_meta"]) if is_urdu else labels["header_meta"]

        if is_urdu:
            canvas.setFillColor(champagne)
            canvas.setFont(font_bold, 10.5)
            canvas.drawRightString(page_width - 16*mm, page_height - 11.5*mm, header_brand)

            canvas.setFillColor(colors.HexColor("#B7C1CF"))
            canvas.setFont(font_regular, 7.2)
            canvas.drawString(16*mm, page_height - 11.5*mm, header_meta)
        else:
            canvas.setFillColor(champagne)
            canvas.setFont(font_bold, 10.5)
            canvas.drawString(16*mm, page_height - 11.5*mm, header_brand)

            canvas.setFillColor(colors.HexColor("#B7C1CF"))
            canvas.setFont(font_regular, 7.2)
            canvas.drawRightString(page_width - 16*mm, page_height - 11.5*mm, header_meta)

        canvas.setStrokeColor(colors.HexColor("#D7DEE6"))
        canvas.setLineWidth(.45)
        canvas.line(16*mm, 13.5*mm, page_width - 16*mm, 13.5*mm)

        canvas.setFillColor(slate)
        canvas.setFont(font_regular, 6.7)
        footer_text = _shape_rtl_text(labels["footer"]) if is_urdu else labels["footer"]
        page_text = (
            _shape_rtl_text(f"{labels['page']} {document.page}")
            if is_urdu
            else f"{labels['page']} {document.page}"
        )

        if is_urdu:
            canvas.drawRightString(page_width - 16*mm, 8.5*mm, footer_text)
            canvas.drawString(16*mm, 8.5*mm, page_text)
        else:
            canvas.drawString(16*mm, 8.5*mm, footer_text)
            canvas.drawRightString(page_width - 16*mm, 8.5*mm, page_text)

        canvas.restoreState()

    doc.build(story, onFirstPage=draw_page, onLaterPages=draw_page)
    buffer.seek(0)
    return buffer.getvalue()


# -----------------------------------------------------------------------------
# Session state
# -----------------------------------------------------------------------------
STATE_DEFAULTS = {
    "analysis_result": None,
    "analysis_findings": [],
    "analysis_heatmap": None,
    "analysis_scan_path": None,
    "analysis_scan_name": None,
    "analysis_language": None,
}
for key, value in STATE_DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -----------------------------------------------------------------------------
# Header / hero
# -----------------------------------------------------------------------------
render_golden_dust_background()
render_topbar()
render_hero()

# -----------------------------------------------------------------------------
# Input workspace
# -----------------------------------------------------------------------------
section_header(
    "01 / New analysis",
    "Radiograph intake",
    "Upload a chest radiograph and choose the language used for the patient-facing explanation.",
)

input_col, architecture_col = st.columns([1.08, 0.92], gap="large")

with input_col:
    uploaded = st.file_uploader(
        "Chest radiograph",
        type=["png", "jpg", "jpeg"],
        help="Supported formats: PNG, JPG, JPEG.",
    )

    st.markdown(
        '<div class="ms-analysis-control-row"></div>',
        unsafe_allow_html=True,
    )
    language_col, run_col = st.columns(2, gap="medium")

    with language_col:
        st.markdown(
            '<div class="ms-control-label">Patient output language</div>',
            unsafe_allow_html=True,
        )
        default_language_index = (
            SUPPORTED_LANGUAGES.index("English")
            if "English" in SUPPORTED_LANGUAGES
            else 0
        )
        language = st.selectbox(
            "Patient output language",
            SUPPORTED_LANGUAGES,
            index=default_language_index,
            label_visibility="collapsed",
        )

    with run_col:
        st.markdown(
            '<div class="ms-control-label ms-control-label-spacer">Analysis action</div>',
            unsafe_allow_html=True,
        )
        run = st.button(
            "Run clinical analysis  →",
            type="primary",
            use_container_width=True,
            disabled=uploaded is None,
        )

    if uploaded is not None:
        st.markdown(
            f"""
            <div class="ms-note">
                Selected study: <strong>{esc(uploaded.name)}</strong><br>
                Ready for analysis.
            </div>
            """,
            unsafe_allow_html=True,
        )

with architecture_col:
    if uploaded is None:
        render_workflow_panel()
    else:
        st.markdown(
            """
            <div class="ms-panel gold-edge" style="padding-bottom:.85rem;">
                <div class="ms-mini-label">Study preview</div>
                <div class="ms-panel-title" style="margin-top:.45rem;">Selected radiograph</div>
                <div class="ms-panel-copy">Review the image before running the analysis workflow.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.image(uploaded.getvalue(), caption=uploaded.name, use_container_width=True)


# -----------------------------------------------------------------------------
# Execute analysis
# -----------------------------------------------------------------------------
if run and uploaded is not None:
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(parents=True, exist_ok=True)

    scan_name = Path(uploaded.name).name
    scan_path = outputs_dir / f"scan_{uuid.uuid4().hex[:10]}{safe_suffix(scan_name)}"
    scan_path.write_bytes(uploaded.getvalue())

    urdu_requested = _is_urdu(language)
    st.session_state.analysis_localization_error = None
    progress = st.progress(
        0,
        text="تجزیہ تیار کیا جا رہا ہے…" if urdu_requested else "Preparing analysis workspace…",
    )

    # ------------------------------------------------------------------
    # CORE MEDICAL ANALYSIS
    # Keep this path as close as possible to the previously working app.
    # Urdu is NOT allowed to break the medical computation.
    # ------------------------------------------------------------------
    try:
        progress.progress(
            12,
            text=(
                "ایکس رے محفوظ کر لیا گیا۔ طبی تجزیہ شروع کیا جا رہا ہے…"
                if urdu_requested
                else "Radiograph secured. Starting clinical analysis…"
            ),
        )

        # The proven clinical agent runs in English for Urdu requests.
        core_language = "English" if urdu_requested else language

        with st.spinner(
            "طبی تجزیہ جاری ہے…"
            if urdu_requested
            else "Running MedScribe clinical intelligence pipeline…"
        ):
            core_result = run_agent(str(scan_path), core_language)

        progress.progress(
            70,
            text=(
                "طبی تجزیہ مکمل۔ وضاحتی نقشہ تیار کیا جا رہا ہے…"
                if urdu_requested
                else "Agent workflow complete. Generating explainability map…"
            ),
        )

        findings, img_tensor = detect_abnormalities(str(scan_path))
        heatmap = generate_heatmap(str(scan_path), img_tensor)

        # Save the valid medical result FIRST. A translation/PDF/UI failure must
        # never turn a successful clinical analysis into "analysis failed".
        st.session_state.analysis_result = core_result
        st.session_state.analysis_findings = findings
        st.session_state.analysis_heatmap = heatmap
        st.session_state.analysis_scan_path = str(scan_path)
        st.session_state.analysis_scan_name = scan_name
        st.session_state.analysis_language = core_language

    except Exception as exc:
        progress.empty()
        print(
            "[MedScribe AI] CORE analysis error: "
            f"{type(exc).__name__}: {exc}"
        )
        st.error(
            "The clinical analysis could not be completed. "
            "Check the server log for the CORE analysis error."
        )
        st.stop()

    # ------------------------------------------------------------------
    # URDU LOCALIZATION
    # Completely separate from core medical computation.
    # If translation fails, the valid medical analysis is retained.
    # ------------------------------------------------------------------
    if urdu_requested:
        progress.progress(
            84,
            text="طبی رپورٹ کو اردو میں تیار کیا جا رہا ہے…",
        )
        try:
            localized_result = _localize_result_for_language_safe(core_result, "Urdu")

            st.session_state.analysis_result = localized_result
            st.session_state.analysis_language = "Urdu"
            st.session_state.analysis_localization_error = None

            progress.progress(100, text="تجزیہ اور اردو رپورٹ مکمل ہو گئی۔")
            st.success("تجزیہ اور اردو رپورٹ کامیابی سے تیار ہو گئی۔")

        except Exception as exc:
            # DO NOT discard the medical analysis.
            st.session_state.analysis_result = core_result
            st.session_state.analysis_language = "English"
            st.session_state.analysis_localization_error = (
                f"{type(exc).__name__}: {exc}"
            )

            progress.progress(100, text="طبی تجزیہ مکمل ہو گیا۔")
            print(
                "[MedScribe AI] Urdu localization error: "
                f"{type(exc).__name__}: {exc}"
            )
            st.warning(
                "طبی تجزیہ کامیابی سے مکمل ہو گیا، لیکن اردو ترجمہ تیار نہیں ہو سکا۔ "
                "اصل طبی نتیجہ محفوظ ہے۔ سرور لاگ میں Urdu localization error دیکھیں۔"
            )
    else:
        progress.progress(100, text="Analysis complete.")
        st.success("Analysis completed successfully.")


# -----------------------------------------------------------------------------
# Results workspace
# -----------------------------------------------------------------------------
result = st.session_state.analysis_result
findings = st.session_state.analysis_findings
heatmap = st.session_state.analysis_heatmap
scan_path = st.session_state.analysis_scan_path
scan_name = st.session_state.analysis_scan_name
result_language = st.session_state.analysis_language

if result and scan_path:
    urdu_output = _is_urdu(result_language)
    urgency = normalize_urgency(result.get("urgency"))
    escalated = bool(result.get("escalated", False))
    confidence = top_confidence(findings)

    section_header(
        "02 / جائزہ" if urdu_output else "02 / Review",
        "ریڈیوگراف کا تجزیہ" if urdu_output else "Radiograph intelligence",
        (
            "اصل ایکس رے، ماڈل کی توجہ کا نقشہ، نمایاں نتائج اور اعتماد کی شرح کا جائزہ لیں۔"
            if urdu_output
            else "Compare the source study with the model attention map, then review the detected findings and confidence values."
        ),
        rtl=urdu_output,
    )

    st.markdown(
        f"""
        <div class="ms-metrics{" ms-rtl" if urdu_output else ""}" dir="{"rtl" if urdu_output else "ltr"}">
            <div class="ms-metric">
                <div class="ms-metric-label">{"نمایاں نتائج" if urdu_output else "Displayed findings"}</div>
                <div class="ms-metric-value">{len(findings):02d}</div>
                <div class="ms-metric-sub">{"ماڈل کی مقررہ حد سے اوپر" if urdu_output else "Above the model display threshold"}</div>
            </div>
            <div class="ms-metric">
                <div class="ms-metric-label">{"سب سے زیادہ اعتماد" if urdu_output else "Highest confidence"}</div>
                <div class="ms-metric-value">{confidence * 100:.1f}%</div>
                <div class="ms-metric-sub">{"سب سے زیادہ پیتھالوجی اسکور" if urdu_output else "Highest returned pathology score"}</div>
            </div>
            <div class="ms-metric">
                <div class="ms-metric-label">{"فوری نوعیت" if urdu_output else "Triage status"}</div>
                <div class="ms-metric-value">{
                    esc(_localized_urgency(urgency, result_language))
                    if urdu_output else esc(urgency)
                }</div>
                <div class="ms-metric-sub">{"طبی جائزے کی ترجیح" if urdu_output else "Agent-assessed urgency class"}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    source_col, cam_col = st.columns(2, gap="medium")
    with source_col:
        st.markdown(
            f'<div class="ms-mini-label" style="margin-bottom:.55rem; text-align:{"right" if urdu_output else "left"};" dir="{"rtl" if urdu_output else "ltr"}">{"اصل سینے کا ایکس رے" if urdu_output else "Source / original radiograph"}</div>',
            unsafe_allow_html=True,
        )
        st.image(
            scan_path,
            caption="اصل سینے کا ایکس رے" if urdu_output else "Original radiograph",
            use_container_width=True,
        )

    with cam_col:
        st.markdown(
            f'<div class="ms-mini-label" style="margin-bottom:.55rem; text-align:{"right" if urdu_output else "left"};" dir="{"rtl" if urdu_output else "ltr"}">{"وضاحت / ماڈل کی توجہ" if urdu_output else "Explainability / model attention"}</div>',
            unsafe_allow_html=True,
        )
        st.image(
            heatmap,
            caption="ماڈل کی توجہ کا نقشہ" if urdu_output else "Grad-CAM attention map",
            use_container_width=True,
        )

    findings_col, urgency_col = st.columns([1.45, .75], gap="medium")
    with findings_col:
        render_findings(findings, result_language or "English")
    with urgency_col:
        render_urgency(urgency, escalated, result_language or "English")


    # -------------------------------------------------------------------------
    # Doctor-facing clinical report
    # -------------------------------------------------------------------------
    section_header(
        "03 / ڈاکٹر کے لیے رپورٹ" if urdu_output else "03 / Doctor-facing output",
        "طبی رپورٹ" if urdu_output else "Clinical report",
        (
            "ڈاکٹر کے طبی جائزے کے لیے منظم تشریح۔"
            if urdu_output
            else "Structured interpretation for clinical review, separated from the patient-facing explanation."
        ),
        rtl=urdu_output,
    )

    st.markdown(
        f"""
        <div class="ms-audience-kicker doctor" dir="{"rtl" if urdu_output else "ltr"}" style="text-align:{"right" if urdu_output else "left"};">{"ڈاکٹر کے لیے · منظم طبی تشریح" if urdu_output else "Doctor-facing · structured clinical interpretation"}</div>
        <div class="ms-report-shell{" ms-rtl" if urdu_output else ""}" dir="{"rtl" if urdu_output else "ltr"}">
            <div class="ms-report-heading">
                <div>
                    <div class="ms-mini-label">{"ریڈیولوجی نتیجہ" if urdu_output else "Radiology output"}</div>
                    <div class="ms-report-title">{"طبی رپورٹ" if urdu_output else "Clinical report"}</div>
                </div>
                <div class="ms-report-meta">{esc(scan_name or 'Study')}</div>
            </div>
        </div>
        <div class="ms-report-marker"></div>
        """,
        unsafe_allow_html=True,
    )
    render_clinical_report_screen(
        result.get("clinical_report") or "",
        result_language or "English",
    )

    # -------------------------------------------------------------------------
    # Patient-facing summary
    # -------------------------------------------------------------------------
    section_header(
        "04 / مریض کے لیے رپورٹ" if urdu_output else "04 / Patient-facing output",
        "مریض کے لیے آسان خلاصہ" if urdu_output else "Patient summary",
        (
            "مریض کے لیے آسان زبان میں الگ وضاحت۔"
            if urdu_output
            else "Plain-language communication is presented separately so patients can read the relevant explanation without clinical audit detail."
        ),
        rtl=urdu_output,
    )

    patient_summary = _pdf_normalize_text(
        result.get("patient_summary") or "No patient summary was returned by the agent."
    )
    is_rtl = (result_language or "") in {"Urdu", "Arabic", "Persian"}
    direction = "rtl" if is_rtl else "ltr"
    st.markdown(
        f"""
        <div class="ms-audience-kicker patient">{"مریض کے لیے · آسان وضاحت" if urdu_output else "Patient-facing · plain-language explanation"}</div>
        <div class="ms-summary-shell patient-facing{" ms-rtl" if urdu_output else ""}" dir="{"rtl" if urdu_output else "ltr"}">
            <div class="ms-report-heading">
                <div>
                    <div class="ms-mini-label">{"مریض کے لیے معلومات" if urdu_output else "Patient communication"}</div>
                    <div class="ms-report-title">{"اردو" if urdu_output else esc(result_language or 'Selected language')}</div>
                </div>
                <div class="ms-report-meta">{"آسان زبان" if urdu_output else "Plain-language output"}</div>
            </div>
            <div class="ms-summary-text" dir="{direction}">{esc(patient_summary)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------------------------------------------------------
    # Audit trail
    # -------------------------------------------------------------------------
    section_header(
        "05 / تجزیے کے مراحل" if urdu_output else "05 / Audit",
        "اے آئی کا طریقۂ کار" if urdu_output else "Agent workflow",
        (
            "اس حصے میں دکھایا گیا ہے کہ اے آئی نے اسکین کے تجزیے میں کون سے مراحل مکمل کیے۔"
            if urdu_output
            else
            "Technical trace of the tools selected by the clinical agent for this analysis."
        ),
        rtl=urdu_output,
    )
    st.markdown(
        (
            '<div class="ms-audit-shell-intro" dir="rtl" style="text-align:right;">یہ حصہ تجزیے کے مراحل کا خلاصہ دکھاتا ہے۔</div>'
            if urdu_output
            else
            '<div class="ms-audit-shell-intro">This section is intended for technical / clinical audit rather than patient communication.</div>'
        ),
        unsafe_allow_html=True,
    )
    render_trace(result.get("agent_trace") or [], result_language or "English")

    # -------------------------------------------------------------------------
    # Export
    # -------------------------------------------------------------------------
    section_header(
        "06 / برآمد" if urdu_output else "06 / Export",
        "طبی دستاویز" if urdu_output else "Clinical document",
        (
            "اصل ایکس رے، ماڈل کی توجہ کا نقشہ، نتائج، طبی رپورٹ، مریض کا خلاصہ اور تجزیے کے مراحل ڈاؤن لوڈ کریں۔"
            if urdu_output
            else
            "Download a formatted PDF containing the original X-ray, Grad-CAM, model findings, doctor-facing report, patient summary and audit trail."
        ),
        rtl=urdu_output,
    )

    pdf_bytes = None
    pdf_error = None
    if PDF_EXPORT_AVAILABLE:
        try:
            pdf_bytes = build_pdf_report(
                scan_name or "study",
                result_language or "English",
                findings,
                result,
                scan_path,
                heatmap,
            )
        except Exception as exc:
            pdf_error = f"{type(exc).__name__}: {exc}"

    pdf_col, text_col = st.columns(2, gap="medium")

    with pdf_col:
        st.markdown(
            f"""
            <div class="ms-export-feature{" ms-rtl" if urdu_output else ""}" dir="{"rtl" if urdu_output else "ltr"}">
                <strong>{"مکمل اردو پی ڈی ایف رپورٹ" if urdu_output else "Clinical PDF report"}</strong>
                <p>{"مکمل اردو طبی رپورٹ، اصل ایکس رے اور ماڈل کی توجہ کے نقشے کے ساتھ۔" if urdu_output else "Presentation-ready document with structured sections and both imaging views embedded at readable size."}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.download_button(
            "اردو پی ڈی ایف رپورٹ ڈاؤن لوڈ کریں" if urdu_output else "Download PDF report",
            data=pdf_bytes or b"",
            file_name=f"medscribe_{Path(scan_name or 'study').stem}_clinical_report.pdf",
            mime="application/pdf",
            use_container_width=True,
            disabled=pdf_bytes is None,
        )
        if pdf_error:
            print(f"[MedScribe AI] PDF generation error: {pdf_error}")
            st.error(
                "اردو پی ڈی ایف تیار نہیں ہو سکی۔ اپ ڈیٹ شدہ app.py اور requirements.txt کے ساتھ دوبارہ deploy کریں۔"
                if urdu_output
                else
                "The PDF could not be prepared. Please redeploy with the updated dependencies."
            )

    with text_col:
        st.markdown(
            f"""
            <div class="ms-export-feature{" ms-rtl" if urdu_output else ""}" dir="{"rtl" if urdu_output else "ltr"}">
                <strong>{"سادہ متن کی رپورٹ" if urdu_output else "Plain-text record"}</strong>
                <p>{"نتائج، طبی رپورٹ، فوری نوعیت اور مریض کے خلاصے پر مشتمل سادہ اردو متن۔" if urdu_output else "Lightweight fallback containing the findings, report, urgency and patient summary without embedded images."}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.download_button(
            "اردو متن کی رپورٹ ڈاؤن لوڈ کریں" if urdu_output else "Download text record",
            data=export_text(scan_name or "study", result_language or "", findings, result),
            file_name=f"medscribe_{Path(scan_name or 'study').stem}_report.txt",
            mime="text/plain",
            use_container_width=True,
        )

    if not PDF_EXPORT_AVAILABLE:
        st.warning(
            "پی ڈی ایف رپورٹ کے لیے ReportLab درکار ہے۔ requirements.txt اپ ڈیٹ کرکے دوبارہ ڈپلائے کریں۔"
            if urdu_output
            else
            "PDF export requires ReportLab. Add `reportlab>=4.2` to requirements.txt and redeploy."
        )


# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown(
    """
    <footer class="ms-footer">
        <div><strong>MedScribe AI</strong> · AI-assisted radiology intelligence</div>
        <div>
            Clinical review required · Generated outputs must not be used as a standalone diagnosis.
        </div>
    </footer>
    """,
    unsafe_allow_html=True,
)
