"""
components/ats_score.py
========================
NEW FEATURE: ATS (Applicant Tracking System) Compatibility Score.

Calculates a score 0-100 based on:
- Fields completeness (name, email, phone, summary, experience, etc.)
- Summary length and quality keywords
- Skills count
- Education presence
- Professional title

Shown as a circular badge + detailed breakdown. Updates on every rerun.
No API call needed — pure local logic.
"""
import streamlit as st


# ATS scoring weights (total = 100)
ATS_CRITERIA = [
    ("name",             "Full Name filled",             10,  lambda d: bool(d.get('name','').strip())),
    ("email",            "Email address added",           8,   lambda d: bool(d.get('email','').strip())),
    ("phone",            "Phone number added",            5,   lambda d: bool(d.get('phone','').strip())),
    ("title",            "Professional title set",        7,   lambda d: bool(d.get('professional_title','').strip())),
    ("summary_len",      "Summary 50+ characters",        10,  lambda d: len(d.get('summary','').strip()) >= 50),
    ("summary_keywords", "Summary has action verbs",      8,   lambda d: _has_action_verbs(d.get('summary',''))),
    ("experience",       "1+ experience entries",         15,  lambda d: len([e for e in d.get('experience',[]) if e.get('title') or e.get('company')]) >= 1),
    ("exp_desc",         "Experience has descriptions",   7,   lambda d: _exp_has_desc(d.get('experience',[]))),
    ("education",        "Education section filled",      10,  lambda d: len([e for e in d.get('education',[]) if e.get('degree')]) >= 1),
    ("skills_count",     "5+ skills listed",             10,  lambda d: len([s for s in d.get('skills','').split(',') if s.strip()]) >= 5),
    ("address",          "Location/city added",           5,   lambda d: bool(d.get('address','').strip())),
    ("linkedin",         "LinkedIn URL added",            5,   lambda d: bool(d.get('linkedin','').strip())),
]

ACTION_VERBS = [
    'developed', 'managed', 'led', 'built', 'designed', 'implemented',
    'created', 'improved', 'achieved', 'delivered', 'optimized',
    'collaborated', 'analyzed', 'launched', 'increased', 'reduced',
    'coordinated', 'spearheaded', 'streamlined', 'established'
]


def _has_action_verbs(summary: str) -> bool:
    summary_lower = summary.lower()
    return any(verb in summary_lower for verb in ACTION_VERBS)


def _exp_has_desc(experiences: list) -> bool:
    for exp in experiences:
        if exp.get('desc') and exp['desc'].strip():
            return True
    return False


def calculate_ats_score(data: dict) -> tuple[int, list]:
    """Returns (score 0-100, list of (label, earned, max_points, passed))."""
    total = 0
    details = []
    for _, label, points, check_fn in ATS_CRITERIA:
        passed = check_fn(data)
        earned = points if passed else 0
        total += earned
        details.append((label, earned, points, passed))
    return min(total, 100), details


def render_ats_score():
    data = st.session_state.resume_data
    score, details = calculate_ats_score(data)

    # Color based on score
    if score < 40:
        color = "#ef4444"
        grade = "Poor"
        grade_bg = "#fef2f2"
        grade_border = "#fecaca"
    elif score < 60:
        color = "#f59e0b"
        grade = "Fair"
        grade_bg = "#fffbeb"
        grade_border = "#fde68a"
    elif score < 80:
        color = "#6366f1"
        grade = "Good"
        grade_bg = "#eef2ff"
        grade_border = "#c7d2fe"
    else:
        color = "#10b981"
        grade = "Excellent"
        grade_bg = "#ecfdf5"
        grade_border = "#6ee7b7"

    # Build details rows HTML
    rows_html = ""
    for label, earned, max_pts, passed in details:
        icon = "✅" if passed else "❌"
        row_color = "#059669" if passed else "#ef4444"
        rows_html += f"""
        <div style="display:flex;align-items:center;justify-content:space-between;
                    padding:4px 0;border-bottom:0.5px solid #f1f5f9;">
            <div style="display:flex;align-items:center;gap:6px;">
                <span style="font-size:0.75rem;">{icon}</span>
                <span style="font-size:0.78rem;color:#374151;">{label}</span>
            </div>
            <span style="font-size:0.75rem;font-weight:600;color:{row_color};">
                {earned}/{max_pts}
            </span>
        </div>"""

    passed_count = sum(1 for _, _, _, p in details if p)

    st.markdown(f"""
    <div style="
        background:#ffffff;border:1px solid #e8eaf6;border-radius:20px;
        padding:1.2rem 1.4rem;margin-bottom:1rem;
        box-shadow:0 2px 12px rgba(99,102,241,0.07);
    ">
        <!-- Header row -->
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
            <div>
                <div style="font-size:0.9rem;font-weight:700;color:#1e293b;">
                    📊 ATS Score
                </div>
                <div style="font-size:0.75rem;color:#64748b;margin-top:1px;">
                    Applicant Tracking System compatibility
                </div>
            </div>
            <!-- Score circle -->
            <div style="text-align:center;">
                <div style="
                    width:64px;height:64px;border-radius:50%;
                    background:conic-gradient({color} {score * 3.6}deg, #f1f5f9 0deg);
                    display:flex;align-items:center;justify-content:center;
                    position:relative;
                ">
                    <div style="
                        width:48px;height:48px;border-radius:50%;
                        background:#ffffff;
                        display:flex;align-items:center;justify-content:center;
                        flex-direction:column;
                    ">
                        <div style="font-size:1rem;font-weight:800;color:{color};line-height:1;">{score}</div>
                        <div style="font-size:0.55rem;color:#94a3b8;">/ 100</div>
                    </div>
                </div>
                <div style="
                    background:{grade_bg};color:{color};
                    border:1px solid {grade_border};
                    font-size:0.7rem;font-weight:700;
                    padding:2px 8px;border-radius:10px;
                    margin-top:4px;display:inline-block;
                ">{grade}</div>
            </div>
        </div>

        <!-- Progress bar -->
        <div style="background:#f1f5f9;border-radius:6px;height:6px;margin-bottom:10px;overflow:hidden;">
            <div style="width:{score}%;height:100%;border-radius:6px;
                        background:linear-gradient(90deg,{color},{color}cc);"></div>
        </div>

        <!-- Summary line -->
        <div style="font-size:0.78rem;color:#64748b;margin-bottom:10px;">
            {passed_count} of {len(details)} criteria passed
        </div>

        <!-- Details (collapsible via expander below) -->
        <div style="border-top:1px solid #f1f5f9;padding-top:8px;">
            {rows_html}
        </div>

        <!-- Tip -->
        <div style="
            background:#f5f3ff;border:1px solid #c7d2fe;border-radius:8px;
            padding:6px 10px;margin-top:10px;font-size:0.75rem;color:#4f46e5;
        ">
            💡 Score above 80 = high chance of passing ATS filters
        </div>
    </div>
    """, unsafe_allow_html=True)
