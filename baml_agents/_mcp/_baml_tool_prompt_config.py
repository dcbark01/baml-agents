from pydantic import BaseModel, ConfigDict, Field


class BamlToolPromptConfig(BaseModel):
    id_field: str = Field(default="intent", description="Field name for tool ID")
    tools_field: str = Field(
        default="intents", description="Field name for tools collection"
    )
    can_select_many: bool = Field(
        default=True, description="Allow selecting multiple tools"
    )

    model_config = ConfigDict(frozen=True)
