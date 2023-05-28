def clamp(value, lower, upper):
    if value < lower:
        value = lower
    if value > upper:
        value = upper

    return value