class TestBamlHooks_Person {
    type "person"
    name string
}

class TestBamlHooks_City {
    type "city"
    name string @description(#"Unabbreviated city name without the state"#)
}

function TestBamlHooks_ExtractCity(text: string) -> TestBamlHooks_City {
  client "openai/gpt-4.1-nano"
  prompt #"
    Extract: 
    "{{ text }}". 
    {{ ctx.output_format }}
  "#
}

function TestBamlHooks_Echo(text: string) -> string {
  client "openai/gpt-4.1-nano"
  prompt #"
    Just repeat the text:
    "{{ text }}". 
    {{ ctx.output_format }}
  "#
}

function TestBamlHooks_ExtractEntities(text: string) -> (TestBamlHooks_City | TestBamlHooks_Person)[] {
  client "openai/gpt-4.1-nano"
  prompt #"
    Extract: 
    "{{ text }}". 
    {{ ctx.output_format }}
  "#
}

test t {
    functions [TestBamlHooks_ExtractCity, TestBamlHooks_Echo, TestBamlHooks_ExtractEntities]
    args {text "Hi, I'm John from LA"}
}

