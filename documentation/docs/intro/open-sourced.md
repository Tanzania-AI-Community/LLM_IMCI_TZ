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
)
```