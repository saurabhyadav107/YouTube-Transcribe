"""Unit tests for YouTubeService and TranscriptService using mocks."""

from unittest.mock import patch, MagicMock
import pytest
from requests.exceptions import RequestException
from youtube_transcript_api import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
    CouldNotRetrieveTranscript,
)

from services.youtube_service import YouTubeService
from services.transcript_service import (
    TranscriptService,
    TranscriptDisabledError,
    NoTranscriptFoundError,
    VideoUnavailableError,
    NetworkConnectionError,
    LanguageUnavailableError,
)
from models.transcript_models import VideoMetadata


class TestYouTubeService:
    """Test YouTubeService metadata retrieval and graceful fallback."""

    @patch("services.youtube_service.requests.get")
    def test_successful_metadata_fetch(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "title": "Awesome Tech Tutorial",
            "author_name": "CodeMaster",
            "thumbnail_url": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
        }
        mock_get.return_value = mock_resp

        metadata = YouTubeService.get_video_metadata("dQw4w9WgXcQ")
        assert metadata.video_id == "dQw4w9WgXcQ"
        assert metadata.title == "Awesome Tech Tutorial"
        assert metadata.channel == "CodeMaster"
        assert metadata.thumbnail_url == "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg"

    @patch("services.youtube_service.requests.get")
    def test_network_failure_metadata_fallback(self, mock_get):
        mock_get.side_effect = RequestException("Timeout")

        metadata = YouTubeService.get_video_metadata("dQw4w9WgXcQ")
        assert metadata.video_id == "dQw4w9WgXcQ"
        assert metadata.title == "YouTube Video (dQw4w9WgXcQ)"
        assert metadata.channel is None
        assert "hqdefault.jpg" in metadata.thumbnail_url


class TestTranscriptService:
    """Test TranscriptService querying and error mappings with mocks."""

    def _create_mock_transcript(self, lang="English", code="en", is_generated=False, snippets=None):
        mock_t = MagicMock()
        mock_t.language = lang
        mock_t.language_code = code
        mock_t.is_generated = is_generated
        mock_t.is_translatable = False

        if snippets is None:
            snippets = [
                {"text": "Hello world", "start": 0.0, "duration": 2.5},
                {"text": "Welcome to testing", "start": 2.5, "duration": 3.0},
            ]
        mock_t.fetch.return_value = snippets
        return mock_t

    @patch.object(TranscriptService, "_get_transcript_list")
    def test_get_available_transcripts(self, mock_get_list):
        manual_t = self._create_mock_transcript(lang="English", code="en", is_generated=False)
        auto_t = self._create_mock_transcript(lang="Spanish", code="es", is_generated=True)
        mock_get_list.return_value = [auto_t, manual_t]

        available = TranscriptService.get_available_transcripts("dQw4w9WgXcQ")
        assert len(available) == 2
        # Original spoken video language (es) is prioritized and placed first
        assert available[0].language_code == "es"
        assert available[0].is_original is True
        assert available[1].language_code == "en"
        assert available[1].is_original is False

    @patch.object(TranscriptService, "_get_transcript_list")
    def test_original_language_manual_preferred(self, mock_get_list):
        # When creator provided manual track in video's native language (es), prefer manual
        manual_es = self._create_mock_transcript(lang="Spanish", code="es", is_generated=False)
        auto_es = self._create_mock_transcript(lang="Spanish", code="es", is_generated=True)
        manual_en = self._create_mock_transcript(lang="English", code="en", is_generated=False)
        mock_get_list.return_value = [auto_es, manual_es, manual_en]

        available = TranscriptService.get_available_transcripts("dQw4w9WgXcQ")
        assert available[0].language_code == "es"
        assert available[0].is_generated is False
        assert available[0].is_original is True

    @patch.object(TranscriptService, "_get_transcript_list")
    def test_transcripts_disabled_error_mapping(self, mock_get_list):
        mock_get_list.side_effect = TranscriptsDisabled("dQw4w9WgXcQ")
        with pytest.raises(TranscriptDisabledError) as exc_info:
            TranscriptService.get_available_transcripts("dQw4w9WgXcQ")
        assert "disabled" in exc_info.value.user_message.lower()

    @patch.object(TranscriptService, "_get_transcript_list")
    def test_no_transcript_found_error_mapping(self, mock_get_list):
        mock_get_list.side_effect = NoTranscriptFound("dQw4w9WgXcQ", [], None)
        with pytest.raises(NoTranscriptFoundError) as exc_info:
            TranscriptService.get_available_transcripts("dQw4w9WgXcQ")
        assert "not currently have an accessible transcript" in exc_info.value.user_message

    @patch.object(TranscriptService, "_get_transcript_list")
    def test_video_unavailable_error_mapping(self, mock_get_list):
        mock_get_list.side_effect = VideoUnavailable("dQw4w9WgXcQ")
        with pytest.raises(VideoUnavailableError) as exc_info:
            TranscriptService.get_available_transcripts("dQw4w9WgXcQ")
        assert "unavailable" in exc_info.value.user_message.lower()

    @patch.object(TranscriptService, "_get_transcript_list")
    def test_network_connection_error_mapping(self, mock_get_list):
        mock_get_list.side_effect = CouldNotRetrieveTranscript("dQw4w9WgXcQ")
        with pytest.raises(NetworkConnectionError) as exc_info:
            TranscriptService.get_available_transcripts("dQw4w9WgXcQ")
        assert "connection" in exc_info.value.user_message.lower()

    @patch.object(TranscriptService, "_get_transcript_list")
    def test_successful_transcript_extraction(self, mock_get_list):
        manual_t = self._create_mock_transcript(
            lang="English",
            code="en",
            is_generated=False,
            snippets=[
                {"text": "Hello world.", "start": 0.0, "duration": 2.0},
                {"text": "Welcome everyone.", "start": 2.0, "duration": 3.0},
            ],
        )
        mock_get_list.return_value = [manual_t]

        result = TranscriptService.get_transcript("dQw4w9WgXcQ")
        assert result.video_id == "dQw4w9WgXcQ"
        assert result.language == "English"
        assert result.language_code == "en"
        assert result.is_generated is False
        assert result.segment_count == 2
        assert result.word_count == 4
        assert "[00:00] Hello world." in result.timestamped_text
        assert "Hello world. Welcome everyone." in result.reading_text
        assert "00:00:00,000 --> 00:00:02,000" in result.srt_text

    @patch.object(TranscriptService, "_get_transcript_list")
    def test_language_unavailable_error(self, mock_get_list):
        mock_t = self._create_mock_transcript(lang="English", code="en", is_generated=False)
        mock_get_list.return_value = [mock_t]

        with pytest.raises(LanguageUnavailableError) as exc_info:
            TranscriptService.get_transcript("dQw4w9WgXcQ", language_code="fr")
        assert "not available" in exc_info.value.user_message.lower()
