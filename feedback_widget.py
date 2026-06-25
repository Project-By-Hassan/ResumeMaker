"""components/feedback_widget.py — Feedback + JazzCash"""
import streamlit as st
from config import DEVELOPER_NAME, JAZZCASH_NUMBER
from data_store import save_feedback
from styles import jazzcash_card_html


def render_feedback_widget():
    st.markdown(
        '<div style="background:#ffffff;border:1px solid #e8eaf6;border-radius:16px;'
        'padding:1.5rem;margin-top:1.5rem;box-shadow:0 2px 10px rgba(99,102,241,0.06);">'
        '<div style="font-size:1rem;font-weight:700;color:#1e293b;margin-bottom:1rem;">'
        '&#128172; Share Your Feedback</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns([1, 3])
    with c1:
        rating = st.select_slider(
            "Rating", options=[1, 2, 3, 4, 5], value=5, key="fb_rating",
            format_func=lambda x: "⭐" * x
        )
    with c2:
        comment = st.text_input(
            "Comment", placeholder="What did you like or what can be improved?",
            key="fb_comment", label_visibility="collapsed"
        )

    if st.button("Submit Feedback", use_container_width=True):
        if comment.strip():
            save_feedback(rating, comment)
            st.success("Thanks for your feedback!")
            st.balloons()
        else:
            st.warning("Please write a short comment before submitting.")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:0.8rem;"></div>', unsafe_allow_html=True)

    if "show_jazzcash" not in st.session_state:
        st.session_state.show_jazzcash = False

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("Buy Me a Coffee ☕", use_container_width=True, type="primary"):
            st.session_state.show_jazzcash = not st.session_state.show_jazzcash

    if st.session_state.show_jazzcash:
        st.markdown(jazzcash_card_html(DEVELOPER_NAME.upper(), JAZZCASH_NUMBER),
                    unsafe_allow_html=True)
