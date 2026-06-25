"""components/page_header.py — Title, tagline, pro tip banner"""
import streamlit as st
from styles import MAIN_TITLE_HTML, TAGLINE_HTML, PRO_TIP_BANNER_HTML


def render_pro_tip_banner():
    st.markdown(PRO_TIP_BANNER_HTML, unsafe_allow_html=True)


def render_main_title():
    st.markdown(MAIN_TITLE_HTML,  unsafe_allow_html=True)
    st.markdown(TAGLINE_HTML,     unsafe_allow_html=True)
