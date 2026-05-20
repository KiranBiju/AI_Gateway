import json
import requests
import streamlit as st

from utils import init_session_state, require_login

init_session_state()
require_login()

BACKEND_URL = "http://127.0.0.1:8000"

st.title("🌀 AI Playground")

selected_api_key = st.session_state.get("selected_api_key")

if not selected_api_key:
    st.warning("Please select an API key from the API Keys page.")
    st.stop()

prompt = st.text_area(
    "Enter your prompt",
    height=220,
    placeholder="Type Here...."
)

col1, col2, col3 = st.columns(3)

with col1:
    mode = st.selectbox(
        "Mode",
        ["fast", "balanced", "detailed"],
        index=0
    )

with col2:
    use_rag = st.checkbox("Use RAG (future)", value=False)

with col3:
    endpoint = st.selectbox(
        "Endpoint",
        ["/v1/generate"],
        index=0
    )


if st.button("Generate Response", type="primary"):

    if not prompt.strip():
        st.warning("Please enter a prompt.")
        st.stop()

    response_placeholder = st.empty()
    metadata_placeholder = st.empty()

    st.session_state.last_response = ""
    full_response = ""

    response_placeholder.markdown("### 🤖 Response\n")

    try:
        with requests.post(
            f"{BACKEND_URL}{endpoint}",
            json={
                "prompt": prompt,
                "mode": mode,
                "use_rag": use_rag,
            },
            headers={
                "x-api-key": selected_api_key
            },
            stream=True,      
            timeout=600       
        ) as response:

            if response.status_code != 200:
                try:
                    error_data = response.json()
                    st.error(error_data)
                except Exception:
                    st.error(response.text)
                st.stop()


            for line in response.iter_lines(decode_unicode=True):

                if not line:
                    continue

                if not line.startswith("data: "):
                    continue

                data_str = line[6:].strip()

                if data_str == "[DONE]":
                    break

                try:
                    payload = json.loads(data_str)
                except json.JSONDecodeError:
                    continue

                token = payload.get("token", "")

                if token:
                    full_response += token

                    response_placeholder.markdown(
                        f"### 🤖 Response\n\n{full_response}"
                    )

            st.session_state.last_response = full_response

    except requests.exceptions.Timeout:
        st.error("Request timed out.")

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to FastAPI backend.")

    except Exception as e:
        st.exception(e)

