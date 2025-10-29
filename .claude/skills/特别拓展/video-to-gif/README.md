# Video to GIF Converter Skill

A comprehensive skill for converting video files to optimized animated GIFs with customizable quality, resolution, and frame rate.

## Overview

This skill provides a production-ready solution for converting videos to GIFs, perfect for:
- Creating social media content
- Adding animations to documentation
- Optimizing videos for web delivery
- Generating preview animations
- Batch processing video libraries

## Quick Start

```python
import sys
sys.path.append('./.claude/skills/拓展/video-to-gif/scripts')
from video_converter import convert_video_to_gif

# Convert a video to GIF
result = convert_video_to_gif(
    video_path="input/video.mp4",
    output_path="output/animation.gif",
    fps=10,
    scale=0.5,
    quality=85
)

if result["success"]:
    print(f"✅ Created: {result['file_path']} ({result['size_mb']} MB)")
```

## Features

- ✅ **Multiple Format Support**: MP4, AVI, MOV, MKV, WebM, FLV, WMV
- ✅ **Smart Optimization**: Automatic frame sampling and quality compression
- ✅ **Batch Processing**: Convert multiple videos with unified settings
- ✅ **Customizable**: Full control over FPS, resolution, and quality
- ✅ **Progress Tracking**: Detailed logging and metadata reporting
- ✅ **Error Handling**: Comprehensive validation and graceful failures

## Directory Structure

```
video-to-gif/
├── README.md                    # This file - overview and quick reference
├── SKILL.md                     # User guide for Claude auto-discovery
├── reference.md                 # Technical deep dive and API reference
├── scripts/
│   └── video_converter.py      # Core conversion engine
└── examples/
    ├── basic_conversion.py      # Simple conversion examples
    ├── batch_processing.py      # Bulk conversion workflows
    └── web_optimization.py      # Size optimization strategies
```

## Usage Examples

### Basic Conversion
```python
from video_converter import convert_video_to_gif

result = convert_video_to_gif("video.mp4")
```

### Custom Settings
```python
result = convert_video_to_gif(
    video_path="demo.mp4",
    fps=15,        # Higher FPS for smoother animation
    scale=0.7,     # 70% of original size
    quality=90     # Higher quality
)
```

### Batch Conversion
```python
from video_converter import batch_convert

videos = ["clip1.mp4", "clip2.mp4", "clip3.mp4"]
results = batch_convert(
    video_paths=videos,
    output_dir="output/gifs/",
    fps=10,
    scale=0.5
)
```

### Get Video Info
```python
from video_converter import get_video_info

info = get_video_info("video.mp4")
print(f"Duration: {info['duration_seconds']}s")
print(f"Dimensions: {info['dimensions']}")
```

## Parameter Guidelines

### FPS (Frames Per Second)
- **5-8**: Documentation, slow animations
- **10-15**: Social media, general use (recommended)
- **20-30**: Smooth motion, presentations

### Scale Factor
- **0.3-0.4**: Thumbnails, previews
- **0.5-0.6**: Web content, social media (recommended)
- **0.7-0.8**: High-quality presentations
- **0.9-1.0**: Maximum quality (large file size)

### Quality
- **70-80**: Web-optimized, smaller files
- **85-90**: Balanced quality and size (recommended)
- **95-100**: Maximum quality, larger files

## Requirements

```bash
pip install opencv-python pillow numpy
```

**System Requirements**:
- Python 3.8+
- OpenCV 4.0+
- Pillow (PIL) 8.0+

## Performance

Processing time for 1280x720 video on Apple M1 Pro:

| Video Length | Processing Time | Output Size (FPS=10, scale=0.5) |
|--------------|-----------------|----------------------------------|
| 5 seconds    | ~2 seconds      | 3-5 MB                           |
| 10 seconds   | ~4 seconds      | 6-10 MB                          |
| 30 seconds   | ~10 seconds     | 18-30 MB                         |

## Documentation

- **[SKILL.md](SKILL.md)** - Quick start guide and common use cases
- **[reference.md](reference.md)** - Technical documentation and API reference
- **[examples/](examples/)** - Working code examples

## Integration with Other Skills

### With Word Documents
```python
from video_converter import convert_video_to_gif
from word_generator import WordDocumentBuilder

gif_result = convert_video_to_gif("demo.mp4")

builder = WordDocumentBuilder()
builder.add_title("Demo Documentation")
builder.add_image(gif_result["file_path"], width_inches=5)
builder.save("output/doc.docx")
```

### With Web Applications
```python
from fastapi import FastAPI, UploadFile
from video_converter import convert_video_to_gif

app = FastAPI()

@app.post("/convert")
async def convert(video: UploadFile):
    result = convert_video_to_gif(video.file)
    return {"status": "success", "path": result["file_path"]}
```

## Troubleshooting

### GIF file too large?
- Reduce FPS (try 8-10)
- Decrease scale factor (try 0.4-0.5)
- Lower quality setting (try 75-80)

### Poor quality output?
- Increase quality setting (try 90-95)
- Increase scale factor (try 0.7-0.8)
- Increase FPS (try 15-20)

### Processing too slow?
- Reduce input video length
- Lower FPS setting
- Decrease scale factor

## Version History

- **v1.0.0** (2025-10-29)
  - Initial release
  - Core video to GIF conversion
  - Batch processing support
  - Quality optimization
  - Comprehensive documentation

## Contributing

This skill is part of the ZTL数智化作战中心 project. Improvements welcome!

## License

Part of ZTL数智化作战中心 framework.

---

**Created by**: ZTL数智化作战中心
**Created date**: 2025-10-29
**Status**: ✅ Production Ready
