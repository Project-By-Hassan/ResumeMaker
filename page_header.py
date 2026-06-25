"""
page_header.py
==============
Renders the Pro Tip banner and main title on the app.
app.py imports: render_pro_tip_banner, render_main_title
"""
import streamlit as st
from styles import PRO_TIP_BANNER_HTML, MAIN_TITLE_HTML, TAGLINE_HTML


def render_pro_tip_banner():
    st.markdown(PRO_TIP_BANNER_HTML, unsafe_allow_html=True)


def render_main_title():
    st.markdown(MAIN_TITLE_HTML, unsafe_allow_html=True)
    st.markdown(TAGLINE_HTML, unsafe_allow_html=True)
