"""
templates_pdf/base.py
======================
ResumePDF ki base class. Ye sirf common/shared helpers rakhti hai:
- safe_text / safe_cell / safe_multi_cell (encoding-safe printing)
- auto 2-column layout logic
- photo embedding
- generic content sections (summary, experience, education, skills,
  languages, hobbies, projects, references) jo HAR template use karta hai.

Har individual template ka sirf "header" alag file me hai
(templates_pdf/modern.py, professional.py, waghera) — wahan se yeh class
ko mixin ki tarah extend kiya jata hai.
"""
import io
import os

from fpdf import FPDF
from PIL import Image


class BaseResumePDF(FPDF):
    """Saare templates ke liye common logic. Khud kabhi seedha use nahi hota."""

    def __init__(self, template='modern', photo_bytes=None):
        super().__init__(format='A4')
        self.template = template
        self.photo_bytes = photo_bytes
        self.set_auto_page_break(auto=False)
        self.set_margins(15, 15, 15)

        self.name = ""
        self.professional_title = ""
        self.email = ""
        self.phone = ""
        self.address = ""
        self.linkedin = ""
        self.father_name = ""
        self.dob = ""
        self.religion = ""
        self.nationality = ""

        # Two-column layout (blue_sidebar template apna alag layout use karta hai)
        self.auto_column_enabled = False if template == 'blue_sidebar' else True
        self.current_column = 1
        self.col_width = 90
        self.left_x = 15
        self.right_x = 110
        self.header_height = 45
        self.sidebar_y = 85

    # ---------- column helpers ----------
    def get_column_width(self):
        if self.template == 'blue_sidebar':
            return 120
        return self.col_width if self.auto_column_enabled else 180

    def get_column_x(self):
        if self.template == 'blue_sidebar':
            return 75
        return self.right_x if self.current_column == 2 else self.left_x

    def check_column_break(self, height_needed=20):
        if not self.auto_column_enabled:
            return False

        if self.current_column == 1 and self.get_y() + height_needed > 270:
            self.set_xy(self.right_x, self.header_height)
            self.current_column = 2
            return True

        if self.current_column == 2 and self.get_y() + height_needed > 270:
            return False

        return False

    # ---------- safe printing helpers ----------
    def safe_cell(self, w, h, txt='', border=0, ln=0, align='', fill=0):
        if self.auto_column_enabled:
            self.set_x(self.get_column_x())
        self.cell(w, h, txt, border, ln, align, fill)

    def safe_multi_cell(self, w, h, txt='', border=0, align='', fill=0):
        if self.auto_column_enabled:
            self.set_x(self.get_column_x())
        self.multi_cell(w, h, txt, border, align, fill)

    def safe_text(self, text):
        """FPDF latin-1 sirf simple characters handle karta hai, isliye
        common Unicode symbols (bullets, dashes, quotes waghera) ko
        replace karke encode karte hain taake crash na ho."""
        if not text:
            return ""
        text = str(text)
        replacements = {
            '•': '-', '●': '-', '▪': '-', '■': '-', '◆': '-', '○': '-',
            '–': '-', '—': '-', '…': '...', '→': '->', '←': '<-',
            '\u201c': '"', '\u201d': '"', '\u2018': "'", '\u2019': "'",
            '™': 'TM', '®': '(R)', '©': '(C)', '€': 'EUR', '£': 'GBP',
            '★': '*', '☆': '*', '✓': 'v', '✗': 'x',
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text.encode('latin-1', 'replace').decode('latin-1')

    def add_photo_safe(self, x, y, w=30, h=35):
        """BUG FIX: temp file ka naam unique rakha hai (id(self) based) aur
        ab finally block me hamesha cleanup hota hai, even on failure."""
        if not self.photo_bytes:
            return
        temp_path = f'temp_resume_photo_{id(self)}.jpg'
        try:
            img = Image.open(io.BytesIO(self.photo_bytes))
            if img.mode == 'RGBA':
                bg = Image.new('RGB', img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[3])
                img = bg
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            img.save(temp_path, 'JPEG', quality=95)
            self.image(temp_path, x=x, y=y, w=w, h=h)
        except Exception as e:
            print(f"Photo error: {e}")
        finally:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass

    # ---------- generic section title ----------
    def section_title(self, title):
        self.check_column_break(15)
        self.ln(3)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(14, 165, 233)
        if self.template == 'blue_sidebar':
            self.set_x(75)
            self.cell(0, 9, self.safe_text(f"> {title.upper()}"), 0, 1, 'L')
        else:
            self.safe_cell(0, 9, self.safe_text(title.upper()), 0, 1, 'L')
        self.set_draw_color(14, 165, 233)
        self.set_line_width(0.5)
        start_x = self.get_column_x() if self.auto_column_enabled else (75 if self.template == 'blue_sidebar' else 15)
        end_x = start_x + 50
        self.line(start_x, self.get_y(), end_x, self.get_y())
        self.set_text_color(0, 0, 0)
        self.ln(3)

    # ---------- content sections (used by all templates) ----------
    def add_summary(self, summary):
        if summary and summary.strip():
            self.check_column_break(25)
            self.section_title('Professional Summary')
            self.set_font('Arial', '', 11)
            if self.template == 'blue_sidebar':
                self.set_x(75)
                self.multi_cell(120, 6, self.safe_text(summary))
            else:
                self.safe_multi_cell(self.get_column_width(), 6, self.safe_text(summary))
            self.ln(2)

    def add_experience(self, experiences):
        valid_exp = [exp for exp in experiences if exp.get('title') or exp.get('company')]
        if not valid_exp:
            return
        self.check_column_break(30)
        self.section_title('Work Experience')
        for exp in valid_exp:
            self.check_column_break(20)
            is_sidebar = self.template == 'blue_sidebar'
            if is_sidebar:
                self.set_x(75)
            self.set_font('Arial', 'B', 12)
            if is_sidebar:
                self.cell(0, 7, self.safe_text(exp.get('title', 'Position')), 0, 1)
            else:
                self.safe_cell(0, 7, self.safe_text(exp.get('title', 'Position')), 0, 1)

            if is_sidebar:
                self.set_x(75)
            self.set_font('Arial', 'B', 11)
            if is_sidebar:
                self.cell(0, 6, self.safe_text(exp.get('company', 'Company')), 0, 1)
            else:
                self.safe_cell(0, 6, self.safe_text(exp.get('company', 'Company')), 0, 1)

            if is_sidebar:
                self.set_x(75)
            self.set_font('Arial', 'I', 10)
            self.set_text_color(100, 100, 100)
            duration = exp.get('duration', '')
            if exp.get('location'):
                duration += f" | {exp['location']}"
            if duration:
                if is_sidebar:
                    self.cell(0, 5, self.safe_text(duration), 0, 1)
                else:
                    self.safe_cell(0, 5, self.safe_text(duration), 0, 1)
            self.set_text_color(0, 0, 0)
            self.set_font('Arial', '', 11)
            if exp.get('desc'):
                desc_lines = exp['desc'].split('\n')
                for line in desc_lines:
                    if line.strip():
                        if is_sidebar:
                            self.set_x(75)
                            self.multi_cell(120, 6, self.safe_text(f"- {line.strip()}"))
                        else:
                            self.safe_multi_cell(self.get_column_width(), 6, self.safe_text(f"- {line.strip()}"))
            self.ln(3)

    def add_education(self, education_list):
        valid_edu = [edu for edu in education_list if edu.get('degree') or edu.get('institute')]
        if not valid_edu:
            return
        self.check_column_break(20)
        self.section_title('Education')
        for edu in valid_edu:
            self.check_column_break(15)
            is_sidebar = self.template == 'blue_sidebar'
            if is_sidebar:
                self.set_x(75)
            self.set_font('Arial', 'B', 12)
            if is_sidebar:
                self.cell(0, 7, self.safe_text(edu.get('degree', 'Degree')), 0, 1)
            else:
                self.safe_cell(0, 7, self.safe_text(edu.get('degree', 'Degree')), 0, 1)

            if is_sidebar:
                self.set_x(75)
            self.set_font('Arial', '', 11)
            inst_text = edu.get('institute', 'Institute')
            if edu.get('year'):
                inst_text += f" - {edu['year']}"
            if is_sidebar:
                self.cell(0, 6, self.safe_text(inst_text), 0, 1)
            else:
                self.safe_cell(0, 6, self.safe_text(inst_text), 0, 1)

            if edu.get('grade'):
                if is_sidebar:
                    self.set_x(75)
                self.set_font('Arial', 'I', 10)
                if is_sidebar:
                    self.cell(0, 5, self.safe_text(f"Grade: {edu['grade']}"), 0, 1)
                else:
                    self.safe_cell(0, 5, self.safe_text(f"Grade: {edu['grade']}"), 0, 1)
            self.ln(2)

    def add_skills(self, skills):
        if not (skills and skills.strip()):
            return
        self.check_column_break(20)
        self.section_title('Skills')
        self.set_font('Arial', '', 11)
        skill_list = [s.strip() for s in skills.split(',') if s.strip()]
        if not skill_list:
            return
        if len(skill_list) > 8 and self.template == 'multi_column' and self.auto_column_enabled:
            col_width = 90
            for i, skill in enumerate(skill_list):
                if i % 2 == 0:
                    self.set_x(self.left_x)
                    self.cell(col_width, 6, self.safe_text(f"- {skill}"), 0, 0)
                else:
                    self.set_x(self.left_x + col_width)
                    self.cell(col_width, 6, self.safe_text(f"- {skill}"), 0, 1)
            if len(skill_list) % 2 == 1:
                self.ln(6)
        else:
            if self.template == 'blue_sidebar':
                self.set_x(75)
                self.multi_cell(120, 6, self.safe_text(' - '.join(skill_list)))
            else:
                self.safe_multi_cell(self.get_column_width(), 6, self.safe_text(' - '.join(skill_list)))
        self.ln(2)

    def add_languages(self, languages):
        if not (languages and languages.strip()):
            return
        self.check_column_break(15)
        self.section_title('Languages')
        self.set_font('Arial', '', 11)
        lang_list = [l.strip() for l in languages.split(',') if l.strip()]
        if lang_list:
            if self.template == 'blue_sidebar':
                self.set_x(75)
                self.multi_cell(120, 6, self.safe_text(' - '.join(lang_list)))
            else:
                self.safe_multi_cell(self.get_column_width(), 6, self.safe_text(' - '.join(lang_list)))
        self.ln(2)

    def add_hobbies(self, hobbies):
        if not (hobbies and hobbies.strip()):
            return
        self.check_column_break(15)
        self.section_title('Hobbies & Interests')
        self.set_font('Arial', '', 11)
        hobby_list = [h.strip() for h in hobbies.split(',') if h.strip()]
        if hobby_list:
            if self.template == 'blue_sidebar':
                self.set_x(75)
                self.multi_cell(120, 6, self.safe_text(' - '.join(hobby_list)))
            else:
                self.safe_multi_cell(self.get_column_width(), 6, self.safe_text(' - '.join(hobby_list)))
        self.ln(2)

    def add_projects(self, projects):
        valid_proj = [proj for proj in projects if proj.get('name')]
        if not valid_proj:
            return
        self.check_column_break(25)
        self.section_title('Projects')
        is_sidebar = self.template == 'blue_sidebar'
        for proj in valid_proj:
            self.check_column_break(18)
            if is_sidebar:
                self.set_x(75)
            self.set_font('Arial', 'B', 12)
            if is_sidebar:
                self.cell(0, 7, self.safe_text(proj['name']), 0, 1)
            else:
                self.safe_cell(0, 7, self.safe_text(proj['name']), 0, 1)

            if proj.get('tech'):
                if is_sidebar:
                    self.set_x(75)
                self.set_font('Arial', 'I', 10)
                self.set_text_color(100, 100, 100)
                if is_sidebar:
                    self.cell(0, 5, self.safe_text(proj['tech']), 0, 1)
                else:
                    self.safe_cell(0, 5, self.safe_text(proj['tech']), 0, 1)
                self.set_text_color(0, 0, 0)

            if proj.get('desc'):
                if is_sidebar:
                    self.set_x(75)
                self.set_font('Arial', '', 11)
                if is_sidebar:
                    self.multi_cell(120, 6, self.safe_text(proj['desc']))
                else:
                    self.safe_multi_cell(self.get_column_width(), 6, self.safe_text(proj['desc']))
            self.ln(2)

    def add_references(self, references):
        valid_ref = [ref for ref in references if ref.get('name')]
        if not valid_ref:
            return
        self.check_column_break(20)
        self.section_title('References')
        is_sidebar = self.template == 'blue_sidebar'
        for ref in valid_ref:
            self.check_column_break(12)
            if is_sidebar:
                self.set_x(75)
            self.set_font('Arial', 'B', 11)
            if is_sidebar:
                self.cell(0, 6, self.safe_text(ref['name']), 0, 1)
            else:
                self.safe_cell(0, 6, self.safe_text(ref['name']), 0, 1)

            self.set_font('Arial', '', 10)
            if ref.get('position'):
                if is_sidebar:
                    self.set_x(75)
                    self.cell(0, 5, self.safe_text(ref['position']), 0, 1)
                else:
                    self.safe_cell(0, 5, self.safe_text(ref['position']), 0, 1)
            if ref.get('contact'):
                if is_sidebar:
                    self.set_x(75)
                    self.cell(0, 5, self.safe_text(ref['contact']), 0, 1)
                else:
                    self.safe_cell(0, 5, self.safe_text(ref['contact']), 0, 1)
            self.ln(2)

    # ---------- blue_sidebar-only helpers ----------
    def add_sidebar_section(self, title, content_list):
        if not content_list:
            return
        self.set_xy(15, self.sidebar_y)
        self.set_font('Arial', 'B', 11)
        self.set_text_color(37, 99, 235)
        self.cell(50, 6, self.safe_text(f"> {title.upper()}"), 0, 1, 'L')
        self.set_font('Arial', '', 9)
        self.set_text_color(0, 0, 0)
        for item in content_list:
            self.set_x(15)
            self.multi_cell(50, 5, self.safe_text(f"- {item}"), 0, 'L')
        self.sidebar_y = self.get_y() + 3

    def add_sidebar_info(self):
        self.set_xy(15, self.sidebar_y)
        self.set_font('Arial', 'B', 11)
        self.set_text_color(37, 99, 235)
        self.cell(50, 6, self.safe_text("> MY INFO."), 0, 1, 'L')
        self.set_font('Arial', '', 9)
        self.set_text_color(0, 0, 0)
        info_items = []
        if self.father_name:
            info_items.append(f"Father: {self.father_name}")
        if self.dob:
            info_items.append(f"DOB: {self.dob}")
        if self.religion:
            info_items.append(f"Religion: {self.religion}")
        if self.nationality:
            info_items.append(f"Nationality: {self.nationality}")
        if self.phone:
            info_items.append(f"Phone: {self.phone}")
        if self.email:
            info_items.append(f"Email: {self.email}")
        for item in info_items:
            self.set_x(15)
            self.multi_cell(50, 5, self.safe_text(item), 0, 'L')
        self.sidebar_y = self.get_y() + 3

    def add_sidebar_projects(self, projects):
        valid_proj = [p for p in projects if p.get('name')]
        if not valid_proj:
            return
        self.set_xy(15, self.sidebar_y)
        self.set_font('Arial', 'B', 11)
        self.set_text_color(37, 99, 235)
        self.cell(50, 6, self.safe_text("> PROJECTS"), 0, 1, 'L')
        self.set_font('Arial', 'B', 9)
        self.set_text_color(0, 0, 0)
        for proj in valid_proj[:3]:
            self.set_x(15)
            self.multi_cell(50, 5, self.safe_text(proj['name']), 0, 'L')
            if proj.get('tech'):
                self.set_x(15)
                self.set_font('Arial', 'I', 8)
                self.set_text_color(100, 100, 100)
                self.multi_cell(50, 4, self.safe_text(proj['tech']), 0, 'L')
                self.set_text_color(0, 0, 0)
                self.set_font('Arial', 'B', 9)
        self.sidebar_y = self.get_y() + 3
