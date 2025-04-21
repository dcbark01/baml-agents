generator target {
    output_type "python/pydantic"
    output_dir ".."
    version "0.84.4"
    default_client_mode sync
}

client<llm> Default {
  provider openai
  options {
    model gpt-4.1
  }
}
class ParamsForCalculate {
  expression string
}

class Calculate {
  tool_id "calculate_tool"
  params ParamsForCalculate  // Calculates/evaluates the given expression.
}