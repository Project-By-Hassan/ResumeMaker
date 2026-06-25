"""
data_store.py
=============
Stats aur feedback ko JSON files me save/load karne wale functions.
"""
import os
import json
from datetime import datetime

from config import STATS_FILE, FEEDBACK_FILE


def load_stats():
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {"total_resumes": 0, "today": str(datetime.now().date()), "today_count": 0}


def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)


def increment_resume_count():
    stats = load_stats()
    today = str(datetime.now().date())
    if stats["today"] != today:
        stats["today"] = today
        stats["today_count"] = 0
    stats["total_resumes"] += 1
    stats["today_count"] += 1
    save_stats(stats)


def save_feedback(rating, comment):
    feedback_list = []
    if os.path.exists(FEEDBACK_FILE):
        try:
            with open(FEEDBACK_FILE, "r") as f:
                feedback_list = json.load(f)
        except (json.JSONDecodeError, OSError):
            feedback_list = []
    feedback_list.append({
        "rating": rating,
        "comment": comment,
        "time": str(datetime.now())
    })
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(feedback_list, f)


def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        try:
            with open(FEEDBACK_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return []


def clear_all_stats():
    """BUG FIX: ab clear karte waqt FileNotFoundError aane ka chance nahi (already checked)."""
    if os.path.exists(STATS_FILE):
        os.remove(STATS_FILE)
    if os.path.exists(FEEDBACK_FILE):
        os.remove(FEEDBACK_FILE)
