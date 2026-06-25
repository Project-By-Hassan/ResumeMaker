"""templates_pdf/multi_column.py — "Multi Column" template: blue top bar, 2-column skills."""


class MultiColumnHeaderMixin:
    def multi_column_header(self):
        self.set_fill_color(14, 165, 233)
        self.rect(0, 0, 210, 30, 'F')
        self.set_text_color(255, 255, 255)
        self.set_xy(15, 8)
        self.set_font('Arial', 'B', 22)
        self.cell(0, 10, self.safe_text(self.name), 0, 1, 'L')
        if self.professional_title:
            self.set_x(15)
            self.set_font('Arial', 'I', 11)
            self.cell(0, 6, self.safe_text(self.professional_title), 0, 1, 'L')
        self.set_text_color(0, 0, 0)
        self.ln(8)
