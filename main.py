"""Main runner for YouTube Transcript Extractor.

Run the Streamlit application via:
    python main.py
    python main.py --server.port 8502
or
    streamlit run app.py
"""

import sys
import subprocess
from pathlib import Path


def run_app():
    """Launch the Streamlit app with optional CLI argument pass-through."""
    app_path = Path(__file__).parent / "app.py"

    # Forward any CLI flags passed to main.py directly to streamlit run
    passthrough_args = sys.argv[1:]
    cmd = [sys.executable, "-m", "streamlit", "run", str(app_path)] + passthrough_args

    print("🚀 Starting YouTube Transcript Extractor...")
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped.")
    except subprocess.CalledProcessError as err:
        print(f"\n❌ Streamlit exited with return code {err.returncode}.")
        sys.exit(err.returncode)


if __name__ == "__main__":
    run_app()