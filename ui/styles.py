"""Centralized Design System and CSS for YouTube Transcript Studio.

Accurately recreates the reference SaaS dark dashboard visual identity:
- Deep midnight navy/charcoal background (#070a13 / #0b0f19)
- Cohesive typography, glassmorphism surfaces, subtle borders, and soft glow effects
- 100% visual fidelity to reference landing and transcript states
"""

def get_custom_css() -> str:
    """Return the complete design system and CSS stylesheet."""
    return """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        /* Design Tokens: Backgrounds */
        --bg-primary: #070a13;
        --bg-secondary: #0c111d;
        --bg-sidebar: #090d18;
        --bg-card: #0e1424;
        --bg-card-glass: rgba(14, 20, 36, 0.72);
        --bg-card-hover: rgba(22, 31, 54, 0.85);
        --bg-input: #101729;
        --bg-active-row: rgba(59, 130, 246, 0.12);

        /* Design Tokens: Text */
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --text-accent-pink: #ec4899;
        --text-accent-purple: #c084fc;

        /* Design Tokens: Accents */
        --accent-red: #ef4444;
        --accent-coral: #f43f5e;
        --accent-purple: #a855f7;
        --accent-indigo: #6366f1;
        --accent-blue: #3b82f6;
        --accent-green: #10b981;
        --accent-amber: #f59e0b;

        /* Design Tokens: Borders */
        --border-subtle: rgba(255, 255, 255, 0.08);
        --border-card: rgba(255, 255, 255, 0.07);
        --border-hover: rgba(255, 255, 255, 0.16);
        --border-active: rgba(239, 68, 68, 0.45);
        --border-active-blue: rgba(59, 130, 246, 0.4);

        /* Design Tokens: Shadows & Effects */
        --shadow-card: 0 12px 36px 0 rgba(0, 0, 0, 0.45);
        --shadow-glow: 0 4px 22px rgba(239, 68, 68, 0.35);
        --shadow-glow-purple: 0 4px 22px rgba(168, 85, 247, 0.3);

        /* Design Tokens: Gradients */
        --gradient-primary: linear-gradient(135deg, #ef4444 0%, #ec4899 100%);
        --gradient-accent: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        --gradient-button: linear-gradient(90deg, #ef4444 0%, #f43f5e 100%);
        --gradient-hero-text: linear-gradient(90deg, #ffffff 0%, #ffffff 35%, #ec4899 65%, #f43f5e 100%);

        /* Design Tokens: Spacing */
        --space-xs: 4px;
        --space-sm: 8px;
        --space-md: 16px;
        --space-lg: 24px;
        --space-xl: 32px;

        /* Design Tokens: Radius */
        --radius-sm: 6px;
        --radius-md: 10px;
        --radius-lg: 16px;
        --radius-xl: 22px;
    }

    /* Base Body & App Canvas */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }

    .stApp {
        background-color: var(--bg-primary) !important;
    }

    /* Main Container Spacing */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: 2.2rem !important;
        padding-right: 2.2rem !important;
        max-width: 1420px !important;
        margin: 0 auto !important;
    }

    /* Fixed Modern Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--bg-sidebar) !important;
        border-right: 1px solid var(--border-subtle) !important;
        width: 270px !important;
        min-width: 270px !important;
        max-width: 270px !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding: 1.2rem 1rem !important;
    }

    /* Sidebar Logo / Brand Header */
    .sidebar-brand-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding-bottom: 1.5rem;
        margin-bottom: 1.2rem;
        border-bottom: 1px solid var(--border-subtle);
    }

    .sidebar-brand-logo {
        width: 36px;
        height: 25px;
        background: #ef4444;
        border-radius: 7px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
    }

    .sidebar-brand-title {
        font-size: 15px;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.15;
    }

    .sidebar-brand-subtitle {
        font-size: 12px;
        color: var(--text-secondary);
        font-weight: 400;
    }

    /* Sidebar Navigation Links */
    .sidebar-nav-group {
        display: flex;
        flex-direction: column;
        gap: 4px;
        margin-bottom: 1.5rem;
    }

    .sidebar-nav-header {
        font-size: 10px;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 8px 12px 4px 12px;
    }

    .sidebar-nav-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 9px 14px;
        border-radius: var(--radius-md);
        color: var(--text-secondary);
        font-size: 13.5px;
        font-weight: 500;
        text-decoration: none;
        transition: all 0.18s ease;
        cursor: pointer;
    }

    .sidebar-nav-item:hover {
        color: #ffffff;
        background: rgba(255, 255, 255, 0.05);
    }

    .sidebar-nav-item.active {
        color: #ffffff;
        background: linear-gradient(90deg, rgba(239, 68, 68, 0.18) 0%, rgba(168, 85, 247, 0.15) 100%);
        border: 1px solid rgba(239, 68, 68, 0.28);
        box-shadow: 0 2px 10px rgba(239, 68, 68, 0.12);
        font-weight: 600;
    }

    .sidebar-nav-item.active svg {
        color: var(--accent-red);
    }

    /* Sidebar Bottom Pro Tip / Fast & Accurate Card */
    .sidebar-tip-card {
        background: linear-gradient(135deg, rgba(26, 17, 36, 0.7) 0%, rgba(16, 21, 36, 0.8) 100%);
        border: 1px solid rgba(239, 68, 68, 0.2);
        border-radius: var(--radius-lg);
        padding: 14px;
        margin-top: auto;
    }

    .sidebar-tip-header {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 13px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .sidebar-tip-badge {
        width: 24px;
        height: 24px;
        border-radius: 6px;
        background: #ef4444;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
        flex-shrink: 0;
    }

    .sidebar-tip-badge.crown {
        background: rgba(245, 158, 11, 0.18);
        border: 1px solid rgba(245, 158, 11, 0.35);
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.2);
    }

    .sidebar-tip-desc {
        font-size: 11.5px;
        color: var(--text-secondary);
        line-height: 1.45;
    }

    /* Top User Bar (Navbar) */
    .top-user-bar {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 16px;
        padding: 6px 0 16px 0;
        margin-bottom: 0.4rem;
    }

    .top-theme-btn {
        background: transparent;
        border: none;
        color: var(--text-secondary);
        cursor: pointer;
        padding: 6px;
        display: flex;
        align-items: center;
    }

    .top-user-badge {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #f1f5f9;
        font-size: 13.5px;
        font-weight: 500;
        cursor: pointer;
    }

    .top-user-avatar {
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: #ffffff;
        font-size: 12px;
        font-weight: 700;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.35);
    }

    /* Hero Banner Container */
    .hero-banner-card {
        background: linear-gradient(135deg, rgba(14, 21, 38, 0.95) 0%, rgba(11, 16, 29, 0.98) 100%);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-xl);
        padding: 2.2rem 2.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: var(--shadow-card);
    }

    .hero-banner-card::before {
        content: "";
        position: absolute;
        top: -60px;
        right: 180px;
        width: 320px;
        height: 240px;
        background: radial-gradient(circle, rgba(239, 68, 68, 0.15) 0%, rgba(168, 85, 247, 0.08) 50%, transparent 70%);
        filter: blur(40px);
        pointer-events: none;
    }

    .hero-content-col {
        max-width: 620px;
        position: relative;
        z-index: 2;
    }

    .hero-eyebrow {
        font-size: 11px;
        font-weight: 700;
        color: #38bdf8;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .hero-title {
        font-size: 2.35rem;
        font-weight: 800;
        line-height: 1.18;
        letter-spacing: -0.025em;
        color: #ffffff;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 8px;
    }

    .hero-title-yt-icon {
        width: 36px;
        height: 25px;
        background: #ef4444;
        border-radius: 8px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 14px rgba(239, 68, 68, 0.5);
        margin-right: 4px;
    }

    .gradient-word {
        background: linear-gradient(90deg, #ec4899 0%, #f43f5e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 0.96rem;
        color: var(--text-secondary);
        line-height: 1.55;
        font-weight: 400;
        margin-bottom: 1rem;
    }

    .hero-artwork-col {
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        z-index: 2;
    }

    .hero-3d-artwork-img {
        width: 320px;
        max-width: 100%;
        height: auto;
        display: block;
        border-radius: 12px;
        filter: drop-shadow(0 14px 32px rgba(0, 0, 0, 0.65));
    }

    /* Embedded Hero URL Bar for Result Page */
    .hero-url-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 1.2rem;
    }

    .hero-url-pill {
        display: flex;
        align-items: center;
        gap: 10px;
        background: rgba(16, 23, 41, 0.95);
        border: 1px solid var(--border-subtle);
        border-radius: 9999px;
        padding: 8px 18px;
        color: var(--text-secondary);
        font-size: 13.5px;
        flex-grow: 1;
        max-width: 440px;
    }

    /* URL Input Card on Landing Page */
    .url-input-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-xl);
        padding: 1.8rem 2.2rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-card);
    }

    .url-input-label {
        font-size: 14.5px;
        font-weight: 600;
        color: #f1f5f9;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 12px;
    }

    .input-action-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
    }

    .sample-pills-row {
        display: flex;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
        font-size: 13px;
        color: var(--text-muted);
    }

    /* Custom Streamlit Input Tweaks */
    div[data-testid="stTextInput"] input {
        background-color: var(--bg-input) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: var(--radius-md) !important;
        color: #ffffff !important;
        font-size: 14px !important;
        padding: 11px 16px !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: rgba(239, 68, 68, 0.45) !important;
        box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.15) !important;
    }

    /* Primary Red Glowing Action Button */
    .btn-get-transcript {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        background: var(--gradient-button) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 11px 22px !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        box-shadow: var(--shadow-glow) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
        white-space: nowrap !important;
        height: 44px !important;
    }

    .btn-get-transcript:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 26px rgba(239, 68, 68, 0.5) !important;
    }

    /* Empty State Card */
    .empty-state-large-card {
        background: linear-gradient(180deg, rgba(14, 20, 36, 0.6) 0%, rgba(9, 13, 23, 0.8) 100%);
        border: 1px dashed rgba(255, 255, 255, 0.12);
        border-radius: var(--radius-xl);
        padding: 3.5rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
    }

    .empty-slate-icon-wrapper {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1.2rem;
    }

    .empty-clapperboard-img {
        width: 80px;
        height: auto;
        display: block;
        filter: drop-shadow(0 8px 24px rgba(168, 85, 247, 0.45));
    }

    .empty-state-heading {
        font-size: 1.45rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }

    .empty-state-desc {
        font-size: 0.95rem;
        color: var(--text-secondary);
        max-width: 540px;
        margin: 0 auto;
        line-height: 1.55;
    }

    /* How It Works Section */
    .how-it-works-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
    }

    .how-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .how-steps-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 2rem;
    }

    .how-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg);
        padding: 1.4rem;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .how-card:hover {
        transform: translateY(-2px);
        border-color: var(--border-hover);
    }

    .how-card-top {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
    }

    .how-step-icon {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .how-num-circle {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        font-weight: 700;
        color: #ffffff;
    }

    .how-card.step-1 { border-color: rgba(239, 68, 68, 0.28); }
    .how-card.step-2 { border-color: rgba(59, 130, 246, 0.28); }
    .how-card.step-3 { border-color: rgba(168, 85, 247, 0.28); }
    .how-card.step-4 { border-color: rgba(16, 185, 129, 0.28); }

    .how-card.step-1:hover { border-color: rgba(239, 68, 68, 0.55); box-shadow: 0 8px 24px rgba(239, 68, 68, 0.12); }
    .how-card.step-2:hover { border-color: rgba(59, 130, 246, 0.55); box-shadow: 0 8px 24px rgba(59, 130, 246, 0.12); }
    .how-card.step-3:hover { border-color: rgba(168, 85, 247, 0.55); box-shadow: 0 8px 24px rgba(168, 85, 247, 0.12); }
    .how-card.step-4:hover { border-color: rgba(16, 185, 129, 0.55); box-shadow: 0 8px 24px rgba(16, 185, 129, 0.12); }

    .how-card.step-1 .how-num-circle { background: #ef4444; }
    .how-card.step-2 .how-num-circle { background: #3b82f6; }
    .how-card.step-3 .how-num-circle { background: #a855f7; }
    .how-card.step-4 .how-num-circle { background: #10b981; }

    .how-card-title {
        font-size: 14.5px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 6px;
    }

    .how-card-desc {
        font-size: 12.5px;
        color: var(--text-secondary);
        line-height: 1.45;
    }

    /* Video Player Card (Result State) */
    .video-card-container {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-xl);
        padding: 1.4rem;
        box-shadow: var(--shadow-card);
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .video-card-title {
        font-size: 1.12rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.35;
        margin-bottom: 1rem;
    }

    .video-embed-box {
        border-radius: var(--radius-lg);
        overflow: hidden;
        border: 1px solid var(--border-subtle);
        position: relative;
        background: #000;
        margin-bottom: 0.8rem;
    }

    /* Transcript Panel Card (Result State) */
    .transcript-panel-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-xl);
        padding: 1.4rem;
        box-shadow: var(--shadow-card);
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    /* Transcript Tabs */
    .transcript-tabs-row {
        display: flex;
        align-items: center;
        gap: 8px;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--border-subtle);
        margin-bottom: 12px;
        overflow-x: auto;
    }

    .transcript-tab-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 7px 16px;
        border-radius: var(--radius-md);
        font-size: 13px;
        font-weight: 600;
        color: var(--text-secondary);
        background: transparent;
        border: none;
        cursor: pointer;
        transition: all 0.15s ease;
        white-space: nowrap;
    }

    .transcript-tab-btn:hover {
        color: #ffffff;
        background: rgba(255, 255, 255, 0.05);
    }

    .transcript-tab-btn.active {
        color: #ffffff;
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.35);
    }

    /* Search and Auto Scroll Bar */
    .transcript-toolbar-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 14px;
    }

    .transcript-search-box {
        flex-grow: 1;
        position: relative;
    }

    .auto-scroll-toggle {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-size: 12.5px;
        font-weight: 600;
        color: var(--text-secondary);
        background: rgba(16, 23, 41, 0.7);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-md);
        padding: 6px 12px;
        white-space: nowrap;
    }

    /* Transcript Scrollable Area */
    .transcript-scroll-area {
        height: 440px;
        overflow-y: auto;
        overflow-x: hidden;
        padding-right: 6px;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }

    .transcript-scroll-area::-webkit-scrollbar {
        width: 6px;
    }
    .transcript-scroll-area::-webkit-scrollbar-track {
        background: rgba(16, 23, 41, 0.5);
        border-radius: 6px;
    }
    .transcript-scroll-area::-webkit-scrollbar-thumb {
        background: rgba(148, 163, 184, 0.25);
        border-radius: 6px;
    }
    .transcript-scroll-area::-webkit-scrollbar-thumb:hover {
        background: rgba(148, 163, 184, 0.45);
    }

    /* Transcript Row */
    .transcript-entry-row {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        padding: 9px 12px;
        border-radius: var(--radius-md);
        background: transparent;
        border: 1px solid transparent;
        transition: all 0.15s ease;
        cursor: pointer;
    }

    .transcript-entry-row:hover {
        background: rgba(255, 255, 255, 0.03);
    }

    .transcript-entry-row.active {
        background: var(--bg-active-row);
        border-color: var(--border-active-blue);
        box-shadow: 0 2px 10px rgba(59, 130, 246, 0.12);
    }

    .transcript-time-badge {
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
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }

    .transcript-entry-row.active .transcript-time-badge {
        background: #3b82f6;
        color: #ffffff;
        border-color: #3b82f6;
    }

    .transcript-text-content {
        font-size: 13.5px;
        line-height: 1.6;
        color: #cbd5e1;
    }

    .transcript-entry-row.active .transcript-text-content {
        color: #ffffff;
        font-weight: 500;
    }

    /* Bottom Row: Transcript Actions & Stats */
    .bottom-dashboard-grid {
        display: grid;
        grid-template-columns: 2.2fr 1fr;
        gap: 16px;
        margin-top: 1.5rem;
    }

    .actions-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-xl);
        padding: 1.4rem;
        box-shadow: var(--shadow-card);
    }

    .actions-title {
        font-size: 15px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 2px;
    }

    .actions-sub {
        font-size: 12px;
        color: var(--text-secondary);
        margin-bottom: 14px;
    }

    .actions-buttons-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
    }

    /* =========================================================================
       Transcript Action Buttons (Screenshot 1 Fidelity)
       ========================================================================= */

    /* Common Download / Action Button style */
    div[data-testid="stDownloadButton"] button {
        height: 42px !important;
        min-height: 42px !important;
        border-radius: 8px !important;
        border: none !important;
        color: #ffffff !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 8px !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
        width: 100% !important;
        cursor: pointer !important;
    }

    div[data-testid="stDownloadButton"] button:hover {
        transform: translateY(-1px) !important;
    }

    div[data-testid="stDownloadButton"] button p {
        color: #ffffff !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
        white-space: nowrap !important;
    }

    /* Col 1: Copy Button iframe alignment */
    div[data-testid="column"]:nth-child(1) iframe {
        border: none !important;
        height: 44px !important;
        width: 100% !important;
        display: block !important;
    }

    div[data-testid="stCustomComponentV1"] {
        line-height: 0 !important;
    }

    /* Col 2: Download TXT (Blue) */
    div[data-testid="column"]:nth-child(2) div[data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35) !important;
    }
    div[data-testid="column"]:nth-child(2) div[data-testid="stDownloadButton"] button:hover {
        box-shadow: 0 6px 18px rgba(2, 132, 199, 0.5) !important;
    }
    div[data-testid="column"]:nth-child(2) div[data-testid="stDownloadButton"] button::before {
        content: "";
        display: inline-block;
        width: 15px;
        height: 15px;
        flex-shrink: 0;
        background-color: #ffffff;
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4'/%3E%3Cpolyline points='7 10 12 15 17 10'/%3E%3Cline x1='12' y1='15' x2='12' y2='3'/%3E%3C/svg%3E") no-repeat center / contain;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4'/%3E%3Cpolyline points='7 10 12 15 17 10'/%3E%3Cline x1='12' y1='15' x2='12' y2='3'/%3E%3C/svg%3E") no-repeat center / contain;
    }

    /* Col 3: Download SRT (Green) */
    div[data-testid="column"]:nth-child(3) div[data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        box-shadow: 0 4px 14px rgba(5, 150, 105, 0.35) !important;
    }
    div[data-testid="column"]:nth-child(3) div[data-testid="stDownloadButton"] button:hover {
        box-shadow: 0 6px 18px rgba(5, 150, 105, 0.5) !important;
    }
    div[data-testid="column"]:nth-child(3) div[data-testid="stDownloadButton"] button::before {
        content: "";
        display: inline-block;
        width: 15px;
        height: 15px;
        flex-shrink: 0;
        background-color: #ffffff;
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='3' y='4' width='18' height='16' rx='2'/%3E%3Cline x1='7' y1='10' x2='11' y2='10'/%3E%3Cline x1='9' y1='10' x2='9' y2='15'/%3E%3Cline x1='13' y1='12.5' x2='17' y2='12.5'/%3E%3C/svg%3E") no-repeat center / contain;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='3' y='4' width='18' height='16' rx='2'/%3E%3Cline x1='7' y1='10' x2='11' y2='10'/%3E%3Cline x1='9' y1='10' x2='9' y2='15'/%3E%3Cline x1='13' y1='12.5' x2='17' y2='12.5'/%3E%3C/svg%3E") no-repeat center / contain;
    }

    /* Col 4: Download VTT (Red) */
    div[data-testid="column"]:nth-child(4) div[data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #e11d48 0%, #be123c 100%) !important;
        box-shadow: 0 4px 14px rgba(225, 29, 72, 0.35) !important;
    }
    div[data-testid="column"]:nth-child(4) div[data-testid="stDownloadButton"] button:hover {
        box-shadow: 0 6px 18px rgba(225, 29, 72, 0.5) !important;
    }
    div[data-testid="column"]:nth-child(4) div[data-testid="stDownloadButton"] button::before {
        content: "";
        display: inline-block;
        width: 15px;
        height: 15px;
        flex-shrink: 0;
        background-color: #ffffff;
        -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'/%3E%3Cpolyline points='14 2 14 8 20 8'/%3E%3Cline x1='10' y1='12' x2='14' y2='16'/%3E%3Cline x1='14' y1='12' x2='10' y2='16'/%3E%3C/svg%3E") no-repeat center / contain;
        mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'/%3E%3Cpolyline points='14 2 14 8 20 8'/%3E%3Cline x1='10' y1='12' x2='14' y2='16'/%3E%3Cline x1='14' y1='12' x2='10' y2='16'/%3E%3C/svg%3E") no-repeat center / contain;
    }

    /* Stat Cards */
    .stats-cards-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 14px;
    }

    .stat-metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-xl);
        padding: 1.4rem 1.2rem;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: var(--shadow-card);
    }

    .stat-metric-icon {
        width: 48px;
        height: 48px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }

    .stat-metric-icon.words-icon {
        background: rgba(168, 85, 247, 0.14);
        border: 1px solid rgba(168, 85, 247, 0.28);
        box-shadow: 0 4px 14px rgba(168, 85, 247, 0.16);
    }

    .stat-metric-icon.time-icon {
        background: rgba(59, 130, 246, 0.14);
        border: 1px solid rgba(59, 130, 246, 0.28);
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.16);
    }

    .stat-metric-val {
        font-size: 1.55rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }

    .stat-metric-label {
        font-size: 12px;
        color: var(--text-muted);
        font-weight: 500;
        text-transform: capitalize;
    }

    /* Responsive Breakdown */
    @media (max-width: 1024px) {
        .how-steps-grid {
            grid-template-columns: 1fr 1fr;
        }
        .bottom-dashboard-grid {
            grid-template-columns: 1fr;
        }
        .actions-buttons-grid {
            grid-template-columns: 1fr 1fr;
        }
    }

    @media (max-width: 768px) {
        .how-steps-grid {
            grid-template-columns: 1fr;
        }
        .hero-banner-card {
            flex-direction: column;
            padding: 1.8rem;
        }
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
    }
    </style>
    """
