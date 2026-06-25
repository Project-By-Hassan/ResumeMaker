"""templates_pdf/academic.py — "Academic" template: centered Times serif, no color blocks."""


class AcademicHeaderMixin:
    def academic_header(self):
        self.set_font('Times', 'B', 24)
        self.set_text_color(30, 41, 59)
        self.cell(0, 12, self.safe_text(self.name), 0, 1, 'C')
        if self.professional_title:
            self.set_font('Times', 'I', 12)
            self.cell(0, 6, self.safe_text(self.professional_title), 0, 1, 'C')
        self.set_draw_color(30, 41, 59)
        self.line(15, self.get_y() + 3, 195, self.get_y() + 3)
        self.ln(10)
