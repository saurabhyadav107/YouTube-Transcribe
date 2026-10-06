"""Utilities for safe file naming and exports."""

import re
import unicodedata

# Reserved filenames on Windows systems
RESERVED_WINDOWS_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
}


def sanitize_filename(
    title: str,
    suffix: str = "transcript",
    max_length: int = 60,
    fallback: str = "youtube-transcript"
) -> str:
    r"""
    Sanitize video title into a safe, cross-platform filename.

    - Removes characters disallowed by Windows/Linux/macOS (/ \ : * ? " < > |)
    - Normalizes unicode characters
    - Truncates to max_length
    - Avoids Windows reserved filenames
    - Produces clean kebab-case or slug format

    Example:
        'My Amazing Video! (Part 1)' -> 'my-amazing-video-part-1-transcript'
    """
    if not title or not title.strip():
        return f"{fallback}-{suffix}" if suffix else fallback

    # Normalize unicode (decompose accents, NFKD)
    normalized = unicodedata.normalize("NFKD", title.strip())
    # Convert to ASCII where possible
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")

    if not ascii_text.strip():
        # Fall back to preserving safe non-ascii unicode alphanumeric characters
        ascii_text = title.strip()

    # Lowercase
    cleaned = ascii_text.lower()

    # Replace invalid filesystem characters and punctuation with hyphens
    cleaned = re.sub(r'[\/\\:\*\?"<>\|\x00-\x1f\x7f]', " ", cleaned)
    # Replace non-alphanumeric chars (excluding hyphens/underscores) with space
    cleaned = re.sub(r"[^\w\s-]", " ", cleaned)
    # Collapse multiple whitespaces/hyphens into single hyphen
    cleaned = re.sub(r"[\s_]+", "-", cleaned)
    cleaned = re.sub(r"-+", "-", cleaned).strip("-")

    # If title became empty after stripping
    if not cleaned:
        cleaned = fallback

    # Check if base word is a reserved Windows name
    if cleaned.upper() in RESERVED_WINDOWS_NAMES:
        cleaned = f"{cleaned}-safe"

    # Truncate
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length].rstrip("-")

    # Append suffix if specified and not already present
    if suffix and not cleaned.endswith(f"-{suffix}"):
        full_name = f"{cleaned}-{suffix}"
    else:
        full_name = cleaned

    base_name = full_name.split(".")[0].upper()
    if base_name in RESERVED_WINDOWS_NAMES:
        full_name = f"{full_name}-file"

    return full_name
