# weather agent with TAO.py

import json
import requests
import textwrap
from langchain_ollama import ChatOllama  

# ── 1. Tools ──────────────────────────────────────────────────────────────
def get_weather(lat: float, lon: float) -> float:
    """Return current temperature in °C via Open-Meteo."""
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )
    r = requests.get(url)
    r.raise_for_status()
    return r.json()["current_weather"]["temperature"]

def convert_c_to_f(c: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return c * 9/5 + 32

# ── 2. LLM client ───────────────────────────────────────────────────────────
llm = ChatOllama(model="llama3.2", temperature=0.0)

# ── 3. System prompt ────────────────────────────────────────────────────────
SYSTEM = textwrap.dedent("""
You are an agent with two tools:

get_weather(lat:float, lon:float)  → float  
convert_c_to_f(c:float)            → float  

When you plan, emit exactly:

Thought: <your thought>  
Action: <tool name>  
Args: {"lat":X,"lon":Y}   or   {"c":Z}

Do NOT output anything else.
""").strip()

# ── 4. Run sequence with explicit Observations ─────────────────────────────
def run(question: str):
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user",   "content": question},
    ]
    print("\n--- Thought → Action → Observation → Final ---\n")

    # First LLM planning turn
    reply1 = llm.invoke(messages)
    plan1 = reply1.content.strip()
    print(plan1 + "\n")

    # Extract coords and call get_weather
    coords = json.loads(plan1.split("Args:")[1].strip())
    obs1 = get_weather(**coords)
    print(f"Observation: {obs1}\n")    # ← explicit observation

    # Feed back observation to LLM
    messages += [
        {"role": "assistant", "content": plan1},
        {"role": "user",      "content": f"Observation: {obs1}"}
    ]

    # Second LLM planning turn
    reply2 = llm.invoke(messages)
    plan2 = reply2.content.strip()
    print(plan2 + "\n")

    # Convert using the first observation
    obs2 = convert_c_to_f(obs1)
    print(f"Observation: {obs2}\n")    

    # Print the final answer
    print(f"Final: {obs2}\n")

# ── 5. Demo ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run(
      "What is the current temperature in Berlin? "
      "Berlin is at latitude 52.52, longitude 13.41. Then convert that to °F."
    )
