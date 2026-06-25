"""
config.py
=========
Saari app-level constants yahan hain — admin password, data file paths waghera.
Kuch change karna ho (jese password) to sirf isi file ko edit karo.
"""

# ========== ADMIN CONFIG ==========
ADMIN_PASSWORD = "hsn.raza"  # ← Apna password yahan change kar lena

# ========== DATA FILES ==========
STATS_FILE = "stats.json"
FEEDBACK_FILE = "feedback.json"

# ========== DEFAULT RESUME DATA ==========
DEFAULT_RESUME_DATA = {
    'name': '', 'father_name': '', 'professional_title': '', 'email': '',
    'phone': '', 'address': '', 'linkedin': '', 'summary': '',
    'experience': [], 'education': [], 'skills': '', 'languages': '',
    'hobbies': '', 'projects': [], 'references': [], 'template': 'modern', 'photo': None,
    'dob': '', 'religion': '', 'nationality': ''
}

TEMPLATE_CHOICES = [
    "modern", "professional", "minimal", "blue_sidebar",
    "executive", "creative", "tech", "academic", "multi_column"
]

APP_VERSION = "Resume Builder Pro v5.2"
DEVELOPER_NAME = "Hassan Raza"
JAZZCASH_NUMBER = "03709240629"
PROFILE_PHOTO_PATH = "profile.jpg"
