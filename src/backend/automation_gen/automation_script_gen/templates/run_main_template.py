if __name__ == "__main__":
    if trigger_check(input_vals):
        if condition_evaluation(input_vals):
            action_execution(input_vals)
        else:
            print(json.dumps({"AutomationResult":"Condition not met"}))
    else:
        print(json.dumps({"AutomationResult":"No trigger detected"}))
