"""
styles.py
=========
Resume Builder Pro — Light Theme + Mobile Responsive
"""

PADDING_RESET_CSS = """
<style>
    section.main > div.block-container {
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        padding-top: 1rem !important;
        max-width: 100% !important;
        width: 100% !important;
    }
    @media (max-width: 768px) {
        section.main > div.block-container {
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
            padding-top: 0.5rem !important;
        }
    }
</style>
"""

ADMIN_LABEL_CSS = """
<style>
    .admin-label {
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
</style>
"""

MAIN_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Sora:wght@400;600;700;800&display=swap');

/* ============================================================
   GLOBAL RESET & BASE
   ============================================================ */
* {
    font-family: 'Inter', sans-serif;
    box-sizing: border-box;
}

/* ============================================================
   APP BACKGROUND
   ============================================================ */
.stApp {
    background: #f8faff !important;
    background-image:
        radial-gradient(ellipse at 20% 10%, rgba(99, 102, 241, 0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 90%, rgba(139, 92, 246, 0.05) 0%, transparent 50%),
        radial-gradient(ellipse at 60% 30%, rgba(59, 130, 246, 0.04) 0%, transparent 40%) !important;
    background-attachment: fixed !important;
    min-height: 100vh;
}

/* ============================================================
   SIDEBAR
   ============================================================ */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #f1f5ff 100%) !important;
    border-right: 1px solid #e2e8f0 !important;
    box-shadow: 4px 0 24px rgba(99, 102, 241, 0.08) !important;
}
section[data-testid="stSidebar"] * { color: #1e293b !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #4f46e5 !important; }

/* ============================================================
   MOBILE RESPONSIVE — two Streamlit columns stacked on mobile
   ============================================================ */
@media (max-width: 768px) {
    /* Stack the two main columns vertically */
    div[data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
    }

    /* Main header smaller on mobile */
    .main-header {
        font-size: 2.2rem !important;
        letter-spacing: -1px !important;
        padding: 1.2rem 0 0.5rem 0 !important;
    }

    /* Section boxes less padding */
    .section-box {
        padding: 1.2rem 1rem !important;
        border-radius: 14px !important;
        margin: 1rem 0 !important;
    }

    /* Buttons full width tap targets */
    .stButton > button {
        height: 3.2em !important;
        font-size: 0.92rem !important;
    }
    .stDownloadButton > button {
        height: 3.2em !important;
        font-size: 0.92rem !important;
    }

    /* Template cards: 2 per row on mobile instead of 3 */
    /* (Streamlit columns can't be overridden per-row easily,
       so we rely on the stacked column approach above) */

    /* Progress bar dots: smaller text */
    .progress-steps { gap: 3px !important; }

    /* Live preview: reduce max-height */
}

/* ============================================================
   MAIN HEADER
   ============================================================ */
.main-header {
    font-size: 4rem;
    font-family: 'Sora', sans-serif;
    font-weight: 800;
    text-align: center;
    margin-bottom: 0.5rem;
    padding: 2.5rem 0 0.8rem 0;
    letter-spacing: -2px;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 40%, #2563eb 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    position: relative;
}
.main-header::after {
    content: '';
    position: absolute;
    bottom: 0px;
    left: 50%;
    transform: translateX(-50%);
    width: 100px;
    height: 4px;
    background: linear-gradient(90deg, transparent 0%, #6366f1 30%, #a855f7 70%, transparent 100%);
    border-radius: 2px;
}

/* ============================================================
   TAGLINE
   ============================================================ */
.tagline {
    text-align: center;
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    color: #64748b;
    margin-bottom: 2rem;
    letter-spacing: 3px;
    text-transform: uppercase;
}
.tagline span { display: inline-block; margin: 0 10px; }
.tagline span::after { content: '•'; color: #a855f7; margin-left: 10px; font-size: 0.7rem; }
.tagline span:last-child::after { content: ''; margin: 0; }

/* ============================================================
   BUTTONS
   ============================================================ */
.stButton > button {
    width: 100%;
    border-radius: 14px;
    height: 3.8em;
    font-weight: 700;
    font-size: 1rem;
    border: none !important;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 60%, #6366f1 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.35), 0 1px 3px rgba(0,0,0,0.1);
    transition: all 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    letter-spacing: 0.3px;
    font-family: 'Inter', sans-serif;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(99, 102, 241, 0.5), 0 2px 8px rgba(0,0,0,0.1);
    background: linear-gradient(135deg, #4338ca 0%, #6d28d9 60%, #4f46e5 100%) !important;
}
.stButton > button:active { transform: translateY(0px); }

/* ============================================================
   DOWNLOAD BUTTON
   ============================================================ */
.stDownloadButton > button {
    width: 100%;
    border-radius: 14px;
    height: 3.8em;
    font-weight: 700;
    font-size: 1.05rem;
    border: none !important;
    background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 20px rgba(5, 150, 105, 0.3);
    transition: all 0.25s ease;
    font-family: 'Inter', sans-serif;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(5, 150, 105, 0.45);
    background: linear-gradient(135deg, #047857 0%, #059669 100%) !important;
}

/* ============================================================
   INPUT FIELDS
   ============================================================ */
div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stFileUploader"] label {
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    color: #374151 !important;
    letter-spacing: 0.3px;
    margin-bottom: 4px !important;
    font-family: 'Inter', sans-serif;
}
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    border-radius: 10px !important;
    border: 1.5px solid #e2e8f0 !important;
    background: #ffffff !important;
    color: #1e293b !important;
    transition: all 0.2s ease;
    font-family: 'Inter', sans-serif;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
    background: #ffffff !important;
    outline: none !important;
}
div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder { color: #94a3b8 !important; }

/* Mobile: slightly smaller inputs */
@media (max-width: 768px) {
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {
        font-size: 0.88rem !important;
        padding: 0.6rem 0.8rem !important;
    }
}

/* ============================================================
   NUMBER INPUT
   ============================================================ */
.stNumberInput > div > div > input {
    border-radius: 10px !important;
    border: 1.5px solid #e2e8f0 !important;
    background: #ffffff !important;
    color: #1e293b !important;
    font-family: 'Inter', sans-serif;
}

/* ============================================================
   SELECTBOX
   ============================================================ */
.stSelectbox > div > div,
div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 10px !important;
    color: #1e293b !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
}

/* ============================================================
   FILE UPLOADER
   ============================================================ */
.stFileUploader > div {
    border-radius: 14px !important;
    border: 2px dashed #c7d2fe !important;
    background: linear-gradient(135deg, #f5f3ff 0%, #eef2ff 100%) !important;
    transition: all 0.2s ease;
}
.stFileUploader > div:hover {
    border-color: #6366f1 !important;
    background: linear-gradient(135deg, #ede9fe 0%, #e0e7ff 100%) !important;
}

/* ============================================================
   SECTION BOXES
   ============================================================ */
.section-box {
    padding: 2rem 2.5rem;
    border-radius: 20px;
    background: #ffffff;
    border: 1px solid #e8eaf6;
    margin: 1.5rem 0;
    box-shadow: 0 2px 12px rgba(99, 102, 241, 0.07), 0 1px 3px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.section-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 3px;
    background: linear-gradient(90deg, #6366f1 0%, #a855f7 50%, #3b82f6 100%);
    border-radius: 20px 20px 0 0;
}
.section-box:hover {
    box-shadow: 0 8px 30px rgba(99, 102, 241, 0.15), 0 2px 8px rgba(0,0,0,0.06);
    transform: translateY(-2px);
    border-color: #c7d2fe;
}

/* ============================================================
   STEP BADGES
   ============================================================ */
.step-badge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: linear-gradient(135deg, #eef2ff, #f5f3ff);
    border: 1px solid #c7d2fe;
    border-radius: 50px;
    padding: 6px 16px 6px 8px;
    margin-bottom: 1.2rem;
    font-size: 0.85rem;
    font-weight: 700;
    color: #4f46e5;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.step-badge .step-num {
    background: linear-gradient(135deg, #6366f1, #7c3aed);
    color: #fff;
    border-radius: 50%;
    width: 26px; height: 26px;
    display: inline-flex;
    align-items: center; justify-content: center;
    font-size: 0.8rem; font-weight: 800;
}

/* ============================================================
   SUCCESS BOX
   ============================================================ */
.success-box {
    padding: 2rem;
    border-radius: 16px;
    background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
    color: #065f46;
    font-size: 1.1rem;
    font-weight: 700;
    text-align: center;
    box-shadow: 0 4px 20px rgba(5, 150, 105, 0.2);
    font-family: 'Inter', sans-serif;
    border: 1.5px solid #6ee7b7;
}

/* ============================================================
   EXPANDERS
   ============================================================ */
div[data-testid="stExpander"] {
    border-radius: 14px !important;
    border: 1.5px solid #e2e8f0 !important;
    background: #ffffff !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    transition: all 0.25s ease;
    overflow: hidden;
}
div[data-testid="stExpander"]:hover {
    border-color: #c7d2fe !important;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.12) !important;
}
div[data-testid="stExpander"] summary {
    color: #1e293b !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 1rem 1.2rem !important;
}

/* ============================================================
   HEADINGS
   ============================================================ */
h1, h2 {
    font-family: 'Sora', sans-serif !important;
    color: #1e293b !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}
h3 {
    color: #1e293b !important;
    font-weight: 700 !important;
    font-size: 1.25rem !important;
    letter-spacing: -0.3px;
    font-family: 'Sora', sans-serif !important;
    display: flex;
    align-items: center;
    gap: 8px;
}
h4, h5, h6 {
    color: #374151 !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
}

/* ============================================================
   MARKDOWN & TEXT
   ============================================================ */
.stMarkdown, .stMarkdown p, p { color: #374151 !important; line-height: 1.7; }
.stMarkdown a { color: #6366f1 !important; text-decoration: none; font-weight: 500; }
.stMarkdown a:hover { text-decoration: underline; }

/* ============================================================
   ALERTS
   ============================================================ */
.stAlert { border-radius: 12px; border: 1.5px solid #e0e7ff; background: #eef2ff; color: #3730a3; }
div[data-testid="stInfo"]    { background: #eff6ff !important; border-color: #bfdbfe !important; color: #1e40af !important; border-radius: 12px !important; }
div[data-testid="stSuccess"] { background: #f0fdf4 !important; border-color: #bbf7d0 !important; color: #166534 !important; border-radius: 12px !important; }
div[data-testid="stWarning"] { background: #fffbeb !important; border-color: #fde68a !important; color: #92400e !important; border-radius: 12px !important; }
div[data-testid="stError"]   { background: #fef2f2 !important; border-color: #fecaca !important; color: #991b1b !important; border-radius: 12px !important; }

/* ============================================================
   DIVIDERS
   ============================================================ */
hr { border: none !important; border-top: 1.5px solid #e2e8f0 !important; margin: 1.5rem 0 !important; }

/* ============================================================
   SCROLLBAR
   ============================================================ */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #f1f5f9; border-radius: 10px; }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #6366f1, #a855f7); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: linear-gradient(180deg, #4f46e5, #7c3aed); }

/* ============================================================
   PROFILE PHOTO
   ============================================================ */
.profile-photo-container {
    position: relative;
    margin-top: 10px;
    margin-left: 14px;
    margin-bottom: 8px;
    width: fit-content;
}
.profile-photo {
    width: 52px; height: 52px;
    border-radius: 50%;
    border: 2.5px solid #6366f1;
    box-shadow: 0 2px 12px rgba(99, 102, 241, 0.3), 0 1px 4px rgba(0,0,0,0.1);
    object-fit: cover;
    object-position: center 20%;
    transition: box-shadow 0.3s ease, border-color 0.3s ease;
    cursor: pointer;
}
.profile-photo:hover { box-shadow: 0 4px 20px rgba(99, 102, 241, 0.5); border-color: #7c3aed; }
@media (max-width: 768px) {
    .profile-photo { width: 40px; height: 40px; border-width: 2px; }
    .profile-photo-container { margin-top: 8px; margin-left: 8px; }
}

/* ============================================================
   FEATURE CARDS
   ============================================================ */
.feature-card {
    background: #ffffff;
    border: 1px solid #e8eaf6;
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(99,102,241,0.06);
}
.feature-card:hover { transform: translateY(-4px); box-shadow: 0 12px 30px rgba(99,102,241,0.15); border-color: #a5b4fc; }
.feature-card .icon { font-size: 2.2rem; margin-bottom: 0.8rem; display: block; }
.feature-card .title { font-weight: 700; font-size: 1rem; color: #1e293b; margin-bottom: 0.4rem; }
.feature-card .desc { font-size: 0.85rem; color: #64748b; line-height: 1.5; }

/* ============================================================
   PROGRESS / STEPS
   ============================================================ */
.progress-steps { display: flex; align-items: center; justify-content: center; gap: 6px; margin: 1.5rem 0; flex-wrap: wrap; }
.progress-step { display: flex; align-items: center; gap: 6px; font-size: 0.8rem; font-weight: 600; color: #6366f1; background: #eef2ff; border: 1px solid #c7d2fe; border-radius: 20px; padding: 4px 12px; }
.progress-step .dot { width: 8px; height: 8px; border-radius: 50%; background: linear-gradient(135deg, #6366f1, #a855f7); }

/* ============================================================
   RADIO & CHECKBOXES
   ============================================================ */
div[data-testid="stRadio"] label,
div[data-testid="stCheckbox"] label { color: #374151 !important; font-weight: 500 !important; font-size: 0.9rem !important; }

/* ============================================================
   METRIC CARDS
   ============================================================ */
div[data-testid="metric-container"] {
    background: #ffffff !important; border: 1px solid #e8eaf6 !important;
    border-radius: 14px !important; padding: 1rem 1.2rem !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.07) !important;
}
div[data-testid="metric-container"] label { color: #64748b !important; font-weight: 600 !important; font-size: 0.8rem !important; text-transform: uppercase; letter-spacing: 0.5px; }
div[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #4f46e5 !important; font-weight: 800 !important; font-family: 'Sora', sans-serif !important; }

/* ============================================================
   SPINNER
   ============================================================ */
.stSpinner > div { border-top-color: #6366f1 !important; }

/* ============================================================
   MOBILE: hide live preview below form (it renders after form)
   so it's naturally below on mobile — add a visible divider
   ============================================================ */
@media (max-width: 768px) {
    /* Give live preview section a top margin for separation */
    div[data-testid="stColumn"]:last-child {
        margin-top: 1rem;
        border-top: 2px dashed #e0e7ff;
        padding-top: 1rem;
    }
}
</style>
"""

# ============================================================
# PRO TIP BANNER
# ============================================================
PRO_TIP_BANNER_HTML = """
<div style="
    background: linear-gradient(135deg, #eef2ff 0%, #f5f3ff 100%);
    border-left: 4px solid #6366f1;
    padding: 0.9rem 1.3rem;
    border-radius: 12px;
    margin: 1rem 0 1.5rem 0;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 2px 10px rgba(99,102,241,0.1);
    border: 1px solid #c7d2fe;
    border-left: 4px solid #6366f1;
">
    <span style="font-size: 1.3rem;">&#128161;</span>
    <span style="color: #4338ca; font-size: 0.88rem; font-weight: 600;">
        <strong>Pro Tip:</strong> For a more professional look, choose the <strong>Blue Sidebar</strong> template &mdash; trusted by top recruiters.
    </span>
</div>
"""

# ============================================================
# MAIN TITLE
# ============================================================
MAIN_TITLE_HTML = """
<div style="width: 100%; text-align: center; padding: 1.5rem 0 0.5rem 0;">
    <div style="
        display: inline-flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 0.5rem;
        flex-wrap: wrap;
        justify-content: center;
    ">
        <span style="font-size: 2.2rem;">&#128196;</span>
        <h1 style="
            font-size: clamp(1.8rem, 6vw, 3.8rem);
            font-weight: 900;
            font-family: 'Sora', sans-serif;
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #2563eb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0;
            letter-spacing: -2px;
            line-height: 1;
        ">Resume Builder Pro</h1>
        <span style="font-size: 2.2rem;">&#10024;</span>
    </div>
</div>
"""

# ============================================================
# TAGLINE
# ============================================================
TAGLINE_HTML = """
<div style="text-align: center; margin-bottom: 2rem; padding: 0 1rem;">
    <div style="
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, #eef2ff, #f5f3ff);
        border: 1px solid #c7d2fe;
        border-radius: 50px;
        padding: 8px 16px;
        font-size: clamp(0.65rem, 2vw, 0.8rem);
        font-weight: 600;
        color: #4f46e5;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        box-shadow: 0 2px 10px rgba(99,102,241,0.12);
        flex-wrap: wrap;
        justify-content: center;
    ">
        <span>&#127942; Enterprise Grade</span>
        <span style="color:#a855f7;">&#9670;</span>
        <span>&#129302; AI Powered</span>
        <span style="color:#a855f7;">&#9670;</span>
        <span>&#128188; Professional</span>
        <span style="color:#a855f7;">&#9670;</span>
        <span>&#128274; Secure</span>
    </div>
</div>
"""

# ============================================================
# JAZZCASH CARD
# ============================================================
def jazzcash_card_html(account_name: str, number: str) -> str:
    return (
        '<div style="text-align:center;padding:24px;'
        'background:linear-gradient(135deg,#fff7ed 0%,#ffedd5 100%);'
        'border-radius:16px;border:1.5px solid #fed7aa;margin-top:12px;'
        'box-shadow:0 4px 16px rgba(234,88,12,0.1);">'
        '<div style="font-size:2.5rem;margin-bottom:10px;">&#128179;</div>'
        '<h4 style="color:#ea580c;margin-bottom:14px;font-size:1.1rem;font-weight:700;">JazzCash Details</h4>'
        '<p style="color:#1e293b;font-size:1rem;font-weight:600;margin:8px 0;">'
        '&#128100; Account Name: <strong>' + account_name + '</strong></p>'
        '<p style="color:#1e293b;font-size:1.1rem;font-weight:700;margin:8px 0;">'
        '&#128241; Number: <strong>' + number + '</strong></p>'
        '<p style="color:#64748b;font-size:0.85rem;margin-top:14px;">'
        '&#128640; Your support helps build better features!</p>'
        '</div>'
    )

# ============================================================
# FOOTER
# ============================================================
def footer_html(app_version: str, developer_name: str) -> str:
    return (
        '<div style="text-align:center;padding:3rem 2rem 2rem 2rem;margin-top:3rem;'
        'border-top:1.5px solid #e2e8f0;'
        'background:linear-gradient(135deg,#f8faff 0%,#f0f4ff 100%);'
        'border-radius:20px 20px 0 0;">'
        '<div style="display:inline-flex;align-items:center;gap:8px;margin-bottom:1rem;">'
        '<span style="font-size:1.8rem;">&#128196;</span>'
        '<p style="font-size:1.15rem;font-weight:800;'
        'background:linear-gradient(135deg,#4f46e5,#7c3aed);'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'background-clip:text;margin:0;font-family:Sora,sans-serif;">'
        + app_version + '</p>'
        '</div>'
        '<p style="font-size:0.82rem;color:#64748b;margin:0.4rem 0;'
        'letter-spacing:1.5px;text-transform:uppercase;font-weight:500;">'
        '&#9889; Engineered With Precision &nbsp;&bull;&nbsp; &#127912; Designed For Excellence</p>'
        '<p style="font-size:0.78rem;color:#94a3b8;margin-top:1rem;">'
        'Developed by <strong style="color:#6366f1;">' + developer_name + '</strong>'
        ' &nbsp;&bull;&nbsp; &copy; 2026 All Rights Reserved</p>'
        '</div>'
    )

# ============================================================
# PROFILE PHOTO
# ============================================================
def profile_photo_html(img_base64: str) -> str:
    return (
        '<div class="profile-photo-container">'
        '<img src="data:image/jpeg;base64,' + img_base64 + '" '
        'class="profile-photo" alt="Profile">'
        '</div>'
    )
