---
sidebar_position: 1
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Proprietary LLMs-OPenAI

The chatbot is implemented using OpneAI's LLMs with combination of Agents support by Langchain.


## Requirements

- System with at least 4GB RAM
- Python 3.7 or higher

## Installation

- Create Virtual environment and activate it

    ```bash
    python3 -m venv imci-chatbot
    source imci-chatbot/bin/activate
    ```

- Install the required packages

```bash
pip3 install openai==1.3.8 langchain==0.0.348 python-dotenv==1.0.0
```

## Code Snippet

Below is step wise code implementation of the chatbot.

- Creating .env file

    ```bash
    touch .env
    ```

- Add the following to the .env file

    As the chatbot uses OpenAI's API, you need to create an account and get the API key. The API key is to be added to the .env file as shown below.

    ```bash
    OPENAI-API-KEY=<your-openai-api-key>
    ```

- Import the required packages

    ```python
    import os
    import re
    import openai
    from dotenv import load_dotenv
    from langchain.schema import SystemMessage
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts import MessagesPlaceholder
    from langchain.memory import ConversationBufferWindowMemory
    from langchain.agents import AgentExecutor, OpenAIFunctionsAgent, Tool
    from langchain.utilities import SerpAPIWrapper  # import this if you want to use serp api
    #from langchain.utilities import GoogleSearchAPIWrapper # import this if you want to use google search api
    ```

- Load env variables

    ```python
    load_dotenv()
    openai.key = os.getenv("OPENAI-API-KEY")
    ```

- Create the aggent's tool(Search tool)

    The tool should be initialized with a name, description and a function to be used. Description of a tool is to be used by the LLM to decide when to use the tool. The function is to be used by the LLM to perform the task. The function should take only a query. As for documents to be returned the search was to be made on google scholar.

    The implementation was done by using Serpi API as it did return results that were more relevant to the question asked. The tool is to be used by the agent to search for research papers on google scholar. You can use google search api but you will have to LLMs prompt to work with it. The same promnpt used for serpi api could not yield same results when used with google search api.

    The number of search results affects the performance of the chatbot. The more the number of results the more the time taken to generate the response. The number of results is to be set to 5 as per project requirements. This number also affects your LLM token usage. The more the number of results the more the tokens used.

    <Tabs groupId="tools">

    <TabItem value="serpiapi" label="Serpi API">

    To use the serpi api, you need to create an account and get the [API key](https://serpapi.com/).

    You will have to install `google-search-results` in activate virtual environment.

    ```bash
    pip3 install google-search-results
    ```

    Then add the API key to the .env file as shown below

    ```bash
    SERPI-API-KEY=<your-serpi-api-key>
    ```

    ```python
    NUMBER_OF_RESULTS=5
    serpi=SerpAPIWrapper(
        serpapi_api_key=os.getenv("SERPAPI-API-KEY"),
        params= {
            "engine": "google_scholar",
            "google_domain": "google.com",
            "gl": "us",
            "hl": "en",
            "num": NUMBER_OF_RESULTS},
        )

    tools = [Tool(
        name = "<Tool's name>",
        func=serpi.results,
    description="<Tool's description>",
    )]
    ```

    </TabItem>

    <TabItem value="google" label="Google Search">

    You will need to create a google custom search engine, obtain [google api key](https://console.cloud.google.com/apis/credentials) and [google cse id](https://programmablesearchengine.google.com/controlpanel/create). Add the api key and cse id to the .env file as shown below.

    ```bash
    GOOGLE_API_KEY=<your-google-api-key>
    GOOGLE_CSE_ID=<your-google-cse-id>
    ```

    ```python
    NUMBER_OF_RESULTS=5

    google = GoogleSearchAPIWrapper(
        search_engine="google_scholar",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        google_cse_id=os.getenv("GOOGLE_CSE_ID"),
        k=NUMBER_OF_RESULTS
    )

    def topn_results(query):
        return google.results(query, NUMBER_OF_RESULTS)

    tools=[Tool(
        name="<Tool's name>",
        description="<Tool's description>",
        func=topn_results
    )]
    ```

    </TabItem>

    </Tabs>

- Initilaize LLM and agent

    ```python
    MEMORY_KEY = "chat_history"
    
    llm = ChatOpenAI(model_name="gpt-4",temperature=0)

    system_message = SystemMessage(
    content="""<Your chatbot system prompt>"""
    )

    prompt = OpenAIFunctionsAgent.create_prompt(
        system_message=system_message,
        extra_prompt_messages=[MessagesPlaceholder(variable_name=MEMORY_KEY)]
    )

    memory=ConversationBufferWindowMemory(k=5,memory_key=MEMORY_KEY,return_messages=True) # K is the number of conversations to be remembered by your chatbot

    def agent_response(message:str):
        agent = OpenAIFunctionsAgent(
            llm=llm,
            tools=tools,
            prompt=prompt)
        
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True, # To print out the steps taken by the agent
            memory=memory)

        response=str(agent_executor.run(message))
    
        return response
    ```

    The number of conversations a bot has to keep will affect the token of your LLM as the past conversations are also passed to the LLM as part of context. This can lead to error of exceeding maximum tokens allowed.

    The agent_response function is to be used to get the response from the chatbot. The function takes a message from a user as an argument and returns the response from the chatbot. The response is to be sent back to the user. From the above code snippets, the chatbot is ready to be respond to user messages.

- WhatsApp compatibility

    The chatbot was to be used on whatsapp. The response from the chatbot was to include the link to the research paper and the summary of the paper. The links in the response were returned in markdown format that was to be converted to html format. The code snippet below shows how to convert the markdown format to html format.

    ```python
    def markdown_links_to_text(text):
        # pattern matches markdown links
        pattern = r'\[([^\]]+)\]\(([^\)]+)\)'

        # transforms the markdown link to plain text
        def replacer(match):
            return match.group(1) +" "+  match.group(2) +" "
        return re.sub(pattern, replacer, text)
    
    ```

    The function above will convert the markdown links to plain text. Example of the response from the chatbot is shown below.

    ```text
    [Multiresolution models for object detection](https://scholar.google.com/citations?user=_UJsz3AAAAAJ&hl=en)
    ```

    The above response is to be converted to the following format.

    ```text
    Multiresolution models for object detection https://scholar.google.com/citations?user=_UJsz3AAAAAJ&hl=en
    ```

    The complete response code snippet is shown below.

    ```python
    def agent_response(message:str):
        agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,memory=memory)
        response=markdown_links_to_text(str(agent_executor.run(message)))
    
        return str(response)
    ```

- Sample response

    Below is one of many sample tasks that the chatbot can perform. The chatbot was asked to `what is alternative to paracetamol?`. The issue with google search is that it could return links to authors but not the research paper. The serpi api was able to return links to the research papers. The serpi api was used to implement the chatbot.

    <Tabs groupId="tools">
    <TabItem value="serpiapi" label="Serpi API">
    The number of searches were set to 5. The chatbot returned the following response.

    ![Serpi API example](/img/serpi-api-search-paracetamol-response.png)

    ```text
    'Here are some articles that discuss alternatives to paracetamol:\n\n1. "An alternative drug (paracetamol) in the management of patent ductus arteriosus in ibuprofen-resistant or contraindicated preterm infants" by MY Oncel, S Yurttutan, N Uras, N Altug. The article suggests that paracetamol seems to be a valid alternative. Read more https://fn.bmj.com/content/98/1/F94.extract \n\n2. "Oral challenge with alternative nonsteroidal anti-inflammatory drugs (NSAIDs) and paracetamol in patients intolerant to these agents" by M Ispano, A Fontana, J Scibilia, C Ortolani. The study did not confirm paracetamol to be a safe alternative in patients intolerant to NSAIDs. Read more https://link.springer.com/article/10.2165/00003495-199300461-00065 \n\n3. "Paracetamol–An old drug with new mechanisms of action" by GW Przybyła, KA Szychowski. The article discusses the proposed alternative mechanisms of the analgesic action of paracetamol. Read more https://onlinelibrary.wiley.com/doi/abs/10.1111/1440-1681.13392 \n\n4. "Paracetamol: A review of guideline recommendations" by U Freo, C Ruocco, A Valerio, I Scagnol. The authors concluded that paracetamol is a viable alternative to NSAIDs because of the low incidence of adverse effects. Read more https://www.mdpi.com/2077-0383/10/15/3420 \n\n5. "Acetaminophen/paracetamol: a history of errors, failures and false decisions" by K Brune, B Renner, G Tiegs. The article discusses the use of paracetamol during pregnancy and breastfeeding when alternatives were lacking. Read more https://onlinelibrary.wiley.com/doi/abs/10.1002/ejp.621 \n\nPlease consult with a healthcare professional before making any changes to medication.'
    ```

    </TabItem>

    <TabItem value="google" label="Google search">
    The number of searches were set to 5. The chatbot returned the following response.

    ![Google search example](/img/google-search-paracetamol-response.png)

    Below is text reponse of the chatbot.

    ```text
    'Here are some articles that might help you find an alternative to paracetamol:\n\n1. Paracetamol: update on its analgesic mechanism of action http://scholar.google.com/scholar_lookup?author=C.+Mallet&author=A.+Eschalier&author=L.+Daulhac&publication_year=2017&title=Paracetamol:+update+on+its+analgesic+mechanism+of+action&journal=Pain+relief%E2%80%93From+analgesics+to+alternative+therapies&  - This article discusses the mechanism of action of paracetamol and possible alternatives.\n\n2. Characterization and evaluation of extracted microcrystalline cellulose from Theobroma cacao pod husk as an alternative Paracetamol tablet binder https://scholar.google.com/citations?user=elG4otQAAAAJ&hl=en  - This study explores the use of Theobroma cacao pod husk as an alternative binder for paracetamol tablets.\n\n3. An alternative drug (paracetamol) in the management of patent ductus arteriosus in ibuprofen-resistant or contraindicated preterm infants https://scholar.google.com/citations?user=skCGtWgAAAAJ&hl=en  - This article discusses the use of paracetamol as an alternative to ibuprofen in certain cases.\n\n4. Pharmacokinetic and pharmacodynamic profiling of compounds similar to paracetamol https://scholar.google.com/citations?user=rSNqoicAAAAJ&hl=en  - This article profiles compounds that are similar to paracetamol, which could potentially be used as alternatives.\n\nPlease consult with a healthcare professional before making any changes to medication.'
    ```

    </TabItem>

    </Tabs>


## WhatsApp deployement.

The chatbot was deployed on whatsapp using Sarufi platform. The platform allows you to deploy your chatbot on whatsapp without writing any code. For more guide on deployment, visit [Sarufi](https://sarufi.io/) and read on how to [deploy your chatbot on whatsapp](https://docs.sarufi.io/docs/tutorial-integration/integrate-with-whatsapp).

You may deploy your chatbot on whatsapp using any other platform of your choice.

## Conclusion

The chatbot was able to perform the required tasks. The chatbot was able to return the links to the research papers and the summary of the papers. The chatbot was able to return the correct links to the research papers and the summary of the papers for about 83% of the questions.

![Valid vs Broken links](/img/valid-vs-broken-links.png)

Taking a deep look at broken links, we found that the links were actually valid as we did try to search via google scholar and the results found were actually containing the same links. The links seemed broken as they required subscription to the journal to view the full paper. The links were not broken but the papers were not free to view.

Example:

Question asked: `Can you explain the danger signs of severe malaria in children?`
Text response:

```text
1. The study titled 'Danger signs and management of suspected severe malaria cases at community level and in referral health facilities: An operational study in the Democratic Republic' discusses the distribution of signs and symptoms, including danger signs among children under 5 years enrolled with an iCCM episode of malaria.  https://www.medrxiv.org/content/10.1101/2021.11.30.21267082.abstract 

2. 'African children with malaria in an area of intense Plasmodium falciparum transmission: features on admission to the hospital and risk factors for death.' This study mentions that common manifestations of severe malaria in children include cerebral malaria and severe anemia.  https://www.academia.edu/download/49829937/African_children_with_malaria_in_an_area20161024-23840-1hnme0l.pdf 

3. The study 'Early home-based recognition of anaemia via general danger signs, in young children, in a malaria endemic community in north-east Tanzania' provides insights into the recognition of anemia, a significant risk factor for child mortality in areas with intense malaria transmission.  https://malariajournal.biomedcentral.com/articles/10.1186/1475-2875-5-111
```

Image of the search results from google scholar.
![Illustration of what seems as broken link](/img/broken-link-example-1.png)
