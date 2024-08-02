def condition(input_vals, trigger_id = None) -> dict:
    condition = input_vals[1]
    if None in condition:
        return {'ValueError': "Condition values cannot be None"}
    
    condition_passed = False

