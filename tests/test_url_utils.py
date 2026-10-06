"""Unit tests for YouTube URL parsing and validation."""

import pytest
from utils.url_utils import extract_video_id, validate_youtube_url, build_canonical_url


class TestUrlExtraction:
    """Test video ID extraction across various YouTube URL formats."""

    @pytest.mark.parametrize(
        "url, expected_id",
        [
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("http://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://m.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/watch?feature=shared&v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("http://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://youtu.be/dQw4w9WgXcQ?t=12", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/shorts/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://youtube.com/shorts/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/v/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/live/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("dQw4w9WgXcQ", "dQw4w9WgXcQ"),  # Raw 11-char ID
            ("  https://youtu.be/dQw4w9WgXcQ  ", "dQw4w9WgXcQ"),  # Trim whitespace
        ],
    )
    def test_valid_youtube_urls(self, url: str, expected_id: str):
        assert extract_video_id(url) == expected_id

    @pytest.mark.parametrize(
        "invalid_input",
        [
            "",
            "   ",
            None,
            "https://www.google.com",
            "https://vimeo.com/12345678",
            "https://youtube.com",
            "https://youtube.com/watch",
            "https://youtube.com/watch?v=tooshort",
            "https://youtu.be/",
            "not-a-valid-url-or-id",
        ],
    )
    def test_invalid_urls(self, invalid_input):
        assert extract_video_id(invalid_input) is None


class TestUrlValidation:
    """Test validate_youtube_url helper."""

    def test_empty_url(self):
        is_valid, video_id, err = validate_youtube_url("")
        assert is_valid is False
        assert video_id is None
        assert "Please enter a YouTube video URL" in err

    def test_whitespace_url(self):
        is_valid, video_id, err = validate_youtube_url("   ")
        assert is_valid is False
        assert video_id is None
        assert "Please enter a YouTube video URL" in err

    def test_none_url(self):
        is_valid, video_id, err = validate_youtube_url(None)
        assert is_valid is False
        assert video_id is None
        assert "Please enter a YouTube video URL" in err

    def test_invalid_url(self):
        is_valid, video_id, err = validate_youtube_url("https://example.com/video")
        assert is_valid is False
        assert video_id is None
        assert "Invalid YouTube URL" in err

    def test_valid_url(self):
        is_valid, video_id, err = validate_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        assert is_valid is True
        assert video_id == "dQw4w9WgXcQ"
        assert err is None


def test_build_canonical_url():
    assert build_canonical_url("dQw4w9WgXcQ") == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
