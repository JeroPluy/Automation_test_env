def action_execution(input_vals) -> None:
    action_inputs = input_vals[2]
    action_results = []
        
    if action_inputs != [] and None in action_inputs:
        return print(json.dumps({"ValueError": "Action input values cannot be None"}))

