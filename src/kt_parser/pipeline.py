# pipeline.py
"""
Pipeline orchestration for KT-parser.
"""

from .templates import TEMPLATES

def run_pipeline(template: str = "context_hub"):
    # Example: select template and print sections
    tpl = TEMPLATES.get(template)
    if not tpl:
        print(f"Unknown template: {template}")
        return
    print(f"Using template: {template}")
    print("Sections:", tpl["SECTIONS"])
