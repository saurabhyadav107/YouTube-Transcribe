# 🎬 YouTube Transcript Extractor

A modern, fast, and SaaS-grade web application built with **Streamlit** and **Python** to extract, view, copy, and download subtitle tracks from any YouTube video or Short.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.35%2B-red)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

- 🔗 **Universal YouTube URL Support**: Works with standard watch links (`youtube.com/watch?v=...`), short links (`youtu.be/...`), Shorts (`youtube.com/shorts/...`), embed links, and direct video IDs.
- 🌐 **Multi-Language Detection**: Automatically lists all available subtitle languages (with country flags) and enables switching between them.
- 🎯 **Manual vs. Auto-Generated Detection**: Identifies whether subtitles are creator-uploaded or auto-generated, prioritizing manual transcripts by default.
- 📖 **Reading Mode**: Formats spoken text into clean, readable paragraphs without timestamps for uninterrupted reading or summarization.
- ⏱️ **Timestamp Mode**: Preserves synchronized `[MM:SS]` or `[HH:MM:SS]` timestamps for every segment.
- 📋 **One-Click Clipboard Copy**: Reliable browser clipboard integration with instant feedback.
- ⬇️ **Multiple Export Formats**:
  - **TXT**: Plain text export formatted for current view mode (Reading or Timestamps).
  - **SRT**: Standard SubRip subtitle file for video editing and players.
  - **VTT**: WebVTT subtitle format for web players.
- 📊 **Accurate Transcript Statistics**: Real-time word count, segment count, and exact duration computed from actual subtitle data.
- 🎨 **Modern SaaS Interface**: Dark aesthetic with cards, responsive layout, status indicators, and empty states.
- 🛡️ **Defensive Error Handling**: Clear user messages for disabled transcripts, missing subtitles, age/region restrictions, or connectivity issues.

---

## 🏗️ Architecture

```text
SpeechToText1/
├── app.py                      # Main Streamlit web application
├── main.py                     # CLI launcher & runner
├── requirements.txt            # Project dependencies
├── README.md                   # Documentation
├── .gitignore                  # Git ignore rules
│
├── models/                     # Strongly typed data structures
│   ├── __init__.py
│   └── transcript_models.py    # TranscriptSegment, TranscriptResult, VideoMetadata
│
├── services/                   # Business and external integration logic
│   ├── __init__.py
│   ├── youtube_service.py      # oEmbed video metadata retrieval
│   └── transcript_service.py   # Subtitle extraction & domain error mapping
│
├── utils/                      # Modular helper functions
│   ├── __init__.py
│   ├── url_utils.py            # Strict URL validation & video ID parsing
│   ├── transcript_utils.py     # Reading, timestamp, SRT, VTT & metrics formatting
│   └── file_utils.py           # Cross-platform filename sanitization
│
├── ui/                         # Streamlit UI presentation layer
│   ├── __init__.py
│   ├── styles.py               # Modern SaaS CSS styling
│   └── components.py           # Cards, headers, transcript viewer & buttons
│
└── tests/                      # Automated test suite (59 unit tests)
    ├── __init__.py
    ├── test_url_utils.py
    ├── test_transcript_utils.py
    ├── test_file_utils.py
    └── test_services.py
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10, 3.11, 3.12, or 3.13
- Internet connection (to query YouTube subtitle tracks)

### 2. Installation

Clone this repository and navigate to the project directory:

```bash
git clone <repository-url>
cd SpeechToText1
```

Create and activate a virtual environment:

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 💻 Running the Application

Launch the Streamlit web application:

```bash
streamlit run app.py
```

Alternatively, you can run the launcher script:

```bash
python main.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 📖 How to Use

1. **Enter URL**: Paste any YouTube video link, Short, or video ID into the input field.
2. **Fetch Transcript**: Click **🚀 Get Transcript**.
3. **Switch Language** *(optional)*: If the video has multiple language tracks, choose your preferred language from the dropdown.
4. **Choose View**: Toggle between **Reading** (clean paragraphs) and **With Timestamps** (`[MM:SS]`).
5. **Export & Share**:
   - Click **📋 Copy Transcript** to copy to your clipboard.
   - Click **⬇️ Download TXT**, **⬇️ Download SRT**, or **⬇️ Download VTT** to save files with automatically sanitized filenames.

---

## 🧪 Running Tests

The project includes unit tests with mocks for external network calls:

```bash
pytest -v
```

All 59 unit tests verify:
- URL parsing across all YouTube link formats
- Reading mode, timestamp mode, SRT, and VTT formatting
- Duration, segment, and word count calculation
- Windows/Linux filename sanitization against invalid characters
- Service error handling and exception mappings

---

## 🔒 Security & Performance

- **No Shell Execution**: All URLs are validated with strict regex patterns; no subprocess or external CLI tools are invoked for downloads.
- **No Scraping Hacks**: Subtitles are fetched using the official and maintained `youtube-transcript-api` library.
- **Deterministic Caching**: Streamlit caching (`@st.cache_data`) minimizes duplicate network requests while capping memory usage.
- **Scrollable Rendering**: Long transcripts are rendered in CSS-bounded scrollable containers to ensure the UI remains smooth and responsive.
