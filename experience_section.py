"""components/experience_section.py — Step 4"""
import streamlit as st
from _section_header import section_header


def render_experience_section():
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    section_header(4, "&#128188;", "Work Experience", "List your most recent jobs first")

    data = st.session_state.resume_data
    exp_count = st.number_input(
        "How many work experiences?", 0, 10,
        value=len(data['experience']), key="exp_count"
    )

    while len(data['experience']) < exp_count:
        data['experience'].append({'title':'','company':'','duration':'','location':'','desc':''})
    while len(data['experience']) > exp_count:
        data['experience'].pop()

    for i in range(exp_count):
        exp = data['experience'][i]
        filled = sum(1 for k in ['title','company','duration','desc'] if exp.get(k,'').strip())
        badge  = "Complete" if filled >= 3 else (str(filled) + "/4 filled")
        label  = exp.get('title') or ("Experience " + str(i + 1))

        with st.expander(label + "  [" + badge + "]", expanded=(i == 0)):
            c1, c2 = st.columns(2)
            with c1:
                exp['title'] = st.text_input(
                    "Job Title *", value=exp['title'],
                    key="exp_title_" + str(i), placeholder="Senior Software Engineer"
                )
                exp['company'] = st.text_input(
                    "Company Name *", value=exp['company'],
                    key="exp_comp_" + str(i), placeholder="Google, Microsoft..."
                )
            with c2:
                exp['duration'] = st.text_input(
                    "Duration *", value=exp['duration'],
                    key="exp_dur_" + str(i), placeholder="Jan 2022 - Present"
                )
                exp['location'] = st.text_input(
                    "Location", value=exp['location'],
                    key="exp_loc_" + str(i), placeholder="Lahore, Pakistan"
                )
            exp['desc'] = st.text_area(
                "Job Description — each point on a new line *",
                value=exp['desc'], key="exp_desc_" + str(i),
                placeholder="Developed REST APIs serving 50k+ daily users\nLed a team of 4 engineers\nReduced load time by 40%",
                height=110,
                help="Write each bullet on a new line. No dashes or bullets needed."
            )
            if exp.get('desc') and len(exp['desc'].strip().split('\n')) < 2:
                st.markdown(
                    '<div style="font-size:0.75rem;color:#f59e0b;">Tip: Add 2-3 bullet points with achievements for better impact</div>',
                    unsafe_allow_html=True
                )

    st.markdown('</div>', unsafe_allow_html=True)
