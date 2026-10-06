"""YouTube Transcript Extractor - Main Streamlit Application.

Extract, read, copy, and download transcripts from YouTube videos instantly.
"""

import logging
import warnings
from typing import Optional, List, Tuple
import streamlit as st

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (%(name)s) %(message)s",
)
logger = logging.getLogger("yt_transcript_app")

# Suppress urllib3 version warning if present
try:
    from requests.exceptions import RequestsDependencyWarning
    warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
except ImportError:
    pass

from models.transcript_models import (
    VideoMetadata,
    TranscriptLanguage,
    TranscriptResult,
)
from utils.url_utils import validate_youtube_url, build_canonical_url
from services.youtube_service import YouTubeService
from services.transcript_service import (
    TranscriptService,
    TranscriptDisabledError,
    NoTranscriptFoundError,
    VideoUnavailableError,
    NetworkConnectionError,
    LanguageUnavailableError,
    TranscriptServiceError,
)
from ui.styles import get_custom_css
from ui.components import (
    render_header,
    render_sidebar,
    render_empty_state,
    render_video_metadata_card,
    render_stats_cards,
    render_transcript_display,
    render_download_section,
)


# =============================================================================
# Cached Service Calls
# =============================================================================

@st.cache_data(show_spinner=False, max_entries=150, ttl=3600)
def fetch_cached_metadata(video_id: str) -> VideoMetadata:
    """Fetch video metadata with memory-safe cache."""
    return YouTubeService.get_video_metadata(video_id)


@st.cache_data(show_spinner=False, max_entries=150, ttl=3600)
def fetch_cached_languages(video_id: str) -> List[TranscriptLanguage]:
    """Fetch available subtitle tracks with cache."""
    return TranscriptService.get_available_transcripts(video_id)


@st.cache_data(show_spinner=False, max_entries=150, ttl=3600)
def fetch_cached_transcript(video_id: str, language_code: Optional[str] = None) -> TranscriptResult:
    """Fetch and format transcript with cache."""
    return TranscriptService.get_transcript(video_id, language_code)


# =============================================================================
# Streamlit Application
# =============================================================================

def init_session_state() -> None:
    """Initialize necessary session state variables."""
    default_state = {
        "url_input": "",
        "current_video_id": None,
        "metadata": None,
        "available_languages": [],
        "selected_language_code": None,
        "transcript_result": None,
        "error_message": None,
        "error_type": None,
        "view_mode": "Reading",
    }
    for key, value in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_results() -> None:
    """Reset transcript results and errors."""
    st.session_state.current_video_id = None
    st.session_state.metadata = None
    st.session_state.available_languages = []
    st.session_state.selected_language_code = None
    st.session_state.transcript_result = None
    st.session_state.error_message = None
    st.session_state.error_type = None


def main() -> None:
    """Application entry point."""
    st.set_page_config(
        page_title="YouTube Transcript Extractor",
        page_icon="🎬",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    # Inject custom styling
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    # Initialize session state
    init_session_state()

    # Render sidebar & hero header
    render_sidebar()
    render_header()

    # =========================================================================
    # URL Input Card
    # =========================================================================
    st.markdown("#### 🔗 YouTube Video URL")
    
    with st.container():
        input_col, btn_col = st.columns([3.8, 1.2], vertical_alignment="bottom")

        with input_col:
            user_url = st.text_input(
                label="YouTube Video URL",
                placeholder="Paste YouTube video URL here... (e.g. https://www.youtube.com/watch?v=...)",
                key="url_input_box",
                value=st.session_state.url_input,
                label_visibility="collapsed",
            )

        with btn_col:
            fetch_btn = st.button(
                "🚀 Get Transcript",
                type="primary",
                use_container_width=True,
            )

    # Trigger processing on button click
    if fetch_btn:
        st.session_state.url_input = user_url.strip()
        is_valid, video_id, validation_error = validate_youtube_url(st.session_state.url_input)

        if not is_valid:
            reset_results()
            st.session_state.error_type = "validation"
            st.session_state.error_message = validation_error
        else:
            reset_results()
            st.session_state.current_video_id = video_id
            
            # Retrieve video metadata and available languages
            with st.status("⏳ Fetching transcript...", expanded=True) as status_box:
                try:
                    status_box.write("📡 Connecting to YouTube and inspecting video...")
                    metadata = fetch_cached_metadata(video_id)
                    st.session_state.metadata = metadata

                    status_box.write("🔍 Finding available transcripts and languages...")
                    available_langs = fetch_cached_languages(video_id)
                    st.session_state.available_languages = available_langs

                    if not available_langs:
                        raise NoTranscriptFoundError(
                            "This YouTube video does not currently have an accessible transcript."
                        )

                    # Default to first available language (manual preferred by service sort)
                    default_lang = available_langs[0].language_code
                    st.session_state.selected_language_code = default_lang

                    status_box.write(f"📝 Extracting transcript track ({available_langs[0].language})...")
                    transcript_res = fetch_cached_transcript(video_id, default_lang)
                    st.session_state.transcript_result = transcript_res

                    status_box.update(
                        label="✅ Transcript retrieved successfully!",
                        state="complete",
                        expanded=False,
                    )
                except TranscriptDisabledError as exc:
                    st.session_state.error_type = "disabled"
                    st.session_state.error_message = exc.user_message
                    status_box.update(label="Transcript unavailable", state="error", expanded=False)
                except NoTranscriptFoundError as exc:
                    st.session_state.error_type = "not_found"
                    st.session_state.error_message = exc.user_message
                    status_box.update(label="No transcript found", state="error", expanded=False)
                except VideoUnavailableError as exc:
                    st.session_state.error_type = "video_unavailable"
                    st.session_state.error_message = exc.user_message
                    status_box.update(label="Video unavailable", state="error", expanded=False)
                except NetworkConnectionError as exc:
                    st.session_state.error_type = "network"
                    st.session_state.error_message = exc.user_message
                    status_box.update(label="Connection error", state="error", expanded=False)
                except Exception as exc:
                    logger.exception("Unexpected error during transcript extraction for %s", video_id)
                    st.session_state.error_type = "general"
                    st.session_state.error_message = (
                        "We couldn't retrieve the transcript right now. Please verify the URL and try again."
                    )
                    status_box.update(label="Extraction failed", state="error", expanded=False)

    # =========================================================================
    # Error Display
    # =========================================================================
    if st.session_state.error_message:
        err_msg = st.session_state.error_message
        err_type = st.session_state.error_type

        if err_type == "validation":
            if "Please enter" in err_msg:
                st.warning(f"⚠️ {err_msg}")
            else:
                st.error(f"❌ {err_msg}")
        elif err_type == "disabled":
            st.error(f"🚫 **Transcript Unavailable**\n\n{err_msg}")
        elif err_type == "not_found":
            st.info(f"😕 **Transcript Not Available**\n\n{err_msg}")
        elif err_type == "video_unavailable":
            st.error(f"❌ **Video Unavailable**\n\n{err_msg}")
        elif err_type == "network":
            st.error(f"🌐 **Connection Error**\n\n{err_msg}")
        else:
            st.error(f"⚠️ **Error**\n\n{err_msg}")

    # =========================================================================
    # Results Display
    # =========================================================================
    elif st.session_state.transcript_result and st.session_state.metadata:
        result: TranscriptResult = st.session_state.transcript_result
        metadata: VideoMetadata = st.session_state.metadata
        available_langs: List[TranscriptLanguage] = st.session_state.available_languages

        st.success("✅ **Transcript Ready** — Your YouTube transcript has been successfully extracted.")

        # Video Metadata Card
        render_video_metadata_card(metadata, result)

        # Statistics Cards
        render_stats_cards(result)

        st.markdown("---")

        # Controls Row: Language Selector (if multiple) & View Mode Switcher
        ctrl_col1, ctrl_col2 = st.columns([1.3, 1.2], vertical_alignment="center")

        with ctrl_col1:
            if len(available_langs) > 1:
                lang_options = [lang.language_code for lang in available_langs]
                lang_labels = {lang.language_code: lang.display_name for lang in available_langs}
                current_idx = (
                    lang_options.index(st.session_state.selected_language_code)
                    if st.session_state.selected_language_code in lang_options
                    else 0
                )

                selected_code = st.selectbox(
                    label="🌐 Available Languages:",
                    options=lang_options,
                    format_func=lambda code: lang_labels.get(code, code),
                    index=current_idx,
                    key="language_selector",
                )

                # If user switched language, fetch new transcript
                if selected_code != st.session_state.selected_language_code:
                    st.session_state.selected_language_code = selected_code
                    with st.spinner("🔄 Loading selected transcript language..."):
                        try:
                            new_result = fetch_cached_transcript(
                                st.session_state.current_video_id, selected_code
                            )
                            st.session_state.transcript_result = new_result
                            st.rerun()
                        except Exception as exc:
                            logger.error("Failed to fetch selected language %s: %s", selected_code, exc)
                            st.error(f"🌐 Could not load transcript for {selected_code}.")
            else:
                st.markdown(
                    f"**🌐 Language:** {result.language} ({'Auto-generated' if result.is_generated else 'Manual'})"
                )

        with ctrl_col2:
            view_mode = st.radio(
                label="Transcript View:",
                options=["Reading", "With Timestamps"],
                horizontal=True,
                index=0 if st.session_state.view_mode == "Reading" else 1,
                key="view_mode_toggle",
            )
            st.session_state.view_mode = view_mode

        # Determine currently displayed transcript text
        is_timestamp_mode = view_mode == "With Timestamps"
        current_text = result.timestamped_text if is_timestamp_mode else result.reading_text

        st.markdown("### 📝 Transcript")
        render_transcript_display(current_text, is_timestamp_mode=is_timestamp_mode)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        # Action Buttons: Copy, Download TXT, SRT, VTT
        render_download_section(
            result=result,
            metadata=metadata,
            current_view_text=current_text,
            view_mode=view_mode,
        )

    else:
        # Empty State
        render_empty_state()


if __name__ == "__main__":
    main()