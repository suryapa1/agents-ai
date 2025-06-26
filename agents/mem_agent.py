# travel_agent_smolagents_with_memory.py
# A travel assistant agent using smolagents with short-term and long-term memory, dynamic start location, and debug prints.

import os
import json
import math
import requests
from smolagents import tool, ToolCallingAgent
from smolagents import LiteLLMModel

# ANSI color codes for terminal output
BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Base system prompt guiding agent behavior (tool must be used for distance)

# ----------------------
# Helper functions
# ----------------------


# ----------------------
# Tool definition
# ----------------------


# ----------------------
# Agent setup
# ----------------------

# Initialize LiteLLMModel
model = LiteLLMModel(
    model_id="ollama/llama3.2",
    api_base="http://localhost:11434",
    api_key="ollama",
    temperature=0.0
)
agent = ToolCallingAgent(
    tools=[calculate_distance_tool],
    model=model
)

# ----------------------
# Memory and Start Location Setup
# ----------------------

# Load or prompt for home location
default_loc = long_memory.get("home_location", "Raleigh, NC")
loc_input = input(f"Enter your starting location (default: {default_loc}) [Press Enter to keep default]: ")
home_location = loc_input.strip() or default_loc

# If coords not set or location changed, geocode and save

# In-memory buffer for short-term memory
memory_buffer = []

# ----------------------
# Main interactive loop
# ----------------------
if __name__ == "__main__":
    print(f"\nTravel Assistant ready! Using start: {home_location} ({home_coords[0]}, {home_coords[1]})")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("\nUser: ")
        if user_input.strip().lower() == "exit":
            print("Goodbye!")
            break

        # Build dynamic prompt with profile and recent conv

        # DEBUG: print prompt
        print("\n========== DEBUG: system_prompt ==========")
        print(dynamic_prompt)
        print("========================================\n")

        # Run the agent
        final_answer = agent.run(user_input)
        print(f"\n{GREEN}Assistant Final Response:{RESET}\n{final_answer}\n")

        # Update memories
