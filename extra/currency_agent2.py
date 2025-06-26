#!/usr/bin/env python
"""
currency_agent_memory_demo.py — A currency‐conversion agent that shows off multiple memory features:

  1. **Conversion history**: store and list past conversions
  2. **Contextual follow‐ups**: convert your last amount into a new currency
  3. **Persistence**: save history across sessions
  4. **Eviction policy**: cap history length and drop the oldest entries
"""

import json
import atexit
from pathlib import Path

from smolagents import ToolCallingAgent, OpenAIServerModel, tool

# ────────────────────────────────────────────────────────────────────────────────
# Configuration: where to persist our history on disk
# ────────────────────────────────────────────────────────────────────────────────
HISTORY_PATH = Path("conversion_history.json")

# ────────────────────────────────────────────────────────────────────────────────
# Memory class: handles in‐process memory and persistence
# ────────────────────────────────────────────────────────────────────────────────
class Memory:
    def __init__(self, max_items: int = 10):
        # max_items caps how many conversions we remember
        self.max_items = max_items
        # buffer holds our history of conversion results as strings
        self.buffer: list[str] = []
        # automatically load any saved history from disk
        self.load()

    def remember(self, entry: str) -> None:
        """Add a new entry and evict oldest if we exceed max_items."""
        self.buffer.append(entry)
        if len(self.buffer) > self.max_items:
            # drop the oldest entry
            self.buffer.pop(0)

    def last(self) -> str | None:
        """Return the most recent entry, or None if empty."""
        return self.buffer[-1] if self.buffer else None

    def list_recent(self, n: int = 5) -> list[str]:
        """Return up to 'n' most recent entries in chronological order."""
        return self.buffer[-n:] if self.buffer else []

    def save(self) -> None:
        """Persist our history buffer to disk as JSON."""
        try:
            with open(HISTORY_PATH, "w") as f:
                json.dump(self.buffer, f)
        except Exception as e:
            print(f"[Memory] Warning: could not save history: {e}")

    def load(self) -> None:
        """Load history from disk if present."""
        if HISTORY_PATH.exists():
            try:
                with open(HISTORY_PATH) as f:
                    data = json.load(f)
                # ensure it's a list of strings
                if isinstance(data, list) and all(isinstance(x, str) for x in data):
                    self.buffer = data[-self.max_items :]
            except Exception as e:
                print(f"[Memory] Warning: could not load history: {e}")

# create a global memory instance and register save on exit
memory = Memory(max_items=10)
atexit.register(memory.save)


# ────────────────────────────────────────────────────────────────────────────────
# Mock FX rates (base USD)
# ────────────────────────────────────────────────────────────────────────────────
USD_RATES = {
    "USD": 1.00, "EUR": 0.92, "GBP": 0.79, "JPY": 158.00,
    "CHF": 0.89, "CAD": 1.37, "AUD": 1.49, "CNY": 7.26, "INR": 83.60,
}


# ────────────────────────────────────────────────────────────────────────────────
# Tool #1: convert_currency
# ────────────────────────────────────────────────────────────────────────────────
@tool
def convert_currency(from_currency: str, to_currency: str, amount: float) -> str:
    """
    Convert an amount from one currency to another using hard‐coded USD base rates.

    Args:
        from_currency (str): ISO‐4217 code to convert from (e.g. "USD").
        to_currency   (str): ISO‐4217 code to convert   to (e.g. "EUR").
        amount        (float): Numeric amount to convert.

    Returns:
        str: e.g. "200 USD = 184.00 EUR", or an error message.
    """
    # validate numeric input
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return "Error: amount must be numeric."

    # normalize currency codes
    fc, tc = from_currency.upper(), to_currency.upper()
    if fc not in USD_RATES:
        return f"Error: unsupported currency '{fc}'."
    if tc not in USD_RATES:
        return f"Error: unsupported currency '{tc}'."
    if fc == tc:
        return f"{amount} {fc} (no conversion)."

    # perform conversion via USD as an intermediary
    usd_amount = amount / USD_RATES[fc]
    converted = usd_amount * USD_RATES[tc]

    # format result and remember in history
    result = f"{amount} {fc} = {converted:.2f} {tc}"
    memory.remember(result)
    return result


# ────────────────────────────────────────────────────────────────────────────────
# Tool #2: recall_last_conversion
# ────────────────────────────────────────────────────────────────────────────────
@tool
def recall_last_conversion() -> str:
    """
    Retrieve the most recent conversion from memory.

    Returns:
        str: The last conversion string, or a message indicating no history.
    """
    last = memory.last()
    if last:
        return f"For reference only (do NOT reconvert): {last}"
    return "No conversions performed yet."


# ────────────────────────────────────────────────────────────────────────────────
# Tool #3: list_conversions
# ────────────────────────────────────────────────────────────────────────────────
@tool
def list_conversions(n: int = 5) -> str:
    """
    List up to 'n' most recent conversions from memory.

    Args:
        n (int): How many recent entries to show.

    Returns:
        str: A newline‐separated list, or "No history yet."
    """
    recent = memory.list_recent(n)
    if not recent:
        return "No history yet."
    return "\n".join(recent)


# ────────────────────────────────────────────────────────────────────────────────
# Tool #4: convert_last_to
# ────────────────────────────────────────────────────────────────────────────────
@tool
def convert_last_to(to_currency: str) -> str:
    """
    Take the amount & source currency from your last conversion
    and convert it again into a new currency.

    Args:
        to_currency (str): ISO‐4217 code to convert to.

    Returns:
        str: New conversion result or an error if no prior conversion.
    """
    last = memory.last()
    if not last:
        return "No previous conversion to repeat."
    # last is like "200 USD = 184.00 EUR"
    parts = last.split()
    # [amount, from_currency, '=', value, to_currency]
    try:
        amt, frm = parts[0], parts[1]
        return convert_currency(frm, to_currency, float(amt))
    except Exception:
        return "Error: could not parse last conversion."


# ────────────────────────────────────────────────────────────────────────────────
# HTTP‐served Ollama model wrapper
# ────────────────────────────────────────────────────────────────────────────────
model = OpenAIServerModel(
    model_id="deepseek-r1:7b",            # ensure you've pulled & quantized
    api_base="http://localhost:11434/v1",
    api_key="ollama",
    # OpenAI‐style generation parameters:
    max_tokens=64,    # cap how many tokens the model can emit
    temperature=0.0,  # deterministic replies
    stream=False,     # do not stream partial outputs
    # device="cuda"   # if Ollama is serving on GPU
)


# ────────────────────────────────────────────────────────────────────────────────
# Agent setup: enable base tools to get `final_answer`
# ────────────────────────────────────────────────────────────────────────────────
INSTRUCTIONS = """
You are a helpful currency‐conversion assistant.
• To convert an amount, call convert_currency(from_currency, to_currency, amount).
• To recall the last conversion, call recall_last_conversion().
• To list recent history, call list_conversions(n).
• To convert your last amount into a new currency, call convert_last_to(to_currency).
• Once you know your reply text, call final_answer(answer="<your reply>") exactly once.
• Do NOT call any other tools beyond that.
""".strip()

agent = ToolCallingAgent(
    tools=[convert_currency, recall_last_conversion, list_conversions, convert_last_to],
    model=model,
    add_base_tools=True,   # brings in final_answer automatically
    instructions=INSTRUCTIONS,
    # allow up to 3 tool calls + 1 final_answer
    max_steps=2,
)


# ────────────────────────────────────────────────────────────────────────────────
# Simple REPL: interact with your agent
# ────────────────────────────────────────────────────────────────────────────────
def main() -> None:
    print("Currency agent with memory demo — type a request (or 'exit').")
    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        # run the agent and print out its final_answer output
        print(agent.run(user_input))


if __name__ == "__main__":
    main()
