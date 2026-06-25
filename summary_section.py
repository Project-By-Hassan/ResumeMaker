"""components/summary_section.py — Step 3"""
import streamlit as st
from _section_header import section_header


def render_summary_section():
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    section_header(3, "&#128221;", "Professional Summary",
                   "2-4 lines that make recruiters want to read more")

    data = st.session_state.resume_data
    data['summary'] = st.text_area(
        "Summary",
        value=data['summary'],
        placeholder=(
            "Experienced Software Engineer with 4+ years in Python and Web Development. "
            "Proven track record of building scalable systems. "
            "Passionate about clean code and continuous learning."
        ),
        height=130, key="summary_input",
        label_visibility="collapsed"
    )

    char_count = len(data['summary'])
    if char_count == 0:
        color, msg = "#94a3b8", "Start writing your summary..."
    elif char_count < 100:
        color, msg = "#f59e0b", str(char_count) + " chars — too short, aim for 300-600"
    elif char_count <= 600:
        color, msg = "#10b981", str(char_count) + " chars — great length"
    else:
        color, msg = "#e11d48", str(char_count) + " chars — too long, keep under 600"

    st.markdown(
        '<div style="font-size:0.78rem;font-weight:600;color:' + color + ';margin-top:5px;">'
        + msg + '</div>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
