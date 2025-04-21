class ToolCall {
    @@dynamic
}

function UseTool(goal: string, output_format_prefix: string) -> ToolCall {
    client Default
    prompt #"
        Solve: {{ goal }}

        {{ ctx.output_format(prefix=output_format_prefix, or_splitter=" OR ")}}
    "#
}
