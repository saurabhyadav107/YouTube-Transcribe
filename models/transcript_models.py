"""Data structures for YouTube transcript processing and metadata."""

from dataclasses import dataclass, field
from typing import Optional, List


# Map common language codes to flags for UI presentation
LANGUAGE_FLAGS = {
    "en": "🇬🇧",
    "en-us": "🇺🇸",
    "en-gb": "🇬🇧",
    "hi": "🇮🇳",
    "es": "🇪🇸",
    "fr": "🇫🇷",
    "de": "🇩🇪",
    "ja": "🇯🇵",
    "ko": "🇰🇷",
    "zh": "🇨🇳",
    "zh-hans": "🇨🇳",
    "zh-hant": "🇹🇼",
    "ar": "🇸🇦",
    "ru": "🇷🇺",
    "pt": "🇵🇹",
    "pt-br": "🇧🇷",
    "it": "🇮🇹",
    "nl": "🇳🇱",
    "tr": "🇹🇷",
    "bn": "🇧🇩",
    "ur": "🇵🇰",
    "ta": "🇮🇳",
    "te": "🇮🇳",
    "mr": "🇮🇳",
    "gu": "🇮🇳",
    "kn": "🇮🇳",
    "ml": "🇮🇳",
    "pa": "🇮🇳",
    "vi": "🇻🇳",
    "id": "🇮🇩",
    "th": "🇹🇭",
}


@dataclass(frozen=True)
class TranscriptSegment:
    """Represents a single timed segment of speech in a transcript."""

    text: str
    start: float  # Start time in seconds
    duration: float  # Duration in seconds

    @property
    def end(self) -> float:
        """Calculate segment end time."""
        return self.start + self.duration


@dataclass(frozen=True)
class TranscriptLanguage:
    """Represents an available subtitle / transcript track."""

    language: str
    language_code: str
    is_generated: bool
    is_translatable: bool = False
    is_original: bool = False
    is_translated: bool = False

    @property
    def flag(self) -> str:
        """Return a flag emoji corresponding to the language code, or generic globe."""
        base_code = self.language_code.lower().split("-")[0]
        full_code = self.language_code.lower()
        return LANGUAGE_FLAGS.get(full_code) or LANGUAGE_FLAGS.get(base_code, "🌐")

    @property
    def display_name(self) -> str:
        """Formatted display name for UI dropdowns."""
        if self.is_original:
            track_type = "Manual" if not self.is_generated else "Auto"
            return f"{self.flag} {self.language} ({self.language_code}) ★ [Original Video Language] • {track_type}"
        elif self.is_translated:
            return f"{self.flag} {self.language} ({self.language_code}) • Translated"
        else:
            track_type = "Auto" if self.is_generated else "Manual"
            return f"{self.flag} {self.language} ({self.language_code}) • {track_type}"


@dataclass(frozen=True)
class VideoMetadata:
    """Represents basic metadata for a YouTube video."""

    video_id: str
    title: str
    url: str
    channel: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration_seconds: Optional[float] = None


@dataclass
class TranscriptResult:
    """Complete transcript extraction result with formatted outputs and statistics."""

    video_id: str
    language: str
    language_code: str
    is_generated: bool
    segments: List[TranscriptSegment]
    total_duration: float
    word_count: int
    segment_count: int
    reading_text: str
    timestamped_text: str
    srt_text: str
    vtt_text: str
