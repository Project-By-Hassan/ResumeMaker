"""
components/live_preview.py  — RIGHT COLUMN LIVE PREVIEW
Bug fixes:
  1. lang_pills variable used before assignment (line 183) — FIXED
  2. All st.markdown calls now have unsafe_allow_html=True explicitly
  3. No nested f-strings — pure string concat throughout
"""
import streamlit as st


def _section(accent, icon_html, title, inner_html):
    """Returns one section block string."""
    return (
        '<div style="margin-bottom:13px;">'
        '<div style="font-size:0.67rem;font-weight:700;letter-spacing:1.4px;'
        'text-transform:uppercase;color:' + accent + ';margin-bottom:5px;">'
        + icon_html + ' ' + title +
        '</div>'
        '<div style="border-left:2px solid #e0e7ff;padding-left:10px;">'
        + inner_html +
        '</div></div>'
    )


def _pill(text, bg, color, border):
    return (
        '<span style="display:inline-block;background:' + bg + ';color:' + color + ';'
        'font-size:0.65rem;font-weight:600;padding:2px 8px;border-radius:20px;'
        'border:1px solid ' + border + ';margin:2px;">' + text + '</span>'
    )


def render_live_preview():
    d = st.session_state.get('resume_data', {})

    name     = d.get('name', '').strip()     or 'Your Name'
    title    = d.get('professional_title', '').strip() or 'Professional Title'
    email    = d.get('email', '').strip()
    phone    = d.get('phone', '').strip()
    addr     = d.get('address', '').strip()
    linkedin = d.get('linkedin', '').strip()

    # accent colour per template
    accent = {
        'modern': '#0ea5e9', 'professional': '#2563eb', 'minimal': '#475569',
        'blue_sidebar': '#2563eb', 'executive': '#334155', 'creative': '#ec4899',
        'tech': '#10b981', 'academic': '#1e293b', 'multi_column': '#0ea5e9',
    }.get(d.get('template', 'modern'), '#6366f1')

    tmpl_label = d.get('template', 'modern').replace('_', ' ').title() + ' Template'

    # ── header widget ──────────────────────────────────────────────
    st.markdown(
        '<div style="display:flex;align-items:center;gap:10px;margin-bottom:1rem;">'
        '<div style="background:linear-gradient(135deg,#6366f1,#7c3aed);border-radius:10px;'
        'width:34px;height:34px;display:flex;align-items:center;justify-content:center;'
        'font-size:1.1rem;flex-shrink:0;">&#128065;</div>'
        '<div>'
        '<div style="font-size:1.05rem;font-weight:700;color:#1e293b;">Live Preview</div>'
        '<div style="font-size:0.8rem;color:#64748b;">Updates as you type</div>'
        '</div>'
        '<span style="margin-left:auto;background:#dcfce7;color:#166534;font-size:0.72rem;'
        'font-weight:600;padding:3px 10px;border-radius:20px;border:1px solid #bbf7d0;">'
        '&#9679; Live</span>'
        '</div>',
        unsafe_allow_html=True
    )

    # ── contact row inside header ──────────────────────────────────
    contact_parts = [p for p in [email, phone, addr, linkedin] if p]
    if contact_parts:
        contact_inner = ' &nbsp;&middot;&nbsp; '.join(
            '<span style="font-size:0.68rem;color:rgba(255,255,255,0.88);">' + p + '</span>'
            for p in contact_parts
        )
    else:
        contact_inner = (
            '<span style="font-size:0.68rem;color:rgba(255,255,255,0.55);font-style:italic;">'
            'No contact info yet</span>'
        )

    # ── body sections ──────────────────────────────────────────────
    body = ''

    # Summary
    summary = d.get('summary', '').strip()
    if summary:
        short = summary[:280] + ('...' if len(summary) > 280 else '')
        body += _section(accent, '&#128221;', 'Professional Summary',
            '<p style="font-size:0.75rem;color:#374151;line-height:1.6;margin:0;">'
            + short + '</p>'
        )

    # Experience
    exps = [e for e in d.get('experience', []) if e.get('title') or e.get('company')]
    if exps:
        rows = ''
        for e in exps[:3]:
            t  = e.get('title', '')
            co = e.get('company', '')
            du = e.get('duration', '')
            lo = e.get('location', '')
            meta = (du + (' &middot; ' + lo if lo else '')) if du else lo
            rows += (
                '<div style="margin-bottom:7px;">'
                '<div style="font-size:0.75rem;font-weight:700;color:#1e293b;">' + t + '</div>'
                '<div style="font-size:0.69rem;color:' + accent + ';font-weight:600;">' + co + '</div>'
                '<div style="font-size:0.65rem;color:#94a3b8;">' + meta + '</div>'
                '</div>'
            )
        body += _section(accent, '&#128188;', 'Work Experience', rows)

    # Education
    edus = [e for e in d.get('education', []) if e.get('degree') or e.get('institute')]
    if edus:
        rows = ''
        for e in edus[:3]:
            deg  = e.get('degree', '')
            inst = e.get('institute', '')
            yr   = e.get('year', '')
            gr   = e.get('grade', '')
            meta = (yr + (' &middot; CGPA: ' + gr if gr else '')) if yr else gr
            rows += (
                '<div style="margin-bottom:7px;">'
                '<div style="font-size:0.75rem;font-weight:700;color:#1e293b;">' + deg + '</div>'
                '<div style="font-size:0.69rem;color:' + accent + ';font-weight:600;">' + inst + '</div>'
                '<div style="font-size:0.65rem;color:#94a3b8;">' + meta + '</div>'
                '</div>'
            )
        body += _section(accent, '&#127891;', 'Education', rows)

    # Skills
    skills_raw = d.get('skills', '').strip()
    if skills_raw:
        skill_list = [s.strip() for s in skills_raw.split(',') if s.strip()][:14]
        pills_html = ''.join(_pill(s, '#eef2ff', '#4f46e5', '#c7d2fe') for s in skill_list)
        body += _section(accent, '&#9889;', 'Skills',
            '<div style="display:flex;flex-wrap:wrap;gap:2px;">' + pills_html + '</div>'
        )

    # Projects
    projs = [p for p in d.get('projects', []) if p.get('name')]
    if projs:
        rows = ''
        for p in projs[:3]:
            rows += (
                '<div style="margin-bottom:6px;">'
                '<div style="font-size:0.75rem;font-weight:700;color:#1e293b;">'
                '&#128640; ' + p.get('name', '') + '</div>'
                '<div style="font-size:0.65rem;color:#94a3b8;font-style:italic;">'
                + p.get('tech', '') + '</div>'
                '</div>'
            )
        body += _section(accent, '&#128640;', 'Projects', rows)

    # Languages  ← BUG WAS HERE — now fixed, no premature variable use
    langs_raw = d.get('languages', '').strip()
    if langs_raw:
        lang_list  = [l.strip() for l in langs_raw.split(',') if l.strip()]
        lang_pills = ''.join(_pill(l, '#f0fdf4', '#166534', '#bbf7d0') for l in lang_list)
        body += _section(accent, '&#127758;', 'Languages',
            '<div style="display:flex;flex-wrap:wrap;gap:2px;">' + lang_pills + '</div>'
        )

    # Hobbies
    hobbies_raw = d.get('hobbies', '').strip()
    if hobbies_raw:
        hobby_list  = [h.strip() for h in hobbies_raw.split(',') if h.strip()]
        hobby_pills = ''.join(_pill(h, '#fff7ed', '#c2410c', '#fed7aa') for h in hobby_list)
        body += _section(accent, '&#127912;', 'Hobbies',
            '<div style="display:flex;flex-wrap:wrap;gap:2px;">' + hobby_pills + '</div>'
        )

    # Empty state
    if not body:
        body = (
            '<div style="text-align:center;padding:2.5rem 1rem;">'
            '<div style="font-size:2.5rem;margin-bottom:10px;">&#128196;</div>'
            '<div style="font-size:0.82rem;color:#94a3b8;line-height:1.6;">'
            'Start filling the form on the left<br>to see your live resume preview here'
            '</div></div>'
        )

    # ── assemble card ──────────────────────────────────────────────
    card = (
        '<div style="background:#ffffff;border:1px solid #e8eaf6;border-radius:16px;'
        'overflow:hidden;box-shadow:0 4px 20px rgba(99,102,241,0.08);">'

        # coloured header strip
        '<div style="background:' + accent + ';padding:16px 18px 13px 18px;">'
        '<div style="font-size:1.2rem;font-weight:800;color:#ffffff;letter-spacing:-0.5px;">'
        + name + '</div>'
        '<div style="font-size:0.78rem;color:rgba(255,255,255,0.85);margin-top:3px;'
        'font-style:italic;">' + title + '</div>'
        '<div style="margin-top:8px;line-height:1.8;">' + contact_inner + '</div>'
        '</div>'

        # template badge row
        '<div style="background:#f8faff;border-bottom:1px solid #e8eaf6;padding:5px 18px;">'
        '<span style="font-size:0.67rem;color:#6366f1;font-weight:600;letter-spacing:0.5px;">'
        '&#128203; ' + tmpl_label + '</span>'
        '</div>'

        # scrollable body
        '<div style="padding:14px 18px;max-height:70vh;overflow-y:auto;">'
        + body +
        '</div></div>'
    )

    st.markdown(card, unsafe_allow_html=True)
