# Restaurant Industry Export Guide

Specialized export configurations and workflows for restaurant design assets.

## Table of Contents

- [Dish Image Export](#dish-image-export)
- [Menu PDF Export](#menu-pdf-export)
- [Icon and Logo Export](#icon-and-logo-export)
- [Social Media Export](#social-media-export)
- [Multi-Store Batch Export](#multi-store-batch-export)

---

## Dish Image Export

### High-Resolution Display (高清展示)

**Use case**: Menu boards, website galleries, app listings

**Configuration**:
```python
DISH_IMAGE_CONFIG = {
    "format": "png",
    "scale": 2.0,              # 2x resolution for high-DPI screens
    "contents_only": True,     # Exclude borders
    "use_absolute_bounds": False
}
```

**Export**:
```python
from scripts.figma_image_client import FigmaImageClient

async with FigmaImageClient() as client:
    result = await client.export_images(
        file_key="menu_design",
        node_ids=dish_node_ids,
        **DISH_IMAGE_CONFIG
    )
```

**Batch script**:
```bash
python scripts/batch_export.py \
  --file-key menu_design \
  --pattern "菜品" \
  --format png \
  --scale 2.0 \
  --contents-only \
  --output-dir ./dishes
```

---

## Menu PDF Export

### Print-Ready PDF (印刷级)

**Use case**: Physical menus, promotional flyers

**Configuration**:
```python
MENU_PDF_CONFIG = {
    "format": "pdf",
    "scale": 1.0,
    "contents_only": False,    # Include full bounds for print
}
```

**Export**:
```python
async with FigmaImageClient() as client:
    result = await client.export_images(
        file_key="menu_design",
        node_ids=["menu_page_1", "menu_page_2"],
        **MENU_PDF_CONFIG
    )

    for node_id, pdf_url in result['images'].items():
        print(f"PDF ready: {pdf_url}")
        print("⚠️  Link valid for 30 minutes")
```

**Download script**:
```bash
python scripts/export_and_save.py \
  --file-key menu_design \
  --node-ids "menu_page_1,menu_page_2" \
  --format pdf \
  --output-dir ./print-ready
```

---

## Icon and Logo Export

### Vector Icons (SVG)

**Use case**: Website icons, app UI, scalable branding

**Configuration**:
```python
ICON_SVG_CONFIG = {
    "format": "svg",
    "svg_outline_text": True,      # Convert text to paths
    "svg_include_id": False,       # Reduce file size
    "svg_simplify_stroke": True,   # Simplify strokes
}
```

**Export**:
```python
async with FigmaImageClient() as client:
    result = await client.export_images(
        file_key="brand_assets",
        node_ids=icon_node_ids,
        **ICON_SVG_CONFIG
    )
```

**Use cases**:
- **Website icons**: Direct SVG embedding
- **App icons**: Convert to platform-specific formats
- **Print logos**: Scalable without quality loss

---

## Social Media Export

### WeChat/Weibo Posts (JPG Compressed)

**Use case**: Social media posts, WeChat articles

**Configuration**:
```python
SOCIAL_MEDIA_CONFIG = {
    "format": "jpg",
    "scale": 1.5,              # Medium resolution
    "contents_only": True,
}
```

**Multi-platform export**:
```python
# WeChat Moments: 1080x1080
# Weibo: 1200x628
# Douyin: 1080x1920

async with FigmaImageClient() as client:
    # WeChat
    wechat_result = await client.export_images(
        file_key="social_posts",
        node_ids=["wechat_post_1"],
        format="jpg",
        scale=1.5
    )

    # Weibo
    weibo_result = await client.export_images(
        file_key="social_posts",
        node_ids=["weibo_post_1"],
        format="jpg",
        scale=1.2
    )
```

**Batch script**:
```bash
# Export all social media posts
python scripts/batch_export.py \
  --file-key social_posts \
  --pattern "推广|促销|活动" \
  --format jpg \
  --scale 1.5 \
  --output-dir ./social-media
```

---

## Multi-Store Batch Export

### Scenario: Export dish images for 10 stores

**Problem**: Each store needs the same dishes exported with consistent quality

**Solution**: Batch export with organized output

```python
import asyncio
from scripts.figma_image_client import FigmaImageClient

STORES = {
    "总店": "file_key_1",
    "分店A": "file_key_2",
    "分店B": "file_key_3",
    # ... 10 stores
}

async def export_all_stores():
    async with FigmaImageClient() as client:
        for store_name, file_key in STORES.items():
            # Find dish nodes
            file_data = await client.get_file(file_key)
            dish_nodes = find_nodes_by_pattern(file_data, r"菜品")
            dish_ids = [n['id'] for n in dish_nodes]

            # Export
            result = await client.export_images(
                file_key=file_key,
                node_ids=dish_ids,
                format="png",
                scale=2.0,
                contents_only=True
            )

            # Save organized by store
            save_dir = f"./exports/{store_name}"
            for node_id, url in result['images'].items():
                # Download and save
                await download_image(url, save_dir)

            print(f"✓ {store_name}: {len(dish_ids)} dishes exported")

asyncio.run(export_all_stores())
```

**Simplified script**:
```bash
# Use configuration file
cat > stores.json <<EOF
{
  "总店": "file_key_1",
  "分店A": "file_key_2",
  "分店B": "file_key_3"
}
EOF

python scripts/multi_store_export.py \
  --config stores.json \
  --pattern "菜品" \
  --format png \
  --scale 2.0 \
  --output-base ./store-exports
```

---

## Seasonal Theme Export

### Export seasonal promotional materials

**Spring Campaign**:
```bash
python scripts/batch_export.py \
  --file-key spring_2024 \
  --pattern "春季|spring" \
  --format png \
  --scale 2.0 \
  --output-dir ./seasons/spring
```

**Multi-season export**:
```python
SEASONS = {
    "spring": {"pattern": r"春季", "output": "./seasons/spring"},
    "summer": {"pattern": r"夏季", "output": "./seasons/summer"},
    "autumn": {"pattern": r"秋季", "output": "./seasons/autumn"},
    "winter": {"pattern": r"冬季", "output": "./seasons/winter"},
}

async with FigmaImageClient() as client:
    for season, config in SEASONS.items():
        # Export seasonal assets
        ...
```

---

## Quality Checklist

Before exporting for production:

### Dish Images
- [ ] Scale: 2.0x or higher for retina displays
- [ ] Format: PNG for transparency, JPG if no transparency
- [ ] Contents only: Enabled to remove padding
- [ ] File naming: Consistent and descriptive

### Menu PDFs
- [ ] Scale: 1.0 (actual size)
- [ ] Format: PDF
- [ ] Contents only: Disabled (include full page)
- [ ] Verify: Check print dimensions match design

### Icons/Logos
- [ ] Format: SVG for scalability
- [ ] Text to outlines: Enabled for consistency
- [ ] Simplify strokes: Enabled to reduce file size
- [ ] Test: Verify at multiple sizes (16px - 512px)

### Social Media
- [ ] Platform requirements: Match exact dimensions
- [ ] Format: JPG for smaller file size
- [ ] Scale: Appropriate for platform (1.5x recommended)
- [ ] Preview: Check appearance on actual platform

---

## Troubleshooting

### Images not exporting
**Symptom**: Empty `images` object in response

**Solutions**:
1. Verify node IDs exist: `python scripts/find_nodes.py --file-key X`
2. Check nodes are visible (not hidden layers)
3. Ensure nodes have renderable content

### Image quality issues
**Symptom**: Blurry or pixelated exports

**Solutions**:
1. Increase scale: `scale=2.0` or `scale=3.0`
2. Use PNG instead of JPG for sharp edges
3. Use SVG for vector content (icons, logos)

### File size too large
**Symptom**: PNG files >5MB

**Solutions**:
1. Use JPG format: `format="jpg"`
2. Reduce scale if appropriate
3. Enable `contents_only=True` to crop whitespace

---

For complete API reference, see [reference.md](reference.md).
