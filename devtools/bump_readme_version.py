#!/usr/bin/env python3

import argparse
import re
from pathlib import Path


def replace_install_line(readme_path: Path, version: str) -> None:
    content = readme_path.read_text(encoding="utf-8")
    major, minor, *_ = version.split(".")
    next_minor = f"{major}.{int(minor)+1}.0"
    new_line = f'pip install "baml-agents>={version},<{next_minor}"'
    # Replace the line exactly matching the old pattern
    new_content, n = re.subn(
        r'pip install "baml-agents>=\d+\.\d+\.\d+,<\d+\.\d+\.\d+"',
        new_line,
        content,
    )
    if n == 0:
        raise RuntimeError("No matching pip install line found in README.md")
    readme_path.write_text(new_content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Update pip install line in README.md")
    parser.add_argument(
        "version", type=str, help="The version string to use (e.g., 0.16.0)"
    )
    args = parser.parse_args()
    readme_path = Path("README.md")
    replace_install_line(readme_path, args.version)


if __name__ == "__main__":
    main()
