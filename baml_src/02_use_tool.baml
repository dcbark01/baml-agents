class ToolCall {
    @@dynamic
}

function UseTool(goal: string) -> ToolCall {
    client Default
    prompt #"
        Solve: {{ goal }}

        {{ ctx.output_format(prefix="What are the next steps?\n\nAnswer in JSON format with one or multiple of the following intents:\n\n", or_splitter=" OR ")}}
    "#
}
