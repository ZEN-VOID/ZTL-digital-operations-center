---
name: AIGC Text-to-Image Generator
description: Generate professional restaurant design images from text descriptions. Supports 9 design types (poster, menu, storefront, panel, magazine, icon, typography, main-image, detail). Use when generating restaurant visuals, marketing materials, or when user mentions text-to-image, design generation, or restaurant graphics. Requires OpenRouter API key.
---

# AIGC Text-to-Image Generator

## Quick Start

### Method 1: Use Skill Convenience Function (Recommended)
```python
import sys
sys.path.append('./.claude/skills/aigc/text-to-image/scripts')
from text_to_image_api import generate_text_to_image

result = generate_text_to_image(
    prompt="Create a modern Chinese hotpot restaurant poster with festive red colors",
    design_type="1-poster"
)

if result["success"]:
    print(f"Generated: {result['image_paths']}")
```

### Method 2: Use Shared Core Library Directly
```python
import sys
from pathlib import Path

# Import shared library
shared = Path('./.claude/skills/aigc/_shared')
sys.path.insert(0, str(shared))

from banana_api_core import NanoBananaAPI

api = NanoBananaAPI()
result = api.generate_text_to_image(
    prompt="Modern hotpot restaurant poster",
    design_type="1-poster"
)
```

### Method 3: Execute from JSON Plan
```python
from text_to_image_api import execute_plan_from_file

result = execute_plan_from_file(
    'api/plans/e1-text-to-image/your-task.json'
)
```

## Design Types

This skill supports 9 professional design types:

| Type | Code | Aspect Ratio | Use Case |
|------|------|--------------|----------|
| **Poster** | `1-poster` | 2:3 vertical | Grand opening, promotions, events |
| **Menu** | `2-menu` | 3:4 vertical | Restaurant menus, price lists |
| **Storefront** | `3-storefront` | 16:9 horizontal | Store signage, exterior design |
| **Panel** | `4-panel` | 4:3 horizontal | Wall menu boards, displays |
| **Magazine** | `5-magazine` | A4 standard | Brand brochures, catalogs |
| **Icon** | `6-icon` | 1:1 square | Logos, brand icons |
| **Typography** | `7-typography` | Horizontal | Brand wordmarks, signage text |
| **Main Image** | `8-main-image` | 1:1 or 16:9 | Food photography, product shots |
| **Detail Page** | `9-detail` | 9:16 vertical | Mobile detail pages, social media |

## Documentation

- **[API Reference](reference.md)**: Complete API documentation and parameter guide
- **[Design Types Guide](design-types.md)**: Detailed guide for each design type
- **[Examples](examples.md)**: Restaurant industry use cases and templates

## Bundled Scripts

- **`scripts/text_to_image_api.py`**: Skill-specific convenience functions
- **`../_shared/banana_api_core.py`**: Core NanoBananaAPI client (shared library)
- **`../_shared/plan_executor.py`**: JSON plan execution utility (shared library)
- **`../_shared/config.py`**: Unified configuration management

## Common Tasks

### Create a promotional poster
```python
result = api.generate_text_to_image(
    prompt="Grand opening celebration for Sichuan hotpot restaurant, festive atmosphere",
    design_type="1-poster"
)
```

### Generate restaurant menu design
```python
result = api.generate_text_to_image(
    prompt="Elegant Japanese sushi menu with minimalist zen aesthetics",
    design_type="2-menu"
)
```

### Create brand logo
```python
result = api.generate_text_to_image(
    prompt="Modern coffee shop logo with artisanal elements",
    design_type="6-icon"
)
```

## Requirements

```bash
# Python dependencies
pip install requests pydantic python-dotenv

# Environment variables
export OPENROUTER_API_KEY=your_key_here
```

## Output Structure

Generated images are saved to:
```
output/
  images/
    e1-text-to-image/
      text_to_image_20250120_103000_1.png
  prompts/
    e1-text-to-image/
      text_to_image_20250120_103000_prompt.json
```

## Error Handling

Common errors:
- **API key missing**: Set `OPENROUTER_API_KEY` environment variable
- **Model error**: Check OpenRouter service status
- **Invalid design type**: Use one of the 9 supported design types
- **Rate limit**: Automatic retry with exponential backoff

See [reference.md](reference.md) for detailed error handling strategies.

## Quality Standards

- **Resolution**: 300 DPI minimum for print-ready designs
- **Format**: PNG with transparency support
- **Color**: Professional restaurant industry color standards
- **Style**: Integrated with professional design corpus from `library/prompts/`

## Related Skills

- For image modification: See `../image-to-image/SKILL.md`
- For image analysis: See `../image-recognition/SKILL.md`
- For advanced processing: See `../advanced-processing/SKILL.md`
