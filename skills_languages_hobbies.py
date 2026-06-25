"""components/skills_languages_hobbies.py — Step 6"""
import streamlit as st
from _section_header import section_header


def _pills(text, bg, color, border):
    items = [s.strip() for s in text.split(',') if s.strip()]
    if not items:
        return
    html = '<div style="display:flex;flex-wrap:wrap;gap:3px;margin-top:6px;margin-bottom:4px;">'
    for item in items:
        html += (
            '<span style="background:' + bg + ';color:' + color + ';'
            'border:1px solid ' + border + ';font-size:0.72rem;font-weight:600;'
            'padding:3px 10px;border-radius:20px;">' + item + '</span>'
        )
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def render_skills_languages_hobbies():
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    section_header(6, "&#9889;", "Skills, Languages & Hobbies",
                   "Comma-separated — live pill preview below each field")

    data = st.session_state.resume_data

    data['skills'] = st.text_area(
        "Technical & Soft Skills",
        value=data['skills'],
        placeholder="Python, Django, React, PostgreSQL, Docker, AWS, Leadership",
        height=85, key="skills_input",
        help="Separate with commas. Include both technical and soft skills."
    )
    if data['skills'].strip():
        skill_count = len([s for s in data['skills'].split(',') if s.strip()])
        color = "#10b981" if skill_count >= 6 else "#f59e0b"
        msg   = ("Good skill mix" if skill_count >= 6
                 else ("Add more skills (have " + str(skill_count) + ", recommend 8+)"))
        st.markdown(
            '<div style="font-size:0.75rem;color:' + color + ';font-weight:600;">'
            + msg + '</div>',
            unsafe_allow_html=True
        )
        _pills(data['skills'], "#eef2ff", "#4f46e5", "#c7d2fe")

    st.markdown('<hr style="border:none;border-top:1px solid #f1f5f9;margin:0.7rem 0;">',
                unsafe_allow_html=True)

    data['languages'] = st.text_area(
        "Languages",
        value=data['languages'],
        placeholder="English - Fluent, Urdu - Native, Arabic - Basic",
        height=70, key="languages_input"
    )
    if data['languages'].strip():
        _pills(data['languages'], "#f0fdf4", "#166534", "#bbf7d0")

    st.markdown('<hr style="border:none;border-top:1px solid #f1f5f9;margin:0.7rem 0;">',
                unsafe_allow_html=True)

    data['hobbies'] = st.text_area(
        "Hobbies & Interests",
        value=data['hobbies'],
        placeholder="Open Source, Photography, Traveling, Cricket",
        height=70, key="hobbies_input"
    )
    if data['hobbies'].strip():
        _pills(data['hobbies'], "#fff7ed", "#c2410c", "#fed7aa")

    st.markdown('</div>', unsafe_allow_html=True)
