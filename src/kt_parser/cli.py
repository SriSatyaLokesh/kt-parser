# cli.py
"""
Typer CLI entry point for KT-parser.
"""
import typer

import typer
from .pipeline import run_pipeline

app = typer.Typer()

@app.callback()
def main():
    """KT-parser CLI"""
    pass

@app.command()
def process(
    template: str = typer.Option("context_hub", help="Template to use for output")
):
    """Process a video or folder and generate Markdown docs."""
    run_pipeline(template=template)

if __name__ == "__main__":
    app()
