# Canvas Design Skill

Create beautiful visual art in PNG and PDF formats using design philosophy principles.

## Quick Start

```python
from scripts.canvas_designer import CanvasDesigner

# Initialize
designer = CanvasDesigner(
    project_name="火锅店开业筹备",
    agent_name="X4-平面设计师"
)

# Create design with philosophy
philosophy = {
    "movement_name": "Sichuan Fiesta",
    "philosophy_content": "Bold crimson and gold dominate...",
    "color_palette": ["#D32F2F", "#FFC107", "#FFFFFF"],
    "primary_font": "BigShoulders-Bold.ttf",
    "text_elements": {"main": "盛大开业"}
}

result = designer.create_design(
    user_prompt="火锅店开业海报",
    design_type="poster",
    philosophy=philosophy
)
```

## Design Types

- **poster**: A4 portrait (2480×3508px @ 300 DPI)
- **menu-cover**: A4 portrait for restaurant menus
- **packaging**: Square format (2000×2000px)
- **logo**: Square format (1000×1000px)
- **flyer**: A5 portrait (1754×2480px)
- **banner**: Wide format (3000×1000px)

## Output Structure

```
output/[项目名]/X4-平面设计师/canvas-design/[design-type]/
├── plans/      # JSON execution specifications
├── results/    # Final PNG/PDF files + philosophy.md
├── logs/       # Execution logs
└── metadata/   # Traceability metadata
```

## Installation

```bash
pip install Pillow reportlab
```

## Documentation

- **SKILL.md**: Complete design philosophy guidelines
- **reference.md**: Technical reference and API documentation
- **README.md**: This file - quick start and overview

---

**Maintained by**: X4-平面设计师 (via Claude Code)
