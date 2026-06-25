"""templates_pdf/minimal.py — "Minimal" template: centered, clean, no color blocks."""


class MinimalHeaderMixin:
    def minimal_header(self):
        self.set_font('Arial', 'B', 22)
        self.set_text_color(14, 165, 233)
        self.cell(0, 12, self.safe_text(self.name if self.name else "Your Name"), 0, 1, 'C')
        if self.professional_title:
            self.set_font('Arial', 'I', 11)
            self.set_text_color(37, 99, 235)
            self.cell(0, 6, self.safe_text(self.professional_title), 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.set_text_color(100, 100, 100)
        contact = []
        if self.email:
            contact.append(self.email)
        if self.phone:
            contact.append(self.phone)
        if self.address:
            contact.append(self.address)
        self.cell(0, 6, self.safe_text(" - ".join(contact)), 0, 1, 'C')
        self.set_text_color(0, 0, 0)
        self.set_draw_color(14, 165, 233)
        self.line(15, self.get_y() + 3, 195, self.get_y() + 3)
        self.ln(10)
