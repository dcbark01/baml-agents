from pydantic import BaseModel


class UsedTool(BaseModel):
    tool_input: str
    tool_output: str
