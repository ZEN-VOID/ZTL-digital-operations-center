---
name: Figma Image Export
description: Export Figma nodes as PNG, JPG, SVG, or PDF images with quality control, batch export, multi-size generation. Use when exporting design assets, generating images from Figma, or when user mentions image export, asset generation, download images, or format conversion. Requires Figma API token.
---

# Figma Image Export

## Quick Start

### Export single node as PNG
```python
import sys
sys.path.append('./.claude/skills/figma/image-export-v2/scripts')
from figma_image_client import FigmaImageClient

async with FigmaImageClient() as client:
    result = await client.export_images(
        file_key="YOUR_FILE_KEY",
        node_ids=["123:456"],
        format="png",
        scale=2.0
    )
    image_url = result['images']['123:456']
    print(f"Download: {image_url}")
```

### Export multiple nodes
```python
async with FigmaImageClient() as client:
    result = await client.export_images(
        file_key="YOUR_FILE_KEY",
        node_ids=["123:456", "789:012", "345:678"],
        format="png",
        scale=2.0
    )
    for node_id, url in result['images'].items():
        print(f"Node {node_id}: {url}")
```

### Download and save images
```bash
# Using bundled script
python scripts/export_and_save.py \
  --file-key YOUR_FILE_KEY \
  --node-ids "123:456,789:012" \
  --format png \
  --scale 2.0 \
  --output-dir ./exports
```

## Documentation

- **[API Reference](reference.md)**: Complete API documentation for all export formats and options
- **[Restaurant Industry Guide](restaurant-guide.md)**: Specialized configurations for menu design, dish images, and promotional materials

## Bundled Scripts

- **`scripts/figma_image_client.py`**: Core image export client
- **`scripts/export_and_save.py`**: Export images and save to local files
- **`scripts/batch_export.py`**: Batch export with progress tracking
- **`scripts/multi_size_export.py`**: Export multiple sizes for responsive design

## Format Comparison

| Format | Use Case | Quality | File Size | Scalable |
|--------|----------|---------|-----------|----------|
| PNG | Web graphics, transparency | Lossless | Large | No |
| JPG | Photos, no transparency | Lossy | Medium | No |
| SVG | Icons, logos, print | Vector | Small | Yes |
| PDF | Print documents | Vector/Raster | Medium | Yes |

## Common Tasks

### Export for different devices
```bash
# Mobile, tablet, desktop sizes
python scripts/multi_size_export.py \
  --file-key YOUR_FILE_KEY \
  --node-id "123:456" \
  --sizes "mobile:1.0,tablet:1.5,desktop:2.0"
```

### Batch export with organized naming
```bash
python scripts/batch_export.py \
  --file-key YOUR_FILE_KEY \
  --pattern "菜品" \
  --output-dir ./dish-images \
  --format png \
  --scale 2.0
```

## Requirements

```bash
pip install httpx backoff pydantic-settings

export FIGMA_API_TOKEN=your_token_here
```

## Related Skills

- For file management: See `../file-management-v2/SKILL.md`
- For batch operations: See `../batch-replace-v2/SKILL.md`
