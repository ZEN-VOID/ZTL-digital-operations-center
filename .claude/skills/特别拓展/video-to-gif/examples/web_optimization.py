#!/usr/bin/env python3
"""
Web-Optimized GIF Generation Example

This example demonstrates creating GIFs optimized for web delivery.
Goal: Create GIFs under 5MB for fast loading on websites.
"""

import sys
sys.path.append('./.claude/skills/拓展/video-to-gif/scripts')

from video_converter import convert_video_to_gif, get_video_info
from pathlib import Path


def optimize_for_web(video_path: str, max_size_mb: float = 5.0):
    """
    Convert video to GIF with automatic optimization to meet size target.

    Strategy:
    1. Start with conservative settings
    2. Check output size
    3. Adjust if needed
    """

    # Get video info first
    info = get_video_info(video_path)
    if not info["success"]:
        print(f"❌ Cannot read video: {info['error']}")
        return

    print(f"📹 Video Info:")
    print(f"   Dimensions: {info['dimensions']}")
    print(f"   Duration: {info['duration_seconds']}s")
    print(f"   FPS: {info['fps']}")

    # Strategy for different video lengths
    duration = info["duration_seconds"]

    if duration <= 5:
        # Short videos: Higher quality possible
        settings = {"fps": 12, "scale": 0.6, "quality": 85}
    elif duration <= 10:
        # Medium videos: Balanced settings
        settings = {"fps": 10, "scale": 0.5, "quality": 80}
    else:
        # Long videos: Aggressive compression
        settings = {"fps": 8, "scale": 0.4, "quality": 75}

    print(f"\n🎯 Target: <{max_size_mb}MB for web delivery")
    print(f"⚙️  Settings: FPS={settings['fps']}, Scale={settings['scale']}, Quality={settings['quality']}")

    # Convert
    output_path = Path(video_path).parent / f"{Path(video_path).stem}_web.gif"

    result = convert_video_to_gif(
        video_path=video_path,
        output_path=str(output_path),
        **settings
    )

    if not result["success"]:
        print(f"❌ Conversion failed: {result['error']}")
        return

    # Check size
    size_mb = result["size_mb"]

    if size_mb <= max_size_mb:
        print(f"\n✅ Success! Output: {result['file_path']}")
        print(f"   Size: {size_mb}MB (within {max_size_mb}MB target)")
        print(f"   Dimensions: {result['dimensions']}")
    else:
        print(f"\n⚠️  Warning: Size {size_mb}MB exceeds {max_size_mb}MB target")
        print(f"   Consider:")
        print(f"   - Reducing FPS (current: {settings['fps']})")
        print(f"   - Reducing scale (current: {settings['scale']})")
        print(f"   - Trimming video length")

    return result


# Example 1: Optimize a product demo for website
print("=" * 60)
print("Example 1: Product Demo for Website")
print("=" * 60)

optimize_for_web("input/product-demo.mp4", max_size_mb=5.0)


# Example 2: Multiple videos with different targets
print("\n" + "=" * 60)
print("Example 2: Batch Optimization with Different Targets")
print("=" * 60)

optimizations = [
    {"video": "input/hero-video.mp4", "max_mb": 3.0},      # Hero section: ultra-fast
    {"video": "input/feature-1.mp4", "max_mb": 5.0},       # Feature demos: balanced
    {"video": "input/tutorial.mp4", "max_mb": 8.0}         # Tutorials: quality priority
]

for opt in optimizations:
    print(f"\n{'─' * 60}")
    print(f"Optimizing: {opt['video']}")
    print(f"{'─' * 60}")
    optimize_for_web(opt["video"], max_size_mb=opt["max_mb"])


# Example 3: Social media optimization (different platforms)
print("\n" + "=" * 60)
print("Example 3: Social Media Platform Optimization")
print("=" * 60)

social_platforms = {
    "twitter": {"fps": 15, "scale": 0.6, "quality": 85, "max_mb": 15},
    "wechat": {"fps": 12, "scale": 0.5, "quality": 80, "max_mb": 10},
    "slack": {"fps": 10, "scale": 0.5, "quality": 75, "max_mb": 5},
}

video_path = "input/announcement.mp4"

for platform, settings in social_platforms.items():
    print(f"\n📱 Optimizing for {platform.upper()}...")

    output_path = f"output/social/{platform}_announcement.gif"

    result = convert_video_to_gif(
        video_path=video_path,
        output_path=output_path,
        fps=settings["fps"],
        scale=settings["scale"],
        quality=settings["quality"]
    )

    if result["success"]:
        size_ok = result["size_mb"] <= settings["max_mb"]
        status = "✅" if size_ok else "⚠️"
        print(f"  {status} {platform}: {result['size_mb']}MB / {settings['max_mb']}MB limit")
