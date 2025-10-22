---
name: AIGC Image-to-Image Processor
description: Process and transform existing restaurant images with AI-powered optimization, style transfer, and creative modifications. Supports local edits, enhancements, multi-image processing, and style transfer. Use when modifying restaurant images, enhancing food photos, or when user mentions image-to-image, photo editing, or visual optimization. Requires OpenRouter API key.
---

# AIGC Image-to-Image Processor

## Quick Start

### Method 1: Use Skill Convenience Function (Recommended)
```python
import sys
sys.path.append('./.claude/skills/aigc/image-to-image/scripts')
from image_to_image_api import generate_image_to_image

result = generate_image_to_image(
    prompt="Enhance food colors and lighting for marketing appeal",
    image_urls=["input/food-photo.jpg"],
    processing_type="local_optimization"
)

if result["success"]:
    print(f"Processed: {result['image_paths']}")
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
result = api.generate_image_to_image(
    prompt="Enhance food colors and lighting",
    image_urls=["input/food-photo.jpg"],
    processing_type="local_optimization"
)
```

### Method 3: Execute from JSON Plan
```python
from image_to_image_api import execute_plan_from_file

result = execute_plan_from_file(
    'api/plans/e2-image-to-image/your-task.json'
)
```

## Processing Types

This skill supports 5 professional processing types:

| Type | Code | Description | Use Case |
|------|------|-------------|----------|
| **Local Modification** | `local_modification` | Precise edits to specific areas | Change logo, modify elements, adjust colors |
| **Local Optimization** | `local_optimization` | Enhance specific regions | Improve food texture, enhance lighting |
| **Multi-Image Processing** | `multi_image_processing` | Process multiple images | Batch enhancement, style unification |
| **Style Transfer** | `style_transfer` | Apply artistic styles | Brand style, seasonal themes |
| **Scene Analysis** | `scene_analysis` | Understand image context | Pre-processing analysis |

## Documentation

- **[API Reference](reference.md)**: Complete API documentation and parameter guide
- **[Processing Guide](processing-types.md)**: Detailed guide for each processing type
- **[Examples](examples.md)**: Restaurant industry use cases and workflows

## Bundled Scripts

- **`scripts/image_to_image_api.py`**: Skill-specific convenience functions
- **`../_shared/banana_api_core.py`**: Core NanoBananaAPI client (shared library)
- **`../_shared/plan_executor.py`**: JSON plan execution utility (shared library)
- **`../_shared/config.py`**: Unified configuration management

## Common Tasks

### Enhance food photography
```python
result = api.generate_image_to_image(
    prompt="Enhance food colors, increase saturation, improve lighting",
    image_urls=["path/to/food.jpg"],
    processing_type="local_optimization"
)
```

### Change logo or branding
```python
result = api.generate_image_to_image(
    prompt="Replace logo with 'HOUXIANG BAOZI', change to blue background",
    image_urls=["path/to/poster.jpg"],
    processing_type="local_modification"
)
```

### Apply brand style
```python
result = api.generate_image_to_image(
    prompt="Apply elegant Japanese minimalist style",
    image_urls=["path/to/menu.jpg"],
    processing_type="style_transfer"
)
```

### Batch process images
```python
result = api.generate_image_to_image(
    prompt="Unify visual style across all menu items",
    image_urls=[
        "path/to/dish1.jpg",
        "path/to/dish2.jpg",
        "path/to/dish3.jpg"
    ],
    processing_type="multi_image_processing"
)
```

## Requirements

```bash
# Python dependencies
pip install requests pydantic python-dotenv pillow

# Environment variables
export OPENROUTER_API_KEY=your_key_here
```

## Input Image Support

### Supported Formats
- **Network URLs**: `http://` or `https://`
- **Local Files**: Absolute or relative paths
- **Base64**: Automatic conversion for local files

### Image Formats
- PNG, JPG, JPEG, WebP
- Maximum size: 10MB per image
- Recommended resolution: 1024x1024 to 4096x4096

## Output Structure

Processed images are saved to:
```
output/
  images/
    e2-image-to-image/
      image_to_image_20250120_103000_1.png
  prompts/
    e2-image-to-image/
      image_to_image_20250120_103000_prompt.json
```

## Error Handling

Common errors:
- **Image not found**: Check file path or URL accessibility
- **Invalid format**: Use supported image formats (PNG, JPG, WebP)
- **File too large**: Reduce image size before processing
- **API key missing**: Set `OPENROUTER_API_KEY` environment variable
- **Processing timeout**: Simplify operation or reduce image count

See [reference.md](reference.md) for detailed error handling strategies.

## Quality Standards

- **Preservation**: Maintains original image quality and resolution
- **Natural Processing**: Seamless edits without visible artifacts
- **Color Accuracy**: Professional color management for food photography
- **Restaurant Standards**: Optimized for restaurant industry aesthetics

## Advanced Features

### Multi-Step Processing

Combine multiple operations for complex workflows:

```python
# Step 1: Enhance lighting
step1 = api.generate_image_to_image(
    prompt="Improve lighting and shadows",
    image_urls=["original.jpg"],
    processing_type="local_optimization"
)

# Step 2: Apply brand style
step2 = api.generate_image_to_image(
    prompt="Apply brand color scheme",
    image_urls=[step1["image_paths"][0]],
    processing_type="style_transfer"
)
```

### Precise Control

Use detailed prompts for better control:

```python
prompt = """
Target modifications:
1. Logo area: Replace with 'NEW BRAND', use red color
2. Background: Change to warm beige tone
3. Food items: Enhance saturation by 20%
4. Lighting: Add subtle highlight from top-left
"""

result = api.generate_image_to_image(
    prompt=prompt,
    image_urls=["design.jpg"],
    processing_type="local_modification"
)
```

## Integration with Analysis

Pre-analyze images before processing:

```python
# 1. Analyze image first (if needed)
from image_recognition import analyze_restaurant_image

analysis = analyze_restaurant_image("photo.jpg")
print(f"Scene: {analysis['scene_type']}")
print(f"Quality: {analysis['technical_quality']}")

# 2. Process based on analysis
if analysis['quality'] < 0.7:
    result = api.generate_image_to_image(
        prompt="Enhance overall quality and visual appeal",
        image_urls=["photo.jpg"],
        processing_type="local_optimization"
    )
```

## Related Skills

- For image generation: See `../text-to-image/SKILL.md`
- For image analysis: See `../image-recognition/SKILL.md`
- For advanced processing: See `../advanced-processing/SKILL.md`

## Best Practices

1. **Start with Analysis**: Understand the image before processing
2. **Use Specific Prompts**: Detailed instructions produce better results
3. **Iterative Processing**: Complex edits work better in multiple steps
4. **Preserve Originals**: Always keep backup of original images
5. **Test Parameters**: Adjust processing strength for optimal results
6. **Batch Wisely**: Group similar processing tasks for efficiency
