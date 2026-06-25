"""components/profile_photo.py — Top-left profile photo (no crash if missing)"""
import base64
import streamlit as st
from config import PROFILE_PHOTO_PATH
from styles import profile_photo_html


def render_profile_photo():
    try:
        with open(PROFILE_PHOTO_PATH, "rb") as f:
            img_data = base64.b64encode(f.read()).decode()
    except (FileNotFoundError, OSError):
        return
    st.markdown(profile_photo_html(img_data), unsafe_allow_html=True)
