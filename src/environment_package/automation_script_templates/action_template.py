def action_execution(input_vals) -> dict:
    action_inputs = input_vals[0]
    action_results = []
        
    if action_inputs != [] and None in action_inputs:
        return {"ValueError": "Action values cannot be None"}

