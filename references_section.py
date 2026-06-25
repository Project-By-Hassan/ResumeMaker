"""components/references_section.py — Step 8"""
import streamlit as st
from _section_header import section_header


def render_references_section():
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    section_header(8, "&#128222;", "References", "Optional — 1-2 professional references")

    data = st.session_state.resume_data
    ref_count = st.number_input(
        "How many references?", 0, 3,
        value=len(data['references']), key="ref_count"
    )

    while len(data['references']) < ref_count:
        data['references'].append({'name':'','position':'','contact':''})
    while len(data['references']) > ref_count:
        data['references'].pop()

    for i in range(ref_count):
        ref   = data['references'][i]
        label = ref.get('name') or ("Reference " + str(i + 1))
        with st.expander(label, expanded=(i == 0)):
            c1, c2 = st.columns(2)
            with c1:
                ref['name'] = st.text_input(
                    "Reference Name *", value=ref['name'],
                    key="ref_name_" + str(i), placeholder="Dr. Ahmed Khan"
                )
                ref['position'] = st.text_input(
                    "Title / Position", value=ref['position'],
                    key="ref_pos_" + str(i), placeholder="Professor, FAST NUCES"
                )
            with c2:
                ref['contact'] = st.text_input(
                    "Contact (Email or Phone)", value=ref['contact'],
                    key="ref_contact_" + str(i), placeholder="ahmed@fast.edu.pk"
                )
                # avatar card
                initials = "".join(w[0].upper() for w in ref['name'].split()[:2]) if ref['name'] else "?"
                rname    = ref['name'] or "Reference Name"
                rpos     = ref['position'] or "Position"
                st.markdown(
                    '<div style="display:flex;align-items:center;gap:10px;margin-top:8px;'
                    'padding:10px;background:#f8faff;border-radius:10px;border:1px solid #e8eaf6;">'
                    '<div style="width:38px;height:38px;border-radius:50%;'
                    'background:linear-gradient(135deg,#6366f1,#7c3aed);'
                    'display:flex;align-items:center;justify-content:center;'
                    'color:white;font-weight:700;font-size:0.85rem;flex-shrink:0;">'
                    + initials +
                    '</div>'
                    '<div>'
                    '<div style="font-size:0.82rem;font-weight:600;color:#1e293b;">' + rname + '</div>'
                    '<div style="font-size:0.72rem;color:#64748b;">' + rpos + '</div>'
                    '</div></div>',
                    unsafe_allow_html=True
                )

    st.markdown('</div>', unsafe_allow_html=True)
