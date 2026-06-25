"""templates_pdf/tech.py — "Tech" template: dark top bar, terminal style.

BUG FIX: Original code filled the WHOLE page (0,0,210,297) with a dark
background, then every body section (summary/experience/education/etc, in
base.py) prints text in plain BLACK — so all of that content became
invisible against the dark page. Since the body sections are shared by all
templates and intentionally use black text, the fix here is to keep the
dark/green styling only in the top header bar (like every other template
does) instead of painting the entire page dark.
"""


class TechHeaderMixin:
    def tech_header(self):
        self.set_fill_color(16, 185, 129)
        self.rect(0, 0, 210, 35, 'F')
        self.set_text_color(17, 24, 39)
        self.set_xy(15, 10)
        self.set_font('Courier', 'B', 20)
        self.cell(0, 10, self.safe_text(f"> {self.name}"), 0, 1, 'L')
        self.set_text_color(0, 0, 0)
        self.ln(10)
