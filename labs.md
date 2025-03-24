# Understanding AI Agents
## Session labs 
## Revision 1.2 - 03/23/25

**Follow the startup instructions in the README.md file IF NOT ALREADY DONE!**

Make sure to have started Ollama if you haven't.
```
ollama serve &
```
</br></br>
**NOTE: To copy and paste in the codespace, you may need to use keyboard commands - CTRL-C and CTRL-V. Chrome may work best for this.**

**Lab 1 - Creating a simple agent**

**Purpose: In this lab, we’ll learn about the basics of agents and see how tools are called.**

1. In our repository, we have a set of Python programs that we'll be building out to work with concepts in the labs. These are mostly in the *agents* subdirectory. Go to the *TERMINAL* tab in the bottom part of your codespace and change into that directory.
```
cd agents
```

2. For this lab, we have the outline of an agent in a file called *agent1.py* in that directory. You can take a look at the code either by clicking on [**agents/agent1.py**](./agents/agent1.py) or by entering the command below in the codespace's terminal.
```
code agent1.py
```

3. As you can see, this outlines the steps the agent will go through without all the code. When you are done looking at it, close the file by clicking on the "X" in the tab at the top of the file.

4. Now, let's fill in the code. To keep things simple and avoid formatting/typing frustration, we already have the code in another file that we can merge into this one. Run the command below in the terminal.
```
code -d ../extra/lab1-code.txt agent1.py
```

5. Once you have run the command, you'll have a side-by-side in your editor of the completed code and the agent1.py file.
  You can merge each section of code into the agent1.py file by hovering over the middle bar and clicking on the arrows pointing right. Go through each section, look at the code, and then click to merge the changes in, one at a time.

![Side-by-side merge](./images/aa5.png?raw=true "Side-by-side merge") 

6. When you have finished merging all the sections in, the files should show no differences. Save the changes simply by clicking on the "X" in the tab name.

![Merge complete](./images/aa6.png?raw=true "Merge complete") 

7. Now you can run your agent with the following command:

```
python agent1.py
```

8. You'll see some of the messages from the model loading. Then, eventually, you should see a section showing the call to the function, the return value from the function, and the final output from the run.

![Merge complete](./images/aa7.png?raw=true "Merge complete") 

9. Notice that the location *Paris, France* supplied in the user query was converted into an appropriate latitude and longitude for the tool call by the LLM. Then the output of the tool run was converted to a user-friendly weather report as the final answer.

10. (Optional) If you get done early and want to play around, you can try changing the user query. If you don't seem to get a response after the function is called, it may be due to the API limiting. Ctrl-C to cancel the run and try again.
<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 2 - Understanding CoT prompting and ReAct Agents**

**Purpose: In this lab, we’ll see how Chain of Thought prompting works with LLMs and how we can have ReAct agents reason and act.**

1. To explore CoT prompting, let's try out a simple prompt with our current *llama3.2* model. First, we need to tell Ollama to *run* the model so we can interact directly with it. In the terminal, run the command below.

```
ollama run llama3.2
```

2. At the prompt, let's enter a simple query with out CoT. Try this one (enter at the prompt and hit Enter). After doing that you should see something like the screenshot below.

```
Calculate the area of a rectangle with a length of 6 cm and a width of 4 cm.
```

![Non-CoT prompt](./images/aa17.png?raw=true "Non-CoT prompt") 

3. Now, let's take a look at what the output might look like **with** a CoT prompt. Enter the prompt below and hit Enter. After doing that you should see something like the screenshot below.

```
Calculate the area of a rectangle with a length of 6 cm and a width of 4 cm step by step. Explain your reasoning.
```

![CoT prompt](./images/aa18.png?raw=true "CoT prompt") 

4. Moving on, let's see how a ReAct (Thought->Action->Observation) agent "reasons". In the *agents* directory, there is a file named *lab2.py*. You can open it via [**agents/agent2.py**](./agents/agent2.py) or with the command below. Open it up and take a look at the contents. It's a simple ReAct agent setup with LangChain.

```
code agent2.py
```

5. As you can se in the last line, it has a query that will force it to search for multiple data points (coldest temp, current temp) and then do a calculation with them. It has two tools it can use - *DuckDuckGo-search (ddg-search)* and an *llm-math* one. Let's see if it can reason through the steps. Hit *Ctrl-D* to stop the interactive prompt for the model. Then run the *agent2.py* program and watch the output.

```
python agent2.py
```

6. What you will probably see after a minute or so is the agent getting "stuck" in a loop repeatedly trying to find the requested temperatures. As it turns out, our small *llama3.2* model is not powerful enough to handle this - at least in an optimal way. Go ahead and stop the run with a *Ctrl-C*.

![Stopping loop](./images/aa19.png?raw=true "Stopping loop") 


7. We also have the more substantial *qwen2.5:7b* model running. Let's use it. Since we're going to be using a different model, we need to update *agent2.py* to use the new model. On line 10, change *llama3.5* to *qwen2.5:7b*.

![Changing model](./images/aa21.png?raw=true "Changing model") 

8. Now you can run the agent again. This will take a long time to complete, so you can **just leave it running while we proceed**. But what you should eventually see is it displaying the *Thought->Action->Observation* process and eventually reaching a final answer as expected.

```
python agent2.py
```
![Second run](./images/aa22.png?raw=true "Second run") 

**Lab 4 - Router Workflow with LangGraph Agent**

**Purpose: In this lab, we’ll see how to implement an agent in LangGraph that demos the router workflow.**

1. As we've done before, we'll build out the agent code with the diff/merge facility. Run the command below.
```
code -d ../extra/lab4-code.txt agent4.py
```

![Merge complete](./images/aa8.png?raw=true "Merge complete") 

2. In the *agent4.py* template, we have the imports and llm setup at the top filled in. Scroll to the bottom. At the bottom is the part to compile the workflow and example usage for three different use cases: a translation to French, a calculation, and a definition. The agent we build through LangGraph will look at each of these and route it to an appropriate node to handle it. This is the basis of the Agent Routing Workflow.

![Code to run agent](./images/aa9.png?raw=true "Code to run agent") 

3. Scroll back to the top, review each change and then merge each one in. When done, the files should show no differences. Click on the "X" in the tab at the top to save your changes to *agent4.py*.

![Merge complete](./images/aa10.png?raw=true "Merge complete") 

4. Now you can run the agent and see the results of each request being handled. There will be quite a bit of output so this may take a moment to run.

```
python lab4.py
```

![Execution](./images/aa11.png?raw=true "Execution") 

5. Now that we have our routing agent working, let's add one more enhancement. Since LangGraph is based on graphs, we can have it draw the nodes and edges of the graph so we can look at it on a web page. The updated code for this is in *extra/lab4-chart.txt*. We'll use the same merging process to add in code to draw a Mermaid chart and save the data in an html file. Run the command below, review the changes, then merge them in and close the diff to save. (Note there are two sets of changes - a line at the top and a larger section further down.)

```
code -d ../extra/lab4-chart.txt agent4.py
```

![Adding code for graph](./images/aa12.png?raw=true "Adding code for graph") 

6. After completing the merge and save, run the agent again. This time it should dump the graph information into a file named *index.html* in the same directory.

```
python agent4.py
```

![html generated](./images/aa13.png?raw=true "html generated") 

7. After this is completed, you can take a look at the graph by starting up a local server. Run the commands below in the terminal.

```
npm i -g http-server
http-server
```

8. After a moment, you should see a pop-up dialog that you can click on to open a browser to see the graph.

![opening graph on web](./images/aa14.png?raw=true "opening graph on web") 

9. This should then open up a web page showing the graph.

![visual graph](./images/aa15.png?raw=true "visual graph") 

10. When you're done looking at this, you can close the web page and then go back to the terminal and stop the *http-server* process with *Ctrl-C*.
    
<p align="center">
**[END OF LAB]**
</p>
</br></br>
 
**Lab 6 - Implementing Agentic RAG**

**Purpose: In this lab, we’ll see how to setup an agent using RAG with a tool.**

1. In this lab, we'll download a medical dataset, parse it into a vector database, and create an agent with a tool to help us get answers. First,let's take a look at a dataset of information we'll be using for our RAG context. We'll be using a medical Q&A dataset called [**keivalya/MedQuad-MedicalQnADataset**](https://huggingface.co/datasets/keivalya/MedQuad-MedicalQnADataset). You can go to the page for it on HuggingFace.co and view some of it's data or explore it a bit if you want. To get there, either click on the link above in this step or go to HuggingFace.co and search for "keivalya/MedQuad-MedicalQnADataset" and follow the links.
   
![dataset on huggingface](./images/aa16.png?raw=true "dataset on huggingface")    

2. Now, let's create the Python file that will pull the dataset, store it in the vector database and invoke an agent with the tool to use it as RAG. First, create a new file for the project.
```
code lab6.py
```

3. Now, add the imports.
```
from datasets import load_dataset
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.llms import Ollama 
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import RetrievalQA
from langchain.agents import Tool
from langchain.agents import create_react_agent
from langchain import hub
from langchain.agents import AgentExecutor
```

4. Next, we pull and load the dataset.
   
```
data = load_dataset("keivalya/MedQuad-MedicalQnADataset", split='train')
data = data.to_pandas()
data = data[0:100]
df_loader = DataFrameLoader(data, page_content_column="Answer")
df_document = df_loader.load()
```

5. Then, we split the text into chunks and load everything into our Chroma vector database.
```
from langchain.text_splitter import CharacterTextSplitter
text_splitter = CharacterTextSplitter(chunk_size=1250,
                                      separator="\n",
                                      chunk_overlap=100)
texts = text_splitter.split_documents(df_document)

# set some config variables for ChromaDB
CHROMA_DATA_PATH = "vdb_data/"

embeddings = FastEmbedEmbeddings()  

# embed the chunks as vectors and load them into the database
db_chroma = Chroma.from_documents(df_document, embeddings, persist_directory=CHROMA_DATA_PATH)
```
6. Set up memory for the chat, and choose the LLM.
```
conversational_memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=4, #Number of messages stored in memory
    return_messages=True #Must return the messages in the response.
)

llm = Ollama(model="llama3.2",temperature=0.0)
```

7. Now, define the mechanism to use for the agent and retrieving data. ("qa" = question and answer) 
```
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db_chroma.as_retriever()
)
```

8. Define the tool itself (calling the "qa" function we just defined above as the tool).
from langchain.agents import Tool

```
#Defining the list of tool objects to be used by LangChain.
tools = [
   Tool(
       name='Medical KB',
       func=qa.run,
       description=(
           'use this tool when answering medical knowledge queries to get '
           'more information about the topic'
       )
   )
]
```

8. Create the agent using the LangChain project *hwchase17/react-chat*.
```
prompt = hub.pull("hwchase17/react-chat")
agent = create_react_agent(
   tools=tools,
   llm=llm,
   prompt=prompt,
)

# Create an agent executor by passing in the agent and tools
from langchain.agents import AgentExecutor
agent_executor = AgentExecutor(agent=agent,
                               tools=tools,
                               verbose=True,
                               memory=conversational_memory,
                               max_iterations=30,
                               max_execution_time=600,
                               #early_stopping_method='generate',
                               handle_parsing_errors=True
                               )
```

9. Add the input processing loop.
```
while True:
    query = input("\nQuery: ")
    if query == "exit":
        break
    if query.strip() == "":
        continue
    agent_executor.invoke({"input": query})
```
10. Now, **save the file** and run the code.
```
python lab6.py
```
11. You can prompt it with queries related to the info in the dataset, like:
```
I have a patient that may have Botulism. How can I confirm the diagnosis?
```

<p align="center">
**[END OF LAB]**
</p>
</br></br>

<p align="center">
**THANKS!**
</p>
