"""
resume_pdf.py — FLAT VERSION (no templates_pdf/ folder needed)
All template files are in root directory.
"""
from base import BaseResumePDF
from modern import ModernHeaderMixin
from professional import ProfessionalHeaderMixin
from minimal import MinimalHeaderMixin
from blue_sidebar import BlueSidebarHeaderMixin
from executive import ExecutiveHeaderMixin
from creative import CreativeHeaderMixin
from tech import TechHeaderMixin
from academic import AcademicHeaderMixin
from multi_column import MultiColumnHeaderMixin


class ResumePDF(
    ModernHeaderMixin,
    ProfessionalHeaderMixin,
    MinimalHeaderMixin,
    BlueSidebarHeaderMixin,
    ExecutiveHeaderMixin,
    CreativeHeaderMixin,
    TechHeaderMixin,
    AcademicHeaderMixin,
    MultiColumnHeaderMixin,
    BaseResumePDF,
):
    """Final PDF class — all 9 template headers + shared content sections."""
    pass
