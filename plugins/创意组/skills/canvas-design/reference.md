# Canvas Design - Technical Reference

## Architecture Overview

The canvas-design skill follows the **three-layer architecture** defined in global CLAUDE.md:

### Layer 1: Knowledge Layer (SKILL.md)
- Design philosophy principles
- Visual expression guidelines
- Craftsmanship standards
- Examples of design movements

### Layer 2: Plan/Configuration Layer (JSON specs)
```json
{
  "project_name": "火锅店开业筹备",
  "agent_name": "X4-平面设计师",
  "design_type": "poster",
  "movement_name": "Sichuan Fiesta",
  "philosophy_content": "...",
  "canvas_size": [2480, 3508],
  "output_format": "png",
  "color_palette": ["#D32F2F", "#FFC107", "#FFFFFF"],
  "primary_font": "BigShoulders-Bold.ttf",
  "text_elements": {
    "main": "盛大开业",
    "sub": "正宗川味火锅"
  }
}
```

### Layer 3: Execution Layer (canvas_designer.py)
- PDF generation via reportlab
- PNG generation via PIL/Pillow
- Font management
- Output path management

---

## Output Path Convention

Following the global standard defined in `~/.claude/CLAUDE.md`:

```
output/[项目名]/[agent-name]/canvas-design/[design-type]/
├── plans/      # JSON execution plans (Layer 2)
├── results/    # Final PNG/PDF outputs + philosophy.md
├── logs/       # Execution logs
└── metadata/   # Traceability metadata
```

---

## API Reference

### CanvasDesigner Class

```python
from scripts.canvas_designer import CanvasDesigner

designer = CanvasDesigner(
    project_name="火锅店开业筹备",
    agent_name="X4-平面设计师",
    fonts_dir=None  # Auto-detects canvas-fonts/
)
```

---

## Dependencies

```bash
pip install Pillow reportlab
```

---

**Last Updated**: 2025-10-29
**Version**: 1.0.0
**Maintainer**: X4-平面设计师 (via Claude Code)
