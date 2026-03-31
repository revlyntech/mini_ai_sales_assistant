import re


def extract_numbers(text):
    return [int(num) for num in re.findall(r"\d+", str(text))]


def normalize_size(size_text):
    size_text = str(size_text).lower()

    if "small" in size_text:
        return 20
    if "medium" in size_text:
        return 100
    if "large" in size_text:
        return 500

    nums = extract_numbers(size_text)
    if nums:
        return nums[0]

    return None


def normalize_revenue(revenue_text):
    revenue_text = str(revenue_text).lower()

    if "low" in revenue_text:
        return 2
    if "medium" in revenue_text:
        return 10
    if "high" in revenue_text:
        return 50

    nums = extract_numbers(revenue_text)
    if nums:
        return nums[0]

    return None


def check_icp(data, summary_data, custom_icp=None):
    if custom_icp is None:
        custom_icp = {
            "industry": "saas",
            "min_size": 10,
            "max_size": 200,
            "location": "united states",
            "min_revenue": 5,
            "max_revenue": 100
        }

    industry = str(summary_data.get("industry", "")).lower()
    size_value = normalize_size(summary_data.get("estimated_size"))
    revenue_value = normalize_revenue(summary_data.get("revenue_range"))
    location = str(summary_data.get("location", "")).lower()

    score = 0
    reasons = []

    target_industry = str(custom_icp.get("industry", "")).lower().strip()
    if not target_industry:
        score += 20
        reasons.append("industry default")
    elif target_industry in industry:
        score += 25
        reasons.append("industry match")

    if size_value:
        if custom_icp["min_size"] <= size_value <= custom_icp["max_size"]:
            score += 25
            reasons.append("size match")
    else:
        score += 10
        reasons.append("size inferred")

    if revenue_value:
        if custom_icp["min_revenue"] <= revenue_value <= custom_icp["max_revenue"]:
            score += 25
            reasons.append("revenue match")
    else:
        score += 10
        reasons.append("revenue inferred")

    target_location = str(custom_icp.get("location", "")).lower().strip()
    if not target_location:
        score += 20
        reasons.append("location default")
    elif target_location in location:
        score += 25
        reasons.append("location match")

    if score >= 75:
        fit = "Yes"
    elif score >= 45:
        fit = "Maybe"
    else:
        fit = "No"

    return {
        "icp_fit": fit,
        "icp_score": score,
        "reason": " | ".join(reasons)
    }