"""
pdf_generator.py
================
MAJOR BUG FIX (sabse important fix is file me):
-------------------------------------------------
Original `app.py` me DO `generate_pdf()` functions thay same naam ke sath.
Python me jab same naam ka function dobara define hota hai, to PEHLA wala
hamesha overridden ho jata hai — sirf AAKHRI definition hi kaam karti hai.

Pehla `generate_pdf` (FPDF/ResumePDF based) sab 9 templates, photo, projects,
references, languages, hobbies, linkedin, address, father_name, dob,
religion, nationality — sab kuch support karta tha.

Dusra `generate_pdf` (ReportLab based, niche define hua tha) is sab ko
silently override kar raha tha, aur woh sirf ek hi generic layout banata
tha — jisme TEMPLATE SELECTION KA KOI ASAR NAHI HOTA THA, aur photo,
languages, hobbies, projects, references, linkedin, address bilkul show
hi nahi hote thay!

Matlab: user "Blue Sidebar" ya "Tech" template choose kare, ya kuch bhi,
PDF hamesha same boring generic style me banta tha aur aadha data PDF me
aata hi nahi tha.

FIX: ReportLab wala duplicate function hata diya gaya hai. Sirf ek
generate_pdf() rakha gaya hai jo ResumePDF (FPDF based, 9 templates wala)
use karta hai — jisme saara data aur sab templates sahi se kaam karte hain.
"""
from resume_pdf import ResumePDF

# Template name -> header method name. Naya template add karte waqt
# yahan ek line add karna kaafi hai.
HEADER_DISPATCH = {
    'modern': 'modern_header',
    'professional': 'professional_header',
    'minimal': 'minimal_header',
    'blue_sidebar': 'blue_sidebar_header',
    'executive': 'executive_header',
    'creative': 'creative_header',
    'tech': 'tech_header',
    'academic': 'academic_header',
    'multi_column': 'multi_column_header',
}


def generate_pdf(data):
    """Resume data (dict) se PDF bytes banata hai.

    Returns: (pdf_bytes, error_message)
        - Success: (bytes, None)
        - Failure: (None, "error string")
    """
    try:
        template = data.get('template', 'modern')
        pdf = ResumePDF(template=template, photo_bytes=data.get('photo'))
        pdf.name = data.get('name', '')
        pdf.professional_title = data.get('professional_title', '')
        pdf.email = data.get('email', '')
        pdf.phone = data.get('phone', '')
        pdf.address = data.get('address', '')
        pdf.linkedin = data.get('linkedin', '')
        pdf.father_name = data.get('father_name', '')
        pdf.dob = data.get('dob', '')
        pdf.religion = data.get('religion', '')
        pdf.nationality = data.get('nationality', '')

        pdf.add_page()

        header_method_name = HEADER_DISPATCH.get(template, 'modern_header')
        getattr(pdf, header_method_name)()

        if template != 'blue_sidebar':
            pdf.set_xy(pdf.left_x, pdf.header_height + 5)

        if template == 'blue_sidebar':
            pdf.add_sidebar_info()

            if data.get('skills'):
                skill_list = [s.strip() for s in data['skills'].split(',') if s.strip()]
                pdf.add_sidebar_section('Skills', skill_list)

            if data.get('hobbies'):
                hobby_list = [h.strip() for h in data['hobbies'].split(',') if h.strip()]
                pdf.add_sidebar_section('Hobbies', hobby_list)

            pdf.add_sidebar_projects(data.get('projects', []))

            if data.get('languages'):
                lang_list = [l.strip() for l in data['languages'].split(',') if l.strip()]
                pdf.add_sidebar_section('Languages', lang_list)

            pdf.set_xy(75, 45)
            pdf.add_summary(data.get('summary', ''))
            pdf.set_x(75)
            pdf.add_experience(data.get('experience', []))
            pdf.set_x(75)
            pdf.add_education(data.get('education', []))
            pdf.set_x(75)
            pdf.add_references(data.get('references', []))
        else:
            pdf.add_summary(data.get('summary', ''))
            pdf.add_experience(data.get('experience', []))
            pdf.add_education(data.get('education', []))
            pdf.add_skills(data.get('skills', ''))
            pdf.add_languages(data.get('languages', ''))
            pdf.add_hobbies(data.get('hobbies', ''))
            pdf.add_projects(data.get('projects', []))
            pdf.add_references(data.get('references', []))

        pdf_bytes = pdf.output(dest='S')
        # BUG FIX: fpdf2's output(dest='S') returns a bytearray in some
        # versions and str in others depending on fpdf version — normalize
        # to bytes so st.download_button always gets the right type.
        if isinstance(pdf_bytes, str):
            pdf_bytes = pdf_bytes.encode('latin-1')
        else:
            pdf_bytes = bytes(pdf_bytes)

        return pdf_bytes, None

    except Exception as e:
        return None, str(e)
