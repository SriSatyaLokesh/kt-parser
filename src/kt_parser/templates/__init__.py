# templates/__init__.py
"""
Template registry for KT-parser.
"""
from .context_hub import SECTIONS, SYSTEM_PROMPTS, OUTPUT_FILES, build

TEMPLATES = {
    "context_hub": {
        "SECTIONS": SECTIONS,
        "SYSTEM_PROMPTS": SYSTEM_PROMPTS,
        "OUTPUT_FILES": OUTPUT_FILES,
        "build": build,
    }
}

