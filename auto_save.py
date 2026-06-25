"""
components/auto_save.py
========================
NEW FEATURE: Auto-save with "Last saved X min ago" indicator.

Since Streamlit has no localStorage, we use session_state as the
in-memory save store. Every time data changes from the last snapshot,
we update the snapshot and timestamp.

Call `auto_save()` once near the top of app.py after init_session_state().
The progress_bar.py reads last_saved_time to show the badge.
"""
import datetime
import json
import streamlit as st


def _data_fingerprint(data: dict) -> str:
    """A lightweight hash-like string to detect data changes."""
    try:
        # Serialize only scalar/list values for comparison
        slim = {
            k: (v if not isinstance(v, bytes) else "<photo>")
            for k, v in data.items()
        }
        return json.dumps(slim, sort_keys=True, default=str)
    except Exception:
        return ""


def auto_save():
    """
    Call this once per rerun (in app.py after init_session_state).
    Compares current resume_data to last snapshot.
    If changed → updates snapshot + timestamp.
    """
    if 'resume_data' not in st.session_state:
        return

    current_fp = _data_fingerprint(st.session_state.resume_data)
    last_fp    = st.session_state.get('auto_save_snapshot', '')

    if current_fp != last_fp:
        st.session_state.auto_save_snapshot = current_fp
        st.session_state.last_saved_time    = datetime.datetime.now()


def get_save_badge_html() -> str:
    """Returns an HTML string for the save badge. Used in page_header."""
    if not st.session_state.get('last_saved_time'):
        return ""

    diff = datetime.datetime.now() - st.session_state.last_saved_time
    mins = int(diff.total_seconds() / 60)

    if mins < 1:
        text = "💾 Saved just now"
        color = "#059669"
        bg = "#ecfdf5"
        border = "#6ee7b7"
    elif mins <= 5:
        text = f"💾 Saved {mins} min ago"
        color = "#4f46e5"
        bg = "#eef2ff"
        border = "#c7d2fe"
    else:
        text = f"💾 Last saved {mins} min ago"
        color = "#94a3b8"
        bg = "#f8fafc"
        border = "#e2e8f0"

    return f"""
    <span style="
        background:{bg};color:{color};
        border:1px solid {border};
        border-radius:20px;padding:3px 10px;
        font-size:0.72rem;font-weight:600;
        display:inline-flex;align-items:center;gap:4px;
    ">{text}</span>"""
