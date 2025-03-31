
import streamlit as st

st.set_page_config(page_title="System Design Assistant", layout="wide")
st.title("System Design Assistant for TPM Interviews")

st.markdown("Use this assistant during system design interviews to input assumptions and get a structured output.")

st.header("1. System Description")
problem_statement = st.text_area("Describe the system you're being asked to design (e.g., 'Design a centralized logging platform').")

st.header("2. General Assumptions")

col1, col2 = st.columns(2)
with col1:
    users = st.number_input("Estimated Daily Active Users", min_value=0, value=100000)
    qps = st.number_input("Peak QPS", min_value=0, value=5000)
    read_write_ratio = st.text_input("Read/Write Ratio", "80/20")
    regions = st.text_input("Regions (e.g., Single-region, Multi-region)", "Multi-region")
    availability = st.text_input("Availability Target (e.g., 99.9%)", "99.9%")
    latency = st.text_input("Latency Target (e.g., <200ms)", "<200ms")

with col2:
    data_retention = st.text_input("Data Retention Policy", "30 days")
    sla_slo = st.text_input("SLA/SLOs", "99.9% uptime, 95% requests < 200ms")
    security = st.text_input("Security Requirements", "OAuth2, Encrypted at rest and in transit")
    compliance = st.text_input("Compliance Needs", "GDPR, SOC2")
    integration = st.text_area("Integration Requirements (e.g., Slack, APIs)", "Slack, Email, Prometheus")
    rollout_plan = st.text_area("Rollout Strategy / Phases", "Alpha → Beta → GA with canary deployments")

st.header("3. Media Handling Assumptions")

enable_photos = st.checkbox("Include Photo Uploads?")
enable_videos = st.checkbox("Include Video Uploads?")

if enable_photos or enable_videos:
    col3, col4 = st.columns(2)
    with col3:
        avg_photo_size = st.number_input("Avg Photo Size (MB)", min_value=0.0, value=3.0)
        avg_video_duration = st.number_input("Avg Video Duration (min)", min_value=0.0, value=2.0)
        avg_video_bitrate = st.number_input("Avg Video Bitrate (Mbps)", min_value=0.0, value=5.0)
    with col4:
        resolution = st.selectbox("Video Resolution", ["480p", "720p", "1080p", "1440p", "2160p (4K)"])
        uploads_per_user = st.number_input("Uploads per User per Day", min_value=0, value=2)
        peak_upload_qps = st.number_input("Peak Upload QPS", min_value=0, value=500)

    transcoding = st.selectbox("Transcoding Required?", ["Yes", "No"])
    preview = st.selectbox("Thumbnail/Preview Generation?", ["Yes", "No"])
    playback_latency = st.text_input("Playback Latency Target", "<5s")
    storage_tiering = st.text_input("Storage Tiering Strategy", "Hot for recent, Cold for archive, CDN for active content")
    adaptive_streaming = st.selectbox("Adaptive Bitrate Streaming Needed?", ["Yes", "No"])
    retention_policy = st.text_input("Media Retention Policy", "User-controlled, default 90 days")

st.header("4. Output")

if st.button("Generate Design Summary"):
    st.subheader("System Design Summary")

    st.markdown(f"**Problem Statement:** {problem_statement}")
    st.markdown("### General Assumptions")
    st.markdown(f"- Users: {users}")
    st.markdown(f"- Peak QPS: {qps}")
    st.markdown(f"- Read/Write Ratio: {read_write_ratio}")
    st.markdown(f"- Regions: {regions}")
    st.markdown(f"- Availability: {availability}")
    st.markdown(f"- Latency Target: {latency}")
    st.markdown(f"- Data Retention: {data_retention}")
    st.markdown(f"- SLA/SLOs: {sla_slo}")
    st.markdown(f"- Security: {security}")
    st.markdown(f"- Compliance: {compliance}")
    st.markdown(f"- Integration: {integration}")
    st.markdown(f"- Rollout Strategy: {rollout_plan}")

    if enable_photos or enable_videos:
        st.markdown("### Media Assumptions")
        if enable_photos:
            st.markdown(f"- Avg Photo Size: {avg_photo_size} MB")
        if enable_videos:
            st.markdown(f"- Avg Video Duration: {avg_video_duration} min")
            st.markdown(f"- Avg Video Bitrate: {avg_video_bitrate} Mbps")
            st.markdown(f"- Video Resolution: {resolution}")
        st.markdown(f"- Uploads/User/Day: {uploads_per_user}")
        st.markdown(f"- Peak Upload QPS: {peak_upload_qps}")
        st.markdown(f"- Transcoding Required: {transcoding}")
        st.markdown(f"- Thumbnail Generation: {preview}")
        st.markdown(f"- Playback Latency Target: {playback_latency}")
        st.markdown(f"- Storage Tiering: {storage_tiering}")
        st.markdown(f"- Adaptive Streaming: {adaptive_streaming}")
        st.markdown(f"- Media Retention Policy: {retention_policy}")

    st.markdown("---")
    st.markdown("Now use these assumptions to structure your system design, explain trade-offs, and walk through your architecture confidently.")
