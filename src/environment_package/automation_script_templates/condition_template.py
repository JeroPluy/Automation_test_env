def condition(input_vals) -> dict:
    condition = input_vals[1]
    if condition != [] and None in condition:
        return {"ValueError": "Condition values cannot be None"}

    condition_passed = False

    if (
