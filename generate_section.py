"""components/generate_section.py — Step 9: Generate PDF & Download"""
import streamlit as st
from pdf_generator import generate_pdf
from data_store import increment_resume_count
from _section_header import section_header


def _ats_score(data):
    score = 0
    if data.get('name'):               score += 10
    if data.get('email'):              score += 10
    if data.get('phone'):              score += 5
    if data.get('professional_title'): score += 10
    if data.get('summary', '').strip(): score += 15
    if data.get('experience'):         score += 20
    if data.get('education'):          score += 15
    count = len([s for s in data.get('skills','').split(',') if s.strip()])
    if count >= 6:  score += 10
    elif count >= 3: score += 5
    if data.get('linkedin'):           score += 5
    return min(score, 100)


def render_generate_section():
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    section_header(9, "&#128190;", "Generate & Download Resume",
                   "Your resume will be generated as a professional PDF")

    data = st.session_state.resume_data
    ats  = _ats_score(data)

    if ats >= 80:
        ac, al, ab = "#10b981", "Excellent", "#f0fdf4"
    elif ats >= 60:
        ac, al, ab = "#6366f1", "Good",      "#eef2ff"
    elif ats >= 40:
        ac, al, ab = "#f59e0b", "Fair",      "#fffbeb"
    else:
        ac, al, ab = "#e11d48", "Needs Work","#fff1f2"

    tip = ("Great! Your resume is ATS-ready." if ats >= 80
           else "Fill more sections to boost your score.")
    bar_w = str(ats) + "%"

    st.markdown(
        '<div style="background:' + ab + ';border:1.5px solid ' + ac + '33;'
        'border-radius:14px;padding:14px 18px;margin-bottom:1.2rem;'
        'display:flex;align-items:center;gap:16px;">'
        '<div style="text-align:center;min-width:56px;">'
        '<div style="font-size:1.8rem;font-weight:800;color:' + ac + ';line-height:1;">'
        + str(ats) + '</div>'
        '<div style="font-size:0.67rem;color:' + ac + ';font-weight:600;">/ 100</div>'
        '</div>'
        '<div style="flex:1;">'
        '<div style="font-size:0.9rem;font-weight:700;color:#1e293b;">'
        'ATS Score — <span style="color:' + ac + ';">' + al + '</span></div>'
        '<div style="background:#e2e8f0;border-radius:6px;height:8px;margin-top:6px;overflow:hidden;">'
        '<div style="width:' + bar_w + ';height:100%;background:' + ac + ';border-radius:6px;"></div>'
        '</div>'
        '<div style="font-size:0.72rem;color:#64748b;margin-top:5px;">' + tip + '</div>'
        '</div></div>',
        unsafe_allow_html=True
    )

    missing = []
    if not data.get('name'):    missing.append("Full Name")
    if not data.get('email'):   missing.append("Email")
    if not data.get('summary'): missing.append("Summary")
    if missing:
        st.warning("Recommended fields missing: " + ", ".join(missing))

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Preview Data (JSON)", use_container_width=True):
            with st.expander("Resume Data", expanded=True):
                st.json(data)
    with c2:
        if st.button("Generate PDF", use_container_width=True, type="primary"):
            with st.spinner("Building your resume PDF..."):
                pdf_bytes, error = generate_pdf(data)
                if pdf_bytes:
                    st.session_state.pdf_ready    = True
                    st.session_state.pdf_bytes    = pdf_bytes
                    safe_name = data['name'].replace(' ','_') if data['name'] else "My_Resume"
                    st.session_state.pdf_filename = safe_name + "_Resume.pdf"
                    increment_resume_count()
                    st.rerun()
                else:
                    st.error("Error generating PDF: " + str(error))

    if st.session_state.get('pdf_ready') and st.session_state.get('pdf_bytes'):
        st.markdown(
            '<div style="background:linear-gradient(135deg,#d1fae5,#a7f3d0);'
            'border:1.5px solid #6ee7b7;border-radius:14px;padding:14px 20px;'
            'text-align:center;margin:12px 0;">'
            '<div style="font-size:1.3rem;">&#127881;</div>'
            '<div style="font-size:1rem;font-weight:700;color:#065f46;">Resume PDF is Ready!</div>'
            '</div>',
            unsafe_allow_html=True
        )
        st.download_button(
            label="Download Resume PDF",
            data=st.session_state.pdf_bytes,
            file_name=st.session_state.pdf_filename,
            mime="application/pdf",
            use_container_width=True
        )
        fname = st.session_state.pdf_filename
        st.markdown(
            '<div style="background:#f8faff;border:1px solid #e8eaf6;border-radius:10px;'
            'padding:10px 14px;font-size:0.78rem;color:#64748b;margin-top:6px;">'
            'File: <strong>' + fname + '</strong> — saved to your Downloads folder'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("Generate New Resume", use_container_width=True):
            st.session_state.pdf_ready = False
            st.session_state.pdf_bytes = None
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
