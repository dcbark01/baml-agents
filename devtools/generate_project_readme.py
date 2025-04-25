#!/usr/bin/env python3

import argparse
from pathlib import Path

import jinja2


def get_root_path() -> Path:
    """
    Returns the absolute Path to the project root (where README.md.template.md is found).
    Raises FileNotFoundError if not found.
    """
    for p in [Path.cwd().resolve(), *Path.cwd().resolve().parents]:
        if (p / "README.md.template.md").is_file():
            return p
    raise FileNotFoundError(
        "Could not find README.md.template.md in current or parent directories"
    )


def render_readme(template_path: Path, output_path: Path, version: str) -> None:
    template_text = template_path.read_text(encoding="utf-8")
    template = jinja2.Template(template_text)
    major, minor, *_ = version.split(".")
    next_minor_version = f"{major}.{int(minor) + 1}.0"
    rendered = template.render(version=version, next_minor_version=next_minor_version)
    output_path.write_text(rendered, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Generate README.md from README.md.template.md and a version string."
    )
    parser.add_argument(
        "version",
        type=str,
        help="The version string to use (e.g., 0.16.0)",
    )
    args = parser.parse_args()

    root_path = get_root_path()
    template_path = root_path / "README.md.template.md"
    output_path = root_path / "README.md"
    render_readme(template_path, output_path, args.version)


if __name__ == "__main__":
    main()
