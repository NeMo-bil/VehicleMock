


def calculate_new_position(current: float, target: float) -> float:
    difference = target - current
    step = difference * 0.1
    if abs(step) < 0.01:
        step = min(0.01, difference) if difference > 0 else max(-0.01, difference)
    return current + step

