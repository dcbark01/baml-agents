from dataclasses import dataclass, field


@dataclass(frozen=True)
class BamlToolPromptConfig:
    id_field: str = field(
        default="intent", metadata={"description": "Field name for tool ID"},
    )
    tools_field: str = field(
        default="intents", metadata={"description": "Field name for tools collection"},
    )
    can_select_many: bool = field(
        default=True, metadata={"description": "Allow selecting multiple tools"},
    )

    def output_format_prefix(self) -> str:
        id_field = self.id_field
        return (
            f"What are the next steps?\n\n"
            f"Answer in JSON format with {'one or multiple' if self.can_select_many else 'one'} of the following {id_field}s\n\n"
        )
