#!/usr/bin/env python3
"""
Batch Video to GIF Conversion Example

This example shows how to convert multiple videos at once.
"""

import sys
sys.path.append('./.claude/skills/拓展/video-to-gif/scripts')

from video_converter import batch_convert
from pathlib import Path

# Example 1: Convert all MP4 files in a directory
video_dir = Path("input/videos")
video_files = list(video_dir.glob("*.mp4"))

print(f"Found {len(video_files)} videos to convert...")

results = batch_convert(
    video_paths=[str(f) for f in video_files],
    output_dir="output/gifs",
    fps=10,
    scale=0.5,
    quality=85
)

# Print summary
successful = sum(1 for r in results if r["success"])
print(f"\n📊 Summary: {successful}/{len(results)} conversions successful")

for result in results:
    status = "✅" if result["success"] else "❌"
    print(f"  {status} {result['filename']}")


# Example 2: Convert specific videos with custom naming
videos_to_convert = [
    {
        "input": "raw/product-demo.mp4",
        "output": "output/social-media/product-demo.gif",
        "settings": {"fps": 12, "scale": 0.6, "quality": 85}
    },
    {
        "input": "raw/tutorial-part1.mp4",
        "output": "output/docs/tutorial-1.gif",
        "settings": {"fps": 8, "scale": 0.5, "quality": 80}
    },
    {
        "input": "raw/feature-preview.mp4",
        "output": "output/presentations/feature-preview.gif",
        "settings": {"fps": 20, "scale": 0.8, "quality": 95}
    }
]

from video_converter import convert_video_to_gif

print("\n🔄 Converting videos with custom settings...")

for video in videos_to_convert:
    print(f"\nProcessing: {video['input']}")

    result = convert_video_to_gif(
        video_path=video["input"],
        output_path=video["output"],
        **video["settings"]
    )

    if result["success"]:
        print(f"  ✅ Created: {result['file_path']} ({result['size_mb']} MB)")
    else:
        print(f"  ❌ Failed: {result['error']}")
