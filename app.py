"""
app.py — Resume Builder Pro (FLAT STRUCTURE — no subfolders)
All files in root directory. No components/ or templates_pdf/ folders needed.
"""
import streamlit as st

from session_init import init_session_state
from styles import PADDING_RESET_CSS, MAIN_THEME_CSS

from admin_sidebar import render_admin_sidebar
from profile_photo import render_profile_photo
from page_header import render_pro_tip_banner, render_main_title
from template_and_photo import render_template_and_photo
from personal_info import render_personal_info
from summary_section import render_summary_section
from experience_section import render_experience_section
from education_section import render_education_section
from skills_languages_hobbies import render_skills_languages_hobbies
from projects_section import render_projects_section
from references_section import render_references_section
from generate_section import render_generate_section
from footer import render_footer
from admin_panel import render_admin_panel
from feedback_widget import render_feedback_widget
from live_preview import render_live_preview
from progress_bar import render_progress_bar

st.set_page_config(
    page_title="Resume Builder Pro",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

render_admin_sidebar()
st.markdown(PADDING_RESET_CSS, unsafe_allow_html=True)
st.markdown(MAIN_THEME_CSS,    unsafe_allow_html=True)
init_session_state()
render_profile_photo()
render_pro_tip_banner()
render_main_title()
render_progress_bar()

form_col, preview_col = st.columns([1.2, 1], gap="large")

with form_col:
    render_template_and_photo()
    render_personal_info()
    render_summary_section()
    render_experience_section()
    render_education_section()
    render_skills_languages_hobbies()
    render_projects_section()
    render_references_section()
    render_generate_section()

with preview_col:
    render_live_preview()

render_footer()
render_admin_panel()
render_feedback_widget()
