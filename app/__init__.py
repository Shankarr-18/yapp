"""yapp - Personal Finance Toolkit."""

import os

# Must be set before gradio is imported anywhere; stops telemetry calls to huggingface.co.
os.environ.setdefault("GRADIO_ANALYTICS_ENABLED", "False")

__version__ = "0.1.0"
