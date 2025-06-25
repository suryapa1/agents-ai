#!/usr/bin/env python3
# weather_mcp_client.py
# ------------------------------------------------------------------
# Robust MCP client showing Thought → Action → Observation → Final
# with deep-flattening of any list/dict/*Content response from server.

import asyncio
import json
import re
import textwrap

from fastmcp import Client
from langchain_ollama import ChatOllama  # pip install langchain-ollama

# ── 1. System prompt ───────────────────────────────────────────────
SYSTEM = textwrap.dedent("""
You are an agent with two tools:

get_weather(lat:float, lon:float)  → float  
    • Returns current temperature (°C).

convert_c_to_f(c:float)            → float  
    • Converts Celsius to Fahrenheit.

When you plan, emit exactly three lines:

Thought: <what you plan>  
Action: <tool name>  
Args: {"lat":X,"lon":Y}   or   {"c":Z}

Do NOT output anything else.
""").strip()

# ── 2. Regex for extracting the JSON args ───────────────────────────
ARGS_RE = re.compile(r"Args:\s*(\{.*?\})(?:\s|$)", re.S)

# ── 3. Flatten helpers ─────────────────────────────────────────────
def extract_number(x):
    """
    Recursively descend into lists/dicts/*Content objects and return the first
    primitive that can be cast to float.
    """
    # List → drill into first element
    if isinstance(x, list) and x:
        return extract_number(x[0])

    # Dict → look for common numeric-bearing keys
    if isinstance(x, dict) and x:
        for key in ("text", "result", "output", "value"):
            if key in x:
                return extract_number(x[key])
        # Fallback: first value
        return extract_number(next(iter(x.values())))

    # FastMCP Content (TextContent, NumberContent, …) → unwrap
    if hasattr(x, "text"):
        return extract_number(x.text)
    if hasattr(x, "value"):
        return extract_number(x.value)

    # Base case: x should now be int/float/str
    return x


def to_float(x) -> float:
    """
    Use extract_number to pull out a primitive, then cast to float.
    """
    return float(extract_number(x))

# ── 4. Main async runner ────────────────────────────────────────────
async def run(question: str):
    llm = ChatOllama(model="llama3.2", temperature=0.0)

    # Adjust path if your server mounts at a different route
    async with Client("http://127.0.0.1:8000/mcp/") as mcp:
        messages = [
            {"role": "system", "content": SYSTEM},
            {"role": "user",   "content": question},
        ]

        print("\n--- Thought → Action → Observation → Final ---\n")

        # ── First planning turn: get_weather ───────────────────────
        reply1 = llm.invoke(messages)
        plan1  = reply1.content.strip()
        print(plan1 + "\n")

        m1    = ARGS_RE.search(plan1)
        args1 = json.loads(m1.group(1))
        raw1  = await mcp.call_tool("get_weather", args1)
        obs1  = to_float(raw1)
        print(f"Observation: {obs1}\n")

        # Feed the LLM its own plan + our observation
        messages += [
            {"role": "assistant", "content": plan1},
            {"role": "user",      "content": f"Observation: {obs1}"},
        ]

        # ── Second planning turn: convert_c_to_f ───────────────────
        reply2 = llm.invoke(messages)
        plan2  = reply2.content.strip()
        print(plan2 + "\n")

        # We ignore any hallucinated Args and just send the value we have
        raw2 = await mcp.call_tool("convert_c_to_f", {"c": obs1})
        obs2 = to_float(raw2)
        print(f"Observation: {obs2}\n")

        # ── Final answer ───────────────────────────────────────────
        print(f"Final: {obs2}\n")

# ── 5. Entry point ─────────────────────────────────────────────────
if __name__ == "__main__":
    question = (
        "What is the current temperature in Berlin? "
        "Berlin is at latitude 52.52, longitude 13.41. "
        "Then convert that temperature to Fahrenheit."
    )
    asyncio.run(run(question))
