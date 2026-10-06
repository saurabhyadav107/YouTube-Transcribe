"""High-fidelity UI components matching the reference design screenshots.

Components:
1. Sidebar: Brand header, modern navigation items, resources, Pro Tip / Fast & Accurate card
2. Top User Bar: Theme toggle icon, JD avatar, John Doe dropdown
3. Hero Banner: Eyebrow, YouTube Transcript Studio title, subtitle, authentic 3D artwork
4. URL Input Card: Label, search input, Get Transcript button, Clear button, sample link pills
5. Empty State Card: Stylized 3D clapperboard icon, heading, description
6. How It Works: 4 colorful step cards (1 Red, 2 Blue, 3 Purple, 4 Green)
7. Video Player Card: Video title, embedded YouTube player, duration badge, channel info
8. Transcript Panel: Interactive tabs (Transcript, Timestamps, Summary, Key Points), search, auto-scroll, active row highlight
9. Transcript Actions: 4 coordinated buttons (Copy, TXT, SRT, VTT) with vector icons
10. Stats Cards: Words metric, Duration metric
"""

import base64
import html
import json
from typing import Optional, List
import streamlit as st
import streamlit.components.v1 as components

from models.transcript_models import VideoMetadata, TranscriptResult, TranscriptLanguage
from utils.file_utils import sanitize_filename
from utils.transcript_utils import format_seconds_to_timestamp
from ui.assets import (
    get_hero_art_b64,
    get_clapperboard_b64,
    get_yt_logo_b64,
    ICON_HOME,
    ICON_ABOUT,
    ICON_HOW_IT_WORKS,
    ICON_TRANSCRIBE,
    ICON_HISTORY,
    ICON_EXPORT,
    ICON_LINKS,
    ICON_CHAIN,
    ICON_FAQ,
    ICON_FEEDBACK,
    ICON_LIGHTNING,
    ICON_CROWN,
    ICON_SUN,
    ICON_CHEVRON_DOWN,
    ICON_SPARKLES,
    ICON_LIGHTBULB,
    ICON_TRASH,
    ICON_GEAR,
    ICON_STEP1_LINK,
    ICON_STEP2_DETECT,
    ICON_STEP3_MODE,
    ICON_STEP4_EXPORT,
    ICON_DASH_COPY,
    ICON_DASH_TXT,
    ICON_DASH_SRT,
    ICON_DASH_VTT,
    ICON_STAT_WORDS,
    ICON_STAT_DURATION,
)


def render_html(html_str: str) -> None:
    """Render HTML string safely via st.markdown while stripping leading whitespace on every line.
    
    This ensures that lines indented by 4+ spaces are never parsed by CommonMark as code blocks,
    while preserving all SVG elements and attributes that DOMPurify in st.html() strips out.
    """
    cleaned = "\n".join(line.strip() for line in html_str.strip().splitlines() if line.strip())
    st.markdown(cleaned, unsafe_allow_html=True)


# =============================================================================
# 1. Sidebar Component
# =============================================================================

def render_sidebar(is_result_page: bool = False) -> None:
    """Render the sidebar matching the reference screenshots with crisp vector icons."""
    yt_logo_b64 = get_yt_logo_b64()

    with st.sidebar:
        # Brand Logo Header
        render_html(
            f"""
            <div class="sidebar-brand-container">
                <div class="sidebar-brand-logo">
                    <img src="data:image/png;base64,{yt_logo_b64}" alt="YouTube" style="width: 28px; height: auto;" />
                </div>
                <div>
                    <div class="sidebar-brand-title">YouTube</div>
                    <div class="sidebar-brand-subtitle">Transcript Studio</div>
                </div>
            </div>
            """
        )

        # Nav items
        if is_result_page:
            # Result page sidebar items (from Screenshot 1)
            render_html(
                f"""
                <div class="sidebar-nav-group">
                    <div class="sidebar-nav-item active">
                        {ICON_HOME} <span>Home</span>
                    </div>
                    <div class="sidebar-nav-item">
                        {ICON_TRANSCRIBE} <span>Transcribe</span>
                    </div>
                    <div class="sidebar-nav-item">
                        {ICON_HISTORY} <span>History</span>
                    </div>
                    <div class="sidebar-nav-item">
                        {ICON_EXPORT} <span>Export Options</span>
                    </div>
                    <div class="sidebar-nav-item">
                        {ICON_CHAIN} <span>Supported Links</span>
                    </div>
                    <div class="sidebar-nav-item">
                        {ICON_ABOUT} <span>About</span>
                    </div>
                    <div class="sidebar-nav-item">
                        {ICON_FEEDBACK} <span>Feedback</span>
                    </div>
                </div>
                """
            )
            # Bottom Card: Pro Tip
            render_html(
                f"""
                <div class="sidebar-tip-card">
                    <div class="sidebar-tip-header">
                        <div class="sidebar-tip-badge crown">{ICON_CROWN}</div>
                        <span>Pro Tip</span>
                    </div>
                    <div class="sidebar-tip-desc">
                        Get clean, well-formatted transcripts with accurate timestamps in seconds.
                    </div>
                </div>
                """
            )
        else:
            # Empty / Landing page sidebar items (from Screenshot 2)
            render_html(
                f"""
                <div class="sidebar-nav-group">
                    <div class="sidebar-nav-item active">
                        {ICON_HOME} <span>Home</span>
                    </div>
                    <div class="sidebar-nav-item">
                        {ICON_ABOUT} <span>About</span>
                    </div>
                    <div class="sidebar-nav-item">
                        {ICON_HOW_IT_WORKS} <span>How it Works</span>
                    </div>
                    <div class="sidebar-nav-item">
                        {ICON_EXPORT} <span>Export Options</span>
                    </div>
                </div>

                <div class="sidebar-nav-header">RESOURCES</div>
                <div class="sidebar-nav-group">
                    <div class="sidebar-nav-item">
                        {ICON_LINKS} <span>Supported Links</span>
                    </div>
                    <div class="sidebar-nav-item">
                        {ICON_FAQ} <span>FAQ</span>
                    </div>
                    <div class="sidebar-nav-item">
                        {ICON_FEEDBACK} <span>Feedback</span>
                    </div>
                </div>
                """
            )
            # Bottom Card: Fast & Accurate
            render_html(
                f"""
                <div class="sidebar-tip-card">
                    <div class="sidebar-tip-header">
                        <div class="sidebar-tip-badge">{ICON_LIGHTNING}</div>
                        <span>Fast & Accurate</span>
                    </div>
                    <div class="sidebar-tip-desc">
                        Get clean, well-formatted transcripts from any YouTube video or Shorts.
                    </div>
                </div>
                """
            )


# =============================================================================
# 2. Top User Bar (Navbar)
# =============================================================================

def render_top_user_bar() -> None:
    """Render top right user badge with theme toggle and user avatar."""
    render_html(
        f"""
        <div class="top-user-bar">
            <button class="top-theme-btn" title="Toggle theme">
                {ICON_SUN}
            </button>
            <div class="top-user-badge">
                <div class="top-user-avatar">JD</div>
                <span>John Doe</span>
                {ICON_CHEVRON_DOWN}
            </div>
        </div>
        """
    )


# =============================================================================
# 3. Hero Section
# =============================================================================

def render_hero(is_result_page: bool = False, current_url: str = "") -> None:
    """Render hero header card with exact typography and authentic 3D artwork."""
    hero_art_b64 = get_hero_art_b64()
    yt_logo_b64 = get_yt_logo_b64()

    artwork_html = (
        f'<div class="hero-artwork-col">'
        f'<img src="data:image/png;base64,{hero_art_b64}" alt="YouTube Transcript Studio" class="hero-3d-artwork-img" />'
        f'</div>'
    ) if hero_art_b64 else ""

    if is_result_page:
        # Result Page Hero (Screenshot 1)
        render_html(
            f"""
            <div class="hero-banner-card">
                <div class="hero-content-col">
                    <div class="hero-eyebrow">EXTRACT • READ • EXPORT</div>
                    <div class="hero-title">
                        <span>YouTube</span>
                        <span class="gradient-word">Transcript</span>
                        <span>Studio</span>
                    </div>
                    <div class="hero-subtitle">
                        Get accurate transcripts, timestamps, and downloadable files from any YouTube video or Shorts — fast and easy.
                    </div>
                </div>
                {artwork_html}
            </div>
            """
        )
    else:
        # Landing Page Hero (Screenshot 2)
        render_html(
            f"""
            <div class="hero-banner-card" style="margin-bottom: 1.2rem;">
                <div class="hero-content-col">
                    <div class="hero-title" style="font-size: 2.5rem; margin-top: 4px;">
                        <span class="hero-title-yt-icon">
                            <img src="data:image/png;base64,{yt_logo_b64}" alt="YouTube" style="width: 28px; height: auto;" />
                        </span>
                        <span>YouTube</span>
                        <span class="gradient-word">Transcript</span>
                        <span>Studio</span>
                    </div>
                    <div class="hero-subtitle" style="font-size: 1rem;">
                        Extract, read and export transcripts from any YouTube video or Shorts — fast, accurate and free.
                    </div>
                </div>
                {artwork_html}
            </div>
            """
        )


# =============================================================================
# 4. URL Input Section (Landing & Result states)
# =============================================================================

def render_url_input_card(
    default_url: str = "",
    is_result_page: bool = False,
) -> tuple[str, bool, bool, Optional[str]]:
    """
    Render URL input section matching the exact layout of the reference.
    Returns: (input_url, submit_clicked, clear_clicked, sample_url_clicked)
    """
    submit_clicked = False
    clear_clicked = False
    sample_url = None

    if is_result_page:
        # Compact top URL card directly below hero on result page
        with st.container():
            col_in, col_btn = st.columns([4.2, 1.3], vertical_alignment="center")
            with col_in:
                input_url = st.text_input(
                    label="YouTube URL",
                    value=default_url,
                    placeholder="https://www.youtube.com/watch?v=...",
                    key="result_url_input",
                    label_visibility="collapsed",
                )
            with col_btn:
                submit_clicked = st.button(
                    "✨ Get Transcript",
                    type="primary",
                    key="result_get_btn",
                    use_container_width=True,
                )
    else:
        # Large URL Input Card (Screenshot 2)
        with st.container():
            render_html(
                f"""
                <div style="margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
                    {ICON_CHAIN}
                    <span style="font-size: 14.5px; font-weight: 600; color: #f1f5f9;">YouTube Video URL</span>
                </div>
                """
            )
            col_in, col_submit, col_clear = st.columns([3.8, 1.2, 0.8], vertical_alignment="bottom")

            with col_in:
                input_url = st.text_input(
                    label="YouTube Video URL",
                    value=default_url,
                    placeholder="Paste any YouTube video or Shorts link (e.g. https://www.youtube.com/watch?v=...)",
                    key="landing_url_input",
                    label_visibility="collapsed",
                )

            with col_submit:
                submit_clicked = st.button(
                    "✨ Get Transcript",
                    type="primary",
                    key="landing_get_btn",
                    use_container_width=True,
                )

            with col_clear:
                clear_clicked = st.button(
                    "🗑️ Clear",
                    key="landing_clear_btn",
                    use_container_width=True,
                )

            # Sample buttons row
            col_label, col_s1, col_s2, _ = st.columns([1.3, 1.6, 1.8, 2.5], vertical_alignment="center")
            with col_label:
                render_html(
                    f"""
                    <div style="display: flex; align-items: center; gap: 6px; font-size: 13px; color: #94a3b8;">
                        {ICON_LIGHTBULB}
                        <span>Try these examples:</span>
                    </div>
                    """
                )
            with col_s1:
                if st.button("Steve Jobs 2005 Speech", key="sample_steve"):
                    sample_url = "https://www.youtube.com/watch?v=UF8uR6Z6KLc"
            with col_s2:
                if st.button("Veritasium – Math Paradox", key="sample_veri"):
                    sample_url = "https://www.youtube.com/watch?v=HeQX2HjkcNo"

    return input_url, submit_clicked, clear_clicked, sample_url


# =============================================================================
# 5. Empty State & How It Works (Screenshot 2)
# =============================================================================

def render_empty_state() -> None:
    """Render the large empty state card featuring authentic 3D clapperboard."""
    clapper_b64 = get_clapperboard_b64()

    render_html(
        f"""
        <div class="empty-state-large-card">
            <div class="empty-slate-icon-wrapper">
                <img src="data:image/png;base64,{clapper_b64}" alt="Ready to Extract" class="empty-clapperboard-img" />
            </div>
            <div class="empty-state-heading">Ready to extract video transcripts</div>
            <div class="empty-state-desc">
                Paste a YouTube video or Shorts link in the box above. We'll automatically detect available subtitle tracks and retrieve the transcript in seconds.
            </div>
        </div>
        """
    )


def render_how_it_works() -> None:
    """Render the 4-step 'How it works' grid from Screenshot 2 with crisp vector icons."""
    render_html(
        f"""
        <div>
            <div class="how-it-works-header">
                <div class="how-title">
                    <span style="display: inline-flex; align-items: center;">{ICON_GEAR}</span>
                    <span>How it works</span>
                </div>
                <div style="font-size: 12.5px; color: #94a3b8;">Get transcript in 4 simple steps</div>
            </div>

            <div class="how-steps-grid">
                <!-- Step 1 (Red) -->
                <div class="how-card step-1">
                    <div class="how-card-top">
                        <div class="how-num-circle">1</div>
                        <div class="how-step-icon">{ICON_STEP1_LINK}</div>
                    </div>
                    <div class="how-card-title">Paste Video URL</div>
                    <div class="how-card-desc">Supports YouTube videos, Shorts, and live videos.</div>
                </div>

                <!-- Step 2 (Blue) -->
                <div class="how-card step-2">
                    <div class="how-card-top">
                        <div class="how-num-circle">2</div>
                        <div class="how-step-icon">{ICON_STEP2_DETECT}</div>
                    </div>
                    <div class="how-card-title">Auto Detection</div>
                    <div class="how-card-desc">Detects available subtitle tracks and prioritizes the best match.</div>
                </div>

                <!-- Step 3 (Purple) -->
                <div class="how-card step-3">
                    <div class="how-card-top">
                        <div class="how-num-circle">3</div>
                        <div class="how-step-icon">{ICON_STEP3_MODE}</div>
                    </div>
                    <div class="how-card-title">Select Mode</div>
                    <div class="how-card-desc">Choose between clean reading paragraphs or timestamped transcripts.</div>
                </div>

                <!-- Step 4 (Green) -->
                <div class="how-card step-4">
                    <div class="how-card-top">
                        <div class="how-num-circle">4</div>
                        <div class="how-step-icon">{ICON_STEP4_EXPORT}</div>
                    </div>
                    <div class="how-card-title">Copy or Export</div>
                    <div class="how-card-desc">Copy to clipboard or export as TXT, SRT, or VTT.</div>
                </div>
            </div>
        </div>
        """
    )


# =============================================================================
# 6. Video Player Card (Screenshot 1)
# =============================================================================

def render_video_card(metadata: VideoMetadata, transcript: TranscriptResult) -> None:
    """Render the video card containing title and embedded player."""
    formatted_duration = format_seconds_to_timestamp(
        transcript.total_duration, force_hours=transcript.total_duration >= 3600
    )

    with st.container():
        # Title of Video
        render_html(
            f"""
            <div style="margin-bottom: 10px;">
                <h3 style="font-size: 1.15rem; font-weight: 700; color: #ffffff; margin: 0; line-height: 1.35;">
                    {html.escape(metadata.title)}
                </h3>
            </div>
            """
        )

        # Embedded Video Player
        st.video(metadata.url)

        # Subtle metadata details under video
        track_type = "Auto-generated" if transcript.is_generated else "Manual"
        render_html(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 2px; font-size: 12.5px; color: #94a3b8;">
                <div>📺 {html.escape(metadata.channel or 'YouTube Channel')}</div>
                <div>⏱️ {formatted_duration} • 🌐 {html.escape(transcript.language)} ({track_type})</div>
            </div>
            """
        )


# =============================================================================
# 7. Transcript Panel with Tabs, Search, and Rows (Screenshot 1)
# =============================================================================

def render_interactive_transcript_panel(
    result: TranscriptResult,
    available_langs: List[TranscriptLanguage],
    selected_lang_code: str,
) -> Optional[str]:
    """
    Render high-fidelity interactive transcript panel matching Screenshot 1:
    - Tabs: Transcript, Timestamps, Summary, Key Points with vector icons
    - Search input & Auto-Scroll toggle
    - Timestamped rows with active highlighting
    - Integrated language switcher
    """
    new_lang_choice = None

    # Language selection dropdown directly above tabs if multiple languages exist
    if available_langs:
        lang_codes = [l.language_code for l in available_langs]
        lang_labels = {l.language_code: l.display_name for l in available_langs}
        cur_idx = lang_codes.index(selected_lang_code) if selected_lang_code in lang_codes else 0

        lang_col, _ = st.columns([2.5, 1])
        with lang_col:
            chosen = st.selectbox(
                label="Transcript Language",
                options=lang_codes,
                format_func=lambda c: lang_labels.get(c, c),
                index=cur_idx,
                key="transcript_lang_selector_box",
                help="Defaults to actual original spoken language of the video",
            )
            if chosen != selected_lang_code:
                new_lang_choice = chosen

    # Prepare segments JSON for client-side interactivity
    segments_data = [
        {
            "start": seg.start,
            "duration": seg.duration,
            "timestamp": format_seconds_to_timestamp(seg.start, force_hours=result.total_duration >= 3600),
            "text": seg.text,
        }
        for seg in result.segments
    ]
    segments_json = json.dumps(segments_data)
    summary_text = html.escape(result.reading_text[:1200] + ("..." if len(result.reading_text) > 1200 else ""))

    # Key points extraction (take first sentence of major segments)
    key_points = [seg.text.strip() for seg in result.segments if len(seg.text.strip()) > 25][:5]
    key_points_html = "".join([f"<li style='margin-bottom: 8px;'>{html.escape(kp)}</li>" for kp in key_points])

    component_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap">
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                font-family: 'Inter', -apple-system, sans-serif;
                background: #0e1424;
                color: #cbd5e1;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 18px 20px;
                user-select: text;
            }}

            /* Tabs */
            .tabs-bar {{
                display: flex;
                align-items: center;
                gap: 8px;
                padding-bottom: 12px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                margin-bottom: 14px;
            }}
            .tab-btn {{
                background: transparent;
                border: none;
                color: #94a3b8;
                font-size: 13px;
                font-weight: 600;
                padding: 7px 16px;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.15s ease;
                display: inline-flex;
                align-items: center;
                gap: 7px;
            }}
            .tab-btn svg {{
                width: 14px;
                height: 14px;
            }}
            .tab-btn:hover {{
                color: #ffffff;
                background: rgba(255, 255, 255, 0.05);
            }}
            .tab-btn.active {{
                background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
                color: #ffffff;
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.35);
            }}

            /* Toolbar (Search & Auto Scroll) */
            .toolbar-row {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                margin-bottom: 14px;
            }}
            .search-input-wrapper {{
                flex-grow: 1;
                position: relative;
            }}
            .search-input-wrapper input {{
                width: 100%;
                background: #111728;
                border: 1px solid rgba(255, 255, 255, 0.09);
                border-radius: 8px;
                color: #ffffff;
                font-size: 13px;
                padding: 8px 12px 8px 34px;
                outline: none;
                transition: border-color 0.2s ease;
            }}
            .search-input-wrapper input:focus {{
                border-color: rgba(59, 130, 246, 0.5);
            }}
            .search-icon {{
                position: absolute;
                left: 11px;
                top: 50%;
                transform: translateY(-50%);
                color: #64748b;
                display: flex;
                align-items: center;
            }}
            .auto-scroll-toggle {{
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 12.5px;
                font-weight: 600;
                color: #94a3b8;
                background: #111728;
                border: 1px solid rgba(255, 255, 255, 0.09);
                border-radius: 8px;
                padding: 6px 12px;
                cursor: pointer;
                user-select: none;
            }}
            .toggle-pill {{
                width: 32px;
                height: 18px;
                background: #4f46e5;
                border-radius: 10px;
                position: relative;
                transition: background 0.2s ease;
            }}
            .toggle-circle {{
                width: 14px;
                height: 14px;
                background: #ffffff;
                border-radius: 50%;
                position: absolute;
                top: 2px;
                right: 2px;
                transition: all 0.2s ease;
            }}

            /* Scrollable rows list */
            .transcript-scroll-area {{
                max-height: 380px;
                overflow-y: auto;
                padding-right: 6px;
                display: flex;
                flex-direction: column;
                gap: 6px;
            }}
            .transcript-scroll-area::-webkit-scrollbar {{
                width: 5px;
            }}
            .transcript-scroll-area::-webkit-scrollbar-thumb {{
                background: rgba(148, 163, 184, 0.25);
                border-radius: 4px;
            }}

            .row-entry {{
                display: flex;
                align-items: flex-start;
                gap: 14px;
                padding: 10px 14px;
                border-radius: 8px;
                background: transparent;
                border: 1px solid transparent;
                cursor: pointer;
                transition: all 0.15s ease;
            }}
            .row-entry:hover {{
                background: rgba(255, 255, 255, 0.04);
            }}
            .row-entry.active {{
                background: rgba(30, 41, 75, 0.7);
                border-color: rgba(59, 130, 246, 0.5);
                box-shadow: 0 2px 10px rgba(59, 130, 246, 0.15);
            }}
            .time-badge {{
                font-family: 'JetBrains Mono', Consolas, monospace;
                font-size: 12px;
                font-weight: 600;
                color: #60a5fa;
                background: rgba(59, 130, 246, 0.14);
                border: 1px solid rgba(59, 130, 246, 0.25);
                border-radius: 6px;
                padding: 3px 9px;
                white-space: nowrap;
                flex-shrink: 0;
            }}
            .row-entry.active .time-badge {{
                background: #3b82f6;
                color: #ffffff;
                border-color: #3b82f6;
            }}
            .row-text {{
                font-size: 13.5px;
                line-height: 1.6;
                color: #cbd5e1;
            }}
            .row-entry.active .row-text {{
                color: #ffffff;
                font-weight: 500;
            }}

            /* Tab View Containers */
            .tab-view {{ display: none; }}
            .tab-view.active {{ display: block; }}
            .summary-card {{
                padding: 16px;
                background: rgba(255, 255, 255, 0.02);
                border-radius: 10px;
                line-height: 1.7;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <!-- Tabs Header with Vector Icons -->
        <div class="tabs-bar">
            <button class="tab-btn active" id="tab-transcript" onclick="switchTab('transcript')">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>
                <span>Transcript</span>
            </button>
            <button class="tab-btn" id="tab-timestamps" onclick="switchTab('timestamps')">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                <span>Timestamps</span>
            </button>
            <button class="tab-btn" id="tab-summary" onclick="switchTab('summary')">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"></path></svg>
                <span>Summary</span>
            </button>
            <button class="tab-btn" id="tab-keypoints" onclick="switchTab('keypoints')">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3L12 3z"></path></svg>
                <span>Key Points</span>
            </button>
        </div>

        <!-- Toolbar: Search & Auto Scroll -->
        <div class="toolbar-row">
            <div class="search-input-wrapper">
                <span class="search-icon">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                </span>
                <input type="text" id="searchInput" placeholder="Search in transcript..." oninput="filterTranscript()" />
            </div>
            <div class="auto-scroll-toggle" onclick="toggleAutoScroll()">
                <span>Auto Scroll</span>
                <div class="toggle-pill" id="togglePill">
                    <div class="toggle-circle" id="toggleCircle"></div>
                </div>
            </div>
        </div>

        <!-- Tab 1: Transcript & Tab 2: Timestamps (Active) -->
        <div class="tab-view active" id="view-transcript">
            <div class="transcript-scroll-area" id="scrollContainer"></div>
        </div>

        <!-- Tab 3: Summary -->
        <div class="tab-view" id="view-summary">
            <div class="summary-card">
                <h4 style="color: #ffffff; margin-bottom: 8px;">Executive Summary</h4>
                <p>{summary_text}</p>
            </div>
        </div>

        <!-- Tab 4: Key Points -->
        <div class="tab-view" id="view-keypoints">
            <div class="summary-card">
                <h4 style="color: #ffffff; margin-bottom: 8px;">Key Takeaways</h4>
                <ul style="padding-left: 20px;">
                    {key_points_html}
                </ul>
            </div>
        </div>

        <script>
            const segments = {segments_json};
            let autoScrollEnabled = true;
            let activeIndex = 0;

            function renderRows(items) {{
                const container = document.getElementById("scrollContainer");
                container.innerHTML = "";
                items.forEach((seg, idx) => {{
                    const row = document.createElement("div");
                    const isActive = (idx === activeIndex);
                    row.className = "row-entry" + (isActive ? " active" : "");
                    row.id = "row-" + idx;
                    row.onclick = () => selectRow(idx);

                    const badge = document.createElement("div");
                    badge.className = "time-badge";
                    badge.innerHTML = (isActive ? "▶ " : "") + seg.timestamp;

                    const text = document.createElement("div");
                    text.className = "row-text";
                    text.textContent = seg.text;

                    row.appendChild(badge);
                    row.appendChild(text);
                    container.appendChild(row);
                }});
            }}

            function selectRow(idx) {{
                activeIndex = idx;
                const rows = document.querySelectorAll(".row-entry");
                rows.forEach((r, i) => {{
                    const badge = r.querySelector(".time-badge");
                    if (i === idx) {{
                        r.classList.add("active");
                        badge.innerHTML = "▶ " + segments[i].timestamp;
                    }} else {{
                        r.classList.remove("active");
                        badge.innerHTML = segments[i].timestamp;
                    }}
                }});

                if (autoScrollEnabled) {{
                    const target = document.getElementById("row-" + idx);
                    if (target) {{
                        target.scrollIntoView({{ behavior: "smooth", block: "center" }});
                    }}
                }}
            }}

            function filterTranscript() {{
                const query = document.getElementById("searchInput").value.toLowerCase().trim();
                const filtered = segments.filter(s => s.text.toLowerCase().includes(query));
                renderRows(filtered.length > 0 ? filtered : [{{ timestamp: "00:00", text: "No matching transcript lines found." }}]);
            }}

            function toggleAutoScroll() {{
                autoScrollEnabled = !autoScrollEnabled;
                const pill = document.getElementById("togglePill");
                const circle = document.getElementById("toggleCircle");
                if (autoScrollEnabled) {{
                    pill.style.background = "#4f46e5";
                    circle.style.right = "2px";
                    circle.style.left = "auto";
                }} else {{
                    pill.style.background = "#334155";
                    circle.style.left = "2px";
                    circle.style.right = "auto";
                }}
            }}

            function switchTab(tabName) {{
                document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
                document.querySelectorAll(".tab-view").forEach(v => v.classList.remove("active"));

                document.getElementById("tab-" + tabName).classList.add("active");
                if (tabName === "transcript" || tabName === "timestamps") {{
                    document.getElementById("view-transcript").classList.add("active");
                }} else {{
                    document.getElementById("view-" + tabName).classList.add("active");
                }}
            }}

            // Initial Render
            renderRows(segments);
        </script>
    </body>
    </html>
    """
    components.html(component_html, height=520)
    return new_lang_choice


# =============================================================================
# 8. Bottom Row: Transcript Actions & Stats Cards (Screenshot 1)
# =============================================================================

def render_bottom_dashboard(result: TranscriptResult, metadata: VideoMetadata) -> None:
    """Render Transcript Actions card and Stats metric cards matching Screenshot 1 with proper icons."""
    base_filename = sanitize_filename(metadata.title)
    formatted_duration = format_seconds_to_timestamp(
        result.total_duration, force_hours=result.total_duration >= 3600
    )

    act_col, stats_col = st.columns([2.2, 1.2], gap="medium")

    # Left Card: Transcript Actions
    with act_col:
        with st.container():
            render_html(
                """
                <div style="margin-bottom: 12px;">
                    <div class="actions-title">Transcript Actions</div>
                    <div class="actions-sub">Download, copy or export your transcript</div>
                </div>
                """
            )

            b_col1, b_col2, b_col3, b_col4 = st.columns(4)

            # Button 1: Copy to Clipboard (Copies clean reading text WITHOUT timestamps)
            with b_col1:
                clean_copy_text_b64 = base64.b64encode(result.reading_text.encode("utf-8")).decode("ascii")
                copy_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <style>
                        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
                        body {{ background: transparent; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; overflow: hidden; }}
                        .btn-copy {{
                            width: 100%;
                            height: 42px;
                            border-radius: 8px;
                            border: none;
                            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
                            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
                            color: #ffffff;
                            font-size: 13px;
                            font-weight: 600;
                            cursor: pointer;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            gap: 7px;
                            transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.2s ease;
                            user-select: none;
                        }}
                        .btn-copy:hover {{
                            transform: translateY(-1px);
                            box-shadow: 0 6px 18px rgba(99, 102, 241, 0.5);
                        }}
                        .btn-copy svg {{
                            width: 15px;
                            height: 15px;
                            flex-shrink: 0;
                        }}
                    </style>
                </head>
                <body>
                    <button class="btn-copy" id="copyBtn" onclick="doCopy()">
                        {ICON_DASH_COPY}
                        <span id="copyLabel">Copy to Clipboard</span>
                    </button>
                    <script>
                        function b64DecodeUnicode(str) {{
                            return decodeURIComponent(atob(str).split('').map(function(c) {{
                                return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
                            }}).join(''));
                        }}
                        function doCopy() {{
                            try {{
                                const text = b64DecodeUnicode("{clean_copy_text_b64}");
                                function showSuccess() {{
                                    const btn = document.getElementById("copyBtn");
                                    const label = document.getElementById("copyLabel");
                                    btn.style.background = "#10b981";
                                    label.textContent = "Copied!";
                                    setTimeout(() => {{
                                        btn.style.background = "linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)";
                                        label.textContent = "Copy to Clipboard";
                                    }}, 2200);
                                }}
                                if (navigator.clipboard && window.isSecureContext) {{
                                    navigator.clipboard.writeText(text).then(showSuccess).catch(() => {{
                                        fallbackCopy(text);
                                        showSuccess();
                                    }});
                                }} else {{
                                    fallbackCopy(text);
                                    showSuccess();
                                }}
                            }} catch (e) {{
                                console.error("Copy failed", e);
                            }}
                        }}
                        function fallbackCopy(text) {{
                            const ta = document.createElement("textarea");
                            ta.value = text;
                            ta.style.position = "fixed";
                            ta.style.opacity = "0";
                            ta.style.left = "-9999px";
                            document.body.appendChild(ta);
                            ta.focus();
                            ta.select();
                            try {{
                                document.execCommand("copy");
                            }} catch (err) {{
                                console.error("Fallback copy failed", err);
                            }}
                            document.body.removeChild(ta);
                        }}
                    </script>
                </body>
                </html>
                """
                components.html(copy_html, height=44)

            # Button 2: Download TXT (Contains clean reading text WITHOUT timestamps)
            with b_col2:
                st.download_button(
                    label="Download TXT",
                    data=result.reading_text,
                    file_name=f"{base_filename}.txt",
                    mime="text/plain",
                    key="btn_dl_txt",
                    width="stretch",
                )

            # Button 3: Download SRT (SubRip subtitles format)
            with b_col3:
                st.download_button(
                    label="Download SRT",
                    data=result.srt_text,
                    file_name=f"{base_filename}.srt",
                    mime="application/x-subrip",
                    key="btn_dl_srt",
                    width="stretch",
                )

            # Button 4: Download VTT (WebVTT subtitles format)
            with b_col4:
                st.download_button(
                    label="Download VTT",
                    data=result.vtt_text,
                    file_name=f"{base_filename}.vtt",
                    mime="text/vtt",
                    key="btn_dl_vtt",
                    width="stretch",
                )

    # Right Side: Stats Metric Cards with Vector Icons
    with stats_col:
        render_html(
            f"""
            <div class="stats-cards-grid">
                <div class="stat-metric-card">
                    <div class="stat-metric-icon words-icon">
                        {ICON_STAT_WORDS}
                    </div>
                    <div>
                        <div class="stat-metric-val">{result.word_count:,}</div>
                        <div class="stat-metric-label">Words</div>
                    </div>
                </div>
                <div class="stat-metric-card">
                    <div class="stat-metric-icon time-icon">
                        {ICON_STAT_DURATION}
                    </div>
                    <div>
                        <div class="stat-metric-val">{formatted_duration}</div>
                        <div class="stat-metric-label">Duration</div>
                    </div>
                </div>
            </div>
            """
        )
