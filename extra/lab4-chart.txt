import os
from typing import List, TypedDict, Literal
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from IPython.display import Image, display

# Setup Ollama LLM
llm = ChatOllama(
    model="llama3.2",
    callbacks=[StreamingStdOutCallbackHandler()],
    temperature=0.2,
    verbose=True
)

# Define the schema for structured output to use as routing logic
class Route(BaseModel):
    task: Literal["translate", "calculate", "define", "end"] = Field(
        description="The task to route to: translate, calculate, define, or end"
    )

# Define the state for the graph
class State(TypedDict):
    messages: List[HumanMessage]
    task: str
    response: str

# Define nodes for each task
def translate(state: State) -> dict:
    """Translate text to another language"""
    result = llm.invoke([
        SystemMessage(content="Translate the following text to the specified language:"),
        state["messages"][-1]
    ])
    return {"response": result.content, "task": "end"}

def calculate(state: State) -> dict:
    """Calculate a mathematical expression"""
    result = llm.invoke([
        SystemMessage(content="Calculate the result of the following mathematical expression:"),
        state["messages"][-1]
    ])
    return {"response": result.content, "task": "end"}

def define(state: State) -> dict:
    """Provide a definition for a term"""
    result = llm.invoke([
        SystemMessage(content="Provide a concise definition for the following term:"),
        state["messages"][-1]
    ])
    return {"response": result.content, "task": "end"}

def route(state: State) -> dict:
    """Route the input to the appropriate task"""
    messages = [
        SystemMessage(content="Route the input to translate, calculate, or define based on the user's request."),
        state["messages"][-1]
    ]
    result = llm.invoke(messages)
    
    # Parse the result to determine the task
    if "translate" in result.content.lower():
        task = "translate"
    elif "calculate" in result.content.lower():
        task = "calculate"
    elif "define" in result.content.lower():
        task = "define"
    else:
        task = "end"
    
    return {"task": task}

# Define conditional edge function for routing
def route_by_task(state: State) -> str:
    return state["task"]

# Build the workflow graph
workflow = StateGraph(State)

# Add nodes
workflow.add_node("route", route)
workflow.add_node("translate", translate)
workflow.add_node("calculate", calculate)
workflow.add_node("define", define)

# Add edges
workflow.set_entry_point("route")
workflow.add_conditional_edges(
    "route",
    route_by_task,
    {
        "translate": "translate",
        "calculate": "calculate",
        "define": "define",
        "end": END
    }
)
workflow.add_edge("translate", END)
workflow.add_edge("calculate", END)
workflow.add_edge("define", END)

# Compile the workflow
chain = workflow.compile()

# Store workflow to display later
# Get the PNG data from your chain (this is binary data).
png_data = chain.get_graph().draw_mermaid_png()

# Save the PNG data to a file.
mermaid_code = chain.get_graph().draw_mermaid()
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{ startOnLoad: true }});
    </script>
</head>
<body>
    <div class="mermaid">
        {mermaid_code}
    </div>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html_content)



# Example usage
inputs = {
    "messages": [
        HumanMessage(content="Translate 'Hello, how are you?' to French."),
        HumanMessage(content="Calculate 15 * 7 + 22"),
        HumanMessage(content="Define the term 'photosynthesis'.")
    ]
}

for message in inputs["messages"]:
    # Invoke the workflow with proper initial state structure
    initial_state = {"messages": [message], "task": "", "response": ""}
    
    # Run the workflow and capture results
    result = chain.invoke(initial_state)
    
    print(f"\nInput: {message.content}")
    
    # Safely access keys in case of missing data
    response = result.get("response", "[No response generated]")
    
    print(f"Task: {result['task']}")
    print(f"Response: {response}\n")
