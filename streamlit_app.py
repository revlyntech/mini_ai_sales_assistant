import streamlit as st
from urllib.parse import urlparse
from app import run_agent

st.set_page_config(
    page_title="RevOps Central | AI Sales Assistant",
    layout="wide"
)

def extract_company_name_from_url(url: str) -> str:
    try:
        domain = urlparse(url).netloc.replace("www.", "")
        return domain.split(".")[0].title() if domain else "Unknown"
    except Exception:
        return "Unknown"


@st.cache_data(show_spinner=False)
def cached_run_agent(input_data, custom_icp):
    return run_agent(input_data, custom_icp)


col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("assets/Logo_RevOps.png", width=140)
with col_title:
    st.title("RevOps Central | Mini AI Sales Assistant")
    st.caption("AI-powered lead enrichment, ICP scoring, and personalized outreach")

st.markdown("---")

st.sidebar.header("Lead Input")
website = st.sidebar.text_input("Company Website", "https://www.remitap.com/")

st.sidebar.header("Custom ICP Criteria")
target_industry = st.sidebar.text_input("Industry", "SaaS")
min_size = st.sidebar.number_input("Min Employees", min_value=1, max_value=10000, value=10)
max_size = st.sidebar.number_input("Max Employees", min_value=1, max_value=10000, value=200)
target_location = st.sidebar.text_input("Location", "United States")
min_revenue = st.sidebar.number_input("Min Revenue ($M)", min_value=1, max_value=1000, value=5)
max_revenue = st.sidebar.number_input("Max Revenue ($M)", min_value=1, max_value=5000, value=100)

if st.sidebar.button("Analyze Lead", use_container_width=True):
    company_name = extract_company_name_from_url(website)

    custom_icp = {
        "industry": target_industry,
        "min_size": min_size,
        "max_size": max_size,
        "location": target_location,
        "min_revenue": min_revenue,
        "max_revenue": max_revenue,
    }

    input_data = {
        "company_name": company_name,
        "website": website,
    }

    with st.spinner("Enriching lead and generating outreach..."):
        result = cached_run_agent(input_data, custom_icp)

    st.success("Analysis Complete")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Company Insights")
        st.info(result.get("company_summary", "No summary available"))
        st.write("**Industry:**", result.get("industry", "Unknown"))
        st.write("**Estimated Size:**", result.get("estimated_size", "10-50 employees"))
        st.write("**Location:**", result.get("location", "United States"))
        st.write("**Revenue:**", result.get("revenue_range", "$5M-$20M"))

    with col2:
        st.subheader("ICP Qualification")
        score = result.get("icp_score", 0)
        fit = result.get("icp_fit", "No")

        if fit == "Yes":
            st.success(f"🟢 ICP Fit: {fit}")
        elif fit == "Maybe":
            st.warning(f"🟡 ICP Fit: {fit}")
        else:
            st.error(f"🔴 ICP Fit: {fit}")

        st.write(f"### ICP Score: {score}/100")
        st.progress(score / 100)

        confidence = min(100, score + 10)
        st.write(f"### Confidence Meter: {confidence}%")
        st.progress(confidence / 100)

        st.caption(result.get("reason", "No reasoning available"))

    st.markdown("---")
    st.subheader("Personalized Outreach")
    st.text_area(
        "Generated Email",
        value=result.get("outreach_email", "No email generated"),
        height=220,
    )
