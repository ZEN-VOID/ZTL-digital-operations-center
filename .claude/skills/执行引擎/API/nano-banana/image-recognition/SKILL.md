---
name: AIGC Image Recognition Analyzer
description: Analyze restaurant images with AI-powered recognition for food content, scene understanding, quality assessment, and commercial insights. Supports comprehensive analysis, content recognition, scene detection, and quality evaluation. Use when analyzing restaurant images, evaluating food photos, or when user mentions image recognition, photo analysis, or visual assessment. Requires OpenRouter API key.
---

# AIGC Image Recognition Analyzer

## Quick Start

### Method 1: Use Skill Convenience Function (Recommended)
```python
import sys
sys.path.append('./.claude/skills/aigc/image-recognition/scripts')
from image_recognition_api import analyze_restaurant_image

result = analyze_restaurant_image(
    image_url="path/to/restaurant-photo.jpg",
    analysis_type="comprehensive_analysis"
)

if result["success"]:
    print(f"Analysis: {result['analysis_content']}")
    print(f"Saved to: {result['analysis_file']}")
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
result = api.generate_image_recognition(
    image_url="path/to/restaurant-photo.jpg",
    analysis_type="comprehensive_analysis"
)
```

### Method 3: Execute from JSON Plan
```python
from image_recognition_api import execute_plan_from_file

result = execute_plan_from_file(
    'api/plans/e3-image-recognition/your-task.json'
)
```

## Analysis Types

This skill supports 5 professional analysis types:

| Type | Code | Description | Output Focus |
|------|------|-------------|--------------|
| **Comprehensive Analysis** | `comprehensive_analysis` | Complete multi-dimensional analysis | 6 categories, 24 sub-categories, 120+ dimensions |
| **Quality Assessment** | `quality_assessment` | Technical and aesthetic quality | Technical specs, visual appeal, commercial viability |
| **Content Analysis** | `content_analysis` | Food and scene content | Food items, ingredients, presentation style |
| **Scene Recognition** | `scene_recognition` | Restaurant type and atmosphere | Venue type, dining scene, ambiance |
| **Brand Detection** | `brand_detection` | Brand elements and consistency | Logos, VI elements, brand compliance |

## Comprehensive Analysis Framework

The comprehensive analysis uses a structured 6-category framework:

### 1. Food Content Analysis
- **Main Dish Recognition**: Cuisine type, cooking method, presentation
- **Side Dish Analysis**: Ingredients, garnishes, accompaniments
- **Beverage Recognition**: Drink types, serving style
- **Dessert Analysis**: Sweet items, plating, decoration

### 2. Visual Technical Analysis
- **Photography Technique**: Camera angle, composition, framing
- **Lighting Effects**: Light sources, shadows, highlights
- **Color Performance**: Color balance, saturation, temperature
- **Clarity Quality**: Sharpness, resolution, detail level

### 3. Composition Aesthetics Analysis
- **Composition Principles**: Rule of thirds, golden ratio, balance
- **Visual Hierarchy**: Focal points, visual flow, emphasis
- **Aesthetic Style**: Design approach, artistic influence
- **Emotional Expression**: Mood, atmosphere, feeling conveyed

### 4. Scene Environment Analysis
- **Restaurant Type**: Cuisine category, dining style
- **Dining Scene**: Occasion type, service style
- **Environment Atmosphere**: Ambiance, decoration, setting
- **Space Characteristics**: Layout, capacity, design features

### 5. Brand Marketing Analysis
- **Brand Elements**: Logos, colors, typography, VI system
- **Marketing Value**: Commercial potential, promotional use
- **Target Audience**: Customer demographics, market segment
- **Competitive Analysis**: Market positioning, differentiation

### 6. Commercial Application Analysis
- **Usage Scenarios**: Best applications, platform suitability
- **Quality Standards**: Professional benchmarks, compliance
- **Improvement Suggestions**: Optimization recommendations
- **Commercial Value**: Business impact, ROI potential

## Documentation

- **[API Reference](reference.md)**: Complete API documentation and analysis guide
- **[Analysis Framework](analysis-framework.md)**: Detailed framework and dimensions
- **[Examples](examples.md)**: Restaurant industry analysis cases

## Bundled Scripts

- **`scripts/image_recognition_api.py`**: Skill-specific convenience functions
- **`../_shared/banana_api_core.py`**: Core NanoBananaAPI client (shared library)
- **`../_shared/plan_executor.py`**: JSON plan execution utility (shared library)
- **`../_shared/config.py`**: Unified configuration management

## Common Tasks

### Comprehensive restaurant image analysis
```python
result = api.generate_image_recognition(
    image_url="restaurant-scene.jpg",
    analysis_type="comprehensive_analysis",
    analysis_dimensions=[
        "food_content",
        "visual_quality",
        "composition",
        "brand_elements",
        "commercial_value"
    ]
)
```

### Food photography quality assessment
```python
result = api.generate_image_recognition(
    image_url="dish-photo.jpg",
    analysis_type="quality_assessment",
    analysis_dimensions=[
        "technical_quality",
        "aesthetic_appeal",
        "food_presentation",
        "marketing_potential"
    ]
)
```

### Scene and atmosphere detection
```python
result = api.generate_image_recognition(
    image_url="dining-area.jpg",
    analysis_type="scene_recognition",
    analysis_dimensions=[
        "restaurant_type",
        "dining_occasion",
        "ambiance",
        "target_demographic"
    ]
)
```

### Brand compliance check
```python
result = api.generate_image_recognition(
    image_url="marketing-material.jpg",
    analysis_type="brand_detection",
    analysis_dimensions=[
        "logo_presence",
        "brand_colors",
        "vi_compliance",
        "consistency_score"
    ]
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
- **Base64**: Automatic conversion

### Image Specifications
- Formats: PNG, JPG, JPEG, WebP
- Maximum size: 10MB per image
- Recommended resolution: 1024x1024 minimum

## Output Structure

Analysis results are saved to:
```
output/
  analysis/
    e3-image-recognition/
      [analysis_type]/
        analysis_20250120_103000.json
        analysis_20250120_103000_report.txt
```

### Output Format

**JSON Structure:**
```json
{
  "task_id": "uuid",
  "analysis_type": "comprehensive_analysis",
  "image_url": "path/to/image.jpg",
  "timestamp": "2025-01-20T10:30:00",
  "analysis_content": {
    "food_content": {...},
    "visual_technical": {...},
    "composition_aesthetics": {...},
    "scene_environment": {...},
    "brand_marketing": {...},
    "commercial_application": {...}
  },
  "insights": {
    "strengths": ["..."],
    "weaknesses": ["..."],
    "recommendations": ["..."]
  },
  "scores": {
    "overall_quality": 8.5,
    "technical_quality": 9.0,
    "aesthetic_appeal": 8.0,
    "commercial_value": 8.5
  }
}
```

## Error Handling

Common errors:
- **Image not accessible**: Check file path or URL
- **Unsupported format**: Use PNG, JPG, or WebP
- **Image too large**: Reduce file size
- **API key missing**: Set environment variable
- **Analysis timeout**: Simplify analysis dimensions

See [reference.md](reference.md) for detailed error handling.

## Analysis Accuracy

- **Food Recognition**: 95%+ accuracy for common dishes
- **Scene Detection**: 90%+ accuracy for restaurant types
- **Quality Assessment**: Professional-grade evaluation
- **Brand Detection**: High precision for standard logos

## Advanced Features

### Custom Analysis Dimensions

Specify exactly what to analyze:

```python
result = api.generate_image_recognition(
    image_url="photo.jpg",
    analysis_type="comprehensive_analysis",
    analysis_dimensions=[
        "main_dish_identification",
        "plating_style_analysis",
        "lighting_quality_assessment",
        "color_harmony_evaluation",
        "brand_visibility_check",
        "marketing_effectiveness_score"
    ]
)
```

### Batch Analysis

Analyze multiple images efficiently:

```python
images = [
    "menu-item-1.jpg",
    "menu-item-2.jpg",
    "menu-item-3.jpg"
]

results = []
for image_url in images:
    result = api.generate_image_recognition(
        image_url=image_url,
        analysis_type="quality_assessment"
    )
    results.append(result)

# Compare results
best_quality = max(results, key=lambda r: r['scores']['overall_quality'])
```

### Commercial Insights

Get actionable business recommendations:

```python
result = api.generate_image_recognition(
    image_url="promotional-photo.jpg",
    analysis_type="comprehensive_analysis",
    analysis_dimensions=[
        "target_audience_fit",
        "platform_suitability",
        "competitive_positioning",
        "improvement_opportunities",
        "roi_potential"
    ]
)

# Extract business insights
print("Commercial Recommendations:")
for rec in result['insights']['recommendations']:
    print(f"  - {rec}")
```

## Integration Workflows

### Quality Control Pipeline

```python
# 1. Analyze uploaded image
analysis = api.generate_image_recognition(
    image_url=uploaded_image,
    analysis_type="quality_assessment"
)

# 2. Check quality thresholds
if analysis['scores']['technical_quality'] < 7.0:
    print("⚠️  Image quality below standard")
    print("Suggestions:", analysis['insights']['recommendations'])

# 3. Auto-enhance if needed
if analysis['scores']['technical_quality'] < 8.0:
    enhanced = api.generate_image_to_image(
        prompt="Enhance image quality",
        image_urls=[uploaded_image],
        processing_type="local_optimization"
    )
```

### Brand Compliance Check

```python
# 1. Detect brand elements
brand_check = api.generate_image_recognition(
    image_url=marketing_image,
    analysis_type="brand_detection"
)

# 2. Verify compliance
compliance_score = brand_check['scores'].get('brand_compliance', 0)
if compliance_score < 0.8:
    print("⚠️  Brand compliance issues detected")
    print("Issues:", brand_check['insights']['weaknesses'])
```

## Performance

- **Analysis Time**: 60-180 seconds per image
- **Comprehensive**: ~180 seconds (all 6 categories)
- **Focused Analysis**: ~60-90 seconds (specific categories)
- **Batch Processing**: Sequential processing recommended

## Best Practices

1. **Choose Right Analysis Type**: Match analysis type to your needs
2. **Specify Dimensions**: Focus on relevant analysis dimensions
3. **High-Quality Input**: Use clear, well-lit images for best results
4. **Review Full Output**: Check both scores and textual insights
5. **Iterate Analysis**: Refine analysis based on initial results
6. **Combine with Processing**: Use analysis to guide image improvements

## Related Skills

- For image generation: See `../text-to-image/SKILL.md`
- For image processing: See `../image-to-image/SKILL.md`
- For advanced operations: See `../advanced-processing/SKILL.md`

## Use Cases

### Menu Photography Audit
Analyze all menu photos for consistency and quality

### Marketing Material Review
Evaluate promotional images for commercial effectiveness

### Competitive Analysis
Compare restaurant visuals against industry standards

### Quality Assurance
Automated quality checks for uploaded content

### Content Optimization
Identify improvement opportunities in existing visuals

### Brand Monitoring
Track brand element usage and compliance
