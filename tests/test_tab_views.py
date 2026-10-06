"""Tests for dedicated content views and navigation tabs."""

from unittest.mock import MagicMock, patch
import pytest

from ui.tab_views import (
    render_how_it_works_view,
    render_supported_links_view,
    render_export_options_view,
    render_faq_view,
    render_about_view,
    render_feedback_view,
)
from ui.components import render_top_navigation_tabs, render_sidebar


class TestTabViews:
    """Test rendering of all dedicated content views."""

    def test_render_how_it_works_view(self):
        with patch("streamlit.markdown") as mock_md, \
             patch("streamlit.button") as mock_btn, \
             patch("streamlit.columns", return_value=[MagicMock(), MagicMock()]):
            render_how_it_works_view()
            assert mock_md.called
            # Verify critical keywords in rendered content
            calls_text = " ".join(call.args[0] for call in mock_md.call_args_list if call.args)
            assert "How YouTube Transcript Studio Works" in calls_text
            assert "Universal URL Parsing" in calls_text
            assert "InnerTube" in calls_text

    def test_render_supported_links_view(self):
        with patch("streamlit.markdown") as mock_md, \
             patch("streamlit.button") as mock_btn, \
             patch("streamlit.text_input", return_value=""), \
             patch("streamlit.columns", return_value=[MagicMock(), MagicMock()]):
            render_supported_links_view()
            calls_text = " ".join(call.args[0] for call in mock_md.call_args_list if call.args)
            assert "Supported YouTube Link Formats" in calls_text
            assert "Standard Desktop Watch URL" in calls_text
            assert "Shorts" in calls_text

    def test_render_export_options_view(self):
        with patch("streamlit.markdown") as mock_md, \
             patch("streamlit.button"), \
             patch("streamlit.tabs", return_value=[MagicMock(), MagicMock(), MagicMock(), MagicMock()]), \
             patch("streamlit.code"), \
             patch("streamlit.caption"), \
             patch("streamlit.columns", return_value=[MagicMock(), MagicMock()]):
            render_export_options_view()
            calls_text = " ".join(call.args[0] for call in mock_md.call_args_list if call.args)
            assert "Export & Download Options" in calls_text
            assert "Clean Reading Text (.txt)" in calls_text
            assert "SRT Subtitles" in calls_text
            assert "WebVTT" in calls_text

    def test_render_faq_view(self):
        with patch("streamlit.markdown") as mock_md, \
             patch("streamlit.button"), \
             patch("streamlit.columns", return_value=[MagicMock(), MagicMock()]), \
             patch("streamlit.expander", return_value=MagicMock()):
            render_faq_view()
            calls_text = " ".join(call.args[0] for call in mock_md.call_args_list if call.args)
            assert "Frequently Asked Questions" in calls_text

    def test_render_about_view(self):
        with patch("streamlit.markdown") as mock_md, \
             patch("streamlit.button"), \
             patch("streamlit.columns", return_value=[MagicMock(), MagicMock()]):
            render_about_view()
            calls_text = " ".join(call.args[0] for call in mock_md.call_args_list if call.args)
            assert "About YouTube Transcript Studio" in calls_text
            assert "Streamlit" in calls_text

    def test_render_feedback_view(self):
        with patch("streamlit.markdown") as mock_md, \
             patch("streamlit.button"), \
             patch("streamlit.columns", return_value=[MagicMock(), MagicMock()]), \
             patch("streamlit.form", return_value=MagicMock()), \
             patch("streamlit.select_slider", return_value="⭐⭐⭐⭐⭐ 5 - Excellent"), \
             patch("streamlit.selectbox", return_value="✨ Feature Request"), \
             patch("streamlit.text_input", return_value=""), \
             patch("streamlit.text_area", return_value=""), \
             patch("streamlit.form_submit_button", return_value=False):
            with patch("streamlit.session_state", {"feedback_submissions": []}):
                render_feedback_view()
                calls_text = " ".join(call.args[0] for call in mock_md.call_args_list if call.args)
                assert "Share Your Feedback" in calls_text

    def test_render_top_navigation_tabs(self):
        with patch("streamlit.segmented_control", return_value="⚙️ How it Works") as mock_sc, \
             patch("streamlit.session_state", {"active_view": "transcribe"}), \
             patch("streamlit.rerun") as mock_rerun:
            render_top_navigation_tabs(active_view="transcribe")
            assert mock_sc.called
            assert mock_rerun.called

    def test_render_sidebar_interactive_buttons(self):
        with patch("streamlit.sidebar.button", return_value=False) as mock_sb_btn, \
             patch("streamlit.components.v1.html"):
            render_sidebar(is_result_page=False, active_view="transcribe")
            # Should have rendered buttons for Home, About, How it Works, Export Options, Supported Links, FAQ, Feedback
            assert mock_sb_btn.call_count >= 7
