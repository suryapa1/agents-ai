import os
from typing import List, TypedDict, Literal
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Setup Ollama LLM
llm = ChatOllama(
    model="llama3.2",
    callbacks=[StreamingStdOutCallbackHandler()],
    temperature=0.2,
    verbose=True
)

# Define the schema for structured output to use as routing logic

# Define the state for the graph

# Define nodes for each task
    
    # Parse the result to determine the task

# Define conditional edge function for routing

# Add edges

# Compile the workflow
chain = workflow.compile()

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

