class KeyframeExtractionError(Exception):
    """Base exception for keyframe extraction errors."""
    pass

class VideoFileNotFoundError(KeyframeExtractionError):
    """Raised when the input video file does not exist."""
    pass

class FFmpegExecutionError(KeyframeExtractionError):
    """Raised when ffmpeg fails to extract keyframes."""
    def __init__(self, message, ffmpeg_output=None):
        super().__init__(message)
        self.ffmpeg_output = ffmpeg_output
