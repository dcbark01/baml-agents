#!/usr/bin/env python3

import re
from pathlib import Path

import jinja2


def get_root_path() -> Path:
    """
    Returns the absolute Path to the project root (where pyproject.toml is found).
    Raises FileNotFoundError if not found.
    """
    for p in [Path.cwd().resolve(), *Path.cwd().resolve().parents]:
        if (p / "pyproject.toml").is_file():
            return p
    raise FileNotFoundError(
        "Could not find pyproject.toml in current or parent directories"
    )


def extract_version(pyproject_path: Path) -> str:
    content = pyproject_path.read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    if not match:
        raise RuntimeError("Version not found in pyproject.toml")
    return match.group(1)


def render_readme(template_path: Path, output_path: Path, version: str) -> None:
    template_text = template_path.read_text(encoding="utf-8")
    template = jinja2.Template(template_text)
    major, minor, *_ = version.split(".")
    next_minor_version = f"{major}.{int(minor) + 1}.0"
    rendered = template.render(version=version, next_minor_version=next_minor_version)
    output_path.write_text(rendered, encoding="utf-8")


def main():
    root_path = get_root_path()
    pyproject_path = root_path / "pyproject.toml"
    template_path = root_path / "README.md.template.md"
    output_path = root_path / "README.md"
    version = extract_version(pyproject_path)
    render_readme(template_path, output_path, version)


if __name__ == "__main__":
    main()
