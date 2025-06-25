import requests
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.ollama import OllamaChatCompletionClient

def convert_currency(from_currency: str, to_currency: str, amount: float) -> str:
    """Convert currency between two currencies using the Frankfurter API."""
    url = f"https://api.frankfurter.app/latest?from={from_currency}&to={to_currency}&amount={amount}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"{amount} {from_currency} = {data['rates'][to_currency]} {to_currency} (rate: {data['rates'][to_currency]/amount})"
    else:
        return f"Error: {response.status_code} - {response.text}"

async def main():
    # Set up Ollama client with llama3.2 model
    ollama_client = OllamaChatCompletionClient(model="llama3.2")

    # Set up AutoGen agent with the function as a tool
    agent = AssistantAgent(
        name="currency_assistant",
        model_client=ollama_client,
        tools=[convert_currency],
        system_message="You are a currency conversion assistant. Use the tools provided to answer questions."
    )

    # Start conversation
    await Console(agent.run_stream(task="How much is 100 USD in EUR?"))

asyncio.run(main())
