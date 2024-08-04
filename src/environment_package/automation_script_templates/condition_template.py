def condition_evaluation(input_vals) -> dict:
    condition = input_vals[1]
    if condition != [] and None in condition:
        return print(json.dumps({"ValueError": "Condition values cannot be None"}))

    condition_passed = False

    if (
