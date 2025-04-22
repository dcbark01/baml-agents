
function IntroToTools_GetWeatherInfo(text: string) -> IntroToTools_GetWeatherInfo_Parameters {
  client Default
  prompt #"
    {{ text }}
    {{ ctx.output_format }}
  "#
}
class IntroToTools_GetWeatherInfo_Parameters {
    city string
    measurement "celsius" | "fahrenheit" @description(#"default: celsius"#)
}
test t {
    functions [IntroToTools_GetWeatherInfo]
    args {city "Hi, I'm John from LA"}
}

class NextAction {
    @@dynamic
}
function GetNextAction(goal: string) -> NextAction {
    client Default
    prompt #"
        Please select the next best action to achieve the goal.
        
        <goal>
        {{ goal }}
        </goal>
        
        {{ ctx.output_format(prefix="Answer in JSON format with exactly one next best action:\n") }}
    "#
}
