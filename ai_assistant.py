"""
components/ai_assistant.py
===========================
AI Resume Assistant — FREE using Google Gemini API
=====================================================

FEATURES:
1. User ka naam pehle message se auto-detect karta hai (bina puche)
2. Name ke sath personalized welcome
3. Resume data ke context ke sath smart suggestions
4. Professional summary auto-generate
5. Skills suggestions based on job title
6. Full resume tips & ATS advice

SETUP (FREE — no credit card):
1. https://aistudio.google.com/app/apikey pe jao
2. "Create API Key" click karo — bilkul free
3. Key ko Streamlit secrets me rakho:
   - Local: .streamlit/secrets.toml me:
       GEMINI_API_KEY = "your-key-here"
   - Streamlit Cloud: App Settings > Secrets me same line add karo

USAGE:
  from ai_assistant import render_ai_assistant
  render_ai_assistant()
"""

import json
import re
import urllib.request
import urllib.error
import streamlit as st

# ── Gemini API config ──────────────────────────────────────────────────────
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-1.5-flash:generateContent?key="
)
MAX_HISTORY = 20   # context window ke liye last N messages rakho


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _get_api_key() -> str | None:
    try:
        return st.secrets.get("GEMINI_API_KEY") or st.secrets.get("gemini_api_key")
    except Exception:
        return None


def _call_gemini(messages: list, system_prompt: str, api_key: str) -> str:
    """Call Gemini 1.5 Flash — free tier, no SDK needed (pure urllib)."""
    # Build contents list for Gemini format
    contents = []
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })

    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": contents,
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1024,
            "topP": 0.9,
        }
    }

    data = json.dumps(payload).encode("utf-8")
    req  = urllib.request.Request(
        GEMINI_URL + api_key,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        err  = json.loads(body).get("error", {}).get("message", str(e))
        return "API Error: " + err
    except Exception as e:
        return "Error: " + str(e)


def _extract_name_from_text(text: str) -> str | None:
    """
    Naam bina puche detect karne ka tarika:
    User ke pehle message se naam extract karta hai pattern matching se.
    e.g. "Hi I'm Hassan", "mera naam Ali hai", "My name is Sara"
    """
    patterns = [
        r"(?:my name is|i am|i'm|naam hai|mera naam|main hoon)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)",
        r"(?:hi|hello|hey)[,\s]+(?:i am|i'm|main)\s+([A-Z][a-z]+)",
        r"^([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)\s+(?:here|speaking|this side)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            name = match.group(1).strip().title()
            # Filter out common words that aren't names
            skip = {"help", "here", "looking", "trying", "want", "need",
                    "resume", "new", "the", "this", "that"}
            if name.lower().split()[0] not in skip and len(name) > 2:
                return name
    return None


def _resume_context_summary(data: dict) -> str:
    """Build a short context string from current resume data."""
    parts = []
    if data.get("name"):
        parts.append("Name: " + data["name"])
    if data.get("professional_title"):
        parts.append("Title: " + data["professional_title"])
    if data.get("summary"):
        parts.append("Summary (current): " + data["summary"][:200])
    if data.get("skills"):
        parts.append("Skills: " + data["skills"][:150])
    if data.get("experience"):
        exp = data["experience"]
        titles = [e.get("title","") + " at " + e.get("company","") for e in exp if e.get("title")]
        if titles:
            parts.append("Experience: " + " | ".join(titles[:3]))
    if data.get("education"):
        edu = data["education"]
        degs = [e.get("degree","") + " from " + e.get("institute","") for e in edu if e.get("degree")]
        if degs:
            parts.append("Education: " + " | ".join(degs[:2]))
    return "\n".join(parts) if parts else "No resume data filled yet."


def _build_system_prompt(user_name: str | None, resume_data: dict) -> str:
    name_line = (
        "The user's name is " + user_name + ". Address them by name naturally in responses."
        if user_name else
        "You don't know the user's name yet. If they introduce themselves, remember it."
    )
    context = _resume_context_summary(resume_data)

    return """You are ResumeAI, a friendly and expert resume assistant built into Resume Builder Pro.

""" + name_line + """

CURRENT RESUME DATA:
""" + context + """

YOUR CAPABILITIES:
1. Answer any resume-related question (ATS, formatting, tips, phrasing)
2. Generate professional summaries — when asked, write a complete 3-4 line summary
3. Suggest skills based on job title or industry
4. Review and improve the user's existing summary or experience descriptions
5. Give ATS optimization advice
6. Help with LinkedIn bio, cover letters
7. Answer general career questions

RULES:
- Be concise, friendly, and practical
- Use bullet points for lists
- When generating a summary, make it ATS-optimized and professional
- Always relate advice to the user's actual resume data when available
- If user asks to "generate my summary", use their name, title, skills, experience to write it
- Respond in the same language the user writes in (Urdu/English/mix)
- Keep responses under 300 words unless writing full content like a summary
- Never make up fake job titles or companies — only use what's in the resume data
"""


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ══════════════════════════════════════════════════════════════════════════════

def _init_chat_state():
    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = []
    if "ai_user_name" not in st.session_state:
        st.session_state.ai_user_name = None
    if "ai_chat_open" not in st.session_state:
        st.session_state.ai_chat_open = False
    if "ai_welcomed" not in st.session_state:
        st.session_state.ai_welcomed = False


# ══════════════════════════════════════════════════════════════════════════════
# QUICK ACTION BUTTONS
# ══════════════════════════════════════════════════════════════════════════════

QUICK_ACTIONS = [
    ("✍️ Generate My Summary",    "Please generate a professional summary for my resume based on my data."),
    ("🛠️ Suggest Skills",         "Based on my job title and experience, what skills should I add to my resume?"),
    ("📊 ATS Tips",               "How can I improve my resume's ATS score? Give me specific tips."),
    ("💼 Improve Experience",     "How can I make my work experience descriptions more impactful?"),
    ("🔍 Review My Resume",       "Please review my current resume data and give me honest feedback."),
    ("📝 Cover Letter Intro",     "Write a short cover letter introduction paragraph for me."),
]


# ══════════════════════════════════════════════════════════════════════════════
# MAIN RENDER
# ══════════════════════════════════════════════════════════════════════════════

def render_ai_assistant():
    _init_chat_state()
    api_key     = _get_api_key()
    resume_data = st.session_state.get("resume_data", {})

    # ── Floating toggle button (when chat is closed) ──────────────────
    if not st.session_state.ai_chat_open:
        st.markdown(
            '<div style="position:fixed;bottom:2rem;right:2rem;z-index:9999;">'
            '<div style="background:linear-gradient(135deg,#6366f1,#7c3aed);'
            'border-radius:50%;width:60px;height:60px;display:flex;align-items:center;'
            'justify-content:center;box-shadow:0 4px 20px rgba(99,102,241,0.5);'
            'cursor:pointer;font-size:1.6rem;">&#129302;</div>'
            '</div>',
            unsafe_allow_html=True
        )
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "🤖 Open AI Resume Assistant",
                use_container_width=True,
                type="primary",
                key="open_ai_chat"
            ):
                st.session_state.ai_chat_open = True
                st.rerun()
        return

    # ── Chat panel ────────────────────────────────────────────────────
    st.markdown(
        '<div style="background:#ffffff;border:1px solid #e8eaf6;border-radius:20px;'
        'overflow:hidden;box-shadow:0 8px 40px rgba(99,102,241,0.12);margin-bottom:2rem;">'

        # Header bar
        '<div style="background:linear-gradient(135deg,#4f46e5,#7c3aed);'
        'padding:1rem 1.5rem;display:flex;align-items:center;gap:12px;">'
        '<div style="background:rgba(255,255,255,0.2);border-radius:50%;width:38px;height:38px;'
        'display:flex;align-items:center;justify-content:center;font-size:1.2rem;">&#129302;</div>'
        '<div>'
        '<div style="color:#ffffff;font-size:1rem;font-weight:700;">ResumeAI Assistant</div>'
        '<div style="color:rgba(255,255,255,0.75);font-size:0.75rem;">'
        'Powered by Gemini — Completely Free</div>'
        '</div>'
        '<span style="margin-left:auto;background:rgba(255,255,255,0.15);color:#ffffff;'
        'font-size:0.7rem;font-weight:600;padding:3px 10px;border-radius:20px;">'
        '&#9679; Online</span>'
        '</div>',
        unsafe_allow_html=True
    )

    # ── API key missing warning ───────────────────────────────────────
    if not api_key:
        st.markdown(
            '<div style="padding:1.2rem 1.5rem;background:#fffbeb;border-bottom:1px solid #fde68a;">'
            '<div style="font-size:0.88rem;font-weight:600;color:#92400e;">&#9888; Setup Required</div>'
            '<div style="font-size:0.8rem;color:#78350f;margin-top:4px;">'
            '1. Go to <strong>aistudio.google.com/app/apikey</strong><br>'
            '2. Click "Create API Key" (free, no credit card)<br>'
            '3. Add to Streamlit secrets: <code>GEMINI_API_KEY = "your-key"</code>'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

    # ── Welcome message (first time) ─────────────────────────────────
    if not st.session_state.ai_welcomed:
        uname = st.session_state.ai_user_name
        # Also check resume_data for name
        if not uname and resume_data.get("name"):
            uname = resume_data["name"].split()[0]  # first name only
            st.session_state.ai_user_name = uname

        if uname:
            welcome = (
                "Hi **" + uname + "**! 👋 I'm your AI resume assistant. "
                "I can see your resume data and I'm here to help you make it outstanding. "
                "What would you like help with?"
            )
        else:
            welcome = (
                "Hi! 👋 I'm **ResumeAI**, your personal resume assistant. "
                "I'm connected to your resume data and can help you write summaries, "
                "suggest skills, optimize for ATS, and much more. "
                "How can I help you today?"
            )
        st.session_state.ai_messages.append({
            "role": "assistant",
            "content": welcome
        })
        st.session_state.ai_welcomed = True

    # ── Chat history display ──────────────────────────────────────────
    st.markdown('<div style="padding:1rem 1.5rem;max-height:400px;overflow-y:auto;" id="chat-body">',
                unsafe_allow_html=True)

    for msg in st.session_state.ai_messages:
        is_user = msg["role"] == "user"
        if is_user:
            bubble_style = (
                "background:linear-gradient(135deg,#4f46e5,#6366f1);"
                "color:#ffffff;margin-left:auto;border-radius:16px 16px 4px 16px;"
            )
            align = "flex-end"
            avatar = "&#128100;"
            avatar_bg = "background:#e0e7ff;color:#4f46e5;"
        else:
            bubble_style = (
                "background:#f8faff;border:1px solid #e8eaf6;"
                "color:#1e293b;margin-right:auto;border-radius:16px 16px 16px 4px;"
            )
            align = "flex-start"
            avatar = "&#129302;"
            avatar_bg = "background:linear-gradient(135deg,#6366f1,#7c3aed);color:white;"

        content = msg["content"].replace("\n", "<br>")
        # Bold markdown **text**
        content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
        # Bullet points
        content = re.sub(r'^[-•]\s', '• ', content, flags=re.MULTILINE)

        st.markdown(
            '<div style="display:flex;align-items:flex-end;gap:8px;margin-bottom:12px;'
            'justify-content:' + align + ';">'

            + ('' if is_user else
               '<div style="width:30px;height:30px;border-radius:50%;' + avatar_bg +
               'display:flex;align-items:center;justify-content:center;'
               'font-size:0.85rem;flex-shrink:0;">' + avatar + '</div>')

            + '<div style="' + bubble_style +
            'padding:10px 14px;max-width:80%;font-size:0.85rem;line-height:1.6;">'
            + content + '</div>'

            + ('' if not is_user else
               '<div style="width:30px;height:30px;border-radius:50%;' + avatar_bg +
               'display:flex;align-items:center;justify-content:center;'
               'font-size:0.85rem;flex-shrink:0;">' + avatar + '</div>')

            + '</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Quick action buttons ──────────────────────────────────────────
    st.markdown(
        '<div style="padding:0 1.5rem;margin-bottom:0.5rem;">'
        '<div style="font-size:0.72rem;color:#64748b;font-weight:600;'
        'letter-spacing:0.5px;margin-bottom:6px;">QUICK ACTIONS</div>'
        '</div>',
        unsafe_allow_html=True
    )

    qa_cols = st.columns(3)
    for idx, (label, prompt) in enumerate(QUICK_ACTIONS):
        with qa_cols[idx % 3]:
            if st.button(label, key="qa_" + str(idx), use_container_width=True):
                st.session_state.ai_messages.append({"role": "user", "content": prompt})
                if api_key:
                    with st.spinner("Thinking..."):
                        system = _build_system_prompt(
                            st.session_state.ai_user_name, resume_data
                        )
                        history = st.session_state.ai_messages[-MAX_HISTORY:]
                        reply   = _call_gemini(history, system, api_key)
                    st.session_state.ai_messages.append({"role": "assistant", "content": reply})
                else:
                    st.session_state.ai_messages.append({
                        "role": "assistant",
                        "content": "Please set up your Gemini API key first. See instructions above."
                    })
                st.rerun()

    # ── Input box ─────────────────────────────────────────────────────
    st.markdown('<div style="padding:0.8rem 1.5rem 1.2rem 1.5rem;border-top:1px solid #f1f5f9;margin-top:0.5rem;">',
                unsafe_allow_html=True)

    user_input = st.chat_input(
        "Ask anything — write a summary, get tips, ask about ATS...",
        key="ai_chat_input"
    )

    if user_input and user_input.strip():
        # ── Name detection from message ──────────────────────────────
        if not st.session_state.ai_user_name:
            detected = _extract_name_from_text(user_input)
            if detected:
                st.session_state.ai_user_name = detected

        # Also update from resume data if not already set
        if not st.session_state.ai_user_name and resume_data.get("name"):
            st.session_state.ai_user_name = resume_data["name"].split()[0]

        st.session_state.ai_messages.append({"role": "user", "content": user_input})

        if api_key:
            with st.spinner("ResumeAI is thinking..."):
                system = _build_system_prompt(
                    st.session_state.ai_user_name, resume_data
                )
                history = st.session_state.ai_messages[-MAX_HISTORY:]
                reply   = _call_gemini(history, system, api_key)
        else:
            reply = (
                "I need a Gemini API key to respond. "
                "Please follow the setup instructions shown above — it's completely free!"
            )

        st.session_state.ai_messages.append({"role": "assistant", "content": reply})
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Footer controls ───────────────────────────────────────────────
    st.markdown('<div style="padding:0 1.5rem 1rem 1.5rem;">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        msg_count = len([m for m in st.session_state.ai_messages if m["role"] == "user"])
        uname = st.session_state.ai_user_name
        label = (uname + " — " if uname else "") + str(msg_count) + " messages"
        st.markdown(
            '<div style="font-size:0.72rem;color:#94a3b8;padding-top:8px;">' + label + '</div>',
            unsafe_allow_html=True
        )
    with c2:
        if st.button("Clear Chat", use_container_width=True, key="clear_ai_chat"):
            st.session_state.ai_messages  = []
            st.session_state.ai_welcomed  = False
            st.session_state.ai_user_name = None
            st.rerun()
    with c3:
        if st.button("Close", use_container_width=True, key="close_ai_chat"):
            st.session_state.ai_chat_open = False
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close main panel
