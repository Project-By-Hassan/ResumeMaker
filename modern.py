"""templates_pdf/modern.py — "Modern" template: blue top banner header."""


class ModernHeaderMixin:
    def modern_header(self):
        self.set_fill_color(14, 165, 233)
        self.rect(0, 0, 210, 45, 'F')
        if self.photo_bytes:
            self.add_photo_safe(15, 7, 28, 33)
            text_x = 50
        else:
            text_x = 15
        self.set_text_color(255, 255, 255)
        self.set_xy(text_x, 8)
        self.set_font('Arial', 'B', 24)
        self.cell(0, 10, self.safe_text(self.name if self.name else "Your Name"), 0, 1, 'L')
        if self.professional_title:
            self.set_x(text_x)
            self.set_font('Arial', 'I', 12)
            self.cell(0, 6, self.safe_text(self.professional_title), 0, 1, 'L')
        self.set_x(text_x)
        self.set_font('Arial', '', 10)
        contact = []
        if self.email:
            contact.append(self.email)
        if self.phone:
            contact.append(self.phone)
        if self.linkedin:
            contact.append(self.linkedin)
        self.cell(0, 6, self.safe_text(" | ".join(contact)), 0, 1, 'L')
        if self.address:
            self.set_x(text_x)
            self.cell(0, 6, self.safe_text(self.address), 0, 1, 'L')
        self.set_text_color(0, 0, 0)
        self.ln(12)
