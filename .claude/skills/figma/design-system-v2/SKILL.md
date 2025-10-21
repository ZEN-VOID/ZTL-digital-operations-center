---
name: Figma Design System Management
description: Manage enterprise-grade design systems including component libraries, style libraries, variables, and theme systems. Use when building design systems, managing components and styles, creating themes, or when user mentions design tokens, component libraries, style guides, variables, themes, dark mode, or brand consistency. Requires Figma API token.
---

# Figma Design System Management

## Quick Start

### Get team components
```python
import sys
sys.path.append('./.claude/skills/figma/design-system-v2/scripts')
from design_system_client import DesignSystemClient

async with DesignSystemClient() as client:
    components = await client.get_team_components(team_id="YOUR_TEAM_ID")
    for component in components['meta']['components']:
        print(f"{component['name']}: {component['key']}")
```

### Create variable collection
```bash
python scripts/create_theme.py \
  --file-key YOUR_FILE_KEY \
  --theme light-dark \
  --output variables.json
```

## Documentation

- **[API Reference](reference.md)**: Complete design system API documentation
- **[Component Management](component-guide.md)**: Component library management guide
- **[Variables Guide](variables-guide.md)**: Variables and theme system guide
- **[Examples](examples.md)**: Design system examples

## Bundled Scripts

- **`scripts/design_system_client.py`**: Core design system operations
- **`scripts/create_theme.py`**: Multi-theme variable creation
- **`scripts/audit_consistency.py`**: Brand consistency audit
- **`scripts/export_tokens.py`**: Export design tokens to JSON/CSS/Tailwind

## Requirements

```bash
pip install httpx backoff pydantic-settings
export FIGMA_API_TOKEN=your_token_here
```

## Related Skills

- For analytics: See `../analytics-v2/SKILL.md`
- For file operations: See `../file-management-v2/SKILL.md`
