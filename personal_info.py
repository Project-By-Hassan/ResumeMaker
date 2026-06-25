"""components/personal_info.py — Step 2"""
import streamlit as st
from _section_header import section_header


def render_personal_info():
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    section_header(2, "&#128100;", "Personal Information",
                   "Basic details that appear at the top of your resume")

    data = st.session_state.resume_data

    c1, c2 = st.columns(2)
    with c1:
        data['name'] = st.text_input(
            "Full Name *", value=data['name'],
            placeholder="Hassan Raza", key="name_input",
            help="Use your real full name — ATS systems match exact names"
        )
    with c2:
        data['professional_title'] = st.text_input(
            "Professional Title", value=data['professional_title'],
            placeholder="Senior Software Engineer", key="prof_title_input"
        )

    c1, c2 = st.columns(2)
    with c1:
        data['email'] = st.text_input(
            "Email Address *", value=data['email'],
            placeholder="hassan@email.com", key="email_input"
        )
    with c2:
        data['phone'] = st.text_input(
            "Phone Number", value=data['phone'],
            placeholder="+92 300 1234567", key="phone_input"
        )

    c1, c2 = st.columns(2)
    with c1:
        data['address'] = st.text_input(
            "City / Address", value=data['address'],
            placeholder="Lahore, Pakistan", key="address_input"
        )
    with c2:
        data['linkedin'] = st.text_input(
            "LinkedIn", value=data['linkedin'],
            placeholder="linkedin.com/in/hassan-raza", key="linkedin_input"
        )

    with st.expander("Additional Details (Father Name, DOB, Religion, Nationality)"):
        c1, c2 = st.columns(2)
        with c1:
            data['father_name'] = st.text_input(
                "Father Name", value=data['father_name'],
                placeholder="Minato Namikaze", key="father_name_input"
            )
            data['dob'] = st.text_input(
                "Date of Birth", value=data['dob'],
                placeholder="01-Jan-1995", key="dob_input"
            )
        with c2:
            data['religion'] = st.text_input(
                "Religion", value=data['religion'],
                placeholder="Islam", key="religion_input"
            )
            data['nationality'] = st.text_input(
                "Nationality", value=data['nationality'],
                placeholder="Pakistani", key="nationality_input"
            )

    if data['name'] and len(data['name']) < 3:
        st.warning("Name seems too short — use your full name.")
    if data['email'] and '@' not in data['email']:
        st.warning("Email address looks invalid.")

    st.markdown('</div>', unsafe_allow_html=True)
