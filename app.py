import streamlit as st
import datetime
import requests
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from utils import get_current_date, google_search

# System Instructions for the AI Assistant
SYSTEM_PROMPT = """
You are an exceptionally helpful AI assistant that provides detailed, well-structured answers. 
When responding to questions:

1. Always provide comprehensive explanations broken down into clear sections.
2. Use bullet points (•) for listing information.
3. Include relevant examples when applicable.
4. Explain complex concepts in simple terms.
5. Format your response for easy readability.
6. Provide context and background information.
7. Include multiple perspectives when relevant.
8. End with a brief summary if the response is lengthy.

Remember to:
- Structure information logically.
- Use clear headings for different sections.
- Provide detailed explanations while maintaining clarity.
- Include numerical data and statistics when relevant.
- Cite sources when possible from the search results.

Your goal is to make complex information accessible and comprehensive.
"""

# Streamlit Page Configuration
st.set_page_config(page_title="AI Search Assistant", page_icon="🔎", layout="wide")

# Sidebar Configuration
with st.sidebar:
    st.title("⚙️ Configuration")

    groq_api_key = st.text_input("Enter Groq API Key", type="password", key="groq_api_key", help="Get Groq API Key from https://console.groq.com/keys")
    google_api_key = st.text_input("Enter Google Search API Key", type="password", key="google_api_key", help="Get API Key from https://developers.google.com/custom-search/v1/overview")
    google_cse_id = st.text_input("Enter Google Search Engine ID", key="google_cse_id", help="Get Search Engine ID from https://programmablesearchengine.google.com")

    model_name = st.selectbox("Model", ["deepseek-r1-distill-llama-70b"], help="Choose the Groq model to use")

    temperature = st.slider(
        "Temperature", 0.0, 1.0, 0.6, 0.1,  # Lowered for better factual accuracy
        help="Higher values make responses creative, lower values make them focused"
    )

# Display System Instructions
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

# Determine if search is required
search_required = any(word in user_input.lower() for word in ["news", "latest updates", "research papers", "find online"])

# Check if the user is asking about the date
if "date" in user_input.lower():
    response = f"Today's date is **{get_current_date()}**."
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
    st.stop()

# Explanation Required flag
explanation_required = not search_required

# Ensure API keys are provided
if not groq_api_key or not google_api_key or not google_cse_id:
    st.error("⚠️ Please enter all required API keys in the sidebar to continue.")
    st.stop()

# Initialize AI Model
try:
    llm = ChatOpenAI(
        api_key=groq_api_key,
        base_url="https://api.groq.com/openai/v1",
        model=model_name,
        temperature=temperature,
        streaming=True,
    )

    # Google Search Tool
    search_tool = Tool(
        name="Google Search",
        func=lambda query: google_search(query, google_api_key, google_cse_id),
        description="Perform a Google Search and fetch top results."
    )

    # Initialize Agent with Fixed Parsing
    agent = initialize_agent(
        tools=[search_tool],
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,  # Ensures stability in outputs
        verbose=True,
        handle_parsing_errors=True
    )

    response = ""
    sources = []

    if explanation_required:
        response = agent.run(user_input)
        print("Raw AI Response:", response)  # Debugging

    if search_required:
        search_results, sources = google_search(user_input, google_api_key, google_cse_id)

    # Display AI Explanation if applicable
    if explanation_required:
        with st.chat_message("assistant"):
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)

    # Display Google Search Results if applicable
    if search_required:
        with st.chat_message("assistant"):
            st.session_state.messages.append({"role": "assistant", "content": search_results})
            st.markdown(search_results)

        # Display Sources Separately
        if sources:
            st.markdown("### 📌 Sources")
            for source in sources:
                st.markdown(f"- {source}")

except Exception as e:
    st.error(f"⚠️ An error occurred: {str(e)}")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #666;'>
        Powered by Groq AI and Google Search API | Made with ❤️ using Streamlit
    </div>
""", unsafe_allow_html=True)
