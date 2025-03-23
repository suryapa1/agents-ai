import json
import os

import requests
from openai import OpenAI
from pydantic import BaseModel, Field

# Set up local model access 


# Define the function that we want to call for find_weather


# Expose the function as a tool for the agent


# 1. Set up system prompt and user message and call the model


# 2. Model decides to call function(s) - convert data into dictionary


# 3. Execute find_weather function and add result to messages for model


# 4. Supply result from tool and call model again to make nice output


# 5. Print final model response
