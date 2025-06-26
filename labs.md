# Understanding AI Agents
## Session labs 
## Revision 2.1 - 06/26/25

**Follow the startup instructions in the README.md file IF NOT ALREADY DONE!**

**NOTE: To copy and paste in the codespace, you may need to use keyboard commands - CTRL-C and CTRL-V. Chrome may work best for this.**

**Lab 1 - Creating a simple agent**

**Purpose: In this lab, we’ll learn about the basics of agents and see how tools are called. We'll also see how Chain of Thought prompting works with LLMs and how we can have ReAct agents reason and act.**

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

![Side-by-side merge](./images/aa40.png?raw=true "Side-by-side merge") 

6. When you have finished merging all the sections in, the files should show no differences. Save the changes simply by clicking on the "X" in the tab name.

![Merge complete](./images/aa41.png?raw=true "Merge complete") 

7. Now you can run your agent with the following command:

```
python agent1.py
```

8. The agent will start running and will prompt for a location (or "exit" to finish). At the prompt, you can type in a location like "Paris, France" or "London" or "Raleigh" and hit *Enter*. After that you'll be able to see the Thought -> Action -> Observation loop in practice as each one is listed out. You'll also see the arguments being passed to the tools as they are called. Finally you should see a human-friendly message from the AI summarizing the weather forecast.

![Agent run](./images/aa42.png?raw=true "Agent run") 

9. You can then input another location and run the agent again or exit. Note that if you get a timeout error, the API may be limiting the number of accesses in a short period of time. You can usually just try again and it will work.

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 2 - Exploring MCP**

**Purpose: In this lab, we’ll see how MCP can be used to standardize an agent's interaction with tools.**

1. Still in the *agents* directory, we have partial implementations of an MCP server and an agent that uses a MCP client to connect to tools on the server. So that you can get acquainted with the main parts of each, we'll build them out as we did the agent in the first lab - by viewing differences and merging. Let's start with the server. Run the command below to see the differences.

```
code -d ../extra/lab2-server.txt mcp_server.py
```
</br></br>
![MCP server code](./images/aa43.png?raw=true "MCP server code") 

2. As you look at the differences, note that we are using FastMCP to more easily set up a server, with its @mcp.tool decorators to designate our functions as MCP tools. Also, we run this using the *streamable-http* transport protocol. Review each difference to see what is being done, then use the arrows to merge. When finished, click the "x"" in the tab at the top to close and save the files.

3. Now that we've built out the server code, run it using the command below. You should see some startup messages similar to the ones in the screenshot.

```
python mpc_server.py
```
</br></br>
![MCP server start](./images/aa44.png?raw=true "MCP server start") 

4. Now, let's turn our attention to the agent that will use the MCP server through an MCP client interface. First, since the terminal is tied up with the running server, we need to have a second terminal to use to work with the client. So that we can see the server responses, let's just open another terminal side-by-side with this one. To do that, right-click in the current terminal and select *Split Terminal* from the pop-up context menu.

![Opening a second terminal](./images/aa45.png?raw=true "Opening a second terminal") 

5. In the second terminal, run a diff command so we can build out the new agent.

```
code -d ../extra/lab2-code.txt mpc_agent.py
```

6. Review and merge the changes as before. What we're highlighting in this step are the *System Prompt* that drives the LLM used by the agent, the connection with the MCP client at the /mcp/ endpoint (line 55), and the mpc calls to the tools on the server. When finished, close the tab to save the changes as before.

![Agent using MCP client code](./images/aa48.png?raw=true "Agent using MCP client code") 
   
7. After you've made and saved the changes, you can run the client in the terminal with the command below.

```
python mpc_agent.py
```

8. The agent should start up, and, as in lab 1, prompt you for a location. You'll be able to see similar TAO output. And you'll also be able to see the server INFO messages in the other terminal as the MCP connections and events happen.

![Agent using MCP client running](./images/aa47.png?raw=true "Agent using MCP client running") 

9. When you're done, you can use 'exit' to stop the client and CTRL-C to stop the server. 

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 3 - Leveraging Memory of Agents**

**Purpose: In this lab, we’ll explore how to utilize short-term and long-term memory techniques while also seeing how agents can be implemented with the SmolAgents framework.**

1. For this lab, we have an application that does the following:

- Lets you input a starting location
- Lets you prompt about a destination location
- Provides 3 interesting facts about the destination
- Calls a tool to calculate distance from the starting location to the destination
- Stores information about past prompts and user preferences in an external file
- Adds information from past runs to the next prompt
- Repeats until user enters *exit*

2. As before, we'll use the "view differences and merge" technique to learn about the code we'll be working with. The command to run this time is below:

```
code -d ../extra/mem_agent.txt mem_agent.py
```
</br></br>

![Code for memory agent](./images/aa51.png?raw=true "Code for memory agent") 

3. The code in this application showcases several SmolAgents features and agent techniques including the following. See how many you can identify as your reviewing the code.

- **`@tool` Decorator**  
  Registers plain Python functions as callable “tools” the agent can invoke.

- **`ToolCallingAgent`**  
  Wraps an LLM and your tools into a multi-step agent that:  
  1. Generates a “thought” sequence  
  2. Emits explicit tool-call requests  
  3. Executes your Python tool(s)  
  4. Continues reasoning with the tool outputs  
  5. Returns only the final clean answer

- **Custom Prompt Templates**  
  Uses `agent.prompt_templates['system_prompt']` to inject both:  
  - A fixed instruction (what to do, when to call tools)  
  - Dynamic context (short-term buffer + long-term JSON memory)

- **Short-Term Memory**  
  Maintains a small in-process `memory_buffer` of recent turns, folded into each new prompt so the agent “remembers” the last N interactions.

- **Long-Term Memory**  
  Persists user preferences and query history to a JSON file, then reloads and injects that profile at startup, demonstrating how agents can “remember” across sessions.

4. When you're done merging, close the tab as usual to save your changes. Now, in a terminal, run the agent with the command below:

```
python mem_agent.py
```

5. At this point, you can choose to override the default starting location, or leave it by either typing a new one or just hitting *Enter*. Then you can prompt about a location like a city (Paris, London, etc.) and watch the agent work. The agent will display the augmented prompt each time as well as information about tool calls, etc. Go through at least three iterations of this. The agent will also append history and profile information to the next prompt. The next screenshot points out several examples of functionality.


![Running agent](./images/aa49.png?raw=true "Running agent")   

 
6. To see the stored profile and history information, in another terminal, in the same directory, look for the file *user_memory.json*. You can *cat* the file to see the contents, which is the stored defaults, profile, and history information for the agent.

![Extermal store](./images/aa50.png?raw=true "External store")  

7. There is a built-in example to trigger a *favorites* selection. If you prompt the agent about something with "beach" in it, it will store that as a favorite. You can try that if you want by asking the model something like the line below. Then, you can look at the *user_memory.json* file and you should see that as a favorite.

```
Tell me about Santa Monica Beach
```

8. Since the agent has memory, you can also try out some other non-location prompts like the ones below.

```
What was my most recent query?
What is my favorite?
How much farther is X than Y from my starting location?
```

9. Once you're done working with the agent code, you can use *exit* or CTRL-C to stop it.

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
   
6. The main difference here is there is an extra input for *increasing* or *decreasing*. Based off of the combined *model* of the inventory amount and whether demand (sales trend) is increasing or decreasing, it will decide whether to order 50 or 100 units. (The combination simulates a "model" for basing action on.) Once you've reviewed the code, you can run it in the usual way. Again, you'll want to put in a current value < 50 to cause the *ordering* to happen.

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

1. For this lab, we'll be using the template file *agent4.py*. Open it up and take a look at the contents. At the top, we have the imports and llm setup filled in. Scroll to the bottom. At the bottom is the part to compile the workflow and example usage for three different use cases: a translation to French, a calculation, and a definition. The agent we build through LangGraph will look at each of these and route it to an appropriate node to handle it. This is the basis of the Agent Routing Workflow.

```
code agent4.py
```

![Initial code for agent 4](./images/aa9.png?raw=true "Initial code for agent 4") 

2. As we've done before, we'll build out the agent code with the diff/merge facility. Close the currently open *agent4.py* instance to avoid confusion. Then run the command below.
```
code -d ../extra/lab4-code.txt agent4.py
```

![Merge complete](./images/aa8.png?raw=true "Merge complete") 


3. Scroll back to the top, review each change and then merge each one in. When done, the files should show no differences. Click on the "X" in the tab at the top to save your changes to *agent4.py*.

![Merge complete](./images/aa10.png?raw=true "Merge complete") 

4. Now you can run the agent and see the results of each request being handled. There will be quite a bit of output so this may take a moment to run.

```
python agent4.py
```

![Execution](./images/aa11.png?raw=true "Execution") 

5. Now that we have our routing agent working, let's add one more enhancement. Since LangGraph is based on graphs, we can have it draw the nodes and edges of the graph so we can look at it on a web page. The updated code for this is in *extra/lab4-chart.txt*. We'll use the same merging process to add in code to draw a Mermaid chart and save the data in an html file. Run the command below, review the changes, then merge them in and close the diff to save. (Note there are two sets of changes - a line at the top and a larger section further down.)

```
code -d ../extra/lab4-chart.txt agent4.py
```

![Adding code for graph](./images/aa12.png?raw=true "Adding code for graph") 

6. After completing the merge and save, run the agent again. This time it should dump the graph information into a file named *index.html* in the same directory. (If you happen to get an error about read timeout when running it, just wait a minute or two and try again.)

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

3. Scroll back to the top, review each change and then merge each one in. Notice the occurrences of "*booking_agent*". This is all being done with a single agent in the crew currently. When done, the files should show no differences. Click on the "X" in the tab at the top to save your changes to *agent5.py*.

![Merge complete](./images/aa24.png?raw=true "Merge complete") 

4. Now you can run the agent and see the larger workflow being handled. There will be quite a bit of output so this may take a while to run. **NOTE: Even though the agent may prompt for human input to select a flight, none is needed. We're not adding that in and using fake info to keep things simple and quick.**

```
python agent5.py
```

![Execution](./images/aa31.png?raw=true "Execution") 

5. Now, that we know how the code works and that it works, let's consider the overall approach. Since there are multiple functions going on here (getting info, finding flights, booking flights) it doesn't necessarily make sense to have just one agent doing all those things. Let's add two other agents - a *travel agent* to help with finding flights, and a customer_service_agent to help with user interactions. To start, replace the single *booking agent* definition with these definitions for the 3 agents (making sure to get the indenting correct):

*NOTE*: Following the block of replacement text, the first screenshot below shows highlighted text to be replaced and second shows replaced text.

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
 
**(Bonus) Lab 6 - Implementing Agentic RAG**

**Purpose: In this lab, we’ll see how to setup an agent using RAG with a tool.**

1. In this lab, we'll download a medical dataset, parse it into a vector database, and create an agent with a tool to help us get answers. First,let's take a look at a dataset of information we'll be using for our RAG context. We'll be using a medical Q&A dataset called [**keivalya/MedQuad-MedicalQnADataset**](https://huggingface.co/datasets/keivalya/MedQuad-MedicalQnADataset). You can go to the page for it on HuggingFace.co and view some of it's data or explore it a bit if you want. To get there, either click on the link above in this step or go to HuggingFace.co and search for "keivalya/MedQuad-MedicalQnADataset" and follow the links.
   
![dataset on huggingface](./images/aa16.png?raw=true "dataset on huggingface")    

2. Now, let's create the Python file that will pull the dataset, store it in the vector database and invoke an agent with the tool to use it as RAG. First, create a new file for the project.
```
code agent6.py
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

llm = Ollama(model="qwen2.5:7b",temperature=0.0)
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

9. Create the agent using the LangChain project *hwchase17/react-chat*.
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

10. Add the input processing loop.
    
```
while True:
    query = input("\nQuery: ")
    if query == "exit":
        break
    if query.strip() == "":
        continue
    agent_executor.invoke({"input": query})
```

11. Now, **save the file** and run the code.
    
```
python agent6.py
```

12. When you get the to the "*Query:*" prompt, you can prompt it with queries related to the info in the dataset, like:
```
I have a patient that may have Botulism. How can I confirm the diagnosis?
```

(Note: This will take a very long time to run, since we are in a limited resource environment.)

![final answer](./images/aa25.png?raw=true "final answer") 

<p align="center">
**[END OF LAB]**
</p>
</br></br>

<p align="center">
**THANKS!**
</p>
