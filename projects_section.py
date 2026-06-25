"""components/projects_section.py — Step 7"""
import streamlit as st
from _section_header import section_header


def render_projects_section():
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    section_header(7, "&#128640;", "Projects", "Optional — highlight your best 2-3 projects")

    data = st.session_state.resume_data
    proj_count = st.number_input(
        "How many projects?", 0, 5,
        value=len(data['projects']), key="proj_count"
    )

    while len(data['projects']) < proj_count:
        data['projects'].append({'name':'','tech':'','desc':''})
    while len(data['projects']) > proj_count:
        data['projects'].pop()

    for i in range(proj_count):
        proj  = data['projects'][i]
        label = proj.get('name') or ("Project " + str(i + 1))
        with st.expander(label, expanded=(i == 0)):
            proj['name'] = st.text_input(
                "Project Name *", value=proj['name'],
                key="proj_name_" + str(i), placeholder="E-Commerce Platform"
            )
            proj['tech'] = st.text_input(
                "Technologies Used", value=proj['tech'],
                key="proj_tech_" + str(i), placeholder="Python, Django, React, PostgreSQL"
            )
            if proj['tech'].strip():
                items = [t.strip() for t in proj['tech'].split(',') if t.strip()]
                pills = ''.join(
                    '<span style="background:#f5f3ff;color:#6d28d9;border:1px solid #ddd6fe;'
                    'font-size:0.68rem;font-weight:600;padding:2px 8px;border-radius:20px;'
                    'margin:2px;display:inline-block;">' + t + '</span>'
                    for t in items
                )
                st.markdown('<div style="margin-bottom:6px;">' + pills + '</div>',
                            unsafe_allow_html=True)
            proj['desc'] = st.text_area(
                "Project Description", value=proj['desc'],
                key="proj_desc_" + str(i),
                placeholder="Built full-stack e-commerce with 1000+ users, integrated payment gateway",
                height=80
            )

    st.markdown('</div>', unsafe_allow_html=True)
