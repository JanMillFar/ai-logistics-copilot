def calculate_health_score(
    healthy,
    warning,
    critical
):
    total = (
        healthy
        + warning
        + critical
    )

    if total == 0:
        return 0

    score = (
        (healthy * 100)
        + (warning * 50)
        + (critical * 0)
    ) / total

    return round(score, 1)


def health_status(score):

    if score >= 80:
        return "🟢 Excellent"

    elif score >= 60:
        return "🟡 Attention Required"

    return "🔴 Critical"