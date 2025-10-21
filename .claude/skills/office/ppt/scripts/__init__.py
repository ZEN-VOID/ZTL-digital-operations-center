"""
PowerPoint Generator Package

This package provides comprehensive PowerPoint generation capabilities with
three different approaches:

1. Direct Generation (ppt_generator.py): Programmatic PPT creation
2. HTML to PPT (html_to_ppt_converter.py): HTML content conversion
3. Template-based (templates.py): Predefined presentation templates
"""

from .ppt_generator import (
    PPTGenerator,
    create_presentation,
    create_from_template
)

from .html_to_ppt_converter import (
    HTMLtoPPTConverter,
    convert_html_to_ppt
)

from .templates import (
    TemplateRegistry,
    PresentationTemplate,
    BusinessReportTemplate,
    ProductLaunchTemplate,
    TrainingTemplate,
    PitchTemplate
)

__version__ = "1.0.0"

__all__ = [
    # Direct generation
    "PPTGenerator",
    "create_presentation",
    "create_from_template",

    # HTML conversion
    "HTMLtoPPTConverter",
    "convert_html_to_ppt",

    # Templates
    "TemplateRegistry",
    "PresentationTemplate",
    "BusinessReportTemplate",
    "ProductLaunchTemplate",
    "TrainingTemplate",
    "PitchTemplate",
]
