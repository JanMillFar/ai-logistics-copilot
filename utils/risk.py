def classify_risk(score):

    if score > 50:
        return "🔴 Critical"

    elif score > 20:
        return "🟡 Warning"

    return "🟢 Healthy"


def forecast_status(days):

    if days < 7:
        return "🔴 Critical"

    elif days < 21:
        return "🟡 Warning"

    return "🟢 Healthy"