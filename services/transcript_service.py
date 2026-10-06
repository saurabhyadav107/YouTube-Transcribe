"""YouTube transcript extraction, language listing, and processing service."""

import logging
import warnings
from typing import List, Optional, Tuple, Any

from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
    CouldNotRetrieveTranscript,
    YouTubeRequestFailed,
    InvalidVideoId,
    AgeRestricted,
)

# Suppress urllib3 version warning if present
try:
    from requests.exceptions import RequestsDependencyWarning
    warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
except ImportError:
    pass

from models.transcript_models import (
    TranscriptSegment,
    TranscriptLanguage,
    TranscriptResult,
)
from utils.transcript_utils import (
    format_reading_mode,
    format_timestamp_mode,
    format_srt,
    format_vtt,
    calculate_transcript_statistics,
)

logger = logging.getLogger(__name__)


# =============================================================================
# Custom Domain Exceptions
# =============================================================================

class TranscriptServiceError(Exception):
    """Base exception for transcript service failures."""

    def __init__(self, user_message: str, technical_details: Optional[str] = None):
        super().__init__(user_message)
        self.user_message = user_message
        self.technical_details = technical_details or user_message


class TranscriptDisabledError(TranscriptServiceError):
    """Raised when subtitles/transcripts are disabled by the creator or YouTube."""
    pass


class NoTranscriptFoundError(TranscriptServiceError):
    """Raised when no subtitles are found for the video or requested language."""
    pass


class VideoUnavailableError(TranscriptServiceError):
    """Raised when the video is private, deleted, or region/age-restricted."""
    pass


class NetworkConnectionError(TranscriptServiceError):
    """Raised when YouTube cannot be reached or requests fail."""
    pass


class LanguageUnavailableError(TranscriptServiceError):
    """Raised when the requested language is not available."""
    pass


# Alias for backward compatibility
TranscriptError = TranscriptServiceError


# =============================================================================
# Transcript Service
# =============================================================================

class TranscriptService:
    """Service for querying and extracting YouTube transcripts."""

    @staticmethod
    def _get_api():
        """Instantiate or get YouTubeTranscriptApi safely across library versions."""
        try:
            return YouTubeTranscriptApi()
        except (TypeError, AttributeError):
            return YouTubeTranscriptApi

    @classmethod
    def _get_transcript_list(cls, video_id: str) -> Any:
        """Call list / list_transcripts using the appropriate API method."""
        api = cls._get_api()
        if hasattr(api, "list"):
            return api.list(video_id)
        if hasattr(api, "list_transcripts"):
            return api.list_transcripts(video_id)
        if hasattr(YouTubeTranscriptApi, "list_transcripts"):
            return YouTubeTranscriptApi.list_transcripts(video_id)
        raise RuntimeError("Compatible transcript listing method not found.")

    @classmethod
    def get_available_transcripts(cls, video_id: str) -> List[TranscriptLanguage]:
        """
        Fetch all available subtitle tracks for a YouTube video.

        Returns:
            List of TranscriptLanguage objects (manual first, then auto-generated).
        """
        logger.info("Listing available transcripts for video ID: %s", video_id)
        try:
            transcript_list = cls._get_transcript_list(video_id)

            languages: List[TranscriptLanguage] = []
            for t in transcript_list:
                languages.append(
                    TranscriptLanguage(
                        language=t.language,
                        language_code=t.language_code,
                        is_generated=t.is_generated,
                        is_translatable=getattr(t, "is_translatable", False),
                    )
                )

            # Sort: Manual tracks first, then alphabetical by language name
            languages.sort(key=lambda lang: (lang.is_generated, lang.language.lower()))
            logger.info("Found %d transcript track(s) for video %s", len(languages), video_id)
            return languages

        except TranscriptsDisabled as exc:
            logger.warning("Transcripts disabled for %s: %s", video_id, str(exc))
            raise TranscriptDisabledError(
                "The creator or YouTube has disabled transcript access for this video.",
                str(exc),
            ) from exc
        except (NoTranscriptFound, InvalidVideoId) as exc:
            logger.warning("No transcript found or invalid video ID %s: %s", video_id, str(exc))
            raise NoTranscriptFoundError(
                "This YouTube video does not currently have an accessible transcript.",
                str(exc),
            ) from exc
        except (VideoUnavailable, AgeRestricted) as exc:
            logger.warning("Video unavailable for %s: %s", video_id, str(exc))
            raise VideoUnavailableError(
                "The video may be private, removed, age-restricted, or unavailable in your region.",
                str(exc),
            ) from exc
        except (CouldNotRetrieveTranscript, YouTubeRequestFailed) as exc:
            logger.warning("Connection error retrieving transcripts for %s: %s", video_id, str(exc))
            raise NetworkConnectionError(
                "We couldn't retrieve the transcript right now. Please check your connection and try again.",
                str(exc),
            ) from exc
        except TranscriptServiceError:
            raise
        except Exception as exc:
            logger.exception("Unexpected error while querying transcripts for %s", video_id)
            raise TranscriptServiceError(
                "An unexpected error occurred while checking transcripts for this video.",
                str(exc),
            ) from exc

    @classmethod
    def get_transcript(
        cls, video_id: str, language_code: Optional[str] = None
    ) -> TranscriptResult:
        """
        Extract the transcript for the specified video and language.
        If language_code is None, automatically prefers manual over auto-generated.

        Returns:
            TranscriptResult with formatted reading, timestamped, SRT, and VTT versions.
        """
        logger.info(
            "Fetching transcript for video ID: %s (language_code=%s)",
            video_id,
            language_code,
        )

        try:
            transcript_list = cls._get_transcript_list(video_id)
            chosen_transcript = None

            if language_code:
                # Search for the requested language
                for t in transcript_list:
                    if t.language_code.lower() == language_code.lower():
                        chosen_transcript = t
                        break

                if not chosen_transcript:
                    raise LanguageUnavailableError(
                        f"The selected language ('{language_code}') is not available for this video."
                    )
            else:
                # Preference: First manual transcript, then first generated transcript
                manual_transcripts = [t for t in transcript_list if not t.is_generated]
                if manual_transcripts:
                    chosen_transcript = manual_transcripts[0]
                else:
                    generated_transcripts = [t for t in transcript_list if t.is_generated]
                    if generated_transcripts:
                        chosen_transcript = generated_transcripts[0]

            if not chosen_transcript:
                raise NoTranscriptFoundError(
                    "This YouTube video does not currently have an accessible transcript."
                )

            # Fetch the actual snippets
            raw_snippets = chosen_transcript.fetch()
            segments: List[TranscriptSegment] = []

            for item in raw_snippets:
                # Handle both dataclass / object attributes and dictionary keys
                if hasattr(item, "text"):
                    text = item.text
                    start = float(item.start)
                    duration = float(item.duration)
                else:
                    text = str(item.get("text", ""))
                    start = float(item.get("start", 0.0))
                    duration = float(item.get("duration", 0.0))

                segments.append(
                    TranscriptSegment(
                        text=text,
                        start=start,
                        duration=duration,
                    )
                )

            # Calculate stats and formatted versions
            stats = calculate_transcript_statistics(segments)
            reading_text = format_reading_mode(segments)
            timestamped_text = format_timestamp_mode(segments)
            srt_text = format_srt(segments)
            vtt_text = format_vtt(segments)

            logger.info(
                "Successfully extracted transcript for %s: %d segments, %d words, duration %s (type=%s)",
                video_id,
                stats["total_segments"],
                stats["total_words"],
                stats["duration_formatted"],
                "Auto-generated" if chosen_transcript.is_generated else "Manual",
            )

            return TranscriptResult(
                video_id=video_id,
                language=chosen_transcript.language,
                language_code=chosen_transcript.language_code,
                is_generated=chosen_transcript.is_generated,
                segments=segments,
                total_duration=stats["duration_seconds"],
                word_count=stats["total_words"],
                segment_count=stats["total_segments"],
                reading_text=reading_text,
                timestamped_text=timestamped_text,
                srt_text=srt_text,
                vtt_text=vtt_text,
            )

        except (
            TranscriptsDisabled,
            NoTranscriptFound,
            VideoUnavailable,
            AgeRestricted,
            CouldNotRetrieveTranscript,
            YouTubeRequestFailed,
            InvalidVideoId,
        ) as exc:
            # Re-map using the common mapping logic in get_available_transcripts
            if isinstance(exc, TranscriptsDisabled):
                raise TranscriptDisabledError(
                    "The creator or YouTube has disabled transcript access for this video.",
                    str(exc),
                ) from exc
            elif isinstance(exc, (VideoUnavailable, AgeRestricted)):
                raise VideoUnavailableError(
                    "The video may be private, removed, age-restricted, or unavailable in your region.",
                    str(exc),
                ) from exc
            elif isinstance(exc, (CouldNotRetrieveTranscript, YouTubeRequestFailed)):
                raise NetworkConnectionError(
                    "We couldn't retrieve the transcript right now. Please check your connection and try again.",
                    str(exc),
                ) from exc
            else:
                raise NoTranscriptFoundError(
                    "This YouTube video does not currently have an accessible transcript.",
                    str(exc),
                ) from exc

        except TranscriptServiceError:
            raise
        except Exception as exc:
            logger.exception("Unexpected error extracting transcript for video %s", video_id)
            raise TranscriptServiceError(
                "An unexpected error occurred while processing the transcript.",
                str(exc),
            ) from exc
