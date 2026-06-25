"""components/admin_panel.py — Admin stats panel"""
import streamlit as st
from data_store import load_stats, load_feedback, clear_all_stats


def render_admin_panel():
    if not st.session_state.is_admin:
        return

    st.markdown(
        '<div style="background:#fff7ed;border:1.5px solid #fed7aa;border-radius:16px;'
        'padding:1.5rem;margin-top:2rem;">'
        '<div style="display:flex;align-items:center;gap:10px;margin-bottom:1rem;">'
        '<span style="font-size:1.5rem;">&#128293;</span>'
        '<div>'
        '<div style="font-size:1.1rem;font-weight:700;color:#c2410c;">Admin Panel</div>'
        '<div style="font-size:0.78rem;color:#ea580c;">Only visible to admin</div>'
        '</div></div></div>',
        unsafe_allow_html=True
    )

    stats         = load_stats()
    feedback_data = load_feedback()
    avg_rating    = (
        sum(f["rating"] for f in feedback_data) / len(feedback_data)
        if feedback_data else 0
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Resumes", stats["total_resumes"])
    with c2:
        st.metric("Today's Resumes", stats["today_count"])
    with c3:
        st.metric("Avg Rating", str(round(avg_rating, 1)) + " / 5")

    st.markdown("**Recent Feedback**")
    if feedback_data:
        for fb in reversed(feedback_data[-5:]):
            stars = "⭐" * int(fb["rating"])
            st.markdown(
                '<div style="background:#ffffff;border:1px solid #e8eaf6;border-radius:10px;'
                'padding:8px 12px;margin-bottom:6px;font-size:0.85rem;">'
                + stars + ' &nbsp; ' + str(fb["comment"]) +
                ' <span style="color:#94a3b8;float:right;">' + str(fb["time"])[:16] + '</span></div>',
                unsafe_allow_html=True
            )
    else:
        st.info("No feedback yet.")

    if st.button("Clear All Stats & Feedback"):
        clear_all_stats()
        st.success("All stats cleared.")
        st.rerun()
