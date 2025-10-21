"""
Word Document Generator Skill

A self-contained skill for generating professional Word documents with
precise formatting control using python-docx library.

Author: ZTL数智化作战中心
Version: 1.0.0
"""

from .word_generator import (
    WordDocumentBuilder,
    create_document,
    create_from_template,
    quick_create
)

from .templates import (
    TemplateRegistry,
    ReportTemplate,
    ProposalTemplate,
    MeetingMinutesTemplate,
    ContractTemplate,
    ManualTemplate,
    LetterTemplate
)

__version__ = "1.0.0"
__all__ = [
    "WordDocumentBuilder",
    "create_document",
    "create_from_template",
    "quick_create",
    "TemplateRegistry",
    "ReportTemplate",
    "ProposalTemplate",
    "MeetingMinutesTemplate",
    "ContractTemplate",
    "ManualTemplate",
    "LetterTemplate"
]
