"""YouTube Transcript Studio - Modern SaaS Application.

Recreates the reference designs with ~100% visual fidelity:
- Empty / Landing state (Screenshot 2): Hero with 3D artwork, URL input card, empty state card, 4-step How It Works cards.
- Result / Transcript state (Screenshot 1): Hero banner, 2-column video player & interactive transcript panel, bottom transcript actions and stats metrics.
"""

import logging
import warnings
from typing import Optional, List
import streamlit as st

# Suppress urllib3 version warning if present
try:
    from requests.exceptions import RequestsDependencyWarning
    warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
except ImportError:
    pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (%(name)s) %(message)s",
)
logger = logging.getLogger("yt_transcript_app")

from models.transcript_models import (
    VideoMetadata,
    TranscriptLanguage,
    TranscriptResult,
)
from utils.url_utils import validate_youtube_url
from services.youtube_service import YouTubeService
from services.transcript_service import (
    TranscriptService,
    TranscriptDisabledError,
    NoTranscriptFoundError,
    VideoUnavailableError,
    NetworkConnectionError,
    TranscriptServiceError,
)
import importlib
import sys

# Ensure UI submodules are refreshed if already in memory (handles Streamlit Cloud hot-reloads)
if "ui.components" in sys.modules:
    importlib.reload(sys.modules["ui.components"])
if "ui.styles" in sys.modules:
    importlib.reload(sys.modules["ui.styles"])

from ui.styles import get_custom_css
from ui.components import (
    render_sidebar,
    render_top_user_bar,
    render_hero,
    render_url_input_card,
    render_empty_state,
    render_how_it_works,
    render_video_card,
    render_interactive_transcript_panel,
    render_bottom_dashboard,
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
# Session State
# =============================================================================

def init_session_state() -> None:
    """Initialize session state defaults."""
    default_state = {
        "url_input": "",
        "current_video_id": None,
        "metadata": None,
        "available_langs": [],
        "selected_language_code": None,
        "transcript_result": None,
        "error_message": None,
        "error_type": None,
    }
    for key, value in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_results() -> None:
    """Clear existing transcript results and errors."""
    st.session_state.current_video_id = None
    st.session_state.metadata = None
    st.session_state.available_langs = []
    st.session_state.selected_language_code = None
    st.session_state.transcript_result = None
    st.session_state.error_message = None
    st.session_state.error_type = None


# =============================================================================
# Core Application Flow
# =============================================================================

def main() -> None:
    """Main application loop."""
    st.set_page_config(
        page_title="YouTube Transcript Studio",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Inject Centralized Design System CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    # Initialize State
    init_session_state()

    has_result = bool(st.session_state.transcript_result and st.session_state.metadata)

    # 1. Render Sidebar (Visual match to reference)
    render_sidebar(is_result_page=has_result)

    # 2. Top Right User Bar (Theme toggle + JD Avatar + User Name)
    render_top_user_bar()

    # 3. Handle Landing Page vs Result Page
    if not has_result:
        # =====================================================================
        # STATE 1: Landing / Empty State (Screenshot 2)
        # =====================================================================
        render_hero(is_result_page=False)

        # URL Input Card
        input_url, submit_clicked, clear_clicked, sample_url = render_url_input_card(
            default_url=st.session_state.url_input,
            is_result_page=False,
        )

        # Handle sample buttons (populates URL input without auto-submitting)
        if sample_url:
            st.session_state.url_input = sample_url
            st.session_state.error_message = None
            st.rerun()

        # Handle clear button
        if clear_clicked:
            reset_results()
            st.session_state.url_input = ""
            st.rerun()

        # Handle transcript extraction request
        if submit_clicked:
            st.session_state.url_input = input_url.strip()
            is_valid, video_id, validation_err = validate_youtube_url(st.session_state.url_input)

            if not is_valid:
                reset_results()
                st.session_state.error_type = "validation"
                st.session_state.error_message = validation_err
            else:
                reset_results()
                st.session_state.current_video_id = video_id

                with st.status("Extracting Transcript...", expanded=True) as status_box:
                    try:
                        status_box.write("📡 Fetching subtitle tracks...")
                        metadata = fetch_cached_metadata(video_id)
                        st.session_state.metadata = metadata

                        status_box.write("🔍 Analyzing available languages...")
                        available_langs = fetch_cached_languages(video_id)
                        st.session_state.available_langs = available_langs

                        if not available_langs:
                            raise NoTranscriptFoundError(
                                "This YouTube video does not currently have an accessible transcript."
                            )

                        # Default to the detected original video language
                        default_lang = available_langs[0].language_code
                        st.session_state.selected_language_code = default_lang

                        status_box.write(f"📝 Preparing transcript ({available_langs[0].language})...")
                        transcript_res = fetch_cached_transcript(video_id, default_lang)
                        st.session_state.transcript_result = transcript_res

                        status_box.update(
                            label="✅ Transcript ready!",
                            state="complete",
                            expanded=False,
                        )
                        st.rerun()

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
                            "Unable to extract transcript. Please verify the URL and try again."
                        )
                        status_box.update(label="Extraction failed", state="error", expanded=False)

        # Error State Display
        if st.session_state.error_message:
            st.error(f"⚠️ {st.session_state.error_message}")

        # Large Empty State Card
        render_empty_state()

        # How It Works 4-Step Cards
        render_how_it_works()

    else:
        # =====================================================================
        # STATE 2: Result / Transcript Page (Screenshot 1)
        # =====================================================================
        result: TranscriptResult = st.session_state.transcript_result
        metadata: VideoMetadata = st.session_state.metadata
        available_langs: List[TranscriptLanguage] = st.session_state.get("available_langs", [])

        # Hero Banner with embedded URL row
        render_hero(is_result_page=True, current_url=st.session_state.url_input)

        # Compact URL Input Row to easily change video anytime
        input_url, submit_clicked, _, _ = render_url_input_card(
            default_url=st.session_state.url_input,
            is_result_page=True,
        )

        if submit_clicked and input_url.strip() != st.session_state.url_input:
            st.session_state.url_input = input_url.strip()
            is_valid, video_id, val_err = validate_youtube_url(st.session_state.url_input)
            if is_valid:
                reset_results()
                st.session_state.current_video_id = video_id
                with st.spinner("Extracting transcript..."):
                    try:
                        m = fetch_cached_metadata(video_id)
                        st.session_state.metadata = m
                        langs = fetch_cached_languages(video_id)
                        st.session_state.available_langs = langs
                        if langs:
                            default_code = langs[0].language_code
                            st.session_state.selected_language_code = default_code
                            st.session_state.transcript_result = fetch_cached_transcript(video_id, default_code)
                        st.rerun()
                    except Exception as err:
                        st.error(f"Error: {err}")
            else:
                st.error(val_err)

        # Main 2-Column Dashboard Layout (Video 42% | Transcript 58%)
        col_video, col_transcript = st.columns([1.1, 1.45], gap="large")

        with col_video:
            render_video_card(metadata, result)

        with col_transcript:
            new_lang = render_interactive_transcript_panel(
                result=result,
                available_langs=available_langs,
                selected_lang_code=st.session_state.selected_language_code,
            )

            if new_lang and new_lang != st.session_state.selected_language_code:
                st.session_state.selected_language_code = new_lang
                with st.spinner("Loading selected language..."):
                    try:
                        updated_res = fetch_cached_transcript(
                            st.session_state.current_video_id, new_lang
                        )
                        st.session_state.transcript_result = updated_res
                        st.rerun()
                    except Exception as exc:
                        logger.error("Failed to load language %s: %s", new_lang, exc)
                        st.error(f"Could not load transcript for {new_lang}.")

        # Bottom Row: Transcript Actions & Stats Cards
        render_bottom_dashboard(result, metadata)


if __name__ == "__main__":
    main()