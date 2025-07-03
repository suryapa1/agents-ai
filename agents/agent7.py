# agent7_offices_memory_canonical.py

import pandas as pd
import json
import litellm

# ── Model config ──────────────────────────────────────────
MODEL = "ollama/llama3.2"

# ── Tool: Load office data ────────────────────────────────


# ── Tool: Analyze using canonical query strings ───────────


# ── LLM Planner: normalize query into canonical form ──────

def llm_decide_next_action(user_query: str, memory: list, data_loaded: bool) -> str:
    history = "\n".join([f"User: {m['user']}\nAgent: {m['agent']}" for m in memory])
    prompt = f"""
You are a helpful AI assistant for analyzing office data.

Your job is to plan tool calls based on user requests.


Conversation so far:
{history}

The user asks: "{user_query}"
You {"already have" if data_loaded else "do not have"} the data loaded.
"""


# ── Main agent loop ───────────────────────────────────────

def main():
    data_loaded = False
    data = None
    memory = []

    print("Office Data Agent is ready — type a question or 'exit' to quit.\n")

    while True:
        user_query = input("User ➤ ").strip()
        if user_query.lower() in ["exit", "quit"]:
            print("Goodbye.")
            break

        current_query = user_query

        while True:
            llm_response = llm_decide_next_action(current_query, memory, data_loaded)

            try:
                plan = json.loads(llm_response)
            except json.JSONDecodeError:
                print("Agent ➤ Sorry, I couldn't understand the plan.")
                break

            print(f"Thought: {plan['thought']}")
            action = plan["action"]


            else:
                print("Agent ➤ Unknown action.")
                break

if __name__ == "__main__":
    main()
