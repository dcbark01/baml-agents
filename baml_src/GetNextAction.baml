function GetNextAction(goal: string, past_actions: PastAction[]) -> NextAction {
    client Default
    prompt #"
        Please select the next best action to achieve the goal.
        
        <goal>
        {{ goal }}
        </goal>
        
        {{ ctx.output_format(or_splitter=" OR ", prefix="Answer in JSON format with exactly one next best action:\n") }}

        {% for k in past_actions %}
        {{ _.role("assistant") }}
        {{ k.chosen_action }}
        {{ _.role("user") }}
        {% if k.result.error %}
        Your chosen action did not succeed. Details:
        {% endif %}
        {{ k.result.content }}
        {% endfor %}
    "#
}
class NextAction {
    @@dynamic
}
class PastAction {
    chosen_action string
    result PastActionResult
}
class PastActionResult {
    content string
    error bool
}
