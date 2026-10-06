"""Custom CSS and styling definitions for modern SaaS interface."""

def get_custom_css() -> str:
    """Return polished custom CSS styling for the Streamlit app."""
    return """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Container padding and maximum width */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1000px !important;
    }

    /* Hero Header */
    .hero-container {
        text-align: center;
        padding: 2.2rem 1.5rem 1.8rem 1.5rem;
        background: radial-gradient(100% 100% at 50% 0%, rgba(255, 0, 0, 0.12) 0%, rgba(255, 255, 255, 0) 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 59, 48, 0.12);
        color: #ff4d4d;
        border: 1px solid rgba(255, 77, 77, 0.25);
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.15;
        margin-bottom: 0.6rem;
        background: linear-gradient(135deg, #ffffff 40%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #94a3b8;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.5;
        font-weight: 400;
    }

    /* Modern Card Container */
    .custom-card {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.4rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .custom-card:hover {
        border-color: rgba(255, 255, 255, 0.15);
    }

    /* Video Metadata Card */
    .video-card {
        display: flex;
        flex-direction: row;
        gap: 1.5rem;
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.55) 0%, rgba(15, 23, 42, 0.65) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.4rem;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.25);
    }

    .video-thumbnail {
        width: 170px;
        height: 100px;
        object-fit: cover;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        flex-shrink: 0;
    }

    .video-info {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .video-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #f8fafc;
        line-height: 1.3;
        margin-bottom: 0.4rem;
        word-break: break-word;
    }

    .video-channel {
        font-size: 0.92rem;
        color: #94a3b8;
        margin-bottom: 0.7rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .meta-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }

    .meta-pill {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: rgba(148, 163, 184, 0.12);
        color: #e2e8f0;
        border: 1px solid rgba(148, 163, 184, 0.2);
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 500;
    }

    .meta-pill.pill-manual {
        background: rgba(34, 197, 94, 0.12);
        color: #4ade80;
        border-color: rgba(34, 197, 94, 0.3);
    }

    .meta-pill.pill-auto {
        background: rgba(56, 189, 248, 0.12);
        color: #38bdf8;
        border-color: rgba(56, 189, 248, 0.3);
    }

    /* Metric Stat Box */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .stat-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        text-align: center;
        transition: transform 0.15s ease;
    }

    .stat-card:hover {
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.15);
    }

    .stat-label {
        font-size: 0.82rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
    }

    .stat-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #f8fafc;
        letter-spacing: -0.02em;
    }

    /* Empty State */
    .empty-state-box {
        text-align: center;
        padding: 3.5rem 1.5rem;
        background: rgba(30, 41, 59, 0.25);
        border: 2px dashed rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        margin-top: 1.5rem;
        margin-bottom: 2rem;
    }

    .empty-icon {
        font-size: 3.2rem;
        margin-bottom: 1rem;
        display: inline-block;
        filter: drop-shadow(0 4px 10px rgba(255, 0, 0, 0.2));
    }

    .empty-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 0.5rem;
    }

    .empty-desc {
        color: #94a3b8;
        font-size: 0.95rem;
        max-width: 480px;
        margin: 0 auto 1.8rem auto;
        line-height: 1.5;
    }

    .features-row {
        display: flex;
        justify-content: center;
        gap: 1.8rem;
        flex-wrap: wrap;
    }

    .feature-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        color: #cbd5e1;
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* Scrollable Transcript Box */
    .transcript-box {
        background: #0d1117;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        padding: 1.5rem;
        max-height: 480px;
        overflow-y: auto;
        overflow-x: hidden;
        color: #e6edf3;
        font-size: 0.96rem;
        line-height: 1.7;
        white-space: pre-wrap;
        word-wrap: break-word;
        box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.35);
    }

    .transcript-box.timestamp-view {
        font-family: 'JetBrains Mono', Consolas, Monaco, monospace;
        font-size: 0.88rem;
        line-height: 1.8;
    }

    /* Scrollbar styling */
    .transcript-box::-webkit-scrollbar {
        width: 8px;
    }
    .transcript-box::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 8px;
    }
    .transcript-box::-webkit-scrollbar-thumb {
        background: rgba(148, 163, 184, 0.3);
        border-radius: 8px;
    }
    .transcript-box::-webkit-scrollbar-thumb:hover {
        background: rgba(148, 163, 184, 0.5);
    }

    /* Copy Button Tooltip & Flash */
    .copy-success-badge {
        color: #4ade80;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.9rem;
    }

    /* Custom Streamlit Button Tweaks */
    button[kind="primary"] {
        background: linear-gradient(135deg, #ff2a2a 0%, #d90429 100%) !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(230, 10, 10, 0.35) !important;
        font-weight: 600 !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }

    button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 18px rgba(230, 10, 10, 0.45) !important;
    }

    /* Responsive adjustments */
    @media (max-width: 640px) {
        .video-card {
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        .video-thumbnail {
            width: 100%;
            height: 160px;
        }
        .meta-pills {
            justify-content: center;
        }
        .stats-grid {
            grid-template-columns: 1fr;
        }
        .hero-title {
            font-size: 1.85rem;
        }
    }
    </style>
    """
