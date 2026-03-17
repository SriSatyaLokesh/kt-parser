import os
from typing import List
import ffmpeg

from .exceptions import (
    KeyframeExtractionError,
    VideoFileNotFoundError,
    FFmpegExecutionError,
)

def extract_keyframes(video_path: str, output_dir: str) -> List[str]:
    """
    Extracts keyframes from a video file and saves them as images in output_dir.

    Args:
        video_path (str): Path to the input video file.
        output_dir (str): Directory to save extracted keyframes.

    Returns:
        List[str]: List of file paths to the extracted keyframe images.

    Raises:
        VideoFileNotFoundError: If the video file does not exist.
        FFmpegExecutionError: If ffmpeg fails to extract keyframes.
        KeyframeExtractionError: For other extraction errors.
    """
    if not os.path.isfile(video_path):
        raise VideoFileNotFoundError(f"Video file not found: {video_path}")

    if not os.path.isdir(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            raise KeyframeExtractionError(f"Failed to create output directory: {output_dir}") from e

    output_pattern = os.path.join(output_dir, "keyframe_%04d.jpg")
    try:
        (
            ffmpeg
            .input(video_path)
            .filter('select', 'eq(pict_type\\,I)')
            .output(output_pattern, vsync='vfr', frame_pts='true')
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        raise FFmpegExecutionError(
            f"ffmpeg failed: {e.stderr.decode('utf8') if e.stderr else str(e)}",
            ffmpeg_output=e.stderr.decode('utf8') if e.stderr else None
        ) from e
    except Exception as e:
        raise KeyframeExtractionError("Unexpected error during keyframe extraction") from e

    # Collect output files
    keyframes = sorted([
        os.path.join(output_dir, f)
        for f in os.listdir(output_dir)
        if f.startswith("keyframe_") and f.endswith(".jpg")
    ])
    if not keyframes:
        raise KeyframeExtractionError("No keyframes were extracted from the video.")

    return keyframes
