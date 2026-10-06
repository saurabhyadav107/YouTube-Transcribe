"""Modular UI components for the YouTube Transcript Extractor."""

import html
import streamlit as st
import streamlit.components.v1 as components

from models.transcript_models import VideoMetadata, TranscriptResult
from utils.file_utils import sanitize_filename
from utils.transcript_utils import format_seconds_to_timestamp


def render_header() -> None:
    """Render the application header with badge and title."""
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-badge">
                <span>⚡ Instant YouTube Subtitles</span>
            </div>
            <div class="hero-title">🎬 YouTube Transcript Extractor</div>
            <div class="hero-subtitle">
                Extract, read, copy and download transcripts from YouTube videos in seconds.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    """Render a clean, informative sidebar."""
    with st.sidebar:
        st.markdown("### ℹ️ About")
        st.markdown(
            """
            **YouTube Transcript Extractor** retrieves accurate transcripts directly from YouTube's subtitle tracks.

            - **No audio upload required**
            - **No AI hallucination**
            - **Original YouTube subtitles**
            """
        )

        st.divider()

        st.markdown("### ✨ Features")
        st.markdown(
            """
            - 🌐 **Multi-Language Detection**
            - 🎯 **Manual & Auto Captions**
            - 📖 **Reading & Timestamp Modes**
            - 📋 **Instant Clipboard Copy**
            - ⬇️ **TXT, SRT & VTT Exports**
            - 📊 **Word & Segment Metrics**
            """
        )

        st.divider()

        st.markdown("### 🔗 Supported Links")
        st.markdown(
            """
            - `youtube.com/watch?v=...`
            - `youtu.be/...`
            - `youtube.com/shorts/...`
            - `youtube.com/embed/...`
            - `youtube.com/live/...`
            """
        )

        st.divider()
        st.caption("Crafted with Streamlit & youtube-transcript-api")


def render_empty_state() -> None:
    """Render the empty state card before any URL is processed."""
    st.markdown(
        """
        <div class="empty-state-box">
            <div class="empty-icon">🎬</div>
            <div class="empty-title">Ready to extract your transcript?</div>
            <div class="empty-desc">
                Paste any public YouTube video or Short link above and we will retrieve the available subtitles instantly.
            </div>
            <div class="features-row">
                <span class="feature-chip">⚡ Fast Extraction</span>
                <span class="feature-chip">🌐 Multi-Language</span>
                <span class="feature-chip">📋 One-Click Copy</span>
                <span class="feature-chip">⬇️ TXT, SRT & VTT</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_video_metadata_card(metadata: VideoMetadata, transcript: TranscriptResult) -> None:
    """Render an aesthetic video metadata summary card."""
    track_type_class = "pill-auto" if transcript.is_generated else "pill-manual"
    track_type_text = "Auto-generated" if transcript.is_generated else "Manual"
    safe_title = html.escape(metadata.title)
    safe_channel = html.escape(metadata.channel or "YouTube Creator")
    safe_thumb = html.escape(metadata.thumbnail_url or "")
    formatted_duration = format_seconds_to_timestamp(
        transcript.total_duration, force_hours=transcript.total_duration >= 3600
    )

    st.markdown(
        f"""
        <div class="video-card">
            <img class="video-thumbnail" src="{safe_thumb}" alt="Video Thumbnail" onerror="this.style.display='none'" />
            <div class="video-info">
                <div class="video-title">{safe_title}</div>
                <div class="video-channel">
                    <span>📺</span> <span>{safe_channel}</span>
                </div>
                <div class="meta-pills">
                    <span class="meta-pill">🌐 {html.escape(transcript.language)} ({html.escape(transcript.language_code)})</span>
                    <span class="meta-pill {track_type_class}">📝 {track_type_text}</span>
                    <span class="meta-pill">⏱️ {formatted_duration}</span>
                    <span class="meta-pill">🆔 {html.escape(metadata.video_id)}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stats_cards(result: TranscriptResult) -> None:
    """Render metric stat boxes for words, segments, and duration."""
    formatted_duration = format_seconds_to_timestamp(
        result.total_duration, force_hours=result.total_duration >= 3600
    )

    st.markdown(
        f"""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">🔤 Words</div>
                <div class="stat-value">{result.word_count:,}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">📄 Segments</div>
                <div class="stat-value">{result.segment_count:,}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">⏱️ Duration</div>
                <div class="stat-value">{formatted_duration}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_transcript_display(text_content: str, is_timestamp_mode: bool) -> None:
    """
    Render a scrollable, styled transcript text container.
    """
    box_class = "transcript-box timestamp-view" if is_timestamp_mode else "transcript-box"
    escaped_text = html.escape(text_content)

    st.markdown(
        f"""
        <div class="{box_class}">{escaped_text}</div>
        """,
        unsafe_allow_html=True,
    )


def render_copy_button(text_to_copy: str, key_suffix: str = "") -> None:
    """
    Render a dependable HTML5/JS browser clipboard copy button with visual confirmation.
    """
    escaped_js_text = text_to_copy.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    button_id = f"copy-btn-{key_suffix}" if key_suffix else "copy-btn-main"

    copy_component_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                margin: 0;
                padding: 0;
                background: transparent;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            .btn-copy {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                background: #1e293b;
                color: #f8fafc;
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 8px;
                padding: 8px 18px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
                width: 100%;
                box-sizing: border-box;
                height: 40px;
            }}
            .btn-copy:hover {{
                background: #334155;
                border-color: rgba(255, 255, 255, 0.3);
                transform: translateY(-1px);
            }}
            .btn-copy.copied {{
                background: #15803d;
                border-color: #22c55e;
                color: #ffffff;
            }}
        </style>
    </head>
    <body>
        <button id="{button_id}" class="btn-copy" onclick="copyContent()">
            <span>📋 Copy Transcript</span>
        </button>

        <script>
            const textToCopy = `{escaped_js_text}`;
            function copyContent() {{
                const btn = document.getElementById("{button_id}");
                navigator.clipboard.writeText(textToCopy).then(() => {{
                    btn.classList.add("copied");
                    btn.innerHTML = "<span>✅ Transcript Copied!</span>";
                    setTimeout(() => {{
                        btn.classList.remove("copied");
                        btn.innerHTML = "<span>📋 Copy Transcript</span>";
                    }}, 2500);
                }}).catch(err => {{
                    // Fallback for restricted clipboard contexts
                    const textarea = document.createElement("textarea");
                    textarea.value = textToCopy;
                    document.body.appendChild(textarea);
                    textarea.select();
                    document.execCommand("copy");
                    document.body.removeChild(textarea);
                    btn.classList.add("copied");
                    btn.innerHTML = "<span>✅ Transcript Copied!</span>";
                    setTimeout(() => {{
                        btn.classList.remove("copied");
                        btn.innerHTML = "<span>📋 Copy Transcript</span>";
                    }}, 2500);
                }});
            }}
        </script>
    </body>
    </html>
    """
    components.html(copy_component_html, height=46)


def render_download_section(
    result: TranscriptResult,
    metadata: VideoMetadata,
    current_view_text: str,
    view_mode: str,
) -> None:
    """Render download buttons for TXT, SRT, and VTT formats."""
    base_filename = sanitize_filename(metadata.title)

    col1, col2, col3, col4 = st.columns([1.2, 1, 1, 1])

    with col1:
        render_copy_button(current_view_text, key_suffix="action-row")

    with col2:
        st.download_button(
            label="⬇️ Download TXT",
            data=current_view_text,
            file_name=f"{base_filename}-{view_mode.lower()}.txt",
            mime="text/plain",
            use_container_width=True,
            help="Download transcript as plain text in currently selected view mode",
        )

    with col3:
        st.download_button(
            label="⬇️ Download SRT",
            data=result.srt_text,
            file_name=f"{base_filename}.srt",
            mime="application/x-subrip",
            use_container_width=True,
            help="Download standard SubRip subtitle format with timestamps",
        )

    with col4:
        st.download_button(
            label="⬇️ Download VTT",
            data=result.vtt_text,
            file_name=f"{base_filename}.vtt",
            mime="text/vtt",
            use_container_width=True,
            help="Download WebVTT subtitle format",
        )
