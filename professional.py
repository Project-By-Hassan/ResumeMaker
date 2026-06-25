"""templates_pdf/professional.py — "Professional" template: classic Times serif header."""


class ProfessionalHeaderMixin:
    def professional_header(self):
        if self.photo_bytes:
            self.add_photo_safe(165, 10, 30, 40)
        self.set_font('Times', 'B', 26)
        self.set_text_color(14, 165, 233)
        self.cell(0, 14, self.safe_text(self.name if self.name else "Your Name"), 0, 1, 'L')
        if self.professional_title:
            self.set_font('Times', 'I', 13)
            self.set_text_color(37, 99, 235)
            self.cell(0, 7, self.safe_text(self.professional_title), 0, 1, 'L')
        self.set_font('Times', '', 11)
        self.set_text_color(0, 0, 0)
        if self.email:
            self.cell(0, 6, self.safe_text(f"Email: {self.email}"), 0, 1, 'L')
        if self.phone:
            self.cell(0, 6, self.safe_text(f"Phone: {self.phone}"), 0, 1, 'L')
        if self.address:
            self.cell(0, 6, self.safe_text(f"Address: {self.address}"), 0, 1, 'L')
        if self.linkedin:
            self.cell(0, 6, self.safe_text(f"LinkedIn: {self.linkedin}"), 0, 1, 'L')
        self.set_draw_color(14, 165, 233)
        self.set_line_width(1)
        self.line(15, self.get_y() + 3, 195, self.get_y() + 3)
        self.ln(10)
