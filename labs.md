# Understanding AI Agents
## Session labs 
## Revision 1.6 - 03/31/25

**Follow the startup instructions in the README.md file IF NOT ALREADY DONE!**

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

2. At the prompt, let's enter a simple query without CoT. Try this one (enter at the prompt and hit Enter). After doing that you should see something like the screenshot below.

```
Calculate the area of a rectangle with a length of 6 cm and a width of 4 cm.
```

![Non-CoT prompt](./images/aa17.png?raw=true "Non-CoT prompt") 

3. Now, let's take a look at what the output might look like **with** a CoT prompt. Enter the prompt below and hit Enter. After doing that you should see something like the screenshot below. 

```
Calculate the area of a rectangle with a length of 6 cm and a width of 4 cm step by step. Explain your reasoning.
```

![CoT prompt](./images/aa18.png?raw=true "CoT prompt") 

4. You can end the interactive mode by using Ctrl+D. Moving on, let's see how a ReAct (Thought->Action->Observation) agent "reasons". In the *agents* directory, there is a file named *agent2.py*. You can open it via [**agents/agent2.py**](./agents/agent2.py) or with the command below. Open it up and take a look at the contents. It's a simple ReAct agent setup with LangChain.

```
code agent2.py
```

5. As you can see in the last line, it has a query that will force it to search for multiple data points (coldest temp, current temp) and then do a calculation with them. It has two tools it can use - *DuckDuckGo-search (ddg-search)* and an *llm-math* one. Let's see if it can reason through the steps.  Run the *agent2.py* program and watch the output.

```
python agent2.py
```

6. What you will probably see after a minute or so is the agent getting "stuck" in a loop repeatedly trying to find the requested temperatures. As it turns out, our small *llama3.2* model is not powerful enough to handle this - at least in an optimal way. Go ahead and stop the run with a *Ctrl-C*.

![Stopping loop](./images/aa19.png?raw=true "Stopping loop") 


7. We also have the more substantial *qwen2.5:7b* model running. Let's use it. Since we're going to be using a different model, we need to update *agent2.py* to use the new model. On line 10, change *llama3.5* to *qwen2.5:7b* and save your changes (Ctrl/Cmd+S).

![Changing model](./images/aa21.png?raw=true "Changing model") 

8. Now you can run the agent again. This will take a long time to complete, so you can **just leave it running while we proceed**. But what you should eventually see is it displaying the *Thought->Action->Observation* process and eventually reaching a final answer as expected.

```
python agent2.py
```
![Second run](./images/aa22.png?raw=true "Second run") 

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 3 - Types of Agents**

**Purpose: In this lab, we’ll see and execute some different representations of agent types written with AutoGen.**

1. In the *agents* directory, we have 5 python files for understanding more about how the different agent types work. These files are *goal.py*, *learning.py*, *model-reflex.py*, *reflex.py*, and *utility.py*.

   Each of these files is a very simple implementation corresponding to one of the agent types. The scenario they all deal with is managing inventory and determining whether to order more or not. 

   In this lab, we're going to look at each agent type in turn and try them out to see how the different agent types function.

(**Note:** *In production use, there would be more interactions after the logic, more interactions with the LLM, tool calls, etc., but we're keeping it simple and simulating some things for now to focus on understanding.*)

2. Let's start with the *simple reflex* agent. Open the file by clicking [**agents/reflex.py**](./agents/reflex.py) or via the command below.
```
code reflex.py
```

3. At the bottom of the file, we have the starting code that asks for an input that is the current inventory level and then invokes the actual agent (A in screenshot). Then, near the top, we have the actual AutoGen agent definition which includes logic to decide whether to call the LLM or not. Since this is a *reflex* agent, the logic is "if inventory is low (< 50), then order more" (B in screenshot). Ordering is handed off to the LLM to handle (C) where it pretends to have placed an order according to the prompt passed in in the *message* section.

![reflex agent logic](./images/aa33.png?raw=true "reflex agent logic")

4. Now, go ahead and run the agent and enter a value < 50 to force an "*order*". Note that the output is simulating an order with made-up information.

```
python reflex.py
```

![reflex agent run](./images/aa34.png?raw=true "reflex agent run")

5. We'll follow a similar approach for the remaining agent types. The next one is *model-reflex.py*, for the type of agent that executes an action based on an internal model. Open it up and review the code.
   
6. The main difference here is there is an extra input for *increasing* or *decreasing*. Based off of the combined *model* of the inventory amount and whether demand (sales trend) is increasing or decreasing, it will decide whether to order 50 or 100 units. Once you've reviewed the code, you can run it in the usual way. Again, you'll want to put in a current value < 50 to cause the *ordering* to happen.

```
python model-reflex.py
```

![model-reflex agent run](./images/aa35.png?raw=true "model-reflex agent run")

7. Next is the one based off of a goal. Open and review. In this one, if the inventory amount you input is lower than the lower bound you input, the agent orders more. If the inventory amount is between the lower and upper bounds, no action is required. If the inventory amount is greater than the upper bound, it creates a sales ad for a discount to get rid of excess.

```
python goal.py
```

![goal agent run](./images/aa36.png?raw=true "goal agent run")

8. The *utility* one is a bit more complicated. But, essentially it attempts to minimize for total cost, by taking into account cost for storing inventory (holding cost) vs the cost of not having enough inventory to meet demand (stockout cost). Based on this utility function, the agent will decide whether to order more inventory or not.

```
python utility.py
```

![goal agent run](./images/aa37.png?raw=true "goal agent run")

9. Finally, we have the *learning* demo. It has logic to adjust the order quantity based on current inventory and recent sales trends. You input those values and it stores the information to *learn* from so it can be considered for the next run. This one repeats in a loop until you type "exit".

```
python learning.py
```

![learning agent run](./images/aa38.png?raw=true "learning agent run")

<p align="center">
**[END OF LAB]**
</p>
</br></br>


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

**Lab 5 - Working with multiple agents**

**Purpose: In this lab, we’ll see how to add an agent to a workflow using CrewAI.**

1. As we've done before, we'll build out the agent code with the diff/merge facility. Run the command below.
```
code -d ../extra/lab5-code.txt agent5.py
```

![Diffs](./images/aa23.png?raw=true "Diffs") 

2. In the *agent5.py* template, we have the imports and llm setup at the top filled in, along with a simulated function to book a flight. Scroll to the bottom. At the bottom is the input and code to kick off the "*crew*". So, we need to fill in the different tasks and setup the crew.

3. Scroll back to the top, review each change and then merge each one in. When done, the files should show no differences. Click on the "X" in the tab at the top to save your changes to *agent5.py*.

![Merge complete](./images/aa24.png?raw=true "Merge complete") 

4. Now you can run the agent and see the larger workflow being handled. There will be quite a bit of output so this may take a while to run. **NOTE: Even though the agent may prompt for human input to select a flight, none is needed. We're not adding that in and using fake info to keep things simple and quick.**

```
python agent5.py
```

![Execution](./images/aa31.png?raw=true "Execution") 

5. Now, that we know how the code works and that it works, let's consider the overall approach. Since there are multiple functions going on here (getting info, finding flights, booking flights) it doesn't necessarily make sense to have just one agent doing all those things. Let's add two other agents - a *travel agent* to help with finding flights, and a customer_service_agent to help with user interactions. To start, replace the single *booking agent* definition with these definitions for the 3 agents (making sure to get the indenting correct):

*NOTE*: First screenshot below shows highlighted text to be replaced and second shows replaced text.

```
# Defines the AI agents

booking_agent = Agent(
    role="Airline Booking Assistant",
    goal="Help users book flights efficiently.",
    backstory="You are an expert airline booking assistant, providing the best booking options with clear information.",
    verbose=True,
    llm=ollama_llm,
)

# New agent for travel planning tasks
travel_agent = Agent(
    role="Travel Assistant",
    goal="Assist in planning and organizing travel details.",
    backstory="You are skilled at planning and organizing travel itineraries efficiently.",
    verbose=True,
    llm=ollama_llm,
)

# New agent for customer service tasks
customer_service_agent = Agent(
    role="Customer Service Representative",
    goal="Provide excellent customer service by handling user requests and presenting options.",
    backstory="You are skilled at providing customer support and ensuring user satisfaction.",
    verbose=True,
    llm=ollama_llm,
)
```
![Text to replace](./images/aa26.png?raw=true "Text to replace") 

![Replaced text](./images/aa27.png?raw=true "Replaced text")

6. Next, we'll change each *task definition* to reflect which agent should own it. The places to make the change are in the task definitions in the lines that start with "*agent=*". Just edit each one as needed per the mapping in the table below.

| **Task** | *Agent* | 
| :--------- | :-------- | 
| **extract_travel_info_task** |  *customer_service_agent*  |        
| **find_flights_task** |  *travel_agent*  |  
| **present_flights_task** |  *customer_service_agent*  |  
| **book_flight_task** | *booking_agent* (ok as-is) |  
         
![Replaced text](./images/aa28.png?raw=true "Replaced text")

7. Finally, we need to add the new agents to our crew. Edit the "*agents=[*" line in the block under the comment "*# Create the crew*". In that line, add *customer_service_agent* and *travel_agent*. The full line is below. The screenshot shows the changes made.

```
agents=[booking_agent, customer_service_agent, travel_agent],
```

![Replaced text](./images/aa29.png?raw=true "Replaced text")

8. Now you can save your changes and then run the program again.

```
python agent5.py
```

9. This time when the code runs, you should see the different agents being used in the processing.

![Run with new agents](./images/aa30.png?raw=true "Run with new agents")

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

![final answer](./images/aa25.png?raw=true "final answer") 

<p align="center">
**[END OF LAB]**
</p>
</br></br>

<p align="center">
**THANKS!**
</p>
