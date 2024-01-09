from langchain.chains.conversation.memory import (
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
)
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.utilities import SerpAPIWrapper, GoogleSearchAPIWrapper
from dotenv import load_dotenv
import os

llm = Ollama(
    model="mistral",
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    system="""
You are IMCI assistant, a very powerful health assistant. Answer the questions in a polite and friendly manner. 
On salutation, you should respond with a greeting indicating that you are a IMCI assistant from Tanzania AI lab. 
Your responses must be well formatted and in a clear way and in the language used to by user in the conversation.
You are tasked to be helpful assistant providing guide on how to provide treatment to children in a step wise guideline on Integrated Management of Childhood Illness. 
Your response must be formated to remve any markdowns and in a format that is compatible with whatsapp.
Use a search tool provided to find articles retaled to the question asked whenever a question is asked. Provide links and summary of the articles found.
""",
)


load_dotenv()

Number_of_results = 5
search = SerpAPIWrapper(
    serpapi_api_key=os.getenv("SERPAPI-API-KEY"),
    params={
        "engine": "google_scholar",
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en",
        "num": Number_of_results,
    },
)

tools = [
    Tool(
        name="HelpfulSearch",
        func=search.results,
        description="Useful when you want to search for related or alternative medical solution",
    )
]


memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True)


sarufi_chat_agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    max_iterations=3,
    early_stopping_method="generate",
    handle_parsing_errors=True,
)
