from enrichment import scrape_website
from icp import check_icp
from email_generator import generate_email
from summary import generate_summary
import json


def run_agent(input_data, custom_icp=None):
    company = input_data["company_name"]
    website = input_data["website"]

    print("Scraping website...")
    enriched = scrape_website(website)

    print("Generating summary...")
    summary_data = generate_summary(enriched)

    print("Checking ICP...")
    icp_result = check_icp(enriched, summary_data, custom_icp)

    print("Generating email...")
    email = generate_email(company, summary_data["company_summary"])

    return {
        "company_summary": summary_data["company_summary"],
        "industry": summary_data.get("industry", "Unknown"),
        "estimated_size": summary_data.get("estimated_size", "Unknown"),
        "location": summary_data.get("location", "Unknown"),
        "revenue_range": summary_data.get("revenue_range", "Unknown"),
        "icp_fit": icp_result["icp_fit"],
        "icp_score": icp_result["icp_score"],
        "reason": icp_result["reason"],
        "outreach_email": email
    }


if __name__ == "__main__":
    input_data = {
        "company_name": "Remitap",
        "website": "https://www.remitap.com/"
    }

    default_icp = {
        "industry": "SaaS",
        "min_size": 10,
        "max_size": 50,
        "location": "US",
        "min_revenue": 5,
        "max_revenue": 50
    }

    result = run_agent(input_data, default_icp)

    print("\n✅ FINAL OUTPUT:\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))