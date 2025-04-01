import streamlit as st
import pandas as pd

st.set_page_config(page_title="System Design Assistant", layout="wide")
st.title("System Design Assistant — Version 3.1")

# --- Sidebar Grouped Inputs ---
st.sidebar.header("System Assumptions")

with st.sidebar.expander("User & Traffic"):
    dau = st.number_input("Daily Active Users (DAU)", value=1_000_000)
    requests_per_user = st.number_input("Requests per User per Day", value=20)
    peak_multiplier = st.number_input("Peak Traffic Multiplier", value=2.0)
    session_length = st.number_input("Avg. Session Length (min)", value=15)
    think_time = st.number_input("Think Time Between Actions (sec)", value=5)

with st.sidebar.expander("Payload & Storage"):
    payload_size_kb = st.number_input("Payload Size (KB)", value=10)
    object_size_kb = st.number_input("Avg Object Size (KB)", value=10)
    retention_days = st.number_input("Retention Period (days)", value=180)
    replication_factor = st.number_input("Replication Factor", value=3)

with st.sidebar.expander("Network & Bandwidth"):
    cache_hit_rate = st.slider("Cache Hit Rate (%)", 0, 100, 80)
    ingress_overhead = st.number_input("Ingress Overhead Factor", value=1.0)
    egress_overhead = st.number_input("Egress Overhead Factor", value=1.0)

with st.sidebar.expander("Reliability & Availability"):
    sla = st.selectbox("Availability Target", ["99.0%", "99.9%", "99.99%", "99.999%"], index=2)
    consistency = st.selectbox("Consistency Model", ["Strong", "Eventual", "Quorum"], index=0)
    rpo = st.number_input("Recovery Point Objective (min)", value=5)
    rto = st.number_input("Recovery Time Objective (min)", value=10)

with st.sidebar.expander("Toggles"):
    use_cdn = st.checkbox("Use CDN", True)
    enable_compression = st.checkbox("Enable Compression", True)
    store_pii = st.checkbox("Stores PII", False)
    region_locking = st.checkbox("Region Locking Required", False)
    disaster_recovery = st.checkbox("Disaster Recovery Setup", True)

# --- Core Calculations ---
st.header("Capacity Estimation")

total_requests = dau * requests_per_user
qps = total_requests / 86400
peak_qps = qps * peak_multiplier
total_object_storage = dau * requests_per_user * object_size_kb * replication_factor
storage_gb = total_object_storage / 1024 / 1024
egress_mb_per_sec = ((qps * payload_size_kb * (1 - cache_hit_rate / 100)) / 1024) * egress_overhead

st.metric("Average QPS", f"{qps:,.0f}")
st.metric("Peak QPS", f"{peak_qps:,.0f}")
st.metric("Estimated Storage (GB)", f"{storage_gb:,.2f}")
st.metric("Egress (MB/sec)", f"{egress_mb_per_sec:,.2f}")

# --- Architecture Suggestions ---
st.header("Architecture & Trade-offs")
arch_layers = ["API Gateway", "App Server", "Cache", "Primary DB", "Object Store", "Async Queue", "Observability"]

if use_cdn:
    arch_layers.insert(0, "CDN")
if region_locking:
    arch_layers.append("Geo-Sharded DB")
if disaster_recovery:
    arch_layers.append("Hot Standby Cluster")
if store_pii:
    arch_layers.append("Vault/KMS")

st.subheader("Suggested Architecture Layers")
st.write(", ".join(arch_layers))

tradeoffs = []
if consistency == "Strong":
    tradeoffs.append("Lower availability under partition")
if enable_compression:
    tradeoffs.append("Saves bandwidth, increases CPU usage")
if store_pii:
    tradeoffs.append("Must implement strict access controls and audit logging")
if region_locking:
    tradeoffs.append("Increased complexity due to geo-partitioning")
if disaster_recovery:
    tradeoffs.append("Higher infra cost but faster recovery")

st.subheader("Design Trade-offs")
for t in tradeoffs:
    st.markdown(f"- {t}")

# --- Walkthrough Generator ---
st.header("Interview Walkthrough")
if st.button("Generate Summary"):
    st.markdown(f"""
    ### System Design Summary
    - **DAU:** {dau:,}, **Requests/User/Day:** {requests_per_user}, **Peak Multiplier:** {peak_multiplier}
    - **Payload:** {payload_size_kb} KB, **Object Size:** {object_size_kb} KB
    - **Replication Factor:** {replication_factor}, **Retention:** {retention_days} days
    - **Storage Estimate:** ~{storage_gb:.2f} GB
    - **Peak QPS:** ~{peak_qps:,.0f}, **Egress:** ~{egress_mb_per_sec:.2f} MB/s
    - **Consistency Model:** {consistency}, **SLA Target:** {sla}
    - **Key Layers:** {", ".join(arch_layers)}
    - **Trade-offs:**
        - {"; ".join(tradeoffs)}
    """)

# --- Download Section ---
st.header("Export Design Summary")
summary_dict = {
    "DAU": dau,
    "Requests/User/Day": requests_per_user,
    "Payload Size (KB)": payload_size_kb,
    "Object Size (KB)": object_size_kb,
    "Replication": replication_factor,
    "Retention (days)": retention_days,
    "Peak QPS": peak_qps,
    "Storage Estimate (GB)": storage_gb,
    "Egress MB/sec": egress_mb_per_sec,
    "SLA": sla,
    "Consistency": consistency,
    "Architecture": ", ".join(arch_layers),
    "Trade-offs": "; ".join(tradeoffs)
}
df = pd.DataFrame([summary_dict])
st.download_button("Download CSV", df.to_csv(index=False).encode("utf-8"), "system_design_summary.csv", "text/csv")
