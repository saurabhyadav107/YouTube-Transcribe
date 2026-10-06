"""Main runner for YouTube Transcript Extractor.

Run the Streamlit application via:
    python main.py
or
    streamlit run app.py
"""

import sys
import subprocess
from pathlib import Path


def run_app():
    """Launch the Streamlit app using subprocess."""
    app_path = Path(__file__).parent / "app.py"
    cmd = [sys.executable, "-m", "streamlit", "run", str(app_path)]
    print(f"Launching YouTube Transcript Extractor: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\nApplication stopped.")


if __name__ == "__main__":
    run_app()