
function LLMClients_ExtractCity(text: string) -> LLMClients_Completion {
  client "openai/gpt-4.1-nano"
  prompt #"{{ text }}. {{ ctx.output_format }}"#
}
class LLMClients_Completion {
    full_city_name string
}
test t {
    functions [LLMClients_ExtractCity]
    args {text "Hi, I'm John from LA"}
}
