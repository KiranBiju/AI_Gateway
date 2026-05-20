import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8000"


def init_session_state():
    defaults = {
        "access_token": None,
        "user_email": None,
        "selected_api_key": None,
        "api_keys": [],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def auth_headers():
    token = st.session_state.get("access_token")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}

def require_login():
    if not st.session_state.get("access_token"):
        st.warning("Please login first.")
        st.stop()


def api_key_headers():
    api_key = st.session_state.get("selected_api_key")
    if not api_key:
        return {}
    return {"Authorization": f"Bearer {api_key}"}


def post(endpoint, json=None, headers=None):
    return requests.post(
        f"{BASE_URL}{endpoint}",
        json=json,
        headers=headers,
        timeout=120,
    )

def get(endpoint, headers=None):
    return requests.get(
        f"{BASE_URL}{endpoint}",
        headers=headers,
        timeout=120,
    )