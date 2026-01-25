---
name: Video to GIF Converter
description: Convert video files (MP4, AVI, MOV, etc.) to optimized animated GIFs with customizable quality, resolution, and frame rate. Supports batch conversion and advanced optimization. Use when creating web-friendly animations, social media content, or documentation assets. Requires OpenCV and Pillow.
---

# Video to GIF Converter

## Quick Start

### Method 1: Simple Conversion (Recommended)
```python
import sys
sys.path.append('./.claude/skills/拓展/video-to-gif/scripts')
from video_converter import convert_video_to_gif

result = convert_video_to_gif(
    video_path="input/video.mp4",
    output_path="output/animation.gif"
)

if result["success"]:
    print(f"GIF created: {result['file_path']} ({result['size_mb']:.2f} MB)")
```

### Method 2: Custom Settings
```python
from video_converter import convert_video_to_gif

result = convert_video_to_gif(
    video_path="input/demo.mp4",
    output_path="output/demo.gif",
    fps=15,           # Higher FPS for smoother animation
    scale=0.75,       # 75% of original size
    quality=90        # Higher quality (1-100)
)
```

### Method 3: Batch Conversion
```python
from video_converter import batch_convert

videos = [
    "videos/clip1.mp4",
    "videos/clip2.mp4",
    "videos/clip3.mp4"
]

results = batch_convert(
    video_paths=videos,
    output_dir="output/gifs/",
    fps=10,
    scale=0.5
)

for result in results:
    print(f"{result['filename']}: {result['status']}")
```

## Use Cases

This skill is ideal for:

| Use Case | Description | Recommended Settings |
|----------|-------------|---------------------|
| **Social Media** | Create engaging animations for Twitter, WeChat, etc. | `fps=12, scale=0.6, quality=85` |
| **Documentation** | Add visual demos to README files and docs | `fps=8, scale=0.5, quality=80` |
| **Presentations** | Convert video clips to embed in slides | `fps=15, scale=0.7, quality=90` |
| **Web Content** | Optimize for fast website loading | `fps=10, scale=0.4, quality=75` |
| **Thumbnails** | Create preview animations | `fps=8, scale=0.3, quality=70` |

## Key Features

### 1. **Smart Optimization**
- Automatic frame sampling to reduce file size
- Intelligent resolution scaling
- Adaptive quality compression
- Loop optimization for seamless playback

### 2. **Quality Control**
- Customizable FPS (1-60)
- Scale factor (0.1-1.0)
- Quality level (1-100)
- Original aspect ratio preservation

### 3. **Batch Processing**
- Convert multiple videos at once
- Uniform settings across batch
- Progress tracking
- Error handling per file

### 4. **Format Support**
- **Input**: MP4, AVI, MOV, MKV, WebM, FLV, WMV
- **Output**: GIF (optimized, animated)
- Automatic format detection

## Parameters Reference

### `convert_video_to_gif()`

```python
def convert_video_to_gif(
    video_path: str,          # Required: Path to input video
    output_path: str = None,  # Optional: Output path (auto-generated if None)
    fps: int = 10,            # Target frames per second (1-60)
    scale: float = 0.5,       # Scale factor (0.1-1.0, 0.5 = 50%)
    quality: int = 85         # Quality level (1-100)
) -> dict
```

**Returns**:
```python
{
    "success": True,
    "file_path": "output/animation.gif",
    "size_mb": 9.2,
    "frames": 61,
    "duration_seconds": 6.1,
    "dimensions": "640x360",
    "fps": 10
}
```

### Parameter Guidelines

**FPS (Frames Per Second)**:
- **Low (5-8)**: Documentation, slow animations
- **Medium (10-15)**: Social media, general use
- **High (20-30)**: Smooth motion, presentations

**Scale Factor**:
- **0.3-0.4**: Thumbnails, previews
- **0.5-0.6**: Web content, social media
- **0.7-0.8**: High-quality presentations
- **0.9-1.0**: Maximum quality (large file size)

**Quality**:
- **70-80**: Web-optimized, smaller files
- **85-90**: Balanced quality and size
- **95-100**: Maximum quality, larger files

## Advanced Usage

### Optimize for File Size
```python
# Create a web-optimized GIF (<5MB target)
result = convert_video_to_gif(
    video_path="large_video.mp4",
    fps=8,        # Lower FPS
    scale=0.4,    # Smaller resolution
    quality=75    # Moderate quality
)
```

### High-Quality Conversion
```python
# Create a high-quality GIF for presentations
result = convert_video_to_gif(
    video_path="demo.mp4",
    fps=20,       # Smoother animation
    scale=0.8,    # Larger size
    quality=95    # High quality
)
```

### Batch with Custom Output Names
```python
from pathlib import Path

videos = [
    {"input": "raw/video1.mp4", "output": "gifs/product-demo.gif"},
    {"input": "raw/video2.mp4", "output": "gifs/user-flow.gif"},
    {"input": "raw/video3.mp4", "output": "gifs/feature-preview.gif"}
]

for video in videos:
    convert_video_to_gif(
        video_path=video["input"],
        output_path=video["output"],
        fps=12,
        scale=0.6
    )
```

## Technical Details

### Video Processing Pipeline

```
1. Load Video
   ↓
   Read video metadata (FPS, dimensions, frame count)
   ↓
2. Frame Extraction
   ↓
   Sample frames based on target FPS
   Convert BGR to RGB color space
   ↓
3. Optimization
   ↓
   Resize frames to target dimensions
   Apply quality compression
   ↓
4. GIF Generation
   ↓
   Combine frames with timing
   Enable loop and optimize
   ↓
5. Save Output
   ↓
   Write optimized GIF file
   Return metadata
```

### Performance Characteristics

| Video Length | Original Size | Output Size | Processing Time |
|--------------|---------------|-------------|-----------------|
| 5 seconds    | 1280x720      | 640x360 GIF | ~2-3 seconds    |
| 10 seconds   | 1920x1080     | 960x540 GIF | ~5-7 seconds    |
| 30 seconds   | 1280x720      | 640x360 GIF | ~8-12 seconds   |

**Note**: Processing time varies based on CPU, video resolution, and settings.

## Requirements

### Python Libraries
```bash
pip install opencv-python pillow numpy
```

### System Dependencies
- **OpenCV**: Video decoding and frame extraction
- **Pillow (PIL)**: Image processing and GIF encoding
- **NumPy**: Array operations (installed with OpenCV)

### Compatibility
- **Python**: 3.8+
- **Operating Systems**: macOS, Linux, Windows
- **Video Codecs**: H.264, H.265, VP9, AV1, etc.

## Error Handling

The skill handles common errors gracefully:

```python
result = convert_video_to_gif("video.mp4")

if not result["success"]:
    print(f"Error: {result['error']}")
    # Possible errors:
    # - "Video file not found"
    # - "Failed to open video file"
    # - "No frames extracted from video"
    # - "Invalid parameters"
```

## Best Practices

### File Size Optimization
1. **Start with low settings** and increase if needed
2. **Test different FPS values** - often 10 FPS is sufficient
3. **Use appropriate scale** - 0.5 works for most use cases
4. **Monitor output size** - aim for <10MB for web use

### Quality Guidelines
1. **Don't over-optimize** - balance quality and size
2. **Match use case** - social media vs. presentations
3. **Test on target platform** - some platforms re-compress GIFs
4. **Consider alternatives** - WebP/APNG for better quality

### Workflow Tips
1. **Batch similar videos** with same settings
2. **Keep originals** - non-destructive conversion
3. **Use descriptive names** - include settings in filename
4. **Version outputs** - date stamps for iterations

## Troubleshooting

### Issue: GIF file too large
**Solutions**:
- Reduce FPS (try 8 or 10)
- Decrease scale factor (try 0.4 or 0.5)
- Lower quality setting (try 75-80)
- Trim video length before conversion

### Issue: Poor quality output
**Solutions**:
- Increase quality setting (try 90-95)
- Increase scale factor (try 0.7-0.8)
- Increase FPS (try 15-20)
- Check source video quality

### Issue: Processing takes too long
**Solutions**:
- Reduce input video length
- Lower FPS setting
- Decrease scale factor
- Close other applications

### Issue: Video file not supported
**Solutions**:
- Check video codec (use `ffmpeg -i video.mp4`)
- Convert to MP4 first if needed
- Update OpenCV library
- Verify file is not corrupted

## Examples

See the `examples/` directory for complete examples:
- `basic_conversion.py` - Simple single-file conversion
- `batch_processing.py` - Convert multiple videos
- `custom_settings.py` - Advanced parameter tuning
- `web_optimization.py` - Optimize for web delivery

## Integration with Other Skills

### With Screenshot Skill
```python
# Combine video conversion with screenshot capture
from video_converter import convert_video_to_gif

# Convert architectural walkthrough to GIF
result = convert_video_to_gif(
    video_path="output/视频生成测试/Z4-建筑动画AIGC助手/walkthrough.mp4",
    output_path="output/gifs/walkthrough.gif",
    fps=12,
    scale=0.6
)
```

### With Office Skills
```python
# Embed GIF in documents
from video_converter import convert_video_to_gif
from word_generator import WordDocumentBuilder

# Convert video
gif_result = convert_video_to_gif("demo.mp4")

# Add to Word document
builder = WordDocumentBuilder()
builder.add_title("Product Demo")
builder.add_paragraph("Feature demonstration:")
builder.add_image(gif_result["file_path"], width_inches=5)
builder.save("output/demo-doc.docx")
```

## Version History

- **v1.0.0** (2025-10-29) - Initial release
  - Core video to GIF conversion
  - Batch processing support
  - Quality optimization
  - Comprehensive error handling

## References

- **SKILL.md** (this file) - Quick start and usage guide
- **reference.md** - Technical implementation details
- **scripts/video_converter.py** - Core conversion engine
- **examples/** - Working code examples

---

**Created by**: ZTL数智化作战中心
**Created date**: 2025-10-29
**Version**: v1.0.0
**Status**: ✅ Production Ready

**Use cases**: Video conversion, animated GIFs, social media content, documentation, web optimization
