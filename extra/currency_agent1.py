#!/usr/bin/env python
"""
currency_agent_fast_http.py  —  optimized for low‐latency over HTTP
• smolagents ToolCallingAgent + OpenAIServerModel
• Quantized Ollama model (int8) served locally
• OpenAI‐style max_tokens, temperature, stream flags
• Scratch‐pad memory, strict 1‐tool budget, with final_answer via base tools
"""

from smolagents import ToolCallingAgent, OpenAIServerModel, tool

# ────────────────────────────────────
# Mock FX rates (base USD)
# ────────────────────────────────────
USD_RATES = {
    "USD": 1.00, "EUR": 0.92, "GBP": 0.79, "JPY": 158.00,
    "CHF": 0.89, "CAD": 1.37, "AUD": 1.49, "CNY": 7.26, "INR": 83.60,
}

# ────────────────────────────────────
# Scratch‐pad memory
# ────────────────────────────────────
class Memory:
    def __init__(self, max_items: int = 10):
        self.max_items = max_items
        self.buffer: list[str] = []

    def remember(self, entry: str) -> None:
        self.buffer.append(entry)
        if len(self.buffer) > self.max_items:
            self.buffer.pop(0)

    def last(self) -> str | None:
        return self.buffer[-1] if self.buffer else None

memory = Memory()

# ────────────────────────────────────
# Currency‐conversion tool
# ────────────────────────────────────
@tool
def convert_currency(from_currency: str, to_currency: str, amount: float) -> str:
    """
    Convert an amount from one currency to another using hard‐coded USD base rates.

    Args:
        from_currency (str): ISO-4217 code to convert **from** (e.g. "USD").
        to_currency   (str): ISO-4217 code to convert **to**   (e.g. "EUR").
        amount        (float): Numeric amount to convert.

    Returns:
        str: Formatted like "200 USD = 184.00 EUR", or an error message.
    """
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return "Error: amount must be numeric."

    fc, tc = from_currency.upper(), to_currency.upper()
    if fc not in USD_RATES:
        return f"Error: unsupported currency '{fc}'."
    if tc not in USD_RATES:
        return f"Error: unsupported currency '{tc}'."
    if fc == tc:
        return f"{amount} {fc} (no conversion)."

    usd = amount / USD_RATES[fc]
    converted = usd * USD_RATES[tc]
    result = f"{amount} {fc} = {converted:.2f} {tc}"
    memory.remember(result)
    return result

# ────────────────────────────────────
# Memory‐recall tool
# ────────────────────────────────────
@tool
def recall_last_conversion() -> str:
    """
    Retrieve the most recent conversion from scratch‐pad memory.
    """
    last = memory.last()
    if last:
        return f"For reference only (do NOT reconvert): {last}"
    return "No conversions performed yet."

# ────────────────────────────────────
# HTTP‐served Ollama model wrapper
# ────────────────────────────────────
model = OpenAIServerModel(
    model_id="llama3.2",                # after: ollama pull llama3.2 --quantize int8
    api_base="http://localhost:11434/v1",
    api_key="ollama",

    # pass OpenAI‐style kwargs directly:
    max_tokens=64,    # cap how many tokens the LLM can emit
    temperature=0.0,  # deterministic replies
    stream=False,     # no streaming
    # device="cuda"   # if Ollama is serving on GPU
)

# ────────────────────────────────────
# Build the agent — base_tools ON for final_answer
# ────────────────────────────────────
INSTRUCTIONS = (
    "You are a helpful currency‐conversion assistant.\n"
    "• To convert, call convert_currency(from_currency, to_currency, amount).\n"
    "• To show the last conversion, call recall_last_conversion().\n"
    "• Once you know your reply, call final_answer(answer=\"<your reply>\") exactly once.\n"
    "• Do NOT call any other tools in that turn."
)

agent = ToolCallingAgent(
    tools=[convert_currency, recall_last_conversion],
    model=model,
    add_base_tools=True,   # brings in final_answer automatically
    instructions=INSTRUCTIONS,
    max_steps=2,           # one tool call + final_answer
)

# ────────────────────────────────────
# Simple REPL
# ────────────────────────────────────
def main() -> None:
    print("Fast HTTP currency agent ready — type a request (or 'exit').")
    while True:
        try:
            query = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if query.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        print(agent.run(query))


if __name__ == "__main__":
    main()
