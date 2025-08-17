import os
import shutil
import subprocess
from pathlib import Path


class McpToolsNotFoundError(Exception):
    """Raised when mcptools binary cannot be found on the system."""



def find_mcptools_binary() -> str:
    """
    Detect and return the path to the mcptools binary.

    This function checks multiple common locations and methods to find mcptools:
    1. Uses shutil.which() to check if 'mcptools' or 'mcpt' is in PATH
    2. Checks common installation paths for Homebrew on macOS
    3. Checks common Go binary locations
    4. Verifies the binary is executable and working

    Returns:
        str: Full path to the mcptools binary

    Raises:
        McpToolsNotFoundError: If mcptools cannot be found or is not working

    """
    # List of possible binary names
    binary_names = ["mcptools", "mcpt"]

    # First, try to find it in PATH
    for binary_name in binary_names:
        binary_path = shutil.which(binary_name)
        if binary_path and _verify_mcptools_binary(binary_path):
            return binary_path

    # Common installation paths to check
    common_paths = [
        # Homebrew paths (Intel and Apple Silicon Mac)
        "/usr/local/bin/mcptools",
        "/usr/local/bin/mcpt",
        "/opt/homebrew/bin/mcptools",
        "/opt/homebrew/bin/mcpt",
        # Go binary paths
        Path.home() / "go" / "bin" / "mcptools",
        Path.home() / "go" / "bin" / "mcpt",
        # User local bin
        Path.home() / ".local" / "bin" / "mcptools",
        Path.home() / ".local" / "bin" / "mcpt",
        # System paths
        "/usr/bin/mcptools",
        "/usr/bin/mcpt",
    ]

    # Check each common path
    for path in common_paths:
        path_str = str(path)
        if os.path.isfile(path_str) and os.access(path_str, os.X_OK):
            if _verify_mcptools_binary(path_str):
                return path_str

    # If we get here, mcptools was not found
    raise McpToolsNotFoundError(
        "mcptools binary not found. Please install mcptools using:\n"
        "  • Homebrew: brew install mcptools\n"
        "  • Go: go install github.com/f/mcptools/cmd/mcptools@latest\n"
        "  • Or download from: https://github.com/f/mcptools/releases"
    )


def _verify_mcptools_binary(binary_path: str) -> bool:
    """
    Verify that the binary at the given path is actually mcptools and is working.

    Args:
        binary_path: Path to the binary to verify

    Returns:
        bool: True if the binary is working mcptools, False otherwise

    """
    try:
        # Run mcptools with --version or --help to verify it's working
        result = subprocess.run(
            [binary_path, "--version"], capture_output=True, text=True, timeout=10, check=False
        )

        # If --version fails, try --help as some versions might not have --version
        if result.returncode != 0:
            result = subprocess.run(
                [binary_path, "--help"], capture_output=True, text=True, timeout=10, check=False
            )

        # Check if the command succeeded and output looks like mcptools
        if result.returncode == 0:
            output = (result.stdout + result.stderr).lower()
            return "mcptools" in output or "mcp" in output

    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
        pass

    return False
