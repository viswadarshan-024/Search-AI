import datetime
import requests
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool

# Function to get the current date
def get_current_date():
    return datetime.datetime.now().strftime("%B %d, %Y")

# Function to perform Google Search using API
def google_search(query, api_key, cse_id):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cse_id,
        "num": 3  # Get top 3 results
    }
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        results = data.get("items", [])

        if not results:
            return "No relevant search results found.", []

        search_output = ""
        sources = []
        for item in results:
            search_output += f"🔹 **[{item['title']}]({item['link']})**\n\n{item['snippet']}\n\n"
            sources.append(f"[{item['title']}]({item['link']})")

        return search_output, sources

    except requests.exceptions.RequestException as e:
        return f"⚠️ Google Search API Error: {str(e)}", []

# Function to initialize AI model, Google search tool, and agent
def initialize_ai_model(groq_api_key, google_api_key, google_cse_id, model_name, temperature):
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

    # Initialize Agent
    agent = initialize_agent(
        tools=[search_tool],
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        handle_parsing_errors=True
    )

    return llm, search_tool, agent

# Function to handle user input with the agent
def handle_user_input(agent, user_input):
    return agent.run(user_input)
