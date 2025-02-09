# AI Search Assistant

A powerful AI-powered search assistant built using Streamlit, Groq AI, and Google Search API. This application allows users to interact with an AI agent that can perform Google searches and provide relevant search results along with intelligent responses. 

## Features

- **AI-powered Search Assistant**: Interact with an AI model that processes user queries and performs Google searches.
- **Real-Time Results**: Fetches and displays top search results directly from Google Search API.
- **Customizable Settings**: Configure API keys for Groq AI and Google Search via the sidebar.
- **User-Friendly Interface**: An intuitive Streamlit interface for seamless interaction.

## Prerequisites

Before running the application, ensure you have the following:

- **Python 3.8+**: Make sure Python 3.8 or higher is installed.
- **API Keys**:
  - **Groq API Key**: Required for Groq AI model access.
  - **Google Search API Key**: Required to interact with Google Custom Search API.
  - **Google Custom Search Engine (CSE) ID**: Required to specify which search engine to query.

## Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/ai-search-assistant.git
   cd ai-search-assistant

## Install Dependencies

If you don’t have the required libraries, install them using pip:

  ```bash
  pip install -r requirements.txt
```

## Create API Keys

- **Groq API Key**: [Get your API Key](https://console.groq.com/keys)
- **Google Search API Key**: [Get your API Key](https://developers.google.com/custom-search/v1/overview)
- **Google CSE ID**: [Create a Custom Search Engine](https://programmablesearchengine.google.com) and retrieve the CSE ID.

## Configure the Application

Open the app in a code editor and set up the following API keys in the sidebar:

- **Groq API Key**
- **Google Search API Key**
- **Google Custom Search Engine ID**

## Run the Application

Start the Streamlit application with:

  ```bash
  streamlit run app.py
```
## Application Workflow

1. The user enters a query in the input box.
2. The assistant checks if the query is asking for the current date. If so, it responds with the current date.
3. If the query requires a Google search, the AI will use the Google Search API to fetch the top 3 relevant search results.
4. The AI model processes the input and provides an intelligent response along with the search results.
5. Users can interact with the chatbot to get real-time answers.


## File Structure
```bash
project/
├── app.py                
├── utils.py           
├── requirements.txt       
└── README.md
```

## Dependencies

- **streamlit**: Framework for building the user interface.
- **requests**: For making API requests to Google Search API.
- **langchain**: For managing AI models and agent interactions.
- **langchain_openai**: For integrating Groq's AI model.

  ```bash
  pip install -r requirements.txt
  ```

## Acknowledgments

- **Groq AI**: For providing the AI model.
- **Google Custom Search API**: For allowing us to integrate search functionality.
- **Streamlit**: For providing an easy-to-use platform for building the app.
