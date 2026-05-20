import streamlit as st
from utils import (
    init_session_state,
    require_login,
    get,
)

init_session_state()
require_login()

st.title("📊 Usage Analytics")

selected_api_key = st.session_state.get("selected_api_key")

if not selected_api_key:
    st.warning("Please select an API key from the API Keys page first.")
    st.stop()

response = get(
    "/v1/usage",
    headers={
        "x-api-key": selected_api_key
    }
)

if response.status_code != 200:
    try:
        st.error(response.json())
    except Exception:
        st.error(response.text)
    st.stop()

data = response.json()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Requests",
        data.get("total_requests", 0)
    )

with col2:
    st.metric(
        "Total Tokens",
        data.get("total_tokens", 0)
    )

with col3:
    st.metric(
        "Total Cost ($)",
        f"{data.get('total_cost', 0):.6f}"
    )

with col4:
    st.metric(
        "Avg Latency (s)",
        f"{data.get('average_latency', 0):.2f}"
    )

st.divider()

models = data.get("models", {})

if models:
    st.subheader("🤖 Model Usage Distribution")
    st.bar_chart(models)

recent_requests = data.get("recent_requests", [])

if recent_requests:
    st.subheader("🕒 Recent Requests")
    st.dataframe(
        recent_requests,
        use_container_width=True
    )
else:
    st.info("No recent usage data found.")