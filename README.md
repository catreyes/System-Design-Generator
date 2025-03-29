# System Design Assistant (Streamlit App)

A web-based interactive tool to help you rapidly design scalable systems for interviews, architecture reviews, or internal planning.

Built with [Streamlit](https://streamlit.io), this assistant provides:

- Problem-type-driven system design presets
- Capacity estimation for QPS, storage, and replication
- Auto-filled system constraints (latency, cache, uptime, retention)
- Database recommendations and rationale
- Clear, metrics-based outputs
- Instant visual feedback for toggles and configuration

## Live Demo
[Launch the App on Streamlit](https://streamlit.io/cloud) *(once deployed)*

---

## Features

### 1. Problem Type Selector
Choose from real-world system types like:
- Social Media Feed
- Real-Time Chat
- Video Streaming
- Metrics Ingestion
- Secure File Storage
- Data Warehouse
- E-Commerce Checkout

Each selection auto-fills best-practice values for:
- Retention, latency, cache hit rate, replication
- Toggle flags like CDN, Compression, PII compliance

---

### 2. Capacity Estimator
Inputs:
- Number of users, DAU, requests per user
- Object size, replication factor, peak multiplier

Outputs:
- Read & write QPS
- Peak QPS
- Estimated storage in GB (with replication)

---

### 3. Architecture & DB Recommendations
Get suggestions for:
- Database types (SQL, NoSQL, TSDB, Blob)
- Example technologies
- Rationale tailored to system type

---

## Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/YOUR_USERNAME/system-design-assistant.git
cd system-design-assistant
