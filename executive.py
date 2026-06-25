"""templates_pdf/executive.py — "Executive" template: dark navy bar with gold accent line."""


class ExecutiveHeaderMixin:
    def executive_header(self):
        self.set_fill_color(15, 23, 42)
        self.rect(0, 0, 210, 40, 'F')
        self.set_draw_color(234, 179, 8)
        self.set_line_width(2)
        self.line(0, 40, 210, 40)
        if self.photo_bytes:
            self.add_photo_safe(165, 5, 30, 30)
        self.set_text_color(255, 255, 255)
        self.set_xy(15, 10)
        self.set_font('Arial', 'B', 24)
        self.cell(0, 10, self.safe_text(self.name), 0, 1, 'L')
        self.set_x(15)
        self.set_font('Arial', 'I', 12)
        self.set_text_color(234, 179, 8)
        self.cell(0, 6, self.safe_text(self.professional_title), 0, 1, 'L')
        self.set_text_color(0, 0, 0)
        self.ln(12)
