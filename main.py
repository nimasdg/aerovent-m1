import os
import sys

os.execvp(
    sys.executable,
    [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "app.py",
        "--server.port=80",
        "--server.address=0.0.0.0",
        "--server.headless=true",
    ],
)
