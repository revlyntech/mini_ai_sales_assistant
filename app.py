from enrichment import scrape_website
from icp import check_icp
from summary import generate_summary
import json


def run_agent(input_data, custom_icp=None):
    company = input_data["company_name"]
    website = input_data["website"]

    print("Scraping website...")
    enriched = scrape_website(website)

    print("Generating summary + outreach...")
    summary_data = generate_summary(enriched, company)

    print("Checking ICP...")
    icp_result = check_icp(enriched, summary_data)

    return {
        "company_summary": summary_data.get("company_summary", "No summary"),
        "industry": summary_data.get("industry", "SaaS"),
        "estimated_size": summary_data.get("estimated_size", "20-50 employees"),
        "location": summary_data.get("location", "United States"),
        "revenue_range": summary_data.get("revenue_range", "$5M-$50M"),
        "icp_fit": icp_result.get("icp_fit", "No"),
        "icp_score": icp_result.get("icp_score", 0),
        "reason": icp_result.get("reason", "No reasoning available"),
        "outreach_email": summary_data.get(
            "outreach_email",
            f"Hi {company} team,\n\nWould love to connect."
        )
    }


if __name__ == "__main__":
    input_data = {
        "company_name": "Remitap",
        "website": "https://www.remitap.com/"
    }

    result = run_agent(input_data)
    print(json.dumps(result, indent=2))
