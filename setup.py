from setuptools import setup, find_packages

setup(
    name="kt-parser",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "typer",
        "rich",
        # Add other dependencies as needed
    ],
    entry_points={
        "console_scripts": [
            "kt-parser=kt_parser.cli:main",
        ],
    },
)