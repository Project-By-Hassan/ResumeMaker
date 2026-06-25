"""templates_pdf/blue_sidebar.py — "Blue Sidebar" template: left gray sidebar + blue top bar."""


class BlueSidebarHeaderMixin:
    def blue_sidebar_header(self):
        self.set_fill_color(229, 231, 235)
        self.rect(0, 0, 70, 297, 'F')
        self.set_fill_color(37, 99, 235)
        self.rect(0, 0, 210, 35, 'F')
        if self.photo_bytes:
            self.set_draw_color(255, 255, 255)
            self.set_line_width(1.5)
            self.rect(18, 38, 34, 39)
            self.add_photo_safe(20, 40, 30, 35)
        self.set_text_color(255, 255, 255)
        self.set_xy(75, 10)
        self.set_font('Arial', 'B', 22)
        self.cell(0, 10, self.safe_text(self.name), 0, 1, 'L')
        self.set_xy(75, 20)
        self.set_font('Arial', 'I', 11)
        self.cell(0, 6, self.safe_text(self.professional_title), 0, 1, 'L')
        self.set_text_color(0, 0, 0)
        self.sidebar_y = 85
