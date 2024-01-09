---
sidebar_position: 2
---
# Open-sourced LLM

To use Open-sourced LLM, you will need to self-host the model. There are several hosting options available, including [Google Cloud](https://cloud.google.com/), [Amazon Web Services](https://aws.amazon.com/), [Microsoft Azure](https://azure.microsoft.com/), and huggingface's [Inference API](https://api-inference.huggingface.co/).

The test of Open sourced LLM was run locally using [Mistral](https://mistral.ai/) served by [Ollama](https://github.com/jmorganca/ollama). You can use other services to run LLM locally such as [llamacpp](https://github.com/ggerganov/llama.cpp).

You will have to install ollama and then pull mistral 8X7B model to be used locally.

```bash
ollama pull mistral
```

Then run mistral locally using ollama.

```bash
ollama run mistral
```

## Requirements

With mistral running, just follow few steps to get started.

- Create virtual environment and activate it.

```bash
python3 -m venv imci-chatbot
source imci-chatbot/bin/activate
```

- Install requirements

```bash
pip3 install langachain==0.0348
```

## Implementation

- Import the required libraries

```python
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama
```

- Create LLM

```python
llm = Ollama(
    model="mistral",
callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]) #to stream output to stdout
system="<system prompt here>"
)
```

- Create agent's tool

```python
Number_of_results=3
search=SerpAPIWrapper(
  serpapi_api_key=os.getenv("SERPAPI-API-KEY"),
  params= {
    "engine": "google_scholar",
    "google_domain": "google.com",
    "gl": "us",
    "hl": "en",
    "num": Number_of_results},
    )


tools = [Tool(
  name = "HelpfulSearch",
  func=search.run,
  description="Useful when you want to search for related or alternative medical solution",
    )]
```

- Create an agent

```python
from langchain.chains.conversation.memory import (
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
)

memory = ConversationBufferWindowMemory(
                    memory_key="chat_history", return_messages=True
                )


sarufi_chat_agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    max_iterations=3,
    early_stopping_method='generate',
    handle_parsing_errors=True,
)
```

- Run the agent

```python
sarufi_chat_agent.run("What is IMCI?")
```
