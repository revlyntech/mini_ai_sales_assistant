import re


def extract_numbers(text):
    return [int(x) for x in re.findall(r"\d+", str(text))]


def check_icp(data, summary_data, custom_icp=None):
    score = 0
    reasons = []

    if not custom_icp:
        custom_icp = {}

    industry = summary_data.get("industry", "").lower()
    size = summary_data.get("estimated_size", "")
    location = summary_data.get("location", "").lower()
    revenue = summary_data.get("revenue_range", "")

    if custom_icp.get("industry"):
        if custom_icp["industry"].lower() in industry:
            score += 25
            reasons.append("industry match")

    size_numbers = extract_numbers(size)
    if len(size_numbers) >= 2:
        if custom_icp.get("min_size", 0) <= size_numbers[0] <= custom_icp.get("max_size", 99999):
            score += 25
            reasons.append("size match")

    if custom_icp.get("location"):
        if custom_icp["location"].lower() in location:
            score += 25
            reasons.append("location match")

    revenue_numbers = extract_numbers(revenue)
    if revenue_numbers:
        if custom_icp.get("min_revenue", 0) <= revenue_numbers[0] <= custom_icp.get("max_revenue", 99999):
            score += 25
            reasons.append("revenue match")

    fit = "Yes" if score >= 75 else "Maybe" if score >= 50 else "No"

    return {
        "icp_fit": fit,
        "icp_score": score,
        "reason": " | ".join(reasons) if reasons else "Weak match"
    }
