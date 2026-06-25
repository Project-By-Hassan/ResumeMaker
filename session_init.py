"""
session_init.py
===============
Streamlit session_state ke saare defaults ek jagah.

UPGRADES:
- auto_saved_data: localStorage-style auto-save state
- last_saved_time: "Last saved X min ago" badge ke liye
- ai_rewriting: AI rewrite spinner flag
- ats_score: cached ATS score
"""
import streamlit as st
from config import DEFAULT_RESUME_DATA


def init_session_state():
    if 'resume_data' not in st.session_state:
        st.session_state.resume_data = {
            k: (list(v) if isinstance(v, list) else v)
            for k, v in DEFAULT_RESUME_DATA.items()
        }

    if 'pdf_ready' not in st.session_state:
        st.session_state.pdf_ready = False
    if 'pdf_bytes' not in st.session_state:
        st.session_state.pdf_bytes = None
    if 'pdf_filename' not in st.session_state:
        st.session_state.pdf_filename = ""
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False

    # ── NEW: Auto-save ───────────────────────────────────────────────
    if 'last_saved_time' not in st.session_state:
        st.session_state.last_saved_time = None
    if 'auto_save_snapshot' not in st.session_state:
        st.session_state.auto_save_snapshot = None

    # ── NEW: ATS score cache ─────────────────────────────────────────
    if 'ats_score' not in st.session_state:
        st.session_state.ats_score = None
    if 'ats_details' not in st.session_state:
        st.session_state.ats_details = {}

    # ── NEW: AI rewrite state ────────────────────────────────────────
    if 'ai_rewrite_result' not in st.session_state:
        st.session_state.ai_rewrite_result = {}

    # ── NEW: completion tracking ─────────────────────────────────────
    if 'sections_completed' not in st.session_state:
        st.session_state.sections_completed = set()
