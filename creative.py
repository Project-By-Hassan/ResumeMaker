"""templates_pdf/creative.py — "Creative" template: tri-color top blocks."""


class CreativeHeaderMixin:
    def creative_header(self):
        self.set_fill_color(236, 72, 153)
        self.rect(0, 0, 70, 35, 'F')
        self.set_fill_color(14, 165, 233)
        self.rect(70, 0, 70, 35, 'F')
        self.set_fill_color(234, 179, 8)
        self.rect(140, 0, 70, 35, 'F')
        if self.photo_bytes:
            self.add_photo_safe(15, 5, 25, 25)
        self.set_text_color(15, 23, 42)
        self.set_xy(15, 38)
        self.set_font('Arial', 'B', 26)
        self.cell(0, 12, self.safe_text(self.name), 0, 1, 'L')
        self.ln(5)
