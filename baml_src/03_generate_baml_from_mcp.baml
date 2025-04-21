class ParamsCalculateAction {
  expression string @alias("Expression")
}

class CalculateAction {
  mcp_tool_id "calculate" @alias("name")
  params ParamsCalculateAction
}

function GetCalculateAction(goal: string) -> CalculateAction {
    client Default
    prompt #"
        Goal: {{ goal }}

        {{ ctx.output_format }}
    "#
}

test example {
    functions [GetCalculateAction]
    args {
        goal "Multiply all numbers between 10 and 15"
    }
}

class SearchPapersArguments {
  query string
  categories string?
  date_from string?
  date_to string?
  max_results int?
}

class SearchPapersTool {
  name "search_papers" @description(#"Search for papers on arXiv with advanced filtering"#)
  arguments SearchPapersArguments
}

function GetSearchStoriesTool(goal: string) -> SearchStoriesTool {
    client Default
    prompt #"
        Goal: {{ goal }}

        {{ ctx.output_format }}
    "#
}