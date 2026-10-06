"""Tests for UI assets, base64 loaders, and vector icons."""

import pytest
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


class TestUIAssets:
    def test_base64_assets_exist_and_non_empty(self):
        hero = get_hero_art_b64()
        clapper = get_clapperboard_b64()
        logo = get_yt_logo_b64()

        assert len(hero) > 1000, "Hero 3D artwork base64 should be non-empty and reasonably sized"
        assert len(clapper) > 500, "Clapperboard base64 should be non-empty"
        assert len(logo) > 100, "YouTube logo base64 should be non-empty"

    def test_svg_icons_are_valid_svg_markup(self):
        icons = [
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
        ]

        for icon in icons:
            assert icon.strip().startswith("<svg"), f"Icon {icon[:20]} should start with <svg>"
            assert icon.strip().endswith("</svg>"), f"Icon {icon[-20:]} should end with </svg>"
            assert "viewBox" in icon, f"Icon {icon[:30]} should have viewBox attribute"
