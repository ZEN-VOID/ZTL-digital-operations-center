#!/usr/bin/env python3
"""
Basic Video to GIF Conversion Example

This example demonstrates the simplest way to convert a video to GIF.
"""

import sys
sys.path.append('./.claude/skills/拓展/video-to-gif/scripts')

from video_converter import convert_video_to_gif

# Example 1: Convert with default settings (10 FPS, 50% scale, quality 85)
result = convert_video_to_gif(
    video_path="input/sample-video.mp4"
)

if result["success"]:
    print("✅ Conversion successful!")
    print(f"   Output: {result['file_path']}")
    print(f"   Size: {result['size_mb']} MB")
    print(f"   Duration: {result['duration_seconds']} seconds")
else:
    print(f"❌ Conversion failed: {result['error']}")


# Example 2: Convert with custom output path
result = convert_video_to_gif(
    video_path="input/demo.mp4",
    output_path="output/animations/demo.gif"
)

if result["success"]:
    print(f"\n✅ Saved to: {result['file_path']}")


# Example 3: Convert with custom settings
result = convert_video_to_gif(
    video_path="input/presentation.mp4",
    output_path="output/presentation.gif",
    fps=15,        # Smoother animation
    scale=0.7,     # Larger size
    quality=90     # Higher quality
)

if result["success"]:
    print(f"\n✅ High-quality GIF created!")
    print(f"   Dimensions: {result['dimensions']}")
    print(f"   Frames: {result['frames']}")
