import json
import shlex
import subprocess
from collections.abc import Sequence
from typing import Any


def run_cli_command(command: str | Sequence[str]) -> str:
    if isinstance(command, str):
        command = shlex.split(command)
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.stderr:
        # print(f"Command wrote to stderr:\n{result.stderr.strip()}")
        pass
    if result.returncode != 0:
        print(f"stderr:\n{result.stderr.strip()}")
        raise RuntimeError(f"Command failed with exit code {result.returncode}")
    return result.stdout.strip()


def filter_tools_by_name(schema_json: str, tool_name: str) -> dict[str, Any]:
    """Parse the given JSON schema string, filter the 'tools' list by tool_name,
    and return a dict with 'tools' containing only the matching tool.
    """
    schema_data = json.loads(schema_json)
    tools = schema_data.get("tools", [])
    filtered_tools = [tool for tool in tools if tool.get("name") == tool_name]
    return {"tools": filtered_tools}
