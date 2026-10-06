"""
Centralized UI Assets & Crisp Vector Icons
=========================================
Provides base64-encoded visual graphics and high-fidelity SVG outline icons (Lucide / Feather style)
matching the reference designs.
"""

import base64
import os
from functools import lru_cache

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")


@lru_cache(maxsize=1)
def get_hero_art_b64() -> str:
    """Return base64 string of high-DPI 3D hero artwork."""
    path = os.path.join(ASSETS_DIR, "hero_3d_art.png")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""


@lru_cache(maxsize=1)
def get_clapperboard_b64() -> str:
    """Return base64 string of high-DPI clapperboard graphic."""
    path = os.path.join(ASSETS_DIR, "clapperboard.png")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""


@lru_cache(maxsize=1)
def get_yt_logo_b64() -> str:
    """Return base64 string of high-DPI YouTube badge logo."""
    path = os.path.join(ASSETS_DIR, "youtube_logo.png")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""


# =============================================================================
# Clean Vector SVG Icons (Lucide / Feather / Heroicons)
# =============================================================================

# Sidebar Navigation Icons
ICON_HOME = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>'
    '<polyline points="9 22 9 12 15 12 15 22"></polyline>'
    '</svg>'
)

ICON_ABOUT = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="10"></circle>'
    '<line x1="12" y1="16" x2="12" y2="12"></line>'
    '<line x1="12" y1="8" x2="12.01" y2="8"></line>'
    '</svg>'
)

ICON_HOW_IT_WORKS = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="10"></circle>'
    '<polygon points="10 8 16 12 10 16 10 8" fill="currentColor"></polygon>'
    '</svg>'
)

ICON_TRANSCRIBE = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<rect x="2" y="4" width="20" height="16" rx="4"></rect>'
    '<polygon points="10 8 16 12 10 16 10 8" fill="currentColor"></polygon>'
    '</svg>'
)

ICON_HISTORY = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="10"></circle>'
    '<polyline points="12 6 12 12 16 14"></polyline>'
    '</svg>'
)

ICON_EXPORT = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>'
    '<polyline points="14 2 14 8 20 8"></polyline>'
    '<line x1="16" y1="13" x2="8" y2="13"></line>'
    '<line x1="16" y1="17" x2="8" y2="17"></line>'
    '</svg>'
)

ICON_LINKS = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>'
    '<path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>'
    '</svg>'
)

ICON_CHAIN = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>'
    '<path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>'
    '</svg>'
)

ICON_FAQ = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="10"></circle>'
    '<path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>'
    '<line x1="12" y1="17" x2="12.01" y2="17"></line>'
    '</svg>'
)

ICON_FEEDBACK = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>'
    '</svg>'
)

# Sidebar Badges
ICON_LIGHTNING = (
    '<svg width="15" height="15" viewBox="0 0 24 24" fill="#ffffff" stroke="#ffffff" '
    'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
    '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>'
    '</svg>'
)

ICON_CROWN = (
    '<svg width="15" height="15" viewBox="0 0 24 24" fill="#f59e0b" stroke="#f59e0b" '
    'stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M2 4l3 12h14l3-12-6 7-4-7-4 7-6-7zm3 16h14v2H5v-2z"></path>'
    '</svg>'
)

# Top Bar Icons
ICON_SUN = (
    '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="5"></circle>'
    '<line x1="12" y1="1" x2="12" y2="3"></line>'
    '<line x1="12" y1="21" x2="12" y2="23"></line>'
    '<line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>'
    '<line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>'
    '<line x1="1" y1="12" x2="3" y2="12"></line>'
    '<line x1="21" y1="12" x2="23" y2="12"></line>'
    '<line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>'
    '<line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>'
    '</svg>'
)

ICON_CHEVRON_DOWN = (
    '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
    '<polyline points="6 9 12 15 18 9"></polyline>'
    '</svg>'
)

# Action / Feature Icons
ICON_SPARKLES = (
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3L12 3z"></path>'
    '</svg>'
)

ICON_LIGHTBULB = (
    '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M9 18h6"></path>'
    '<path d="M10 22h4"></path>'
    '<path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5.76.76 1.23 1.52 1.41 2.5"></path>'
    '</svg>'
)

ICON_TRASH = (
    '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<polyline points="3 6 5 6 21 6"></polyline>'
    '<path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>'
    '</svg>'
)

ICON_GEAR = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="3"></circle>'
    '<path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>'
    '</svg>'
)

# Step Cards Icons
ICON_STEP1_LINK = (
    '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#ef4444" '
    'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>'
    '<path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>'
    '</svg>'
)

ICON_STEP2_DETECT = (
    '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" '
    'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>'
    '<polyline points="14 2 14 8 20 8"></polyline>'
    '<circle cx="11.5" cy="14.5" r="2.5"></circle>'
    '<line x1="13.5" y1="16.5" x2="16" y2="19"></line>'
    '</svg>'
)

ICON_STEP3_MODE = (
    '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#a855f7" '
    'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
    '<line x1="8" y1="6" x2="21" y2="6"></line>'
    '<line x1="8" y1="12" x2="21" y2="12"></line>'
    '<line x1="8" y1="18" x2="21" y2="18"></line>'
    '<circle cx="4" cy="6" r="1.5" fill="#a855f7"></circle>'
    '<circle cx="4" cy="12" r="1.5" fill="#a855f7"></circle>'
    '<circle cx="4" cy="18" r="1.5" fill="#a855f7"></circle>'
    '</svg>'
)

ICON_STEP4_EXPORT = (
    '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#10b981" '
    'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>'
    '<polyline points="7 10 12 15 17 10"></polyline>'
    '<line x1="12" y1="15" x2="12" y2="3"></line>'
    '</svg>'
)

# Dashboard Result Icons
ICON_DASH_COPY = (
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
    '<rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>'
    '<path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>'
    '</svg>'
)

ICON_DASH_TXT = (
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>'
    '<polyline points="7 10 12 15 17 10"></polyline>'
    '<line x1="12" y1="15" x2="12" y2="3"></line>'
    '</svg>'
)

ICON_DASH_SRT = (
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
    '<rect x="3" y="4" width="18" height="16" rx="2"></rect>'
    '<line x1="7" y1="10" x2="11" y2="10"></line>'
    '<line x1="9" y1="10" x2="9" y2="15"></line>'
    '<line x1="13" y1="12.5" x2="17" y2="12.5"></line>'
    '</svg>'
)

ICON_DASH_VTT = (
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>'
    '<polyline points="14 2 14 8 20 8"></polyline>'
    '<line x1="10" y1="12" x2="14" y2="16"></line>'
    '<line x1="14" y1="12" x2="10" y2="16"></line>'
    '</svg>'
)

ICON_STAT_WORDS = (
    '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#a855f7" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>'
    '<polyline points="14 2 14 8 20 8"></polyline>'
    '<line x1="16" y1="13" x2="8" y2="13"></line>'
    '<line x1="16" y1="17" x2="8" y2="17"></line>'
    '</svg>'
)

ICON_STAT_DURATION = (
    '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#60a5fa" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="10"></circle>'
    '<polyline points="12 6 12 12 16 14"></polyline>'
    '</svg>'
)
