"""
components/template_and_photo.py — Step 1
Visual template cards + photo upload + quick actions.
All st.markdown calls have unsafe_allow_html=True.
"""
import streamlit as st
from config import TEMPLATE_CHOICES, DEFAULT_RESUME_DATA
from _section_header import section_header

TEMPLATE_META = {
    "modern":       ("&#128309;", "Blue banner header, clean",        "#0EA5E9"),
    "professional": ("&#128220;", "Classic serif, formal",             "#2563EB"),
    "minimal":      ("&#9633;",   "Ultra-clean, no color blocks",      "#64748B"),
    "blue_sidebar": ("&#128193;", "Sidebar layout — recruiter fav",    "#2563EB"),
    "executive":    ("&#127963;", "Dark navy + gold accent",           "#0F172A"),
    "creative":     ("&#127912;", "Tri-color header, bold",            "#EC4899"),
    "tech":         ("&#128187;", "Green terminal, dev-friendly",      "#10B981"),
    "academic":     ("&#127891;", "Serif, centered — great for CVs",   "#1E293B"),
    "multi_column": ("&#128202;", "Two-column skills, info-dense",     "#0EA5E9"),
}


def render_template_and_photo():
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    section_header(1, "&#127912;", "Choose Template & Upload Photo",
                   "Click a card to select your template style")

    current = st.session_state.resume_data.get('template', 'modern')
    templates = TEMPLATE_CHOICES
    rows = [templates[i:i+3] for i in range(0, len(templates), 3)]

    for row in rows:
        cols = st.columns(len(row))
        for col, tmpl in zip(cols, row):
            with col:
                icon, tagline, color = TEMPLATE_META.get(tmpl, ("&#128196;", "", "#6366f1"))
                is_selected = (tmpl == current)
                border = ("2px solid " + color) if is_selected else "1.5px solid #e2e8f0"
                bg     = "#f5f3ff" if is_selected else "#ffffff"
                shadow = "0 4px 12px rgba(99,102,241,0.18)" if is_selected else "0 1px 4px rgba(0,0,0,0.05)"
                check  = "Selected" if is_selected else tmpl.replace('_',' ').title()

                st.markdown(
                    '<div style="background:' + bg + ';border:' + border + ';'
                    'border-radius:14px;padding:12px 10px;text-align:center;'
                    'box-shadow:' + shadow + ';margin-bottom:4px;">'
                    '<div style="font-size:1.5rem;margin-bottom:4px;">' + icon + '</div>'
                    '<div style="font-size:0.8rem;font-weight:700;color:#1e293b;">'
                    + tmpl.replace('_',' ').title() + '</div>'
                    '<div style="font-size:0.7rem;color:#64748b;margin-top:3px;line-height:1.3;">'
                    + tagline + '</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

                if st.button(
                    check,
                    key="tmpl_btn_" + tmpl,
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"
                ):
                    st.session_state.resume_data['template'] = tmpl
                    st.rerun()

    st.markdown('<hr style="border:none;border-top:1px solid #e2e8f0;margin:1rem 0;">',
                unsafe_allow_html=True)

    photo_col, action_col = st.columns([1, 1])

    with photo_col:
        st.markdown(
            '<div style="font-size:0.9rem;font-weight:600;color:#374151;margin-bottom:6px;">'
            '&#128248; Profile Photo <span style="font-size:0.75rem;color:#94a3b8;">(optional)</span>'
            '</div>',
            unsafe_allow_html=True
        )
        uploaded_photo = st.file_uploader(
            "Upload photo", type=['jpg','jpeg','png'],
            key="photo_upload", label_visibility="collapsed",
            help="Square crop recommended, min 200x200px"
        )
        if uploaded_photo:
            st.session_state.resume_data['photo'] = uploaded_photo.getvalue()
            st.image(uploaded_photo, width=100, caption="Photo ready")
        elif st.session_state.resume_data.get('photo'):
            st.markdown(
                '<div style="font-size:0.8rem;color:#059669;">Photo already uploaded</div>',
                unsafe_allow_html=True
            )

    with action_col:
        st.markdown(
            '<div style="font-size:0.9rem;font-weight:600;color:#374151;margin-bottom:6px;">'
            '&#9889; Quick Actions</div>',
            unsafe_allow_html=True
        )
        if st.button("Clear All Data", use_container_width=True):
            st.session_state.resume_data = dict(DEFAULT_RESUME_DATA)
            for k in ['experience','education','projects','references']:
                st.session_state.resume_data[k] = []
            st.session_state.pdf_ready = False
            st.session_state.pdf_bytes = None
            st.rerun()

        if st.button("Fill Sample Data", use_container_width=True,
                     help="Fills demo data to preview how the app looks"):
            st.session_state.resume_data.update({
                'name': 'Ali Hassan', 'professional_title': 'Senior Software Engineer',
                'email': 'ali.hassan@email.com', 'phone': '+92 300 1234567',
                'address': 'Lahore, Pakistan', 'linkedin': 'linkedin.com/in/alihassan',
                'summary': (
                    'Experienced Software Engineer with 4+ years in Python and Web Development. '
                    'Proven track record of building scalable systems serving 100k+ users.'
                ),
                'skills': 'Python, Django, React, PostgreSQL, Docker, AWS',
                'languages': 'English - Fluent, Urdu - Native',
                'hobbies': 'Open Source, Photography, Traveling',
            })
            st.success("Sample data filled!")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
