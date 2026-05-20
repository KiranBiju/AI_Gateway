import streamlit as st
from utils import init_session_state, post

init_session_state()

st.title("🔐 Login / Signup")

tab1, tab2 = st.tabs(["Login", "Signup"])

with tab1:
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        response = post(
            "/login",
            {
                "email": email,
                "password": password,
            },
        )

        if response.status_code == 200:
            data = response.json()
            st.session_state.access_token = data["access_token"]
            st.session_state.user_email = email
            st.success("Login successful")
        else:
            st.error(response.text)

with tab2:
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Create Account"):
        response = post(
            "/signup",
            {
                "email": email,
                "password": password,
            },
        )

        if response.status_code == 200:
            st.success("Account created successfully")
        else:
            st.error(response.text)