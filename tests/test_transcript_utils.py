"""Unit tests for transcript formatting, timestamps, SRT, VTT, and statistics."""

import pytest
from models.transcript_models import TranscriptSegment
from utils.transcript_utils import (
    format_seconds_to_timestamp,
    format_seconds_to_srt_time,
    format_seconds_to_vtt_time,
    format_reading_mode,
    format_timestamp_mode,
    format_srt,
    format_vtt,
    calculate_transcript_statistics,
)


class TestTimestampFormatting:
    """Test timestamp conversion functions."""

    def test_format_seconds_to_timestamp(self):
        assert format_seconds_to_timestamp(0) == "00:00"
        assert format_seconds_to_timestamp(4.2) == "00:04"
        assert format_seconds_to_timestamp(65) == "01:05"
        assert format_seconds_to_timestamp(3600) == "01:00:00"
        assert format_seconds_to_timestamp(5076) == "01:24:36"
        assert format_seconds_to_timestamp(12, force_hours=True) == "00:00:12"
        assert format_seconds_to_timestamp(-5) == "00:00"

    def test_format_seconds_to_srt_time(self):
        assert format_seconds_to_srt_time(0) == "00:00:00,000"
        assert format_seconds_to_srt_time(4.25) == "00:00:04,250"
        assert format_seconds_to_srt_time(65.123) == "00:01:05,123"
        assert format_seconds_to_srt_time(3661.005) == "01:01:01,005"

    def test_format_seconds_to_vtt_time(self):
        assert format_seconds_to_vtt_time(0) == "00:00:00.000"
        assert format_seconds_to_vtt_time(4.25) == "00:00:04.250"
        assert format_seconds_to_vtt_time(65.123) == "00:01:05.123"
        assert format_seconds_to_vtt_time(3661.005) == "01:01:01.005"


class TestTranscriptFormatting:
    """Test reading mode, timestamp mode, SRT, and VTT."""

    @pytest.fixture
    def sample_segments(self):
        return [
            TranscriptSegment(text="Hello everyone.", start=0.0, duration=4.0),
            TranscriptSegment(text="Welcome to this video.", start=4.0, duration=4.0),
            TranscriptSegment(text="Today we are going to discuss...", start=8.0, duration=5.0),
        ]

    def test_empty_transcript(self):
        assert format_reading_mode([]) == ""
        assert format_timestamp_mode([]) == ""
        assert format_srt([]) == ""
        assert format_vtt([]) == "WEBVTT\n"

    def test_single_segment(self):
        seg = [TranscriptSegment(text="Just one segment.", start=2.5, duration=3.0)]
        reading = format_reading_mode(seg)
        assert reading == "Just one segment."

        timestamped = format_timestamp_mode(seg)
        assert timestamped == "[00:02] Just one segment."

        srt = format_srt(seg)
        assert "1\n00:00:02,500 --> 00:00:05,500\nJust one segment." in srt

        vtt = format_vtt(seg)
        assert "WEBVTT" in vtt
        assert "00:00:02.500 --> 00:00:05.500\nJust one segment." in vtt

    def test_multiple_segments(self, sample_segments):
        timestamped = format_timestamp_mode(sample_segments)
        expected_lines = [
            "[00:00] Hello everyone.",
            "[00:04] Welcome to this video.",
            "[00:08] Today we are going to discuss...",
        ]
        assert timestamped == "\n".join(expected_lines)

        reading = format_reading_mode(sample_segments)
        assert "Hello everyone. Welcome to this video. Today we are going to discuss..." in reading

        srt = format_srt(sample_segments)
        assert "1\n00:00:00,000 --> 00:00:04,000\nHello everyone." in srt
        assert "2\n00:00:04,000 --> 00:00:08,000\nWelcome to this video." in srt
        assert "3\n00:00:08,000 --> 00:00:13,000\nToday we are going to discuss..." in srt

    def test_long_transcript_paragraphing(self):
        # Create 50 segments
        segments = [
            TranscriptSegment(
                text=f"Sentence number {i} in the presentation.",
                start=float(i * 3),
                duration=3.0,
            )
            for i in range(50)
        ]
        reading = format_reading_mode(segments)
        paragraphs = reading.split("\n\n")
        assert len(paragraphs) > 1  # Verify it is broken into readable paragraphs
        assert len(paragraphs[0].split()) >= 60

    def test_hours_timestamp_mode(self):
        segments = [
            TranscriptSegment(text="Early segment.", start=10.0, duration=2.0),
            TranscriptSegment(text="Late segment past hour.", start=3665.0, duration=4.0),
        ]
        timestamped = format_timestamp_mode(segments)
        assert "[00:00:10] Early segment." in timestamped
        assert "[01:01:05] Late segment past hour." in timestamped


class TestTranscriptStatistics:
    """Test statistics calculation."""

    def test_empty_segments_stats(self):
        stats = calculate_transcript_statistics([])
        assert stats["total_words"] == 0
        assert stats["total_segments"] == 0
        assert stats["duration_seconds"] == 0.0
        assert stats["duration_formatted"] == "00:00"

    def test_calculated_stats(self):
        segments = [
            TranscriptSegment(text="Hello beautiful world.", start=0.0, duration=5.0),
            TranscriptSegment(text="This is an automated test transcript.", start=5.0, duration=5.5),
        ]
        stats = calculate_transcript_statistics(segments)
        assert stats["total_segments"] == 2
        assert stats["total_words"] == 3 + 6  # 9 words
        assert stats["duration_seconds"] == 10.5
        assert stats["duration_formatted"] == "00:10"
