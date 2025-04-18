class CalculatorArguments {
    expression string
}

class CalculatorUsage {
    tool_name "calculate"
    arguments CalculatorArguments
}

function UseCalculator(goal: string) -> CalculatorUsage {
    client Default
    prompt #"
        Use the calculator to solve: {{ goal }}

        {{ ctx.output_format }}
    "#
}

test usage_example {
    functions [UseCalculator]
    args {
        goal "Multiply all numbers between 10 and 15"
    }
}