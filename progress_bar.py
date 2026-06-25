"""
components/progress_bar.py — 9-step progress bar
MOBILE FIX: dots ab overflow nahi karenge — min-width kam ki, font size
responsive rakhi, aur dot size mobile pe reduce ki.
"""
import streamlit as st


def _calc_progress():
    d = st.session_state.get('resume_data', {})
    sections = [
        ("Template",   bool(d.get('template'))),
        ("Personal",   bool(d.get('name') and d.get('email'))),
        ("Summary",    bool(d.get('summary', '').strip())),
        ("Experience", bool(d.get('experience'))),
        ("Education",  bool(d.get('education'))),
        ("Skills",     bool(d.get('skills', '').strip())),
        ("Projects",   bool(d.get('projects'))),
        ("References", bool(d.get('references'))),
        ("Generate",   bool(st.session_state.get('pdf_ready'))),
    ]
    filled = sum(1 for _, done in sections if done)
    return filled, len(sections), sections


def render_progress_bar():
    filled, total, sections = _calc_progress()
    pct = int((filled / total) * 100)

    if pct == 100:
        bar_color = "#10b981"
        label     = "Resume Complete — Ready to Download!"
    elif pct >= 60:
        bar_color = "#6366f1"
        label     = str(pct) + "% Complete — Almost there!"
    elif pct >= 30:
        bar_color = "#f59e0b"
        label     = str(pct) + "% Complete — Keep going!"
    else:
        bar_color = "#e11d48"
        label     = str(pct) + "% Complete — Let's get started!"

    dots_html = ""
    for name, done in sections:
        dot_bg  = bar_color if done else "#e2e8f0"
        txt_clr = "#374151" if done else "#94a3b8"
        mark    = "&#10003;" if done else ""
        dots_html += (
            '<div style="display:flex;flex-direction:column;align-items:center;'
            'gap:2px;flex:1;min-width:0;max-width:68px;">'
            '<div style="width:clamp(20px,4vw,26px);height:clamp(20px,4vw,26px);'
            'border-radius:50%;background:' + dot_bg + ';'
            'display:flex;align-items:center;justify-content:center;'
            'font-size:clamp(0.6rem,1.5vw,0.72rem);color:white;font-weight:700;">'
            + mark + '</div>'
            '<div style="font-size:clamp(0.45rem,1.2vw,0.55rem);color:' + txt_clr + ';'
            'font-weight:500;text-align:center;line-height:1.2;'
            'word-break:break-word;max-width:100%;">' + name + '</div>'
            '</div>'
        )

    bar_w = str(pct) + "%"

    html = (
        '<div style="background:#ffffff;border:1px solid #e8eaf6;border-radius:14px;'
        'padding:0.9rem 1.1rem;margin:0 0 1.2rem 0;'
        'box-shadow:0 2px 10px rgba(99,102,241,0.06);">'

        '<div style="display:flex;justify-content:space-between;'
        'align-items:center;margin-bottom:8px;flex-wrap:wrap;gap:4px;">'
        '<span style="font-size:clamp(0.75rem,2vw,0.84rem);font-weight:700;color:#374151;">'
        + label + '</span>'
        '<span style="font-size:clamp(0.68rem,1.8vw,0.75rem);color:#64748b;font-weight:500;">'
        + str(filled) + ' / ' + str(total) + ' sections</span>'
        '</div>'

        '<div style="background:#f1f5f9;border-radius:8px;height:7px;'
        'overflow:hidden;margin-bottom:10px;">'
        '<div style="width:' + bar_w + ';height:100%;background:' + bar_color + ';'
        'border-radius:8px;transition:width 0.4s ease;"></div>'
        '</div>'

        '<div style="display:flex;justify-content:space-between;'
        'align-items:flex-start;gap:2px;overflow:hidden;">'
        + dots_html +
        '</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)
