import json
import os

import requests
from openai import OpenAI
from pydantic import BaseModel, Field

# Set up local model access 

client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama', # required, but unused
)

# Define the function that we want to call for find_weather
 
def find_weather(latitude, longitude):
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m"
    )
    data = response.json()
    return data["current"]

# Expose the function as a tool for the agent

tools = [
    {
        "type": "function",
        "function": {
            "name": "find_weather",
            "description": "Find current weather for provided coordinates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                },
                "required": ["latitude", "longitude"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]

# 1. Set up system prompt and user message and call the model

system_prompt = "You are a helpful and accurate weather assistant."

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What's the weather like in Paris, France today?"},
]

completion = client.chat.completions.create(
    model="llama3.2",
    messages=messages,
    tools=tools,
)


# 2. Model decides to call function(s) - convert data into dictionary

completion.model_dump()

# 3. Execute find_weather function and add result to messages for model

def call_function(name, args):
    if name == "find_weather":
        return find_weather(**args)

for tool_call in completion.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    messages.append(completion.choices[0].message)

    print(f"\n\nCalling function: {name}")
    print(f"Arguments: {args}")

    result = call_function(name, args)
    messages.append(
        {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)}
    )

    print(f"Function result: {result}\n\n")

# 4. Supply result from tool and call model again to make nice output

class WeatherResponse(BaseModel):
    response: str = Field(
        description="A natural language response to the user's question."
    )

completion_2 = client.beta.chat.completions.parse(
    model="qwen2.5:7b",
    messages=messages,
    tools=tools,
    response_format=WeatherResponse,
)

# 5. Print final model response

final_response = completion_2.choices[0].message.parsed
print(final_response.response)
