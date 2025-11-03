#!/usr/bin/env python3
"""
Video to GIF Converter
Core conversion engine for transforming video files into optimized animated GIFs
"""

import cv2
from PIL import Image
import os
from pathlib import Path
from typing import Optional, List, Dict, Union
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VideoToGIFConverter:
    """
    Core video to GIF conversion engine with optimization features.
    """

    def __init__(self):
        """Initialize the converter."""
        self.supported_formats = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv']

    def convert(
        self,
        video_path: str,
        output_path: Optional[str] = None,
        fps: int = 10,
        scale: float = 0.5,
        quality: int = 85
    ) -> Dict[str, Union[bool, str, float, int]]:
        """
        Convert video to animated GIF.

        Args:
            video_path: Path to input video file
            output_path: Path to output GIF file (optional, auto-generated if None)
            fps: Target frames per second for GIF (default: 10)
            scale: Scale factor for resizing (0.5 = 50% of original size)
            quality: Quality level 1-100 (default: 85)

        Returns:
            Dictionary with conversion result and metadata
        """
        try:
            # Validate parameters
            validation_result = self._validate_parameters(
                video_path, fps, scale, quality
            )
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "error": validation_result["error"]
                }

            video_path = Path(video_path)

            # Generate output path if not provided
            if output_path is None:
                output_path = video_path.parent / f"{video_path.stem}.gif"
            else:
                output_path = Path(output_path)

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            logger.info(f"Converting video to GIF...")
            logger.info(f"Input: {video_path}")
            logger.info(f"Output: {output_path}")

            # Extract frames and create GIF
            result = self._process_video(
                video_path=video_path,
                output_path=output_path,
                target_fps=fps,
                scale_factor=scale,
                quality_level=quality
            )

            return result

        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _validate_parameters(
        self,
        video_path: str,
        fps: int,
        scale: float,
        quality: int
    ) -> Dict[str, Union[bool, str]]:
        """Validate input parameters."""
        video_path = Path(video_path)

        # Check if file exists
        if not video_path.exists():
            return {
                "valid": False,
                "error": f"Video file not found: {video_path}"
            }

        # Check file format
        if video_path.suffix.lower() not in self.supported_formats:
            return {
                "valid": False,
                "error": f"Unsupported format: {video_path.suffix}. Supported: {', '.join(self.supported_formats)}"
            }

        # Validate FPS
        if not (1 <= fps <= 60):
            return {
                "valid": False,
                "error": f"FPS must be between 1 and 60, got: {fps}"
            }

        # Validate scale
        if not (0.1 <= scale <= 1.0):
            return {
                "valid": False,
                "error": f"Scale must be between 0.1 and 1.0, got: {scale}"
            }

        # Validate quality
        if not (1 <= quality <= 100):
            return {
                "valid": False,
                "error": f"Quality must be between 1 and 100, got: {quality}"
            }

        return {"valid": True}

    def _process_video(
        self,
        video_path: Path,
        output_path: Path,
        target_fps: int,
        scale_factor: float,
        quality_level: int
    ) -> Dict[str, Union[bool, str, float, int]]:
        """Process video file and generate GIF."""

        # Open video
        cap = cv2.VideoCapture(str(video_path))

        if not cap.isOpened():
            raise ValueError(f"Failed to open video file: {video_path}")

        # Get video properties
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        logger.info(f"Video properties:")
        logger.info(f"  - FPS: {original_fps}")
        logger.info(f"  - Frames: {frame_count}")
        logger.info(f"  - Size: {width}x{height}")

        # Calculate frame skip
        frame_skip = max(1, int(original_fps / target_fps))

        # New dimensions
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)

        logger.info(f"GIF settings:")
        logger.info(f"  - Target FPS: {target_fps}")
        logger.info(f"  - Frame skip: {frame_skip}")
        logger.info(f"  - Output size: {new_width}x{new_height}")

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
                    logger.info(f"  Processed {len(frames)} frames...")

            frame_idx += 1

        cap.release()

        logger.info(f"Total frames extracted: {len(frames)}")

        if not frames:
            raise ValueError("No frames extracted from video")

        # Save as GIF
        logger.info("Saving GIF...")

        # Calculate duration per frame (in milliseconds)
        duration = int(1000 / target_fps)

        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0,  # 0 means infinite loop
            optimize=True,
            quality=quality_level
        )

        # Get file size
        file_size_mb = output_path.stat().st_size / (1024 * 1024)
        duration_seconds = len(frames) / target_fps

        logger.info(f"✅ GIF created successfully!")
        logger.info(f"  - Output: {output_path}")
        logger.info(f"  - Size: {file_size_mb:.2f} MB")
        logger.info(f"  - Frames: {len(frames)}")
        logger.info(f"  - Duration: {duration_seconds:.1f} seconds")

        return {
            "success": True,
            "file_path": str(output_path),
            "size_mb": round(file_size_mb, 2),
            "frames": len(frames),
            "duration_seconds": round(duration_seconds, 1),
            "dimensions": f"{new_width}x{new_height}",
            "fps": target_fps
        }


# Convenience functions for direct use

def convert_video_to_gif(
    video_path: str,
    output_path: Optional[str] = None,
    fps: int = 10,
    scale: float = 0.5,
    quality: int = 85
) -> Dict[str, Union[bool, str, float, int]]:
    """
    Convert a video file to an animated GIF.

    Args:
        video_path: Path to input video file
        output_path: Path to output GIF (optional)
        fps: Target frames per second (1-60)
        scale: Scale factor (0.1-1.0)
        quality: Quality level (1-100)

    Returns:
        Dictionary with conversion result and metadata

    Example:
        >>> result = convert_video_to_gif("video.mp4", fps=12, scale=0.6)
        >>> if result["success"]:
        ...     print(f"Created: {result['file_path']}")
    """
    converter = VideoToGIFConverter()
    return converter.convert(video_path, output_path, fps, scale, quality)


def batch_convert(
    video_paths: List[str],
    output_dir: Optional[str] = None,
    fps: int = 10,
    scale: float = 0.5,
    quality: int = 85
) -> List[Dict[str, Union[bool, str, float, int]]]:
    """
    Convert multiple videos to GIFs with the same settings.

    Args:
        video_paths: List of video file paths
        output_dir: Output directory for all GIFs (optional)
        fps: Target frames per second
        scale: Scale factor
        quality: Quality level

    Returns:
        List of result dictionaries for each conversion

    Example:
        >>> videos = ["clip1.mp4", "clip2.mp4"]
        >>> results = batch_convert(videos, output_dir="output/gifs/")
        >>> for r in results:
        ...     print(f"{r.get('filename', 'unknown')}: {r['status']}")
    """
    converter = VideoToGIFConverter()
    results = []

    logger.info(f"Starting batch conversion of {len(video_paths)} videos...")

    for idx, video_path in enumerate(video_paths, 1):
        logger.info(f"\nProcessing {idx}/{len(video_paths)}: {video_path}")

        video_path_obj = Path(video_path)

        # Determine output path
        if output_dir:
            output_dir_obj = Path(output_dir)
            output_dir_obj.mkdir(parents=True, exist_ok=True)
            output_path = output_dir_obj / f"{video_path_obj.stem}.gif"
        else:
            output_path = None

        # Convert
        result = converter.convert(
            video_path=video_path,
            output_path=str(output_path) if output_path else None,
            fps=fps,
            scale=scale,
            quality=quality
        )

        # Add filename to result
        result["filename"] = video_path_obj.name
        result["status"] = "success" if result.get("success") else "failed"

        results.append(result)

    # Summary
    successful = sum(1 for r in results if r.get("success"))
    logger.info(f"\nBatch conversion complete: {successful}/{len(video_paths)} successful")

    return results


def get_video_info(video_path: str) -> Dict[str, Union[bool, str, int, float]]:
    """
    Get metadata about a video file without converting it.

    Args:
        video_path: Path to video file

    Returns:
        Dictionary with video metadata

    Example:
        >>> info = get_video_info("video.mp4")
        >>> print(f"Duration: {info['duration_seconds']}s")
    """
    try:
        video_path = Path(video_path)

        if not video_path.exists():
            return {
                "success": False,
                "error": f"Video file not found: {video_path}"
            }

        cap = cv2.VideoCapture(str(video_path))

        if not cap.isOpened():
            return {
                "success": False,
                "error": f"Failed to open video file: {video_path}"
            }

        # Get properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = frame_count / fps if fps > 0 else 0

        cap.release()

        return {
            "success": True,
            "filename": video_path.name,
            "fps": fps,
            "frame_count": frame_count,
            "width": width,
            "height": height,
            "dimensions": f"{width}x{height}",
            "duration_seconds": round(duration, 1),
            "format": video_path.suffix
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python video_converter.py <video_path> [output_path] [fps] [scale] [quality]")
        print("Example: python video_converter.py input.mp4 output.gif 10 0.5 85")
        print("\nOr get video info:")
        print("  python video_converter.py --info <video_path>")
        sys.exit(1)

    if sys.argv[1] == "--info":
        if len(sys.argv) < 3:
            print("Error: Please provide video path")
            sys.exit(1)

        info = get_video_info(sys.argv[2])
        if info["success"]:
            print("\nVideo Information:")
            print(f"  Filename: {info['filename']}")
            print(f"  Dimensions: {info['dimensions']}")
            print(f"  FPS: {info['fps']}")
            print(f"  Frames: {info['frame_count']}")
            print(f"  Duration: {info['duration_seconds']}s")
            print(f"  Format: {info['format']}")
        else:
            print(f"Error: {info['error']}")
        sys.exit(0)

    video_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    fps = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
    quality = int(sys.argv[5]) if len(sys.argv) > 5 else 85

    try:
        result = convert_video_to_gif(
            video_path=video_path,
            output_path=output_path,
            fps=fps,
            scale=scale,
            quality=quality
        )

        if result["success"]:
            print(f"\n✅ Conversion completed successfully!")
            print(f"  Output: {result['file_path']}")
            print(f"  Size: {result['size_mb']} MB")
            print(f"  Frames: {result['frames']}")
            print(f"  Duration: {result['duration_seconds']}s")
        else:
            print(f"\n❌ Conversion failed: {result['error']}")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
