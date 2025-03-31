import streamlit as st
import pandas as pd

st.set_page_config(page_title="System Design Assistant", layout="wide")
st.title("System Design Assistant — Version 3")

# --- Problem Types ---
problem_types = {
    "General": {
        "toggles": {
            "Use CDN": False,
            "Multi-Region": False,
            "Compression": False,
            "Adaptive Bitrate": False,
            "Lifecycle Policies": False,
            "Stores PII": False,
            "Region Locking": False
        },
        "params": {
            "Data Retention (days)": 180,
            "Target Uptime (%)": 99.9,
            "P95 Latency Target (ms)": 300,
            "Cache Hit Rate (%)": 80,
            "Growth Rate (%/mo)": 10,
            "Payload Size (KB)": 10
        },
        "layers": ["API Gateway", "Load Balancer", "App Layer", "Cache", "DB", "Object Store", "Queue", "Observability"],
        "tradeoffs": "Default CAP trade-off: CP. PACELC: PA/EL.",
        "failure_modeling": "Describe component failures and fallback strategies."
    },
    "LLM Chat Assistant": {
        "toggles": {
            "Use CDN": True,
            "Multi-Region": True,
            "Compression": True,
            "Adaptive Bitrate": False,
            "Lifecycle Policies": False,
            "Stores PII": True,
            "Region Locking": True
        },
        "params": {
            "Data Retention (days)": 30,
            "Target Uptime (%)": 99.99,
            "P95 Latency Target (ms)": 150,
            "Cache Hit Rate (%)": 90,
            "Growth Rate (%/mo)": 25,
            "Payload Size (KB)": 2
        },
        "layers": ["Frontend", "Inference Gateway", "Prompt Engine", "Embedding Cache", "Vector DB", "LLM API", "Observability"],
        "tradeoffs": "Focus on low latency over strong consistency. CAP: PA/EC. Use aggressive caching.",
        "failure_modeling": "LLM timeout, prompt injection, API throttling."
    }
}

# --- Sidebar Config ---
with st.sidebar:
    st.header("Configuration")
    selected_type = st.selectbox("Problem Type", list(problem_types.keys()), index=0)

    st.subheader("Toggles (Editable)")
    toggles = {}
    for k, v in problem_types[selected_type]["toggles"].items():
        toggles[k] = st.checkbox(k, value=v)

    st.subheader("System Assumptions")
    params = {}
    for k, v in problem_types[selected_type]["params"].items():
        step = 0.1 if isinstance(v, float) and not v.is_integer() else 1
        params[k] = st.number_input(k, value=v, step=step)

# --- Capacity Estimation ---
st.subheader("Capacity Estimation")
users = st.number_input("Total Users", value=10_000_000, step=100_000)
dau = st.number_input("Daily Active Users (DAU)", value=1_000_000)
reqs_per_user = st.number_input("Requests per User per Day", value=20)
replication = st.number_input("Replication Factor", value=3)
peak_multiplier = st.number_input("Peak Traffic Multiplier", value=2.0)

total_daily_requests = dau * reqs_per_user
qps = total_daily_requests / 86400
peak_qps = qps * peak_multiplier
storage_kb = dau * reqs_per_user * params["Payload Size (KB)"] * replication
storage_gb = storage_kb / 1024 / 1024

st.metric("QPS (avg)", f"{qps:,.0f}")
st.metric("Peak QPS", f"{peak_qps:,.0f}")
st.metric("Storage (GB)", f"{storage_gb:,.2f}")

# --- Architecture & Tradeoffs ---
st.subheader("Architecture Layers")
for layer in problem_types[selected_type]["layers"]:
    st.markdown(f"- {layer}")

st.subheader("Trade-off Reasoning")
st.text_area("Trade-offs", problem_types[selected_type]["tradeoffs"])

st.subheader("Failure Modeling")
st.text_area("Failure Points & Mitigations", problem_types[selected_type]["failure_modeling"])

# --- Walkthrough Generator ---
st.subheader("Interview Walkthrough Summary")
if st.button("Generate Walkthrough"):
    st.markdown(f"""
    ### Problem Type: {selected_type}
    - DAU: {dau:,}
    - Retention: {params["Data Retention (days)"]} days
    - Latency Target: {params["P95 Latency Target (ms)"]} ms
    - Cache Hit Rate: {params["Cache Hit Rate (%)"]}%
    - Growth Rate: {params["Growth Rate (%/mo)"]}%

    **Key Layers:** {', '.join(problem_types[selected_type]["layers"])}

    **Trade-offs:**  
    {problem_types[selected_type]["tradeoffs"]}

    **Failure Planning:**  
    {problem_types[selected_type]["failure_modeling"]}
    """)

# --- Download Design Summary ---
st.subheader("Download Design Summary")
summary_dict = {
    "Problem Type": selected_type,
    "DAU": dau,
    "Avg QPS": qps,
    "Peak QPS": peak_qps,
    "Storage (GB)": storage_gb,
    "Trade-offs": problem_types[selected_type]["tradeoffs"],
    "Failure Model": problem_types[selected_type]["failure_modeling"]
}
summary_df = pd.DataFrame([summary_dict])
csv = summary_df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", data=csv, file_name="design_summary.csv", mime="text/csv")
