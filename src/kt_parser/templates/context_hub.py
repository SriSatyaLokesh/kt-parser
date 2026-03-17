# context_hub.py
"""
Example template for context hub style documentation.
"""
SECTIONS = ["Introduction", "Details", "Summary"]
SYSTEM_PROMPTS = {"Introduction": "Summarize the session.", "Details": "Provide technical details.", "Summary": "Conclude the documentation."}
OUTPUT_FILES = {"Introduction": "introduction.md", "Details": "details.md", "Summary": "summary.md"}

def build(chunk_outputs, docs_dir):
    # Example: merge and write outputs
    for section, outputs in chunk_outputs.items():
        out_path = docs_dir / OUTPUT_FILES[section]
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(outputs))
