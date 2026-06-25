"""components/education_section.py — Step 5"""
import streamlit as st
from _section_header import section_header


def render_education_section():
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    section_header(5, "&#127891;", "Education", "Most recent degree first")

    data = st.session_state.resume_data
    edu_count = st.number_input(
        "How many degrees / diplomas?", 0, 5,
        value=len(data['education']), key="edu_count"
    )

    while len(data['education']) < edu_count:
        data['education'].append({'degree':'','institute':'','year':'','grade':''})
    while len(data['education']) > edu_count:
        data['education'].pop()

    for i in range(edu_count):
        edu   = data['education'][i]
        label = edu.get('degree') or ("Degree " + str(i + 1))
        with st.expander(label, expanded=(i == 0)):
            c1, c2, c3 = st.columns([2, 2, 1])
            with c1:
                edu['degree'] = st.text_input(
                    "Degree / Program *", value=edu['degree'],
                    key="edu_deg_" + str(i), placeholder="BS Computer Science"
                )
            with c2:
                edu['institute'] = st.text_input(
                    "University / Institute *", value=edu['institute'],
                    key="edu_inst_" + str(i), placeholder="FAST NUCES Lahore"
                )
            with c3:
                edu['year'] = st.text_input(
                    "Year", value=edu['year'],
                    key="edu_year_" + str(i), placeholder="2020-2024"
                )
            edu['grade'] = st.text_input(
                "CGPA / Grade", value=edu['grade'],
                key="edu_grade_" + str(i), placeholder="3.8/4.0  or  85%"
            )

    st.markdown('</div>', unsafe_allow_html=True)
