"""Entrypoint shim for running the Streamlit app.

Supports both `python main.py` (spawns Streamlit) and `streamlit run main.py`
without double-starting the runtime (which raises "Runtime instance already exists!").
"""

import sys
from streamlit.web import cli as stcli
from streamlit.runtime.runtime import Runtime

if __name__ == "__main__":
    if Runtime.exists():
        # Already inside Streamlit runtime: just load the UI module.
        import app.main as _  # noqa: F401
    else:
        # Normal CLI execution: start Streamlit pointed at the UI file.
        sys.argv = ["streamlit", "run", "app/main.py"]
        sys.exit(stcli.main())
