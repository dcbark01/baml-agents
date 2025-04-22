function Four_WriteShortStory() -> Four_ShortStory {
  client "openai/gpt-4.1-nano"
  prompt #"Write a short story about anything  {{ ctx.output_format }}"#
}
class Four_ShortStory {
    genre string
    characters Four_Character[] @description(#"at least three characters"#)
    story_summary string @description(#"Short story excerpt about anything, 30 words"#)
}
class Four_Character {
    name string
    age int
    occupation string
}
test t {
    functions [Four_WriteShortStory]
    args {}
}
