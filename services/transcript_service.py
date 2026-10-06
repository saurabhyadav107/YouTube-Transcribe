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
        Identifies the actual original spoken language of the video and places it first.
        """
        logger.info("Listing available transcripts for video ID: %s", video_id)
        try:
            transcript_list = cls._get_transcript_list(video_id)

            # 1. Detect actual spoken language of the video
            # YouTube Automatic Speech Recognition creates generated tracks strictly in the spoken language
            generated_tracks = [t for t in transcript_list if t.is_generated]
            manual_tracks = [t for t in transcript_list if not t.is_generated]

            original_code = None
            original_is_generated = False

            if generated_tracks:
                # The auto-generated track language code indicates YouTube's detected audio language
                spoken_code = generated_tracks[0].language_code.lower()
                # Check if a manual transcript was provided by the creator in that same native language
                matching_manual = next(
                    (t for t in manual_tracks if t.language_code.lower() == spoken_code),
                    None,
                )
                if matching_manual:
                    original_code = matching_manual.language_code.lower()
                    original_is_generated = False
                else:
                    original_code = spoken_code
                    original_is_generated = True
            elif manual_tracks:
                # If only manual tracks exist, the first uploaded manual track is typically the original language
                original_code = manual_tracks[0].language_code.lower()
                original_is_generated = False

            direct_languages: List[TranscriptLanguage] = []
            seen_codes = set()

            for t in transcript_list:
                t_code = t.language_code.lower()
                is_orig = (t_code == original_code and t.is_generated == original_is_generated)
                direct_languages.append(
                    TranscriptLanguage(
                        language=t.language,
                        language_code=t.language_code,
                        is_generated=t.is_generated,
                        is_translatable=getattr(t, "is_translatable", False),
                        is_original=is_orig,
                        is_translated=False,
                    )
                )
                seen_codes.add(t_code)

            # Sort direct tracks: Original video language FIRST, then other manual tracks, then auto tracks
            direct_languages.sort(
                key=lambda lang: (
                    not lang.is_original,  # True (not original) goes after False (original)
                    lang.is_generated,      # Manual before auto
                    lang.language.lower(),
                )
            )

            # 2. Add common translation tracks if original transcript is translatable
            translatable_base = next((t for t in transcript_list if getattr(t, "is_translatable", False)), None)
            translated_languages: List[TranscriptLanguage] = []

            if translatable_base and hasattr(translatable_base, "translation_languages"):
                popular_translation_codes = [
                    "en", "es", "hi", "fr", "de", "ja", "ko", "zh-Hans", "ar", "ru", "pt", "it"
                ]
                trans_dict = {
                    tl.language_code.lower(): tl.language
                    for tl in getattr(translatable_base, "translation_languages", [])
                }
                for code in popular_translation_codes:
                    if code.lower() in trans_dict and code.lower() not in seen_codes:
                        translated_languages.append(
                            TranscriptLanguage(
                                language=trans_dict[code.lower()],
                                language_code=code,
                                is_generated=True,
                                is_translatable=False,
                                is_original=False,
                                is_translated=True,
                            )
                        )
                        seen_codes.add(code.lower())

                translated_languages.sort(key=lambda lang: lang.language.lower())

            all_languages = direct_languages + translated_languages
            logger.info("Identified %d total track(s) (original: %s) for %s", len(all_languages), original_code, video_id)
            return all_languages

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
        If language_code is None, automatically selects the actual original language of the video.

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
                req_code = language_code.lower()
                # 1. Search for a direct transcript track (prefer manual over generated if both exist)
                candidates = [t for t in transcript_list if t.language_code.lower() == req_code]
                if candidates:
                    manual = [t for t in candidates if not t.is_generated]
                    chosen_transcript = manual[0] if manual else candidates[0]
                else:
                    # 2. Check if a base transcript can be translated
                    translatable_base = next(
                        (t for t in transcript_list if getattr(t, "is_translatable", False)),
                        None,
                    )
                    if translatable_base and hasattr(translatable_base, "translate"):
                        try:
                            chosen_transcript = translatable_base.translate(language_code)
                        except Exception as trans_err:
                            logger.warning("Translation to %s failed: %s", language_code, trans_err)
                            chosen_transcript = None

                if not chosen_transcript:
                    raise LanguageUnavailableError(
                        f"The selected language ('{language_code}') is not available for this video."
                    )
            else:
                # Default to actual original language:
                available_langs = cls.get_available_transcripts(video_id)
                if available_langs:
                    best_code = available_langs[0].language_code
                    return cls.get_transcript(video_id, language_code=best_code)
                else:
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
