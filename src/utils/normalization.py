def min_max_normalize(values):

    min_val = min(values)
    max_val = max(values)

    if max_val == min_val:
        return [0.5 for _ in values]

    return [
        (v - min_val) / (max_val - min_val)
        for v in values
    ]