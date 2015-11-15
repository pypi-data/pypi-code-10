round_number = lambda x: int(round(abs(x)))


def get_percent_change(new_value, old_value):
    if not old_value and not new_value:
        return 0
    if not old_value:
        sign = 1 if new_value > 0 else -1
        return sign * float('inf')
    change_difference = new_value - old_value
    change_ratio = change_difference / float(old_value)
    return 100 * change_ratio
