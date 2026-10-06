"""YouTube URL validation and video ID extraction utilities."""

import re
from typing import Optional, Tuple
from urllib.parse import urlparse, parse_qs


# Standard 11-character YouTube video ID regex pattern
VIDEO_ID_REGEX = re.compile(r"^[a-zA-Z0-9_-]{11}$")

# Comprehensive patterns for YouTube URLs
YOUTUBE_URL_PATTERNS = [
    # https://www.youtube.com/watch?v=VIDEO_ID
    # https://m.youtube.com/watch?v=VIDEO_ID
    re.compile(r"(?:https?:\/\/)?(?:www\.|m\.)?youtube\.com\/watch\?(?:.*&)?v=([a-zA-Z0-9_-]{11})", re.IGNORECASE),
    # https://youtu.be/VIDEO_ID
    re.compile(r"(?:https?:\/\/)?youtu\.be\/([a-zA-Z0-9_-]{11})", re.IGNORECASE),
    # https://www.youtube.com/shorts/VIDEO_ID
    re.compile(r"(?:https?:\/\/)?(?:www\.|m\.)?youtube\.com\/shorts\/([a-zA-Z0-9_-]{11})", re.IGNORECASE),
    # https://www.youtube.com/embed/VIDEO_ID
    re.compile(r"(?:https?:\/\/)?(?:www\.|m\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]{11})", re.IGNORECASE),
    # https://www.youtube.com/v/VIDEO_ID
    re.compile(r"(?:https?:\/\/)?(?:www\.|m\.)?youtube\.com\/v\/([a-zA-Z0-9_-]{11})", re.IGNORECASE),
    # https://www.youtube.com/live/VIDEO_ID
    re.compile(r"(?:https?:\/\/)?(?:www\.|m\.)?youtube\.com\/live\/([a-zA-Z0-9_-]{11})", re.IGNORECASE),
]


def extract_video_id(url_or_id: str) -> Optional[str]:
    """
    Extract the 11-character YouTube video ID from various YouTube URL formats or direct IDs.

    Supported formats:
        - https://www.youtube.com/watch?v=dQw4w9WgXcQ
        - https://youtu.be/dQw4w9WgXcQ
        - https://www.youtube.com/shorts/dQw4w9WgXcQ
        - https://www.youtube.com/embed/dQw4w9WgXcQ
        - https://www.youtube.com/v/dQw4w9WgXcQ
        - https://www.youtube.com/live/dQw4w9WgXcQ
        - dQw4w9WgXcQ (direct ID)
    """
    if not url_or_id:
        return None

    cleaned = url_or_id.strip()

    # Direct 11-character video ID
    if VIDEO_ID_REGEX.match(cleaned):
        return cleaned

    # Try standard URL parsing first for watch?v= queries
    try:
        # Prepend scheme if missing so urlparse works properly
        parse_target = cleaned if cleaned.startswith(("http://", "https://")) else f"https://{cleaned}"
        parsed = urlparse(parse_target)
        hostname = (parsed.hostname or "").lower()

        if "youtube.com" in hostname or "youtu.be" in hostname:
            # Query param v=
            if parsed.path == "/watch" or parsed.path.startswith("/watch"):
                query_params = parse_qs(parsed.query)
                v_param = query_params.get("v")
                if v_param and VIDEO_ID_REGEX.match(v_param[0]):
                    return v_param[0]

            # Short youtu.be/ID
            if "youtu.be" in hostname:
                path_segments = [p for p in parsed.path.split("/") if p]
                if path_segments and VIDEO_ID_REGEX.match(path_segments[0]):
                    return path_segments[0]

            # Path formats: /shorts/ID, /embed/ID, /v/ID, /live/ID
            for prefix in ("/shorts/", "/embed/", "/v/", "/live/"):
                if parsed.path.startswith(prefix):
                    parts = parsed.path[len(prefix):].split("/")
                    candidate = parts[0] if parts else ""
                    if VIDEO_ID_REGEX.match(candidate):
                        return candidate
    except Exception:
        # Fall back to regex patterns below
        pass

    # Regex matching
    for pattern in YOUTUBE_URL_PATTERNS:
        match = pattern.search(cleaned)
        if match:
            candidate = match.group(1)
            if VIDEO_ID_REGEX.match(candidate):
                return candidate

    return None


def validate_youtube_url(url: Optional[str]) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Validate a YouTube video URL and extract its video ID.

    Returns:
        tuple (is_valid, video_id, error_message)
    """
    if not url or not url.strip():
        return False, None, "Please enter a YouTube video URL."

    cleaned_url = url.strip()
    video_id = extract_video_id(cleaned_url)

    if not video_id:
        return False, None, "Invalid YouTube URL. Please enter a valid YouTube video link."

    return True, video_id, None


def build_canonical_url(video_id: str) -> str:
    """Return standard canonical YouTube watch URL for a video ID."""
    return f"https://www.youtube.com/watch?v={video_id}"
