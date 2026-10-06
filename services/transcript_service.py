"""YouTube transcript extraction, language listing, and processing service."""

import os
import html
import re
import logging
import warnings
from typing import List, Optional, Tuple, Any
import requests
import xml.etree.ElementTree as ET

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
# Helper Functions: Proxy and HTTP Session Management
# =============================================================================

def get_configured_proxy_url() -> Optional[str]:
    """
    Retrieve configured proxy URL from Streamlit secrets or system environment variables.
    Supports:
      - st.secrets["YOUTUBE_PROXY"]
      - st.secrets["youtube"]["proxy"]
      - os.environ["YOUTUBE_PROXY"]
      - os.environ["HTTPS_PROXY"]
      - os.environ["HTTP_PROXY"]
    """
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            if "YOUTUBE_PROXY" in st.secrets:
                proxy_val = str(st.secrets["YOUTUBE_PROXY"]).strip()
                if proxy_val:
                    return proxy_val
            if "youtube" in st.secrets and isinstance(st.secrets["youtube"], dict):
                proxy_val = str(st.secrets["youtube"].get("proxy", "")).strip()
                if proxy_val:
                    return proxy_val
    except Exception:
        pass

    env_proxy = os.environ.get("YOUTUBE_PROXY") or os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")
    if env_proxy and env_proxy.strip():
        return env_proxy.strip()

    return None


def create_resilient_session() -> requests.Session:
    """
    Create a requests Session with modern browser headers and configured proxy.
    Browser headers and gzip/deflate support are essential to prevent YouTube
    timedtext servers from throttling or timing out chunked subtitle streams.
    """
    session = requests.Session()
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    })
    proxy_url = get_configured_proxy_url()
    if proxy_url:
        session.proxies.update({
            "http": proxy_url,
            "https": proxy_url,
        })
    return session


# =============================================================================
# Transcript Service
# =============================================================================

class TranscriptService:
    """Service for querying and extracting YouTube transcripts with multi-tier fallback."""

    @classmethod
    def _create_session(cls) -> requests.Session:
        """Create configured HTTP session."""
        return create_resilient_session()

    @classmethod
    def _get_api(cls):
        """Instantiate or get YouTubeTranscriptApi safely across library versions."""
        session = cls._create_session()
        proxy_url = get_configured_proxy_url()

        proxy_config = None
        if proxy_url:
            try:
                from youtube_transcript_api.proxies import GenericProxyConfig
                proxy_config = GenericProxyConfig(http_url=proxy_url, https_url=proxy_url)
            except Exception:
                pass

        try:
            if proxy_config:
                return YouTubeTranscriptApi(proxy_config=proxy_config, http_client=session)
            return YouTubeTranscriptApi(http_client=session)
        except TypeError:
            try:
                if proxy_config:
                    return YouTubeTranscriptApi(proxy_config=proxy_config)
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

    # -------------------------------------------------------------------------
    # InnerTube Android Player Direct API Fallback
    # -------------------------------------------------------------------------

    @classmethod
    def _fetch_innertube_player_data(cls, video_id: str) -> dict:
        """
        Query YouTube's InnerTube Android Player endpoint to retrieve player metadata
        and captionTracks directly without loading the desktop HTML watch page.
        This bypasses datacenter IP blocking commonly encountered on AWS/Streamlit Cloud.
        """
        url = "https://www.youtube.com/youtubei/v1/player?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
        headers = {
            "User-Agent": "com.google.android.youtube/20.10.38 (Linux; U; Android 14) gzip",
            "Content-Type": "application/json",
        }
        payload = {
            "context": {
                "client": {
                    "clientName": "ANDROID",
                    "clientVersion": "20.10.38",
                    "androidSdkVersion": 34,
                }
            },
            "videoId": video_id,
        }
        session = cls._create_session()
        try:
            resp = session.post(url, headers=headers, json=payload, timeout=(10, 25))
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as req_err:
            logger.warning("InnerTube player API request failed for %s: %s", video_id, req_err)
            raise CouldNotRetrieveTranscript(video_id) from req_err

        status = data.get("playabilityStatus", {}).get("status", "")
        if status not in ("OK", ""):
            reason = data.get("playabilityStatus", {}).get("reason", "Video unavailable")
            reason_lower = reason.lower()
            if "private" in reason_lower or "unavailable" in reason_lower or "removed" in reason_lower:
                raise VideoUnavailable(video_id)
            elif "age" in reason_lower:
                raise AgeRestricted(video_id)
            else:
                logger.warning("InnerTube video playability status for %s: %s (%s)", video_id, status, reason)

        return data

    @classmethod
    def _get_innertube_captions_list(cls, video_id: str) -> List[TranscriptLanguage]:
        """
        Extract available subtitle tracks using the InnerTube Android API.
        """
        data = cls._fetch_innertube_player_data(video_id)
        raw_tracks = (
            data.get("captions", {})
            .get("playerCaptionsTracklistRenderer", {})
            .get("captionTracks", [])
        )
        if not raw_tracks:
            raise NoTranscriptFound(video_id, [], None)

        direct_languages: List[TranscriptLanguage] = []
        original_code = None
        original_is_generated = False

        # Identify native spoken language: asr (auto-generated) track indicates detected audio language
        asr_track = next((t for t in raw_tracks if t.get("kind") == "asr"), None)
        if asr_track:
            spoken_code = asr_track.get("languageCode", "").lower()
            matching_manual = next(
                (t for t in raw_tracks if t.get("kind") != "asr" and t.get("languageCode", "").lower() == spoken_code),
                None,
            )
            if matching_manual:
                original_code = spoken_code
                original_is_generated = False
            else:
                original_code = spoken_code
                original_is_generated = True
        elif raw_tracks:
            original_code = raw_tracks[0].get("languageCode", "").lower()
            original_is_generated = raw_tracks[0].get("kind") == "asr"

        for t in raw_tracks:
            code = t.get("languageCode", "").strip()
            name_runs = t.get("name", {}).get("runs", [{}])
            name = name_runs[0].get("text", code) if name_runs else code
            is_gen = t.get("kind") == "asr"
            is_orig = (code.lower() == original_code and is_gen == original_is_generated)

            direct_languages.append(
                TranscriptLanguage(
                    language=name,
                    language_code=code,
                    is_generated=is_gen,
                    is_translatable=True,
                    is_original=is_orig,
                    is_translated=False,
                )
            )

        # Sort: original language first, then manual tracks, then auto tracks
        direct_languages.sort(
            key=lambda lang: (
                not lang.is_original,
                lang.is_generated,
                lang.language.lower(),
            )
        )
        return direct_languages

    @classmethod
    def _get_innertube_transcript(
        cls, video_id: str, language_code: Optional[str] = None
    ) -> TranscriptResult:
        """
        Download and parse transcript snippets directly from InnerTube timedtext stream.
        """
        data = cls._fetch_innertube_player_data(video_id)
        raw_tracks = (
            data.get("captions", {})
            .get("playerCaptionsTracklistRenderer", {})
            .get("captionTracks", [])
        )
        if not raw_tracks:
            raise NoTranscriptFound(video_id, [], None)

        chosen_track = None
        if language_code:
            req_code = language_code.lower()
            candidates = [t for t in raw_tracks if t.get("languageCode", "").lower() == req_code]
            if candidates:
                manual = [t for t in candidates if t.get("kind") != "asr"]
                chosen_track = manual[0] if manual else candidates[0]
            else:
                raise LanguageUnavailableError(
                    f"The selected language ('{language_code}') is not available for this video."
                )
        else:
            # Default to native audio track
            asr_track = next((t for t in raw_tracks if t.get("kind") == "asr"), None)
            if asr_track:
                spoken = asr_track.get("languageCode", "").lower()
                chosen_track = next(
                    (t for t in raw_tracks if t.get("kind") != "asr" and t.get("languageCode", "").lower() == spoken),
                    asr_track,
                )
            else:
                chosen_track = raw_tracks[0]

        base_url = chosen_track.get("baseUrl")
        if not base_url:
            raise NoTranscriptFound(video_id, [], None)

        session = cls._create_session()
        try:
            # Subtitle download can be over 1MB on multi-hour videos; allow up to 45s read timeout
            cap_resp = session.get(base_url, timeout=(10, 45))
            cap_resp.raise_for_status()
        except requests.RequestException as req_err:
            logger.warning("InnerTube caption stream download failed for %s: %s", video_id, req_err)
            raise CouldNotRetrieveTranscript(video_id) from req_err

        # Parse XML content (supports both format 3 / srv3 and standard format 1 XML)
        try:
            root = ET.fromstring(cap_resp.content)
        except ET.ParseError as pe:
            logger.error("Failed to parse caption XML for %s: %s", video_id, pe)
            raise CouldNotRetrieveTranscript(video_id) from pe

        segments: List[TranscriptSegment] = []
        p_tags = root.findall(".//p")
        if p_tags:
            # Format 3 (<p t="milliseconds" d="milliseconds"><s>text</s></p>)
            for p in p_tags:
                t_attr = p.attrib.get("t")
                d_attr = p.attrib.get("d", "0")
                if t_attr is None:
                    continue
                start = float(t_attr) / 1000.0
                duration = float(d_attr) / 1000.0
                text = html.unescape("".join(p.itertext())).strip()
                if text:
                    segments.append(TranscriptSegment(text=text, start=start, duration=duration))
        else:
            # Format 1 (<text start="seconds" dur="seconds">text</text>)
            text_tags = root.findall(".//text")
            for elem in text_tags:
                start = float(elem.attrib.get("start", 0.0))
                duration = float(elem.attrib.get("dur", 0.0))
                text = html.unescape("".join(elem.itertext())).strip()
                if text:
                    segments.append(TranscriptSegment(text=text, start=start, duration=duration))

        if not segments:
            raise NoTranscriptFound(video_id, [], None)

        lang_code = chosen_track.get("languageCode", language_code or "en")
        name_runs = chosen_track.get("name", {}).get("runs", [{}])
        lang_name = name_runs[0].get("text", lang_code) if name_runs else lang_code
        is_gen = chosen_track.get("kind") == "asr"

        stats = calculate_transcript_statistics(segments)
        reading_text = format_reading_mode(segments)
        timestamped_text = format_timestamp_mode(segments)
        srt_text = format_srt(segments)
        vtt_text = format_vtt(segments)

        return TranscriptResult(
            video_id=video_id,
            language=lang_name,
            language_code=lang_code,
            is_generated=is_gen,
            segments=segments,
            total_duration=stats["duration_seconds"],
            word_count=stats["total_words"],
            segment_count=stats["total_segments"],
            reading_text=reading_text,
            timestamped_text=timestamped_text,
            srt_text=srt_text,
            vtt_text=vtt_text,
        )

    # -------------------------------------------------------------------------
    # Public Methods
    # -------------------------------------------------------------------------

    @classmethod
    def get_available_transcripts(cls, video_id: str) -> List[TranscriptLanguage]:
        """
        Fetch all available subtitle tracks for a YouTube video.
        Identifies the actual original spoken language of the video and places it first.
        Falls back to InnerTube Android API if standard desktop endpoint is blocked.
        """
        logger.info("Listing available transcripts for video ID: %s", video_id)
        try:
            transcript_list = cls._get_transcript_list(video_id)

            # 1. Detect actual spoken language of the video
            generated_tracks = [t for t in transcript_list if t.is_generated]
            manual_tracks = [t for t in transcript_list if not t.is_generated]

            original_code = None
            original_is_generated = False

            if generated_tracks:
                spoken_code = generated_tracks[0].language_code.lower()
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
                    not lang.is_original,
                    lang.is_generated,
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
            logger.warning(
                "Standard API connection issue for %s: %s. Attempting InnerTube fallback...",
                video_id,
                str(exc),
            )
            try:
                return cls._get_innertube_captions_list(video_id)
            except Exception as fb_exc:
                logger.warning("InnerTube fallback also failed for %s: %s", video_id, str(fb_exc))
                raise NetworkConnectionError(
                    "We couldn't retrieve the transcript right now. Please check your connection and try again. "
                    "If hosted on Streamlit Cloud, YouTube may be rate-limiting cloud IP addresses (configure YOUTUBE_PROXY in secrets to resolve).",
                    f"Standard: {exc} | Fallback: {fb_exc}",
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
        Falls back to InnerTube Android API if standard desktop endpoint is blocked.

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

        except (TranscriptsDisabled, VideoUnavailable, AgeRestricted, InvalidVideoId, LanguageUnavailableError):
            raise
        except (CouldNotRetrieveTranscript, YouTubeRequestFailed) as exc:
            logger.warning(
                "Standard API connection issue extracting %s: %s. Attempting InnerTube fallback...",
                video_id,
                str(exc),
            )
            try:
                return cls._get_innertube_transcript(video_id, language_code)
            except Exception as fb_exc:
                logger.warning("InnerTube fallback also failed for %s: %s", video_id, str(fb_exc))
                raise NetworkConnectionError(
                    "We couldn't retrieve the transcript right now. Please check your connection and try again. "
                    "If hosted on Streamlit Cloud, YouTube may be rate-limiting cloud IP addresses (configure YOUTUBE_PROXY in secrets to resolve).",
                    f"Standard: {exc} | Fallback: {fb_exc}",
                ) from exc
        except NoTranscriptFound as exc:
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
