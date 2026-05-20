import streamlit as st
from utils import (
    init_session_state,
    require_login,
    auth_headers,
    post,
    get,
)

init_session_state()
require_login()

st.title("🔑 API Key Management")

if st.button("Generate New API Key"):
    response = post(
        "/api-keys/create",
        headers=auth_headers(),
    )

    if response.status_code == 200:
        data = response.json()

        new_key = data.get("api_key")

        if new_key:
            st.success("API key created")
            st.code(new_key)

            st.session_state.selected_api_key = new_key

            if "api_keys" not in st.session_state:
                st.session_state.api_keys = []

            if new_key not in st.session_state.api_keys:
                st.session_state.api_keys.append(new_key)
        else:
            st.error("API key not found in response.")
    else:
        st.error(response.text)


if st.button("Refresh API Keys"):
    response = get(
        "/api-keys/list",
        headers=auth_headers(),
    )

    if response.status_code == 200:
        data = response.json()

        if isinstance(data, list):
            st.session_state.api_keys = data

        elif isinstance(data, dict):
            if "api_keys" in data and isinstance(data["api_keys"], list):
                st.session_state.api_keys = data["api_keys"]
            else:
                st.session_state.api_keys = []

        else:
            st.session_state.api_keys = []

        st.success("API keys refreshed.")
    else:
        st.error(response.text)


api_keys = st.session_state.get("api_keys", [])

if not isinstance(api_keys, list):
    api_keys = []
    st.session_state.api_keys = []

if api_keys:
    selected = st.selectbox(
        "Select Active API Key",
        api_keys,
    )

    st.session_state.selected_api_key = selected

    st.success("Selected API key saved for AI Playground.")

    st.code(selected)

else:
    st.info("No API keys loaded yet. Generate or refresh API keys first.")

