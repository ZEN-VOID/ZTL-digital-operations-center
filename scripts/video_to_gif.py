#!/usr/bin/env python3
"""
Video to GIF Converter
Converts MP4 videos to optimized animated GIFs
"""

import cv2
from PIL import Image
import os
from pathlib import Path
from typing import Optional


def video_to_gif(
    video_path: str,
    output_path: Optional[str] = None,
    fps: int = 10,
    scale: float = 0.5,
    quality: int = 85
) -> str:
    """
    Convert video to animated GIF.

    Args:
        video_path: Path to input video file
        output_path: Path to output GIF file (optional, auto-generated if None)
        fps: Target frames per second for GIF (default: 10)
        scale: Scale factor for resizing (0.5 = 50% of original size)
        quality: Quality level 1-100 (default: 85)

    Returns:
        Path to generated GIF file
    """
    video_path = Path(video_path)

    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    # Generate output path if not provided
    if output_path is None:
        output_path = video_path.parent / f"{video_path.stem}.gif"
    else:
        output_path = Path(output_path)

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Converting video to GIF...")
    print(f"Input: {video_path}")
    print(f"Output: {output_path}")

    # Open video
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise ValueError(f"Failed to open video file: {video_path}")

    # Get video properties
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"Video properties:")
    print(f"  - FPS: {original_fps}")
    print(f"  - Frames: {frame_count}")
    print(f"  - Size: {width}x{height}")

    # Calculate frame skip
    frame_skip = max(1, int(original_fps / fps))

    # New dimensions
    new_width = int(width * scale)
    new_height = int(height * scale)

    print(f"GIF settings:")
    print(f"  - Target FPS: {fps}")
    print(f"  - Frame skip: {frame_skip}")
    print(f"  - Output size: {new_width}x{new_height}")

    # Extract frames
    frames = []
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Skip frames to achieve target FPS
        if frame_idx % frame_skip == 0:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Resize frame
            frame_resized = cv2.resize(
                frame_rgb,
                (new_width, new_height),
                interpolation=cv2.INTER_AREA
            )

            # Convert to PIL Image
            pil_image = Image.fromarray(frame_resized)
            frames.append(pil_image)

            if len(frames) % 10 == 0:
                print(f"  Processed {len(frames)} frames...")

        frame_idx += 1

    cap.release()

    print(f"Total frames extracted: {len(frames)}")

    # Save as GIF
    if frames:
        print("Saving GIF...")

        # Calculate duration per frame (in milliseconds)
        duration = int(1000 / fps)

        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0,  # 0 means infinite loop
            optimize=True,
            quality=quality
        )

        # Get file size
        file_size_mb = output_path.stat().st_size / (1024 * 1024)

        print(f"✅ GIF created successfully!")
        print(f"  - Output: {output_path}")
        print(f"  - Size: {file_size_mb:.2f} MB")
        print(f"  - Frames: {len(frames)}")
        print(f"  - Duration: {len(frames) / fps:.1f} seconds")

        return str(output_path)
    else:
        raise ValueError("No frames extracted from video")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python video_to_gif.py <video_path> [output_path] [fps] [scale] [quality]")
        print("Example: python video_to_gif.py input.mp4 output.gif 10 0.5 85")
        sys.exit(1)

    video_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    fps = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
    quality = int(sys.argv[5]) if len(sys.argv) > 5 else 85

    try:
        result = video_to_gif(
            video_path=video_path,
            output_path=output_path,
            fps=fps,
            scale=scale,
            quality=quality
        )
        print(f"\n✅ Conversion completed: {result}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
