"""Unit tests for filename sanitization and safe file naming."""

import pytest
from utils.file_utils import sanitize_filename


class TestFilenameSanitization:
    """Test filename sanitization against disallowed and special characters."""

    @pytest.mark.parametrize(
        "title, expected_contains",
        [
            ("My Amazing YouTube Video", "my-amazing-youtube-video"),
            ('Video with / and \\ and : and *', "video-with-and-and-and"),
            ('Question? "Quote" <Less> >More< |Pipe|', "question-quote-less-more-pipe"),
            ("Special Characters: #1 @2 $3 %4 &5!", "special-characters-1-2-3-4-5"),
        ],
    )
    def test_illegal_characters_removed(self, title: str, expected_contains: str):
        sanitized = sanitize_filename(title)
        # Verify disallowed characters are gone
        for illegal in [r"/", "\\", ":", "*", "?", '"', "<", ">", "|"]:
            assert illegal not in sanitized
        assert expected_contains in sanitized

    def test_empty_and_whitespace_title(self):
        assert sanitize_filename("") == "youtube-transcript-transcript"
        assert sanitize_filename("   ", fallback="custom-fallback") == "custom-fallback-transcript"
        assert sanitize_filename("   ", suffix="") == "youtube-transcript"

    def test_unicode_normalization(self):
        title = "Café & Naïve Résumé"
        sanitized = sanitize_filename(title)
        assert "cafe" in sanitized
        assert "resume" in sanitized

    def test_max_length_truncation(self):
        long_title = "a" * 150
        sanitized = sanitize_filename(long_title, max_length=50)
        # Should be truncated to 50 chars plus suffix
        assert len(sanitized) <= 50 + len("-transcript")

    def test_windows_reserved_names(self):
        assert sanitize_filename("CON") == "con-safe-transcript"
        assert sanitize_filename("NUL") == "nul-safe-transcript"
        assert sanitize_filename("CON", suffix="") == "con-safe"
