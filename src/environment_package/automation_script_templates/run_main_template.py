if __name__ == "__main__":
    trigger_result = trigger(input_vals)
    if trigger_result['triggered'] is True:
        condition_result = condition(input_vals, trigger_result['trigger_id'])