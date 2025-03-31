
# System Design Assistant (Version 3)

An interactive architecture generator built with Streamlit to help you prepare for system design interviews and technical reviews.

## Features
- Editable problem type presets
- Capacity estimation (QPS, storage, peak traffic)
- SLO & latency budget modeling
- Failure simulation + mitigation planner
- Architecture layer suggestions
- CAP & PACELC trade-off frameworks
- Interview walkthrough generator
- Downloadable summary (Markdown/CSV)
- Custom theme + streamlit-extras

## Run Locally
```
pip install -r requirements.txt
streamlit run system_design_tool_app_v3.py
```

## Deploy to Streamlit Cloud
1. Push this repo to GitHub
2. Visit https://streamlit.io/cloud
3. Click "New App", select this repo
4. Set the file path to `system_design_tool_app_v3.py`
5. Click Deploy
