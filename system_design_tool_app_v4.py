
import streamlit as st
import pandas as pd

st.set_page_config(page_title="System Design Assistant v4", layout="wide")
st.title("System Design Assistant — Version 4.0")

# Problem type selector
problem_type = st.selectbox("Problem Type", [
    "General",
    "LLM Chat Assistant",
    "Financial App",
    "Autonomous Vehicle Platform",
    "Reservation System",
    "Scheduling App",
    "Proximity App",
    "Communication App",
    "Collaborative App",
    "Data Processing"
])

# Example prefill dictionary
defaults = {
    "General": {
        "dau": 100000,
        "req_per_user": 10,
        "object_size_kb": 10,
        "retention_days": 30
    },
    "LLM Chat Assistant": {
        "dau": 500000,
        "req_per_user": 20,
        "object_size_kb": 150,
        "retention_days": 7
    }
    # Add the rest later
}

# Load default for the problem type
use_defaults = st.checkbox("Use problem-type defaults", value=True)

def get_default(key, fallback=0):
    if use_defaults and problem_type in defaults and key in defaults[problem_type]:
        return defaults[problem_type][key]
    return fallback

# Inputs (simplified)
dau = st.number_input("Daily Active Users (DAU)", value=get_default("dau", 100000))
req_per_user = st.number_input("Requests per User per Day", value=get_default("req_per_user", 10))
object_size_kb = st.number_input("Average Object Size (KB)", value=get_default("object_size_kb", 10))
retention_days = st.number_input("Retention (days)", value=get_default("retention_days", 30))

# Estimation
total_objects = dau * req_per_user
storage_gb = (total_objects * object_size_kb) / (1024 * 1024)
st.metric("Total Storage Estimate (GB)", f"{storage_gb:.2f}")

# Architecture + Tradeoffs (simplified)
st.subheader("Suggested Architecture Components")
arch = ["API Gateway", "App Server", "Database", "Object Store"]
if problem_type == "LLM Chat Assistant":
    arch.append("Vector Store")
if problem_type == "Data Processing":
    arch.append("Stream Processor")
st.write(", ".join(arch))

st.subheader("Trade-offs")
if problem_type == "LLM Chat Assistant":
    st.write("- High memory cost for embeddings and inference")
if problem_type == "Financial App":
    st.write("- Prioritize strong consistency; lower availability during partition")

# Export
df = pd.DataFrame([{
    "DAU": dau,
    "Requests/User/Day": req_per_user,
    "Object Size (KB)": object_size_kb,
    "Retention Days": retention_days,
    "Storage (GB)": storage_gb,
    "Architecture": ", ".join(arch),
    "Problem Type": problem_type
}])
st.download_button("Download Summary CSV", df.to_csv(index=False).encode("utf-8"), "system_design_v4_summary.csv", "text/csv")
