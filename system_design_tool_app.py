
import streamlit as st

# --- SETUP ---
st.set_page_config(page_title="System Design Tool", layout="wide")
st.title("System Design Assistant")

# --- PROBLEM TYPE SELECTION ---
problem_types = {
    "Social Media Feed": {
        "toggles": {
            "Use CDN": True,
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
            "Cache Hit Rate (%)": 90
        },
        "db": "Cassandra, Redis, Postgres",
        "reason": "Feeds need fast reads/writes, large fan-out, and simple indexing"
    },
    "Real-Time Chat": {
        "toggles": {
            "Use CDN": False,
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
            "P95 Latency Target (ms)": 100,
            "Cache Hit Rate (%)": 10
        },
        "db": "MongoDB, Redis, Postgres",
        "reason": "Messages are semi-structured with ordering and fast access"
    },
    "Video Streaming Platform": {
        "toggles": {
            "Use CDN": True,
            "Multi-Region": True,
            "Compression": True,
            "Adaptive Bitrate": True,
            "Lifecycle Policies": False,
            "Stores PII": False,
            "Region Locking": False
        },
        "params": {
            "Data Retention (days)": 365,
            "Target Uptime (%)": 99.9,
            "P95 Latency Target (ms)": 400,
            "Cache Hit Rate (%)": 80
        },
        "db": "Postgres, S3, GCS",
        "reason": "Metadata in RDBMS, media in replicated object storage"
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.header("Configuration")
    problem = st.selectbox("Select Problem Type", list(problem_types.keys()))
    st.markdown("---")
    st.subheader("Auto-Filled Toggles")
    for k, v in problem_types[problem]["toggles"].items():
        st.checkbox(k, value=v, disabled=True)
    st.markdown("---")
    st.subheader("System Assumptions")
    for k, v in problem_types[problem]["params"].items():
        st.number_input(k, value=v, step=1, disabled=True)

# --- MAIN ---
st.subheader("1. Capacity Estimation Inputs")
col1, col2 = st.columns(2)
with col1:
    users = st.number_input("Number of Users", value=10_000_000, step=100_000)
    dau = st.number_input("Daily Active Users (DAU)", value=1_000_000, step=50_000)
    reqs_per_user = st.number_input("Requests per User per Day", value=20)
with col2:
    avg_obj_size_kb = st.number_input("Average Object Size (KB)", value=1)
    replication = st.number_input("Replication Factor", value=3)
    peak_multiplier = st.number_input("Peak Traffic Multiplier", value=2.0)

# --- CALCULATIONS ---
total_daily_requests = dau * reqs_per_user
read_ratio = problem_types[problem]["params"]["Cache Hit Rate (%)"] / 100
read_qps = (total_daily_requests / 86400) * read_ratio
write_qps = (total_daily_requests / 86400) * (1 - read_ratio)
peak_qps = (total_daily_requests / 86400) * peak_multiplier
total_storage_kb = dau * reqs_per_user * avg_obj_size_kb * replication
total_storage_gb = total_storage_kb / 1024 / 1024

# --- RESULTS ---
st.subheader("2. Estimated System Load")
st.metric("Total Daily Requests", f"{total_daily_requests:,.0f}")
st.metric("Read QPS (estimated)", f"{read_qps:,.0f}")
st.metric("Write QPS (estimated)", f"{write_qps:,.0f}")
st.metric("Peak QPS", f"{peak_qps:,.0f}")
st.metric("Total Storage (GB, replicated)", f"{total_storage_gb:,.2f}")

# --- DESIGN SUMMARY ---
st.subheader("3. Architecture & DB Recommendations")
st.markdown(f"**Problem Type:** {problem}")
st.markdown(f"**Recommended DBs:** {problem_types[problem]['db']}")
st.markdown(f"**Why:** {problem_types[problem]['reason']}")

# --- FOOTER ---
st.markdown("---")
st.caption("Built with Streamlit by your System Design Assistant")
