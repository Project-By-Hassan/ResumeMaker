"""
components/_section_header.py
==============================
Shared section header renderer used by all step components.
Import: from _section_header import section_header
"""
import streamlit as st


def section_header(step_num: int, icon: str, title: str, subtitle: str):
    """Renders the coloured icon + title + step badge row."""
    html = (
        '<div style="display:flex;align-items:center;gap:10px;margin-bottom:1.1rem;">'
        '<div style="background:linear-gradient(135deg,#6366f1,#7c3aed);border-radius:10px;'
        'width:34px;height:34px;display:flex;align-items:center;justify-content:center;'
        'font-size:1.1rem;flex-shrink:0;">' + icon + '</div>'
        '<div>'
        '<div style="font-size:1rem;font-weight:700;color:#1e293b;">' + title + '</div>'
        '<div style="font-size:0.78rem;color:#64748b;margin-top:1px;">' + subtitle + '</div>'
        '</div>'
        '<span style="margin-left:auto;background:#eef2ff;color:#4f46e5;font-size:0.72rem;'
        'font-weight:600;padding:3px 10px;border-radius:20px;border:1px solid #c7d2fe;">'
        'Step ' + str(step_num) + ' / 9</span>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)
