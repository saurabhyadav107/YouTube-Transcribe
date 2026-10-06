"""Transcript formatting, timestamp conversion, and statistics calculation."""

import re
from typing import List, Dict, Any
from models.transcript_models import TranscriptSegment


def format_seconds_to_timestamp(seconds: float, force_hours: bool = False) -> str:
    """
    Format seconds into MM:SS or HH:MM:SS string.

    Examples:
        5.0 -> '00:05'
        65.0 -> '01:05'
        3665.0 -> '01:01:05'
    """
    if seconds < 0:
        seconds = 0.0

    total_seconds = int(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60

    if hours > 0 or force_hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def format_seconds_to_srt_time(seconds: float) -> str:
    """
    Format seconds to SRT timestamp format: HH:MM:SS,mmm

    Example:
        12.345 -> '00:00:12,345'
    """
    if seconds < 0:
        seconds = 0.0

    total_millis = int(round(seconds * 1000))
    hours = total_millis // 3_600_000
    minutes = (total_millis % 3_600_000) // 60_000
    secs = (total_millis % 60_000) // 1000
    millis = total_millis % 1000

    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def format_seconds_to_vtt_time(seconds: float) -> str:
    """
    Format seconds to WebVTT timestamp format: HH:MM:SS.mmm

    Example:
        12.345 -> '00:00:12.345'
    """
    if seconds < 0:
        seconds = 0.0

    total_millis = int(round(seconds * 1000))
    hours = total_millis // 3_600_000
    minutes = (total_millis % 3_600_000) // 60_000
    secs = (total_millis % 60_000) // 1000
    millis = total_millis % 1000

    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def clean_text_spacing(text: str) -> str:
    """Remove redundant spaces and normalize newlines."""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def format_reading_mode(segments: List[TranscriptSegment]) -> str:
    """
    Format transcript segments into clean, readable paragraphs without timestamps.

    Groups sentences naturally into paragraphs (approx every 4-6 sentences or 60-90 words).
    """
    if not segments:
        return ""

    paragraphs: List[str] = []
    current_sentences: List[str] = []
    word_count_in_para = 0

    for seg in segments:
        cleaned = clean_text_spacing(seg.text)
        if not cleaned:
            continue

        current_sentences.append(cleaned)
        word_count_in_para += len(cleaned.split())

        # Create paragraph break after punctuation if paragraph has accumulated sufficient words
        ends_with_sentence_terminator = bool(re.search(r"[.!?…]$", cleaned))
        if ends_with_sentence_terminator and word_count_in_para >= 65:
            paragraphs.append(" ".join(current_sentences))
            current_sentences = []
            word_count_in_para = 0

    if current_sentences:
        paragraphs.append(" ".join(current_sentences))

    return "\n\n".join(paragraphs)


def format_timestamp_mode(segments: List[TranscriptSegment]) -> str:
    """
    Format transcript segments with timestamps.

    Example:
        [00:00] Hello everyone.
        [00:04] Welcome to this video.
    """
    if not segments:
        return ""

    # Check if max time exceeds 1 hour to format timestamps uniformly
    max_time = max((s.start for s in segments), default=0.0)
    force_hours = max_time >= 3600

    lines: List[str] = []
    for seg in segments:
        cleaned = clean_text_spacing(seg.text)
        if not cleaned:
            continue
        timestamp = format_seconds_to_timestamp(seg.start, force_hours=force_hours)
        lines.append(f"[{timestamp}] {cleaned}")

    return "\n".join(lines)


def format_srt(segments: List[TranscriptSegment]) -> str:
    """
    Format transcript into SubRip (.srt) subtitle format.
    """
    if not segments:
        return ""

    entries: List[str] = []
    index = 1

    for seg in segments:
        cleaned = clean_text_spacing(seg.text)
        if not cleaned:
            continue

        start_str = format_seconds_to_srt_time(seg.start)
        end_str = format_seconds_to_srt_time(seg.end)

        entries.append(f"{index}\n{start_str} --> {end_str}\n{cleaned}\n")
        index += 1

    return "\n".join(entries).strip() + "\n"


def format_vtt(segments: List[TranscriptSegment]) -> str:
    """
    Format transcript into WebVTT (.vtt) subtitle format.
    """
    if not segments:
        return "WEBVTT\n"

    entries: List[str] = ["WEBVTT\n"]

    for seg in segments:
        cleaned = clean_text_spacing(seg.text)
        if not cleaned:
            continue

        start_str = format_seconds_to_vtt_time(seg.start)
        end_str = format_seconds_to_vtt_time(seg.end)

        entries.append(f"{start_str} --> {end_str}\n{cleaned}\n")

    return "\n".join(entries).strip() + "\n"


def calculate_transcript_statistics(segments: List[TranscriptSegment]) -> Dict[str, Any]:
    """
    Compute actual statistics from transcript segments.
    """
    if not segments:
        return {
            "total_words": 0,
            "total_segments": 0,
            "duration_seconds": 0.0,
            "duration_formatted": "00:00",
        }

    total_segments = len(segments)
    total_words = sum(len(clean_text_spacing(s.text).split()) for s in segments if s.text.strip())

    last_segment = max(segments, key=lambda s: s.end)
    duration_seconds = max(last_segment.end, 0.0)
    duration_formatted = format_seconds_to_timestamp(
        duration_seconds, force_hours=duration_seconds >= 3600
    )

    return {
        "total_words": total_words,
        "total_segments": total_segments,
        "duration_seconds": duration_seconds,
        "duration_formatted": duration_formatted,
    }
