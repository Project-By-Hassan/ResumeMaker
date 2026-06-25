"""components/footer.py — Footer (upgraded)"""
import streamlit as st
from config import APP_VERSION, DEVELOPER_NAME
from styles import footer_html


def render_footer():
    st.divider()
    st.markdown(footer_html(APP_VERSION, DEVELOPER_NAME), unsafe_allow_html=True)
