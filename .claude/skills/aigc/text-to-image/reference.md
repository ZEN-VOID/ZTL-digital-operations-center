# AIGC Text-to-Image API Reference

## NanoBananaAPI Class

### Core Method: `generate_text_to_image()`

Generate restaurant design images from text descriptions.

```python
def generate_text_to_image(
    prompt: str,
    design_type: Optional[str] = None,
    style: str = "professional",
    **kwargs
) -> Dict[str, Any]
```

#### Parameters

- **prompt** (str, required): Text description of desired design
  - Should be detailed and specific
  - Include design elements, colors, mood, style
  - English recommended for best results

- **design_type** (str, optional): Design type code
  - Options: `1-poster`, `2-menu`, `3-storefront`, `4-panel`, `5-magazine`, `6-icon`, `7-typography`, `8-main-image`, `9-detail`
  - Default: `8-main-image` (food photography)
  - Determines aspect ratio and quality standards

- **style** (str, optional): Design style preference
  - Options: `professional`, `creative`, `minimalist`, `luxurious`, `traditional`
  - Default: `professional`

- **kwargs**: Additional parameters
  - `temperature` (float): Model creativity (0.0-1.0, default: 0.7)
  - `max_tokens` (int): Maximum response tokens (default: 4000)

#### Return Value

Returns a dictionary with the following structure:

```python
{
    "success": bool,           # Whether generation succeeded
    "task_id": str,            # Unique task identifier (UUID)
    "message": str,            # Success/error message
    "images": List[str],       # Base64 encoded images
    "image_paths": List[str],  # Saved file paths
    "prompt_file": str,        # Saved prompt metadata file
    "processing_time": float,  # Time taken in seconds
    "design_type": str,        # Design type used

    # Error fields (if success=False)
    "error": str,              # Error message
    "details": str             # Error details
}
```

#### Example Usage

**Basic Usage:**
```python
from banana_api_core import NanoBananaAPI

api = NanoBananaAPI()
result = api.generate_text_to_image(
    prompt="Create a modern hotpot restaurant poster with red festive colors",
    design_type="1-poster"
)

if result["success"]:
    print(f"Generated {len(result['image_paths'])} images:")
    for path in result['image_paths']:
        print(f"  - {path}")
else:
    print(f"Error: {result['error']}")
```

**Advanced Usage with Custom Parameters:**
```python
result = api.generate_text_to_image(
    prompt="Elegant Japanese restaurant menu with cherry blossom elements",
    design_type="2-menu",
    style="minimalist",
    temperature=0.8,  # More creative
    max_tokens=5000
)
```

## JSON Execution Plan Method

### `execute_from_plan()`

Execute generation from a JSON configuration file.

```python
def execute_from_plan(plan_file_path: str) -> Dict[str, Any]
```

#### JSON Plan Structure

```json
{
  "agent_id": "E1",
  "task_description": "Generate restaurant design from text",
  "input_data": {
    "text_prompt": "Detailed text description",
    "design_type": "1-poster",
    "design_requirements": [
      "High visual impact",
      "Brand consistent",
      "Commercial quality"
    ]
  },
  "output_settings": {
    "save_path": "output/images/e1-text-to-image/",
    "format": "png"
  },
  "metadata": {
    "created_at": "2025-01-20T10:30:00",
    "created_by": "User or Agent Name",
    "version": "1.0"
  }
}
```

#### Using plan_executor.py Script

```bash
# Execute a specific plan
python .claude/skills/aigc/_shared/plan_executor.py \
  --plan api/plans/e1-text-to-image/my-task.json

# With verbose output
python .claude/skills/aigc/_shared/plan_executor.py \
  --plan api/plans/e1-text-to-image/my-task.json \
  --verbose
```

## Design Type Specifications

### 1. Poster Design (1-poster)
- **Aspect Ratio**: 2:3 vertical
- **DPI**: 300 (print ready)
- **Best for**: Grand openings, promotions, events
- **Corpus Weight**: visual-composition(0.9) + color-theory(0.8) + design-masters(0.7)

### 2. Menu Design (2-menu)
- **Aspect Ratio**: 3:4 vertical
- **DPI**: 300 (print ready)
- **Best for**: Restaurant menus, price lists
- **Corpus Weight**: layout-principles(0.9) + typography-fundamentals(0.8) + restaurant-design-corpus(0.9)

### 3. Storefront Design (3-storefront)
- **Aspect Ratio**: 16:9 horizontal
- **DPI**: Construction grade
- **Best for**: Store signage, exterior design
- **Corpus Weight**: aesthetic-principles(0.8) + visual-texture(0.7) + restaurant-design-corpus(0.9)

### 4. Panel Design (4-panel)
- **Aspect Ratio**: 4:3 horizontal
- **DPI**: 300 (display quality)
- **Best for**: Wall menu boards, hanging panels
- **Corpus Weight**: layout-principles(0.9) + typography-fundamentals(0.8) + visual-composition(0.7)

### 5. Magazine/Brochure (5-magazine)
- **Aspect Ratio**: A4 standard
- **DPI**: 300 (high-end print)
- **Best for**: Brand brochures, catalogs
- **Corpus Weight**: design-masters(0.8) + humanistic-values(0.9) + advanced-techniques(0.7)

### 6. Icon Design (6-icon)
- **Aspect Ratio**: 1:1 square
- **DPI**: Vector quality (scalable)
- **Best for**: Logos, brand icons
- **Corpus Weight**: aesthetic-principles(0.9) + visual-composition(0.8) + advanced-techniques(0.7)

### 7. Typography Design (7-typography)
- **Aspect Ratio**: Horizontal
- **DPI**: High resolution vector
- **Best for**: Brand wordmarks, signage text
- **Corpus Weight**: typography-fundamentals(0.9) + humanistic-values(0.8) + design-masters(0.7)

### 8. Main Image Photography (8-main-image)
- **Aspect Ratio**: 1:1 or 16:9
- **DPI**: High resolution
- **Best for**: Food photography, product shots
- **Corpus Weight**: visual-texture(0.9) + color-theory(0.8) + advanced-techniques(0.8)

### 9. Detail Page (9-detail)
- **Aspect Ratio**: 9:16 vertical
- **DPI**: High resolution mobile
- **Best for**: Mobile detail pages, social media
- **Corpus Weight**: layout-principles(0.9) + visual-composition(0.8) + thematic-concepts(0.7)

## Prompt Engineering Best Practices

### Structure Your Prompts

**Good Prompt Structure:**
```
[Main Subject] + [Style/Mood] + [Key Elements] + [Technical Requirements]
```

**Example:**
```
Chinese hotpot restaurant poster + festive celebratory atmosphere +
steaming hotpot ingredients and red lanterns +
commercial photography quality with high visual impact
```

### Corpus Integration

The API automatically integrates professional design corpus from `library/prompts/`:

- `aesthetic-principles.json`: Art theory and aesthetics
- `color-theory.json`: Color psychology and schemes
- `design-masters.json`: Master designer styles
- `layout-principles.json`: Layout and composition
- `restaurant-design-corpus.json`: Restaurant industry standards
- `typography-fundamentals.json`: Typography principles
- `visual-composition.json`: Visual balance and composition
- `visual-texture.json`: Texture and material rendering
- `thematic-concepts.json`: Creative themes
- `humanistic-values.json`: Emotional expression
- `advanced-techniques.json`: Advanced design techniques

The corpus is automatically weighted based on design type.

## Error Handling

### Common Errors and Solutions

**1. Missing API Key**
```python
Error: "OPENROUTER_API_KEY not found"
Solution: Set environment variable
  export OPENROUTER_API_KEY=sk-or-v1-xxx...
```

**2. Invalid Design Type**
```python
Error: "Invalid design_type"
Solution: Use one of: 1-poster, 2-menu, 3-storefront, 4-panel,
         5-magazine, 6-icon, 7-typography, 8-main-image, 9-detail
```

**3. API Rate Limit**
```python
Error: "Rate limit exceeded"
Solution: Automatic retry with backoff, or wait before retry
```

**4. Model Timeout**
```python
Error: "Request timeout"
Solution: Simplify prompt or increase timeout parameter
```

### Retry Logic

The API includes automatic retry with exponential backoff:

```python
# Automatic retry for transient errors
max_retries = 3
timeout = 120  # seconds
```

## Performance Optimization

### Generation Time

- **Simple designs**: 30-60 seconds
- **Complex designs**: 60-120 seconds
- **High-detail designs**: 120-180 seconds

### Batch Processing

For multiple images, use separate API calls:

```python
designs = [
    {"prompt": "Poster 1", "design_type": "1-poster"},
    {"prompt": "Poster 2", "design_type": "1-poster"},
]

results = []
for design in designs:
    result = api.generate_text_to_image(**design)
    results.append(result)
```

## Output Quality Control

### Automatic Checks

The API performs automatic quality validation:

1. **Resolution check**: Ensures minimum DPI requirements
2. **Format validation**: Verifies PNG output integrity
3. **Prompt recording**: Saves full prompt metadata
4. **Version tracking**: Records generation parameters

### Quality Standards

- **Commercial Use**: All outputs meet commercial quality standards
- **Print Ready**: 300 DPI minimum for print designs
- **Color Accuracy**: Professional color management
- **Brand Consistency**: Integrated with restaurant industry standards

## Advanced Features

### Custom Model Configuration

```python
# Available in JSON plan format
{
  "model_config": {
    "temperature": 0.8,
    "max_tokens": 5000,
    "top_p": 0.95
  }
}
```

### Multi-Language Support

The API supports prompts in multiple languages, but English prompts generally produce better results:

```python
# English (recommended)
prompt = "Modern hotpot restaurant poster with festive atmosphere"

# Chinese (supported)
prompt = "现代火锅店海报，喜庆氛围"
```

## Integration Examples

### Integration with Claude Agent

The intelligent agent (V3-AIGC文生图设计师) uses this skill:

1. Agent receives user request
2. Analyzes design type and requirements
3. Generates execution plan
4. Calls this skill via `execute_from_plan()`
5. Returns results to user

### Custom Workflow

```python
# 1. Analyze user input
design_type = analyze_design_type(user_input)

# 2. Generate prompt
enhanced_prompt = build_professional_prompt(
    user_input,
    design_type,
    corpus_weights
)

# 3. Generate image
result = api.generate_text_to_image(
    prompt=enhanced_prompt,
    design_type=design_type
)

# 4. Post-process if needed
if result["success"]:
    optimize_output(result["image_paths"])
```

## Troubleshooting

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now API calls will show detailed logs
result = api.generate_text_to_image(...)
```

### Validate Plans

Check JSON plan validity:

```bash
python -m json.tool api/plans/e1-text-to-image/my-task.json
```

### Test API Connection

```python
# Quick connection test
api = NanoBananaAPI()
result = api.generate_text_to_image(
    prompt="Test connection",
    design_type="6-icon"
)
print(f"API Status: {'OK' if result['success'] else 'ERROR'}")
```

## Support

For issues or questions:

1. Check [examples.md](examples.md) for common use cases
2. Review [design-types.md](design-types.md) for type-specific guidance
3. Consult main API documentation: `.claude/skills/aigc/_shared/README.md`
4. Check agent documentation: `.claude/agents/创意组/V3-AIGC文生图设计师.md`
