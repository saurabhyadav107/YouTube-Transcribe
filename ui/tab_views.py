"""Dedicated rich content views for How it Works, Supported Links, Export Options, FAQ, About, and Feedback."""

import html
from typing import List, Optional
import streamlit as st

from ui.assets import (
    ICON_HOME,
    ICON_ABOUT,
    ICON_HOW_IT_WORKS,
    ICON_EXPORT,
    ICON_LINKS,
    ICON_CHAIN,
    ICON_FAQ,
    ICON_FEEDBACK,
    ICON_LIGHTNING,
    ICON_CROWN,
    ICON_SPARKLES,
    ICON_LIGHTBULB,
    ICON_GEAR,
    ICON_STEP1_LINK,
    ICON_STEP2_DETECT,
    ICON_STEP3_MODE,
    ICON_STEP4_EXPORT,
    ICON_DASH_COPY,
    ICON_DASH_TXT,
    ICON_DASH_SRT,
    ICON_DASH_VTT,
)
from utils.url_utils import validate_youtube_url


# =============================================================================
# Helper: Top Navigation Back Bar
# =============================================================================

def render_view_header(badge_text: str, title_text: str, subtitle_text: str) -> None:
    """Render standardized top header card for dedicated content views."""
    st.markdown(
        f"""
        <div class="content-view-header">
            <div class="content-view-badge">{badge_text}</div>
            <h1 class="content-view-title">{title_text}</h1>
            <p class="content-view-subtitle">{subtitle_text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_back_button(key_suffix: str = "") -> None:
    """Render a clean back button to return to the transcriber."""
    col1, _ = st.columns([1, 4])
    with col1:
        if st.button("← Back to Transcribe", key=f"back_btn_{key_suffix}", width="stretch", type="primary"):
            st.session_state["active_view"] = "transcribe"
            st.rerun()


# =============================================================================
# 1. How It Works View
# =============================================================================

def render_how_it_works_view() -> None:
    """Render comprehensive How It Works view with interactive workflow cards."""
    render_back_button("how_it_works")
    render_view_header(
        badge_text="WORKFLOW & PIPELINE",
        title_text="How YouTube Transcript Studio Works",
        subtitle_text="A transparent look at the intelligent 4-step pipeline that extracts, parses, formats, and exports your transcripts with sub-second latency.",
    )

    # 4 Main Workflow Step Cards
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-card-header">
                    <div class="info-step-num">Step 01</div>
                    <div class="info-card-icon">{ICON_STEP1_LINK}</div>
                </div>
                <h3 class="info-card-title">Universal URL Parsing</h3>
                <p class="info-card-desc">
                    Our multi-pattern regex engine accepts any valid YouTube URL format: standard watch links, 
                    YouTube Shorts, shortened <code>youtu.be</code> links, mobile URLs, embed players, and direct 11-character video IDs. 
                    Query parameters like timestamp markers (<code>&t=42s</code>) and playlist tags are parsed and cleaned safely.
                </p>
                <div class="info-card-pill">Supports: Watch, Shorts, youtu.be, Embeds, Timestamps</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-card-header">
                    <div class="info-step-num">Step 03</div>
                    <div class="info-card-icon">{ICON_STEP3_MODE}</div>
                </div>
                <h3 class="info-card-title">Smart Text Formatting Engine</h3>
                <p class="info-card-desc">
                    Raw YouTube subtitle streams arrive as fragmentary 2-3 word segments. Our clustering algorithm transforms them into two distinct presentation modes:
                </p>
                <ul class="info-card-list">
                    <li><strong>Reading Mode:</strong> Cohesive, flowing paragraphs with speech artifact deduplication and natural sentence breaks. Ideal for article reading and AI prompting.</li>
                    <li><strong>Timestamp Mode:</strong> Synchronized <code>[MM:SS]</code> or <code>[HH:MM:SS]</code> time indicators aligned with video playback.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-card-header">
                    <div class="info-step-num">Step 02</div>
                    <div class="info-card-icon">{ICON_STEP2_DETECT}</div>
                </div>
                <h3 class="info-card-title">Language Detection & Fallback</h3>
                <p class="info-card-desc">
                    The engine queries YouTube's subtitle catalog and identifies the video's actual spoken audio language:
                </p>
                <ul class="info-card-list">
                    <li><strong>Creator Manual Tracks:</strong> If the creator provided human-reviewed captions in the spoken language, they are prioritized first.</li>
                    <li><strong>Auto-Generated ASR:</strong> YouTube Automatic Speech Recognition is selected when manual captions are absent.</li>
                    <li><strong>InnerTube Mobile Fallback:</strong> If datacenter IPs are throttled on cloud hosting (AWS / Streamlit Cloud), our Android mobile player client automatically streams captions without disruption.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-card-header">
                    <div class="info-step-num">Step 04</div>
                    <div class="info-card-icon">{ICON_STEP4_EXPORT}</div>
                </div>
                <h3 class="info-card-title">One-Click Multi-Format Export</h3>
                <p class="info-card-desc">
                    Export your transcript instantly in the format suited for your workflow:
                </p>
                <ul class="info-card-list">
                    <li><strong>Clean TXT:</strong> Pure prose without bracketed timestamps, perfect for feeding into ChatGPT, Claude, and Gemini.</li>
                    <li><strong>Timestamped TXT:</strong> Timecode markers for lecture notes and citation indexing.</li>
                    <li><strong>SRT Subtitles:</strong> Standard SubRip subtitles with millisecond timecodes for Premiere, Final Cut, DaVinci, and VLC.</li>
                    <li><strong>WebVTT:</strong> Modern HTML5 video track format.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Technical Architecture Deep-Dive Callout
    st.markdown(
        f"""
        <div class="highlight-callout">
            <div class="highlight-callout-header">
                <div class="sidebar-tip-badge">{ICON_LIGHTNING}</div>
                <span class="highlight-callout-title">Resilient Cloud Fallback Architecture</span>
            </div>
            <p class="highlight-callout-desc">
                When apps are hosted on cloud providers like Streamlit Community Cloud (AWS EC2), YouTube frequently blocks desktop web scrapers with HTTP 429 rate limits. 
                YouTube Transcript Studio incorporates a proprietary fallback to the <strong>InnerTube Android Player API</strong>, querying signed timedtext streams directly with browser-grade headers and dual-format XML parsing (format 3 and format 1).
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    if st.button("🚀 Try It Now With a Video", key="try_now_btn", width="stretch", type="primary"):
        st.session_state["active_view"] = "transcribe"
        st.rerun()


# =============================================================================
# 2. Supported Links View
# =============================================================================

def render_supported_links_view() -> None:
    """Render comprehensive Supported Links view with live URL tester."""
    render_back_button("supported_links")
    render_view_header(
        badge_text="URL COMPATIBILITY",
        title_text="Supported YouTube Link Formats",
        subtitle_text="YouTube Transcript Studio supports every standard YouTube URL variation, including desktop watch links, Shorts, shortlinks, embeds, and mobile links.",
    )

    # Interactive Live URL Tester
    st.markdown("### 🧪 Live URL Validator")
    test_input = st.text_input(
        "Paste any YouTube URL below to verify format support:",
        placeholder="https://www.youtube.com/watch?v=...",
        key="live_tester_input",
    )

    if test_input.strip():
        is_valid, extracted_id, err_msg = validate_youtube_url(test_input.strip())
        if is_valid:
            col_res, col_act = st.columns([3, 1])
            with col_res:
                st.success(f"✅ Valid URL format detected! Video ID: **`{extracted_id}`**")
            with col_act:
                if st.button("Transcribe This Video", key="load_tested_url", type="primary", width="stretch"):
                    st.session_state["url_input"] = test_input.strip()
                    st.session_state["active_view"] = "transcribe"
                    st.session_state["error_message"] = None
                    st.rerun()
        else:
            st.error(f"❌ {err_msg}")

    st.write("")
    st.markdown("### 📋 Supported Format Catalog")

    supported_formats = [
        {
            "title": "Standard Desktop Watch URL",
            "pattern": "https://www.youtube.com/watch?v={VIDEO_ID}",
            "example": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "desc": "The primary desktop link generated when viewing any YouTube video in your web browser.",
            "status": "Fully Supported",
        },
        {
            "title": "Shortened youtu.be Link",
            "pattern": "https://youtu.be/{VIDEO_ID}",
            "example": "https://youtu.be/dQw4w9WgXcQ",
            "desc": "The compact share URL generated when clicking YouTube's 'Share' button on desktop or mobile.",
            "status": "Fully Supported",
        },
        {
            "title": "YouTube Shorts URL",
            "pattern": "https://www.youtube.com/shorts/{VIDEO_ID}",
            "example": "https://www.youtube.com/shorts/3fK8nBqZ-qM",
            "desc": "Vertical short-form video URLs. Extracted seamlessly just like standard long-form videos.",
            "status": "Fully Supported",
        },
        {
            "title": "Mobile Web URL",
            "pattern": "https://m.youtube.com/watch?v={VIDEO_ID}",
            "example": "https://m.youtube.com/watch?v=dQw4w9WgXcQ",
            "desc": "Links copied from mobile browser sessions (e.g. Chrome or Safari on iOS and Android).",
            "status": "Fully Supported",
        },
        {
            "title": "Embedded Video Player",
            "pattern": "https://www.youtube.com/embed/{VIDEO_ID}",
            "example": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "desc": "Embed URLs used inside blogs, iframe embeds, and educational documentation platforms.",
            "status": "Fully Supported",
        },
        {
            "title": "Timestamped Video URL",
            "pattern": "https://www.youtube.com/watch?v={VIDEO_ID}&t={SECONDS}s",
            "example": "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s",
            "desc": "Links with a specific timestamp query parameter. The parameter is safely parsed without breaking extraction.",
            "status": "Fully Supported",
        },
        {
            "title": "Playlist Context Link",
            "pattern": "https://www.youtube.com/watch?v={VIDEO_ID}&list={PLAYLIST_ID}",
            "example": "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ",
            "desc": "Video links with playlist parameters attached. The video ID is isolated cleanly for transcript extraction.",
            "status": "Fully Supported",
        },
        {
            "title": "Raw 11-Character Video ID",
            "pattern": "{VIDEO_ID} (11 alphanumeric characters)",
            "example": "dQw4w9WgXcQ",
            "desc": "Direct input of YouTube's 11-character video identifier without any surrounding domain or protocol.",
            "status": "Fully Supported",
        },
    ]

    for idx, fmt in enumerate(supported_formats):
        col_info, col_btn = st.columns([3.5, 1], gap="medium")
        with col_info:
            st.markdown(
                f"""
                <div class="format-spec-card">
                    <div class="format-spec-header">
                        <span class="format-spec-title">{fmt['title']}</span>
                        <span class="format-spec-badge">{fmt['status']}</span>
                    </div>
                    <div class="format-spec-desc">{fmt['desc']}</div>
                    <div class="format-spec-code"><code>{fmt['example']}</code></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_btn:
            st.write("")
            if st.button("Use Sample", key=f"use_fmt_{idx}", width="stretch"):
                st.session_state["url_input"] = fmt["example"]
                st.session_state["active_view"] = "transcribe"
                st.session_state["error_message"] = None
                st.rerun()


# =============================================================================
# 3. Export Options View
# =============================================================================

def render_export_options_view() -> None:
    """Render comprehensive Export Options view with comparison preview."""
    render_back_button("export_options")
    render_view_header(
        badge_text="EXPORT FORMATS & COMPARISON",
        title_text="Export & Download Options",
        subtitle_text="Choose the exact format needed for your workflow: clean AI prompt text, timestamped lecture study notes, or millisecond-accurate video subtitles.",
    )

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown(
            f"""
            <div class="export-spec-card">
                <div class="export-spec-header">
                    <div class="export-spec-icon txt">{ICON_DASH_TXT}</div>
                    <div>
                        <div class="export-spec-name">Clean Reading Text (.txt)</div>
                        <div class="export-spec-meta">Pure Prose • Zero Timestamps</div>
                    </div>
                </div>
                <div class="export-spec-body">
                    <p>
                        Exports the entire transcript as clean, uninterrupted prose with natural paragraph flow. 
                        <strong>Contains absolutely zero bracketed timestamps</strong>, speaker indices, or time codes.
                    </p>
                    <div class="export-spec-usecases">
                        <span class="export-tag">ChatGPT / Claude Prompts</span>
                        <span class="export-tag">Notion & Obsidian Notes</span>
                        <span class="export-tag">Blog & Article Drafting</span>
                        <span class="export-tag">Document Summaries</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="export-spec-card">
                <div class="export-spec-header">
                    <div class="export-spec-icon srt">{ICON_DASH_SRT}</div>
                    <div>
                        <div class="export-spec-name">SRT Subtitles (.srt)</div>
                        <div class="export-spec-meta">SubRip Standard • Millisecond Accuracy</div>
                    </div>
                </div>
                <div class="export-spec-body">
                    <p>
                        The worldwide industry standard subtitle file format. Includes sequential entry numbering, 
                        exact start and end timecodes formatted as <code>HH:MM:SS,mmm</code>, and speech text lines.
                    </p>
                    <div class="export-spec-usecases">
                        <span class="export-tag">Adobe Premiere Pro</span>
                        <span class="export-tag">DaVinci Resolve</span>
                        <span class="export-tag">Final Cut Pro</span>
                        <span class="export-tag">VLC Media Player</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="export-spec-card">
                <div class="export-spec-header">
                    <div class="export-spec-icon time">{ICON_HOW_IT_WORKS}</div>
                    <div>
                        <div class="export-spec-name">Timestamped Text (.txt)</div>
                        <div class="export-spec-meta">Segmented Lines • [MM:SS] Markers</div>
                    </div>
                </div>
                <div class="export-spec-body">
                    <p>
                        Formats speech into chronologically indexed lines prefixed with clean start timestamps. 
                        Ideal for following along during video playback or citing specific audio moments.
                    </p>
                    <div class="export-spec-usecases">
                        <span class="export-tag">Lecture Study Notes</span>
                        <span class="export-tag">Podcast Transcriptions</span>
                        <span class="export-tag">Legal & Meeting Minutes</span>
                        <span class="export-tag">Video Chapter Creation</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="export-spec-card">
                <div class="export-spec-header">
                    <div class="export-spec-icon vtt">{ICON_DASH_VTT}</div>
                    <div>
                        <div class="export-spec-name">WebVTT Subtitles (.vtt)</div>
                        <div class="export-spec-meta">W3C Standard • HTML5 Video Ready</div>
                    </div>
                </div>
                <div class="export-spec-body">
                    <p>
                        Web Video Text Tracks format featuring the <code>WEBVTT</code> header and period-separated 
                        millisecond precision (<code>00:00:00.000</code>). Directly compatible with web browsers.
                    </p>
                    <div class="export-spec-usecases">
                        <span class="export-tag">HTML5 &lt;track&gt; Tag</span>
                        <span class="export-tag">LMS & E-Learning Platforms</span>
                        <span class="export-tag">Video.js & Plyr Players</span>
                        <span class="export-tag">Web Accessibility</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Interactive Comparison Snippet Tabs
    st.write("")
    st.markdown("### 🔍 Side-by-Side Format Preview")
    st.caption("Inspect how the exact same 15-second speech snippet formats across each output option:")

    tab_txt, tab_time, tab_srt, tab_vtt = st.tabs([
        "📄 Clean Reading TXT",
        "⏱️ Timestamped TXT",
        "🎬 SRT Subtitle",
        "🌐 WebVTT",
    ])

    sample_sentence = "Artificial intelligence has rapidly evolved over the past decade. Today, language models can understand context and summarize long-form video lectures in mere seconds."

    with tab_txt:
        st.code(sample_sentence, language="text")
        st.caption("Notice: Clean continuous prose with zero brackets or timestamps.")

    with tab_time:
        st.code(
            "[00:00] Artificial intelligence has rapidly evolved over the past decade.\n"
            "[00:05] Today, language models can understand context.\n"
            "[00:09] And summarize long-form video lectures in mere seconds.",
            language="text",
        )

    with tab_srt:
        st.code(
            "1\n00:00:00,000 --> 00:00:05,200\nArtificial intelligence has rapidly evolved over the past decade.\n\n"
            "2\n00:00:05,200 --> 00:00:09,100\nToday, language models can understand context.\n\n"
            "3\n00:00:09,100 --> 00:00:14,500\nAnd summarize long-form video lectures in mere seconds.",
            language="text",
        )

    with tab_vtt:
        st.code(
            "WEBVTT\n\n"
            "00:00:00.000 --> 00:00:05.200\nArtificial intelligence has rapidly evolved over the past decade.\n\n"
            "00:00:05.200 --> 00:00:09.100\nToday, language models can understand context.\n\n"
            "00:00:09.100 --> 00:00:14.500\nAnd summarize long-form video lectures in mere seconds.",
            language="text",
        )


# =============================================================================
# 4. FAQ View
# =============================================================================

def render_faq_view() -> None:
    """Render comprehensive FAQ view with searchable expanders."""
    render_back_button("faq")
    render_view_header(
        badge_text="KNOWLEDGE BASE",
        title_text="Frequently Asked Questions",
        subtitle_text="Everything you need to know about transcript extraction, languages, cloud rate limits, and exports.",
    )

    faqs = [
        {
            "q": "Is YouTube Transcript Studio free to use?",
            "a": "Yes! YouTube Transcript Studio is 100% free with unlimited extractions. No accounts, login credentials, subscriptions, or API keys are required.",
        },
        {
            "q": "Why does a video show 'No transcript found' or 'Transcripts disabled'?",
            "a": "Transcripts may be unavailable for a few reasons:\n\n1. **Creator Settings:** The video creator explicitly disabled subtitle access in their YouTube Studio dashboard.\n2. **Processing Delay:** If the video was uploaded very recently, YouTube's auto-caption AI may still be processing the audio.\n3. **No Speech:** The video contains only background music, ambient sound, or silent video footage.\n4. **Restricted Content:** Private videos, age-restricted videos, or videos blocked in your geographic region cannot provide public subtitles.",
        },
        {
            "q": "How does the language selector work and which language is default?",
            "a": "Our engine queries YouTube's audio metadata to detect the **actual original spoken language** of the video. If the creator uploaded a human-edited transcript in that native tongue, we select it as the default. If only auto-generated captions exist, that native track is selected. You can switch to any other creator-uploaded language or translated language at any time from the language dropdown.",
        },
        {
            "q": "Why did I encounter 'We couldn't retrieve the transcript right now. Please check your connection'?",
            "a": "When running on cloud hosting environments (such as Streamlit Community Cloud on AWS EC2), YouTube frequently throttles desktop scrapers from known cloud datacenter IP addresses with HTTP 429 rate limits.\n\nOur app includes an automatic **InnerTube Android Mobile API fallback** that bypasses desktop bot challenges. If you are self-hosting or deploying on Streamlit Cloud, you can also configure `YOUTUBE_PROXY` in your Streamlit Secrets to route through a residential or datacenter proxy.",
        },
        {
            "q": "Can I extract transcripts from YouTube Shorts?",
            "a": "Yes! Just copy any YouTube Shorts URL (e.g. `https://www.youtube.com/shorts/...`) and paste it into the search box. The transcript will be extracted and formatted exactly like a standard video.",
        },
        {
            "q": "Are downloaded TXT files clean of timestamps?",
            "a": "Yes! When you click **Download TXT (Reading)** or copy to clipboard in Reading mode, the output contains pure prose with zero bracketed timestamps. It is designed to be pasted directly into LLMs (ChatGPT, Claude, Gemini) or notes apps without manual cleanup.",
        },
        {
            "q": "Is there a maximum video length limit?",
            "a": "No hard limit exists. We have verified extractions from short 15-second Shorts all the way up to 3+ hour conference streams containing more than 28,000 words. Long videos stream with a generous 45-second timeout.",
        },
        {
            "q": "Do you store or log my transcribed videos or transcripts?",
            "a": "No. We respect user privacy completely. Transcripts are retrieved and rendered ephemerally in active browser session state. Nothing is stored in a database or tracked.",
        },
    ]

    for item in faqs:
        with st.expander(f"❓ {item['q']}", expanded=False):
            st.markdown(item["a"])

    st.write("")
    st.markdown(
        f"""
        <div class="sidebar-tip-card">
            <div class="sidebar-tip-header">
                <div class="sidebar-tip-badge">{ICON_SPARKLES}</div>
                <span>Still have questions?</span>
            </div>
            <div class="sidebar-tip-desc">
                Feel free to share your question or suggestion directly through our Feedback tab!
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# 5. About View
# =============================================================================

def render_about_view() -> None:
    """Render comprehensive About view with mission, features, and tech stack."""
    render_back_button("about")
    render_view_header(
        badge_text="ABOUT THE STUDIO",
        title_text="About YouTube Transcript Studio",
        subtitle_text="A high-performance, developer-grade web tool designed to extract, format, and export YouTube transcripts with zero friction.",
    )

    col1, col2 = st.columns([1.8, 1.2], gap="large")

    with col1:
        st.markdown("### 🎯 Mission & Philosophy")
        st.markdown(
            """
            Video is the world's richest educational medium, but skimming, searching, citing, and extracting 
            information from video is notoriously slow.
            
            **YouTube Transcript Studio** transforms spoken video knowledge into structured, searchable text. 
            Whether you are a student preparing study summaries, a researcher compiling citations, a video editor 
            generating subtitle files, or an AI developer preparing training data, this tool gets you from video link 
            to clean text in seconds.
            """
        )

        st.markdown("### ✨ Core Highlights")
        st.markdown(
            """
            - ⚡ **Sub-Second Extraction:** Fast asynchronous streaming for videos of any length.
            - 🛡️ **Dual-Engine Cloud Resilience:** InnerTube Android player mobile fallback bypasses cloud datacenter IP blocks.
            - 🌐 **Spoken Language Auto-Detection:** Automatically discovers native video audio languages and manual creator tracks.
            - 📄 **4 Output Formats:** Clean TXT, Timestamped lines, SRT SubRip files, and WebVTT tracks.
            - 🔒 **Zero-Data Tracking:** Private and ephemeral execution with no cookies or telemetry.
            """
        )

    with col2:
        st.markdown(
            f"""
            <div class="tech-spec-box">
                <div class="tech-spec-header">
                    <div class="info-card-icon">{ICON_GEAR}</div>
                    <span class="tech-spec-title">Technology Stack</span>
                </div>
                <div class="tech-spec-row">
                    <span class="tech-label">Framework</span>
                    <span class="tech-val">Streamlit 1.65+</span>
                </div>
                <div class="tech-spec-row">
                    <span class="tech-label">Language</span>
                    <span class="tech-val">Python 3.13 / 3.14</span>
                </div>
                <div class="tech-spec-row">
                    <span class="tech-label">Extraction</span>
                    <span class="tech-val">YouTube Transcript API</span>
                </div>
                <div class="tech-spec-row">
                    <span class="tech-label">Mobile Fallback</span>
                    <span class="tech-val">InnerTube Android v20</span>
                </div>
                <div class="tech-spec-row">
                    <span class="tech-label">XML Stream</span>
                    <span class="tech-val">ElementTree / Gzip</span>
                </div>
                <div class="tech-spec-row">
                    <span class="tech-label">Design System</span>
                    <span class="tech-val">Dark Cyberpunk Studio</span>
                </div>
                <div class="tech-spec-row">
                    <span class="tech-label">License</span>
                    <span class="tech-val">Open Source MIT</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =============================================================================
# 6. Feedback View
# =============================================================================

def render_feedback_view() -> None:
    """Render interactive Feedback submission form with state persistence."""
    render_back_button("feedback")
    render_view_header(
        badge_text="COMMUNITY FEEDBACK",
        title_text="Share Your Feedback",
        subtitle_text="Your thoughts and bug reports directly shape YouTube Transcript Studio. Tell us what you like or what we should build next!",
    )

    if "feedback_submissions" not in st.session_state:
        st.session_state["feedback_submissions"] = []

    with st.form("user_feedback_form", clear_on_submit=True):
        col_rating, col_cat = st.columns(2)

        with col_rating:
            rating = st.select_slider(
                "Overall Satisfaction Rating:",
                options=["⭐ 1 - Poor", "⭐⭐ 2 - Fair", "⭐⭐⭐ 3 - Good", "⭐⭐⭐⭐ 4 - Very Good", "⭐⭐⭐⭐⭐ 5 - Excellent"],
                value="⭐⭐⭐⭐⭐ 5 - Excellent",
            )

        with col_cat:
            category = st.selectbox(
                "Feedback Category:",
                options=[
                    "✨ Feature Request",
                    "🐛 Bug Report",
                    "🌐 Language / Subtitle Accuracy",
                    "💾 Export Options Suggestion",
                    "🎨 UI / Design Feedback",
                    "💡 General Thoughts",
                ],
            )

        col_name, col_email = st.columns(2)
        with col_name:
            user_name = st.text_input("Your Name (Optional):", placeholder="e.g. Alex Smith")
        with col_email:
            user_email = st.text_input("Your Email (Optional, for updates):", placeholder="alex@example.com")

        feedback_message = st.text_area(
            "Your Feedback or Suggestion *",
            placeholder="Tell us what you liked, what went wrong, or what feature you'd like to see added...",
            height=130,
        )

        submitted = st.form_submit_button("Submit Feedback", type="primary", width="stretch")

        if submitted:
            if not feedback_message.strip():
                st.error("Please enter a message before submitting.")
            else:
                entry = {
                    "rating": rating,
                    "category": category,
                    "name": user_name.strip() or "Anonymous",
                    "email": user_email.strip() or "Not provided",
                    "message": feedback_message.strip(),
                }
                st.session_state["feedback_submissions"].append(entry)
                st.success("🎉 Thank you! Your feedback has been received and helps improve YouTube Transcript Studio.")
                st.balloons()

    # Display recently submitted feedback in this session if any
    submissions = st.session_state.get("feedback_submissions", [])
    if submissions:
        st.write("")
        st.markdown("### 📝 Submissions in Current Session")
        for idx, item in enumerate(reversed(submissions)):
            st.markdown(
                f"""
                <div class="feedback-card">
                    <div class="feedback-card-header">
                        <strong>{html.escape(item['name'])}</strong> — <em>{html.escape(item['category'])}</em>
                        <span>{html.escape(item['rating'])}</span>
                    </div>
                    <div class="feedback-card-body">{html.escape(item['message'])}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
