class CalculatorToolArguments {
    expression string
}

class CalculatorToolCall {
    tool_name "calculate"
    arguments CalculatorToolArguments
}

function UseCalculatorTool(goal: string) -> CalculatorToolCall {
    client Default
    prompt #"
        Use the calculator to solve: {{ goal }}

        {{ ctx.output_format }}
    "#
}

test usage_example {
    functions [UseCalculatorTool]
    args {
        goal "Multiply all numbers between 10 and 15"
    }
}
