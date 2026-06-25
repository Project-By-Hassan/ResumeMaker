"""components/admin_sidebar.py — Sidebar admin login"""
import streamlit as st
from config import ADMIN_PASSWORD
from styles import ADMIN_LABEL_CSS


def render_admin_sidebar():
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False

    with st.sidebar:
        st.markdown(ADMIN_LABEL_CSS, unsafe_allow_html=True)
        st.markdown('<p class="admin-label">&#128272; Admin Access</p>', unsafe_allow_html=True)
        st.markdown("---")

        if not st.session_state.is_admin:
            admin_pass = st.text_input(
                "Password", type="password", key="admin_pass",
                label_visibility="collapsed", placeholder="Admin Password"
            )
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Login", use_container_width=True):
                    if admin_pass == ADMIN_PASSWORD:
                        st.session_state.is_admin = True
                        st.success("Admin access granted")
                        st.rerun()
                    else:
                        st.error("Wrong password")
            with c2:
                if st.button("Normal", use_container_width=True):
                    st.info("Normal mode")
        else:
            st.success("Admin Active")
            if st.button("Logout", use_container_width=True):
                st.session_state.is_admin = False
                st.rerun()
