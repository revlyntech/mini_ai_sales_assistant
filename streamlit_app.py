import streamlit as st
from app import run_agent
import json

st.set_page_config(
    page_title="Mini AI Sales Assistant",
    layout="wide"
)

st.title("Mini AI Sales Assistant")
st.write("AI-powered B2B lead enrichment, ICP qualification, and personalized outreach")

st.sidebar.header("Lead Input")
company_name = st.sidebar.text_input("Company Name")
website = st.sidebar.text_input("Website")

st.sidebar.header("Custom ICP Criteria")
target_industry = st.sidebar.text_input("Industry")
min_size = st.sidebar.number_input("Min Employees", 1, 1000, 10)
max_size = st.sidebar.number_input("Max Employees", 1, 5000, 50)
target_location = st.sidebar.text_input("Location")
min_revenue = st.sidebar.number_input("Min Revenue ($M)", 1, 1000, 5)
max_revenue = st.sidebar.number_input("Max Revenue ($M)", 1, 5000, 50)

if st.sidebar.button("Analyze Lead"):
    custom_icp = {
        "industry" : target_industry,
        "min_size" : min_size,
        "max_size" : max_size,
        "location" : target_location,
        "min_revenue" : min_revenue,
        "max_revenue" : max_revenue
    }


    input_data = {
        "company_name" : company_name,
        "website" : website
    }

    with st.spinner("Processing Lead..."):
        result = run_agent(input_data)

    st.success("Analysis Complete")
        
    col1, col2 = st.columns(2)

    with col1 :
        st.subheader("Company Insights")
        st.write("**Summary:**", result["company_summary"])
        st.write("**Industry:**", result["industry"])
        st.write("**Estimated Size:**", result["estimated_size"])
        st.write("**Location:**", result["location"])
        st.write("**Revenue:**", result["revenue_range"])

    with col2 :
        st.subheader("ICP Qualification")

        score = result.get("icp_score", 0)
        fit = result.get("icp_fit","No")

        st.write(f"### ICP Score: {score}/100")
        st.progress(score / 100)

    
        confidence = min(100, score + 10)
        st.write(f"Confidence Meter: {confidence}%")
        st.progress(confidence / 100)

        st.write("**Reason:**", result["reason"])
        st.subheader("Outreach Email")
        st.text_area("Generated Email", result["outreach_email"], height=220)

              