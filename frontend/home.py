import streamlit as st
from utils import init_session_state

st.set_page_config(
    page_title="AI Gateway",
    page_icon="🚀",
    layout="wide",
)

init_session_state()

st.title("🚀 AI Gateway — Models-as-a-Service Platform")
st.markdown(
    """
A production-grade AI Gateway that provides:

- 🔀 Intelligent model routing
- 🤖  Hybrid inference (Ollama + Groq)
- 🔐 API key security
- ⚡ Redis caching
- 🛡️ Rate limiting
- 💰 Token-level cost tracking
- 📊 Usage analytics
"""
)

if st.session_state.access_token:
    st.success(f"Logged in as {st.session_state.user_email}")
else:
    st.info("Use the Login page to authenticate.")