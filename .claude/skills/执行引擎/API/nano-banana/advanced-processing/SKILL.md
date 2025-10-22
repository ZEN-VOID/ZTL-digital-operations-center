---
name: AIGC Advanced Image Processing
description: Professional restaurant image processing with 6 advanced capabilities - smart repair, structure control, multi-image fusion, character consistency, design iteration, and super-resolution enhancement. Use when performing complex image operations, creating brand IP, or when user mentions advanced editing, image fusion, upscaling, or professional post-production. Requires OpenRouter API key.
---

# AIGC Advanced Image Processing

## Quick Start

### Method 1: Use Skill Convenience Function (Recommended)
```python
import sys
sys.path.append('./.claude/skills/aigc/advanced-processing/scripts')
from advanced_processing_api import repair_image, upscale_image

# Smart repair
result = repair_image(
    image_url="photo-with-watermark.jpg",
    repair_prompt="Remove watermark from bottom-right corner",
    repair_type="watermark_removal"
)

if result["success"]:
    print(f"Repaired: {result['image_paths']}")

# Upscale image
result = upscale_image(
    source_image="low-res-photo.jpg",
    target_resolution="4K",
    enhancement_type="intelligent_upscaling"
)
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
result = api.generate_smart_repair(
    image_url="photo-with-watermark.jpg",
    repair_prompt="Remove watermark from bottom-right corner",
    repair_type="watermark_removal"
)
```

### Method 3: Execute from JSON Plan
```python
from advanced_processing_api import execute_plan_from_file

result = execute_plan_from_file(
    'api/plans/e4-smart-repair/your-task.json'
)
```

## 6 Advanced Capabilities

This skill integrates 6 professional image processing engines:

### 1. Smart Repair & Extension (E4)
**Remove unwanted elements and extend scenes**

| Repair Type | Code | Use Case |
|-------------|------|----------|
| Watermark Removal | `watermark_removal` | Remove watermarks, logos, stamps |
| Object Removal | `object_removal` | Remove unwanted objects, people |
| Background Repair | `background_repair` | Fix backgrounds, remove clutter |
| Inpainting | `inpainting` | Fill missing regions naturally |
| Outpainting | `outpainting` | Extend image boundaries, add context |

**Quick Example:**
```python
result = api.generate_smart_repair(
    image_url="photo.jpg",
    repair_prompt="Remove table stains and clutter",
    repair_type="object_removal"
)
```

### 2. Structure Control (E5)
**Generate with precise structural guidance**

| Control Type | Code | Use Case |
|--------------|------|----------|
| Pose Control | `pose_control` | Control human/object poses |
| Depth Control | `depth_control` | Control spatial depth, 3D structure |
| Edge Control | `edge_control` | Control outlines, boundaries |
| Layout Control | `layout_control` | Control element positioning |

**Quick Example:**
```python
result = api.generate_structure_control(
    reference_image="pose-reference.jpg",
    target_prompt="Chef in same pose with different background",
    control_type="pose_control",
    control_strength=0.8
)
```

### 3. Multi-Image Fusion (E6)
**Combine multiple images creatively**

| Fusion Type | Code | Use Case |
|-------------|------|----------|
| Creative Combination | `creative_combination` | Artistic multi-image composites |
| Brand Integration | `brand_integration` | Merge brand elements seamlessly |
| Scene Composition | `scene_composition` | Compose complete scenes |
| Element Collage | `element_collage` | Extract and combine elements |

**Quick Example:**
```python
result = api.generate_image_fusion(
    source_images=["dish1.jpg", "dish2.jpg", "dish3.jpg"],
    fusion_prompt="Create unified menu header with all dishes",
    fusion_type="creative_combination"
)
```

### 4. Character Consistency (E7)
**Generate consistent brand IP/mascots**

| Character Type | Code | Use Case |
|----------------|------|----------|
| Brand Mascot | `brand_mascot` | Restaurant mascots, logos |
| Chef Character | `chef_character` | Chef personas, spokespeople |
| Spokesperson | `spokesperson` | Brand ambassadors |
| Product IP | `product_ip` | Product characters, icons |

**Quick Example:**
```python
result = api.generate_character_consistency(
    character_reference="mascot-design.jpg",
    scene_prompt="Mascot welcoming customers at entrance",
    character_type="brand_mascot",
    consistency_level=5
)
```

### 5. Design Iteration (E8)
**Refine designs progressively**

| Iteration Type | Code | Use Case |
|----------------|------|----------|
| Local Optimization | `local_optimization` | Improve specific areas |
| Progressive Improvement | `progressive_improvement` | Step-by-step enhancement |
| Feedback Response | `feedback_response` | Address client feedback |
| Aesthetic Enhancement | `aesthetic_enhancement` | Polish visual aesthetics |

**Quick Example:**
```python
result = api.generate_design_iteration(
    current_version="poster-v1.jpg",
    feedback="Make logo larger, brighten colors, add festive elements",
    iteration_type="feedback_response",
    iteration_goals=["increase_visibility", "enhance_festivity"]
)
```

### 6. Super-Resolution (E9)
**Upscale and enhance image quality**

| Enhancement Type | Code | Use Case |
|------------------|------|----------|
| Intelligent Upscaling | `intelligent_upscaling` | AI-powered resolution boost |
| Detail Enhancement | `detail_enhancement` | Sharpen details, textures |
| Texture Optimization | `texture_optimization` | Enhance material quality |
| Noise Reduction | `noise_reduction` | Remove noise, grain |

**Quick Example:**
```python
result = api.generate_super_resolution(
    source_image="menu-photo.jpg",
    target_resolution="4K",
    enhancement_type="intelligent_upscaling",
    enhancement_strength=0.8
)
```

## Documentation

- **[API Reference](reference.md)**: Complete API documentation for all 6 capabilities
- **[Capability Guide](capabilities.md)**: Detailed guide for each processing engine
- **[Examples](examples.md)**: Restaurant industry workflows and use cases
- **[Integration Guide](integration.md)**: Multi-capability workflows

## Bundled Scripts

- **`scripts/advanced_processing_api.py`**: Skill-specific convenience functions
- **`../_shared/banana_api_core.py`**: Core NanoBananaAPI client (shared library)
- **`../_shared/plan_executor.py`**: JSON plan execution utility (shared library)
- **`../_shared/config.py`**: Unified configuration management

## Common Workflows

### Professional Menu Photo Pipeline
```python
# Step 1: Remove unwanted elements
step1 = api.generate_smart_repair(
    image_url="raw-photo.jpg",
    repair_prompt="Remove table clutter and background distractions",
    repair_type="object_removal"
)

# Step 2: Optimize lighting and colors
step2 = api.generate_image_to_image(
    prompt="Enhance food colors and lighting",
    image_urls=[step1["image_paths"][0]],
    processing_type="local_optimization"
)

# Step 3: Upscale to print quality
step3 = api.generate_super_resolution(
    source_image=step2["image_paths"][0],
    target_resolution="4K",
    enhancement_type="intelligent_upscaling"
)

print(f"Final output: {step3['image_paths'][0]}")
```

### Brand IP Creation
```python
# Step 1: Generate initial character
character = api.generate_text_to_image(
    prompt="Cute dumpling mascot with chef hat",
    design_type="6-icon"
)

# Step 2: Create consistent variations
scenes = [
    "Mascot cooking in kitchen",
    "Mascot serving customers",
    "Mascot on restaurant signage"
]

variations = []
for scene in scenes:
    result = api.generate_character_consistency(
        character_reference=character["image_paths"][0],
        scene_prompt=scene,
        character_type="brand_mascot",
        consistency_level=5
    )
    variations.append(result)
```

### Marketing Material Enhancement
```python
# Step 1: Analyze current design
analysis = api.generate_image_recognition(
    image_url="current-poster.jpg",
    analysis_type="quality_assessment"
)

# Step 2: Apply feedback-based iteration
improved = api.generate_design_iteration(
    current_version="current-poster.jpg",
    feedback=f"Based on analysis: {analysis['insights']['recommendations']}",
    iteration_type="feedback_response"
)

# Step 3: Upscale for print
final = api.generate_super_resolution(
    source_image=improved["image_paths"][0],
    target_resolution="4K"
)
```

## Requirements

```bash
# Python dependencies
pip install requests pydantic python-dotenv pillow

# Environment variables
export OPENROUTER_API_KEY=your_key_here
```

## Output Structure

Results are organized by capability:
```
output/
  images/
    e4-smart-repair/
      [repair_type]/
        repaired_20250120_103000_1.png
    e5-structure-control/
      [control_type]/
        controlled_20250120_103000_1.png
    e6-creative-combination/
      [fusion_type]/
        fused_20250120_103000_1.png
    e7-character-consistency/
      [character_type]/
        character_20250120_103000_1.png
    e8-design-iteration/
      [iteration_type]/
        iterated_20250120_103000_1.png
    e9-super-resolution/
      [enhancement_type]/
        enhanced_20250120_103000_1.png
```

## Error Handling

Common errors:
- **Image not accessible**: Check file paths
- **Insufficient resolution**: Provide higher quality input
- **Complex repair failed**: Break into smaller steps
- **Character inconsistency**: Adjust consistency_level parameter
- **Processing timeout**: Reduce image size or complexity

See [reference.md](reference.md) for detailed troubleshooting.

## Quality Standards

### Smart Repair
- **Seamless Integration**: No visible repair marks
- **Natural Fill**: Contextually appropriate content
- **Quality Preservation**: Maintains original image quality

### Structure Control
- **Precision**: Accurate structural adherence
- **Natural Fusion**: Structure and content harmonize
- **Flexibility**: Adjustable control strength

### Multi-Image Fusion
- **Seamless Blending**: No visible seams
- **Unified Lighting**: Consistent light sources
- **Style Coherence**: Harmonized visual style

### Character Consistency
- **Feature Stability**: Consistent character features
- **Identity Recognition**: Strong character identity
- **Scene Adaptation**: Natural in various contexts

### Design Iteration
- **Clear Improvement**: Visible quality enhancement
- **Progressive**: Logical step-by-step refinement
- **Goal-Oriented**: Addresses specific objectives

### Super-Resolution
- **Resolution Boost**: Significant size increase
- **Detail Enhancement**: Natural detail addition
- **Print Quality**: Professional output standards

## Performance

| Capability | Processing Time | Complexity |
|------------|----------------|------------|
| Smart Repair | 60-120 sec | Medium-High |
| Structure Control | 60-120 sec | High |
| Multi-Image Fusion | 90-180 sec | High |
| Character Consistency | 90-150 sec | High |
| Design Iteration | 60-120 sec | Medium |
| Super-Resolution | 60-90 sec | Medium |

## Advanced Features

### Multi-Capability Workflows

Chain multiple capabilities for complex operations:

```python
# Complete restaurant photo production pipeline
def complete_production_pipeline(raw_photo):
    # 1. Clean up
    cleaned = api.generate_smart_repair(
        image_url=raw_photo,
        repair_prompt="Remove all unwanted elements",
        repair_type="object_removal"
    )

    # 2. Optimize
    optimized = api.generate_image_to_image(
        prompt="Enhance colors and lighting",
        image_urls=[cleaned["image_paths"][0]],
        processing_type="local_optimization"
    )

    # 3. Add brand elements (if needed)
    if needs_branding:
        branded = api.generate_image_fusion(
            source_images=[optimized["image_paths"][0], "brand-elements.png"],
            fusion_prompt="Integrate brand logo naturally",
            fusion_type="brand_integration"
        )
        current = branded
    else:
        current = optimized

    # 4. Upscale to final quality
    final = api.generate_super_resolution(
        source_image=current["image_paths"][0],
        target_resolution="4K",
        enhancement_type="intelligent_upscaling"
    )

    return final["image_paths"][0]
```

### Capability Selection Guide

**When to use Smart Repair:**
- Remove watermarks, unwanted objects
- Fix damaged or incomplete images
- Extend image boundaries

**When to use Structure Control:**
- Generate variations with same structure
- Control specific compositional elements
- Maintain spatial relationships

**When to use Multi-Image Fusion:**
- Combine multiple sources
- Create composite designs
- Merge brand elements

**When to use Character Consistency:**
- Create brand mascots/IP
- Generate consistent characters
- Multi-scene character deployment

**When to use Design Iteration:**
- Refine existing designs
- Address client feedback
- Progressive quality improvement

**When to use Super-Resolution:**
- Upscale for print/large format
- Enhance details and sharpness
- Improve low-quality sources

## Integration Points

### With Text-to-Image
Generate base → Repair/Enhance → Upscale

### With Image-to-Image
Modify → Iterate → Finalize

### With Image Recognition
Analyze → Process → Validate

## Best Practices

1. **Understand Capabilities**: Choose right tool for the task
2. **Quality Input**: Better input = better output
3. **Iterative Approach**: Complex tasks need multiple steps
4. **Preserve Versions**: Keep intermediate results
5. **Test Parameters**: Adjust strength/level for optimal results
6. **Batch Wisely**: Group similar operations
7. **Monitor Performance**: Track processing times
8. **Validate Output**: Always verify quality

## Related Skills

- For basic generation: See `../text-to-image/SKILL.md`
- For basic processing: See `../image-to-image/SKILL.md`
- For analysis: See `../image-recognition/SKILL.md`

## Use Cases

### Restaurant Marketing
- Clean up food photos for menus
- Create consistent brand mascot
- Upscale for billboard printing

### Brand Development
- Generate IP character variations
- Maintain character consistency across media
- Create brand visual system

### Content Production
- Batch process menu photos
- Progressive design refinement
- Quality enhancement pipeline

### Creative Campaigns
- Multi-image creative composites
- Artistic style applications
- Campaign visual unification

### Quality Control
- Repair damaged images
- Enhance low-quality photos
- Meet print standards
