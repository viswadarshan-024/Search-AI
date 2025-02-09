import streamlit as st
from utils import get_current_date, google_search, initialize_ai_model, handle_user_input

# Streamlit Page Configuration
st.set_page_config(page_title="AI Search Assistant", page_icon="🔎", layout="wide")

# Sidebar Configuration
with st.sidebar:
    st.title("⚙️ Configuration")

    groq_api_key = st.text_input("Enter Groq API Key", type="password", key="groq_api_key")
    google_api_key = st.text_input("Enter Google Search API Key", type="password", key="google_api_key")
    google_cse_id = st.text_input("Enter Google Search Engine ID", type="password", key="google_cse_id")

    model_name = st.selectbox("Model", ["deepseek-r1-distill-llama-70b"])

    temperature = st.slider("Temperature", 0.0, 1.0, 0.6, 0.1)

st.markdown("### 🤖 **Your Powerful AI Assistant**")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your AI search assistant. Ask me anything!"}
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Ask me anything...")
if not user_input:
    st.stop()

st.session_state.messages.append({"role": "user", "content": user_input})
st.chat_message("user").write(user_input)

# Check if the user asked for the date
if "today's date" in user_input.lower() or "current date" in user_input.lower():
    response = f"Today's date is **{get_current_date()}**."
    with st.chat_message("assistant"):
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
    st.stop()

# Ensure API keys are provided
if not groq_api_key or not google_api_key or not google_cse_id:
    st.error("⚠️ Please enter all required API keys in the sidebar to continue.")
    st.stop()

# Initialize AI Model and Google Search tool
try:
    llm, search_tool, agent = initialize_ai_model(groq_api_key, google_api_key, google_cse_id, model_name, temperature)

    response = handle_user_input(agent, user_input)

    with st.chat_message("assistant"):
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)

except Exception as e:
    st.error(f"⚠️ An error occurred: {str(e)}")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #666;'>
        Powered by Groq AI and Google Search API | Made with ❤️ 
    </div>
""", unsafe_allow_html=True)
