# Video to GIF Converter - Technical Reference

## Architecture Overview

### System Components

```
video-to-gif/
├── SKILL.md                     # Quick start guide (500-2000 tokens)
├── reference.md                 # This file - technical deep dive
├── scripts/
│   ├── video_converter.py      # Core conversion engine
│   └── __init__.py             # Module initialization (optional)
└── examples/
    ├── basic_conversion.py      # Simple use cases
    ├── batch_processing.py      # Bulk conversion
    └── web_optimization.py      # Size optimization strategies
```

### Processing Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    Video Input                               │
│  (MP4, AVI, MOV, MKV, WebM, FLV, WMV)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│               Parameter Validation                           │
│  • File existence check                                     │
│  • Format validation                                        │
│  • Parameter bounds checking (FPS, scale, quality)          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│               Video Metadata Extraction                      │
│  • Original FPS, frame count                                │
│  • Dimensions (width × height)                              │
│  • Duration calculation                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│               Frame Extraction                               │
│  • Calculate frame skip (original_fps / target_fps)         │
│  • Sample frames at target intervals                        │
│  • Color space conversion (BGR → RGB)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│               Frame Optimization                             │
│  • Resize to target dimensions (scale factor)               │
│  • Interpolation: cv2.INTER_AREA (best for downscaling)    │
│  • Convert to PIL Image objects                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│               GIF Assembly                                   │
│  • Set frame duration (1000ms / target_fps)                 │
│  • Enable infinite loop (loop=0)                            │
│  • Apply quality compression                                │
│  • Enable GIF optimization                                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│               Output & Metadata                              │
│  • Save GIF file                                            │
│  • Calculate file size                                      │
│  • Return conversion metadata                               │
└─────────────────────────────────────────────────────────────┘
```

## API Reference

### Class: VideoToGIFConverter

Core conversion engine with optimization features.

#### Constructor

```python
converter = VideoToGIFConverter()
```

No parameters required. Initializes with supported format list.

#### Method: convert()

Main conversion method.

```python
def convert(
    self,
    video_path: str,
    output_path: Optional[str] = None,
    fps: int = 10,
    scale: float = 0.5,
    quality: int = 85
) -> Dict[str, Union[bool, str, float, int]]
```

**Parameters**:

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `video_path` | str | - | Required | Path to input video file |
| `output_path` | Optional[str] | - | None | Output GIF path (auto-generated if None) |
| `fps` | int | 1-60 | 10 | Target frames per second |
| `scale` | float | 0.1-1.0 | 0.5 | Resolution scale factor |
| `quality` | int | 1-100 | 85 | Compression quality level |

**Returns**: Dictionary with structure:

```python
{
    "success": bool,              # Conversion success status
    "file_path": str,             # Path to output GIF
    "size_mb": float,             # File size in megabytes
    "frames": int,                # Number of frames in GIF
    "duration_seconds": float,    # Total duration
    "dimensions": str,            # "widthxheight" format
    "fps": int,                   # Actual FPS of output
    "error": str                  # Error message (if success=False)
}
```

**Example**:

```python
converter = VideoToGIFConverter()

result = converter.convert(
    video_path="input/demo.mp4",
    output_path="output/demo.gif",
    fps=15,
    scale=0.7,
    quality=90
)

if result["success"]:
    print(f"Created: {result['file_path']}")
    print(f"Size: {result['size_mb']} MB")
```

---

### Function: convert_video_to_gif()

Convenience function for direct conversion without instantiating class.

```python
def convert_video_to_gif(
    video_path: str,
    output_path: Optional[str] = None,
    fps: int = 10,
    scale: float = 0.5,
    quality: int = 85
) -> Dict[str, Union[bool, str, float, int]]
```

**Usage**:

```python
result = convert_video_to_gif("video.mp4", fps=12, scale=0.6)
```

Parameters and return value identical to `VideoToGIFConverter.convert()`.

---

### Function: batch_convert()

Convert multiple videos with unified settings.

```python
def batch_convert(
    video_paths: List[str],
    output_dir: Optional[str] = None,
    fps: int = 10,
    scale: float = 0.5,
    quality: int = 85
) -> List[Dict[str, Union[bool, str, float, int]]]
```

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `video_paths` | List[str] | List of video file paths |
| `output_dir` | Optional[str] | Output directory for all GIFs (optional) |
| `fps` | int | Target FPS for all conversions |
| `scale` | float | Scale factor for all conversions |
| `quality` | int | Quality level for all conversions |

**Returns**: List of result dictionaries (one per video), each with added fields:

```python
{
    "filename": str,   # Original video filename
    "status": str,     # "success" or "failed"
    # ... (other fields from convert())
}
```

**Example**:

```python
videos = ["clip1.mp4", "clip2.mp4", "clip3.mp4"]

results = batch_convert(
    video_paths=videos,
    output_dir="output/batch/",
    fps=10,
    scale=0.5
)

for r in results:
    print(f"{r['filename']}: {r['status']}")
```

---

### Function: get_video_info()

Extract metadata without converting.

```python
def get_video_info(video_path: str) -> Dict[str, Union[bool, str, int, float]]
```

**Returns**:

```python
{
    "success": bool,
    "filename": str,
    "fps": float,
    "frame_count": int,
    "width": int,
    "height": int,
    "dimensions": str,         # "widthxheight"
    "duration_seconds": float,
    "format": str              # File extension
}
```

**Example**:

```python
info = get_video_info("video.mp4")

if info["success"]:
    print(f"Duration: {info['duration_seconds']}s")
    print(f"Dimensions: {info['dimensions']}")
    print(f"FPS: {info['fps']}")
```

---

## Parameter Optimization Guide

### FPS Selection Strategy

| Video Type | Recommended FPS | Rationale |
|------------|----------------|-----------|
| **Static Presentations** | 5-8 | Minimal motion, prioritize file size |
| **Documentation/Tutorials** | 8-10 | Balanced clarity and size |
| **Product Demos** | 10-15 | Smooth enough for user flows |
| **Animations** | 15-20 | Capture smooth motion |
| **High-Action Content** | 20-30 | Maximum smoothness |

**Frame Skip Calculation**:
```python
frame_skip = max(1, int(original_fps / target_fps))
```

Example: 24 FPS video → 10 FPS GIF = skip every 2.4 frames (rounded to 2)

---

### Scale Factor Selection

| Target Use Case | Recommended Scale | Output Size (from 1920x1080) |
|----------------|-------------------|------------------------------|
| **Thumbnails** | 0.25-0.3 | 480x270 - 576x324 |
| **Social Media** | 0.4-0.6 | 768x432 - 1152x648 |
| **Documentation** | 0.5-0.6 | 960x540 - 1152x648 |
| **Presentations** | 0.7-0.8 | 1344x756 - 1536x864 |
| **High Quality** | 0.9-1.0 | 1728x972 - 1920x1080 |

**Resolution Impact on File Size**:
- Each dimension halved (scale=0.5) → ~4x smaller file
- Scale 0.5 → 50% width × 50% height = 25% pixel count

---

### Quality Level Guidelines

| Quality Range | Compression | File Size Impact | Visual Quality | Use Case |
|--------------|-------------|------------------|----------------|----------|
| **70-75** | Aggressive | 30-50% smaller | Noticeable artifacts | Web thumbnails |
| **80-85** | Moderate | Balanced | Good quality | General web use |
| **90-95** | Light | 20-30% larger | Excellent | Presentations |
| **96-100** | Minimal | Largest | Maximum | Archival/print |

**Note**: GIF format has inherent limitations (256 colors), so quality >95 may show diminishing returns.

---

## Performance Characteristics

### Processing Time Estimates

Based on 1280x720 video on Apple M1 Pro:

| Video Length | Frames Extracted | Processing Time | Output Size (FPS=10, scale=0.5) |
|--------------|------------------|-----------------|----------------------------------|
| 5 seconds | ~30 frames | 1-2 seconds | 3-5 MB |
| 10 seconds | ~60 frames | 2-4 seconds | 6-10 MB |
| 20 seconds | ~120 frames | 4-8 seconds | 12-20 MB |
| 30 seconds | ~180 frames | 6-12 seconds | 18-30 MB |
| 60 seconds | ~360 frames | 12-24 seconds | 35-60 MB |

**Factors Affecting Speed**:
- **CPU**: Single-threaded processing (no GPU acceleration)
- **Resolution**: Higher source resolution = longer processing
- **FPS**: Higher target FPS = more frames to process
- **Quality**: Higher quality = more compression time
- **Video Codec**: H.264 fastest, HEVC/VP9 slower

---

### Memory Usage

**Peak memory usage** ≈ `(width × height × 3 bytes × frame_count)`

Example: 1280x720 video, 60 frames:
```
1280 × 720 × 3 × 60 = ~165 MB
```

**Optimization tips**:
- Process long videos in segments
- Reduce scale factor for large videos
- Use batch processing for multiple small videos

---

## Technical Implementation Details

### OpenCV Configuration

```python
import cv2

# Open video with default backend
cap = cv2.VideoCapture(str(video_path))

# Extract properties
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Read frames
while True:
    ret, frame = cap.read()
    if not ret:
        break
    # Process frame...

cap.release()
```

### Color Space Conversion

OpenCV reads frames in **BGR** format, but PIL expects **RGB**:

```python
# Convert BGR to RGB
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Convert to PIL Image
pil_image = Image.fromarray(frame_rgb)
```

### Frame Interpolation

Using `cv2.INTER_AREA` for downscaling (best quality):

```python
frame_resized = cv2.resize(
    frame_rgb,
    (new_width, new_height),
    interpolation=cv2.INTER_AREA
)
```

**Interpolation methods**:
- `INTER_AREA`: Best for shrinking (used in this skill)
- `INTER_CUBIC`: Good for enlarging
- `INTER_LINEAR`: Fast, moderate quality
- `INTER_NEAREST`: Fastest, lowest quality

### GIF Encoding (Pillow)

```python
frames[0].save(
    output_path,
    save_all=True,              # Enable multi-frame GIF
    append_images=frames[1:],   # Append remaining frames
    duration=100,               # Duration per frame (ms)
    loop=0,                     # 0 = infinite loop
    optimize=True,              # Enable GIF optimization
    quality=85                  # Compression quality
)
```

**Optimization techniques**:
- `optimize=True`: Reduces file size by ~10-20%
- Frame differencing: Only stores changed pixels
- Color palette optimization: Reduces to optimal 256 colors

---

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `Video file not found` | Invalid path | Verify file exists |
| `Failed to open video` | Corrupted file or unsupported codec | Try re-encoding with ffmpeg |
| `No frames extracted` | Video duration too short or corrupted | Check video with media player |
| `FPS must be between 1 and 60` | Invalid parameter | Use valid range |
| `Scale must be between 0.1 and 1.0` | Invalid parameter | Use valid range |
| `MemoryError` | Video too large | Reduce scale or process in segments |

### Validation Logic

```python
def _validate_parameters(self, video_path, fps, scale, quality):
    """Validate all input parameters before processing."""

    # File existence
    if not Path(video_path).exists():
        return {"valid": False, "error": "File not found"}

    # Format check
    if suffix not in ['.mp4', '.avi', '.mov', ...]:
        return {"valid": False, "error": "Unsupported format"}

    # Parameter bounds
    if not (1 <= fps <= 60):
        return {"valid": False, "error": "FPS out of range"}

    if not (0.1 <= scale <= 1.0):
        return {"valid": False, "error": "Scale out of range"}

    if not (1 <= quality <= 100):
        return {"valid": False, "error": "Quality out of range"}

    return {"valid": True}
```

---

## Advanced Use Cases

### Adaptive Quality Selection

Automatically adjust settings based on video properties:

```python
def adaptive_convert(video_path: str, target_size_mb: float = 5.0):
    """Convert with adaptive settings to meet size target."""

    info = get_video_info(video_path)
    duration = info["duration_seconds"]

    # Longer videos need more compression
    if duration < 5:
        settings = {"fps": 15, "scale": 0.7, "quality": 90}
    elif duration < 10:
        settings = {"fps": 12, "scale": 0.6, "quality": 85}
    elif duration < 20:
        settings = {"fps": 10, "scale": 0.5, "quality": 80}
    else:
        settings = {"fps": 8, "scale": 0.4, "quality": 75}

    return convert_video_to_gif(video_path, **settings)
```

### Segment Processing for Long Videos

Process long videos in chunks to manage memory:

```python
def convert_long_video(video_path: str, segment_length: int = 10):
    """Convert long video by processing segments."""

    # Extract segments using ffmpeg
    # Convert each segment to GIF
    # Combine GIFs (if needed)

    # Implementation left as exercise
    pass
```

### Custom Frame Filtering

Apply custom logic during frame extraction:

```python
def convert_with_filter(video_path: str, frame_filter: callable):
    """Convert with custom frame filtering."""

    converter = VideoToGIFConverter()

    # Modify _process_video to apply frame_filter
    # e.g., skip blurry frames, enhance contrast, etc.

    # Implementation requires subclassing VideoToGIFConverter
    pass
```

---

## Integration Patterns

### With Office Skills (Word Documents)

```python
from video_converter import convert_video_to_gif
from word_generator import WordDocumentBuilder

# Convert video
result = convert_video_to_gif("demo.mp4")

# Embed in Word document
builder = WordDocumentBuilder()
builder.add_title("Product Documentation")
builder.add_heading("Feature Demo", level=1)
builder.add_paragraph("See the feature in action:")
builder.add_image(result["file_path"], width_inches=5)
builder.save("output/documentation.docx")
```

### With Web Frameworks (Flask/FastAPI)

```python
from fastapi import FastAPI, UploadFile
from video_converter import convert_video_to_gif
import tempfile

app = FastAPI()

@app.post("/convert")
async def convert_endpoint(video: UploadFile):
    """API endpoint for video to GIF conversion."""

    # Save uploaded file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await video.read())
        tmp_path = tmp.name

    # Convert
    result = convert_video_to_gif(tmp_path, fps=10, scale=0.5)

    # Return GIF
    return FileResponse(result["file_path"])
```

### Batch Processing Pipeline

```python
from pathlib import Path
from video_converter import batch_convert

def process_video_directory(input_dir: str, output_dir: str):
    """Process all videos in a directory."""

    # Find all video files
    videos = []
    for ext in ['.mp4', '.avi', '.mov']:
        videos.extend(Path(input_dir).glob(f"**/*{ext}"))

    # Batch convert
    results = batch_convert(
        video_paths=[str(v) for v in videos],
        output_dir=output_dir
    )

    # Generate report
    report = {
        "total": len(results),
        "successful": sum(1 for r in results if r["success"]),
        "failed": sum(1 for r in results if not r["success"]),
        "total_size_mb": sum(r.get("size_mb", 0) for r in results if r["success"])
    }

    return report
```

---

## Testing

### Unit Tests

```python
import unittest
from video_converter import VideoToGIFConverter, convert_video_to_gif

class TestVideoConverter(unittest.TestCase):

    def test_basic_conversion(self):
        """Test basic conversion with default settings."""
        result = convert_video_to_gif("test_video.mp4")
        self.assertTrue(result["success"])
        self.assertIn("file_path", result)
        self.assertGreater(result["size_mb"], 0)

    def test_invalid_path(self):
        """Test handling of invalid video path."""
        result = convert_video_to_gif("nonexistent.mp4")
        self.assertFalse(result["success"])
        self.assertIn("error", result)

    def test_custom_settings(self):
        """Test conversion with custom settings."""
        result = convert_video_to_gif(
            "test_video.mp4",
            fps=15,
            scale=0.7,
            quality=90
        )
        self.assertTrue(result["success"])
        self.assertEqual(result["fps"], 15)
```

### Integration Tests

```python
def test_end_to_end_conversion():
    """Test complete conversion workflow."""

    # Setup
    video_path = "test_assets/sample.mp4"
    output_path = "test_output/sample.gif"

    # Convert
    result = convert_video_to_gif(video_path, output_path)

    # Verify
    assert result["success"]
    assert Path(output_path).exists()
    assert Path(output_path).stat().st_size > 0

    # Cleanup
    Path(output_path).unlink()
```

---

## Troubleshooting

### Debug Mode

Enable detailed logging:

```python
import logging

logging.basicConfig(level=logging.DEBUG)

# All converter operations will now log detailed information
result = convert_video_to_gif("video.mp4")
```

### Verify OpenCV Installation

```python
import cv2
print(f"OpenCV version: {cv2.__version__}")

# Test video opening
cap = cv2.VideoCapture("test.mp4")
print(f"Video opened: {cap.isOpened()}")
cap.release()
```

### Verify Pillow Installation

```python
from PIL import Image
print(f"Pillow version: {Image.__version__}")

# Test GIF creation
img = Image.new('RGB', (100, 100), color='red')
img.save("test.gif")
```

---

## Future Enhancements

Potential features for future versions:

- **GPU Acceleration**: Use CUDA for faster processing
- **Video Trimming**: Built-in start/end time selection
- **Frame Filtering**: Skip duplicate/similar frames
- **Text Overlays**: Add captions and timestamps
- **WebP Output**: Alternative format with better compression
- **Parallel Processing**: Multi-threaded batch conversion
- **Progress Callbacks**: Real-time progress updates
- **Frame Effects**: Apply filters, transitions, etc.

---

## References

- **OpenCV Documentation**: https://docs.opencv.org/
- **Pillow Documentation**: https://pillow.readthedocs.io/
- **GIF Specification**: https://www.w3.org/Graphics/GIF/spec-gif89a.txt
- **Video Codecs**: https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Video_codecs

---

**Document Version**: v1.0.0
**Last Updated**: 2025-10-29
**Maintainer**: ZTL数智化作战中心
