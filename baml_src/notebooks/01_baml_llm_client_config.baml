
function LLMClientConfig_ExtractCity(text: string) -> LLMClientConfig_Completion {
  client "openai/gpt-4.1-nano"
  prompt #"{{ text }}. {{ ctx.output_format }}"#
}
class LLMClientConfig_Completion {
    full_city_name string
}
test t {
    functions [LLMClientConfig_ExtractCity]
    args {text "Hi, I'm John from LA"}
}
