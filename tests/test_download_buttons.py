"""Tests for bottom dashboard action buttons and timestamp-free downloads."""

import base64
import re
from unittest.mock import MagicMock, patch
import pytest

from models.transcript_models import TranscriptResult, VideoMetadata, TranscriptSegment
from ui.components import render_bottom_dashboard


@pytest.fixture
def sample_result():
    segments = [
        TranscriptSegment(text="Hello everyone and welcome.", start=0.0, duration=3.5),
        TranscriptSegment(text="Today we build an AI application.", start=3.5, duration=4.0),
        TranscriptSegment(text="Let us begin with step one.", start=7.5, duration=3.0),
    ]
    return TranscriptResult(
        video_id="test12345",
        language="English",
        language_code="en",
        is_generated=False,
        segments=segments,
        total_duration=10.5,
        word_count=15,
        segment_count=3,
        reading_text="Hello everyone and welcome. Today we build an AI application. Let us begin with step one.",
        timestamped_text="[00:00] Hello everyone and welcome.\n[00:03] Today we build an AI application.\n[00:07] Let us begin with step one.",
        srt_text="1\n00:00:00,000 --> 00:00:03,500\nHello everyone and welcome.\n\n2\n00:00:03,500 --> 00:00:07,500\nToday we build an AI application.\n\n3\n00:00:07,500 --> 00:00:10,500\nLet us begin with step one.",
        vtt_text="WEBVTT\n\n00:00:00.000 --> 00:00:03.500\nHello everyone and welcome.\n\n00:00:03.500 --> 00:00:07.500\nToday we build an AI application.\n\n00:00:07.500 --> 00:00:10.500\nLet us begin with step one.",
    )


@pytest.fixture
def sample_metadata():
    return VideoMetadata(
        video_id="test12345",
        title="Sample YouTube Video Tutorial",
        url="https://www.youtube.com/watch?v=test12345",
        channel="Tech Channel",
        duration_seconds=10.5,
    )


def test_render_bottom_dashboard_no_timestamps_in_txt_download(sample_result, sample_metadata):
    """Verify that TXT download uses reading_text with zero timestamps."""
    download_calls = []

    def mock_download_button(label, data, file_name, mime, **kwargs):
        download_calls.append({"label": label, "data": data, "file_name": file_name, "mime": mime})
        return False

    with patch("streamlit.columns") as mock_columns, \
         patch("streamlit.container"), \
         patch("streamlit.download_button", side_effect=mock_download_button), \
         patch("streamlit.components.v1.html") as mock_html_comp:

        # Setup mock columns returns
        col_mock = MagicMock()
        col_mock.download_button = mock_download_button
        def fake_columns(spec, **kwargs):
            if isinstance(spec, (list, tuple)) and len(spec) == 2:
                return [col_mock, col_mock]
            return [col_mock, col_mock, col_mock, col_mock]
        mock_columns.side_effect = fake_columns

        render_bottom_dashboard(sample_result, sample_metadata)

        # Check that mock_html_comp (the copy button) was called
        assert mock_html_comp.called
        html_args = mock_html_comp.call_args[0][0]

        # Extract base64 text from copy button html
        b64_match = re.search(r'b64DecodeUnicode\("([^"]+)"\)', html_args)
        assert b64_match is not None, "Base64 payload should be present in copy button"
        decoded_text = base64.b64decode(b64_match.group(1)).decode("utf-8")

        # Verify NO timestamps in copied text
        assert not re.search(r"\[\d{2}:\d{2}", decoded_text), "Copied text must not contain timestamps"
        assert "Hello everyone and welcome." in decoded_text

        # Verify TXT download call
        txt_downloads = [c for c in download_calls if c["label"] == "Download TXT"]
        assert len(txt_downloads) == 1
        txt_data = txt_downloads[0]["data"]

        # Critical check: zero timestamps in downloaded TXT data
        assert not re.search(r"\[\d{2}:\d{2}", txt_data), "TXT download must not contain timestamps"
        assert not re.search(r"\d{2}:\d{2}", txt_data), "TXT download must not contain any timestamp digits"
        assert txt_data == sample_result.reading_text

        # Verify SRT and VTT downloads exist
        srt_downloads = [c for c in download_calls if c["label"] == "Download SRT"]
        assert len(srt_downloads) == 1
        assert "00:00:00,000 -->" in srt_downloads[0]["data"]

        vtt_downloads = [c for c in download_calls if c["label"] == "Download VTT"]
        assert len(vtt_downloads) == 1
        assert "WEBVTT" in vtt_downloads[0]["data"]
