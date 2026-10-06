"""YouTube video metadata retrieval service."""

import logging
import warnings
from typing import Optional
import requests
from requests.exceptions import RequestException

from models.transcript_models import VideoMetadata
from utils.url_utils import build_canonical_url

# Suppress urllib3 version warning if present
try:
    from requests.exceptions import RequestsDependencyWarning
    warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
except ImportError:
    pass

logger = logging.getLogger(__name__)

OEMBED_ENDPOINT = "https://www.youtube.com/oembed"
REQUEST_TIMEOUT_SECONDS = 8


class YouTubeService:
    """Service for interacting with YouTube metadata."""

    @staticmethod
    def get_video_metadata(video_id: str) -> VideoMetadata:
        """
        Fetch public video metadata (title, channel, thumbnail) using YouTube oEmbed API.
        Does not require an API key. Gracefully falls back if unavailable.
        """
        canonical_url = build_canonical_url(video_id)
        default_thumbnail = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

        logger.info("Fetching metadata for video ID: %s", video_id)

        try:
            params = {
                "url": canonical_url,
                "format": "json",
            }
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                )
            }
            response = requests.get(
                OEMBED_ENDPOINT,
                params=params,
                headers=headers,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )

            if response.status_code == 200:
                data = response.json()
                title = data.get("title", f"YouTube Video ({video_id})").strip()
                channel = data.get("author_name", "Unknown Channel").strip()
                thumbnail_url = data.get("thumbnail_url") or default_thumbnail

                logger.info("Successfully retrieved metadata for %s: '%s' by %s", video_id, title, channel)
                return VideoMetadata(
                    video_id=video_id,
                    title=title,
                    channel=channel,
                    thumbnail_url=thumbnail_url,
                    url=canonical_url,
                )
            else:
                logger.warning(
                    "oEmbed endpoint returned status %s for video %s",
                    response.status_code,
                    video_id,
                )
        except RequestException as exc:
            logger.warning("Network error while fetching oEmbed metadata for %s: %s", video_id, str(exc))
        except Exception as exc:
            logger.warning("Unexpected error fetching metadata for %s: %s", video_id, str(exc))

        # Graceful fallback without crashing
        return VideoMetadata(
            video_id=video_id,
            title=f"YouTube Video ({video_id})",
            channel=None,
            thumbnail_url=default_thumbnail,
            url=canonical_url,
        )
