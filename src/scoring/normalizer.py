def normalize_scores(scores):
    min_s = min(scores)
    max_s = max(scores)

    if max_s == min_s:
        return [50 for _ in scores]

    return [(s - min_s) / (max_s - min_s) * 100 for s in scores]