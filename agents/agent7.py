import pandas as pd
import json
import litellm

# ── Model config ──
MODEL = "ollama/llama3.2"

# ── Color helpers ──
BLUE = "\033[94m"    # User
BRIGHT_GREEN = "\033[92m"  # Action
BRIGHT_RED = "\033[91m"   # Thought
BOLD_CYAN = "\033[1;96m"   # Agent
RESET = "\033[0m"
# ── Tool: Load office data ────────────────────────────────

# ── Tool: Analyze using canonical query strings ───────────

# ── LLM Planner: normalize query into canonical form ──
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


# ── Main agent loop ──
def main():
    data_loaded = False
    data = None
    memory = []

    print("Office Data Agent is ready — type a question or 'exit' to quit.\n")

    while True:
        user_query = input(f"{BLUE}\nUser ➔ {RESET}").strip()
        if user_query.lower() in ["exit", "quit"]:
            print("Goodbye.")
            break

        current_query = user_query

        while True:
            llm_response = llm_decide_next_action(current_query, memory, data_loaded)

            try:
                plan = json.loads(llm_response)
            except json.JSONDecodeError:
                print(f"{BOLD_CYAN}\nAgent ➔ Sorry, I couldn't understand the plan.{RESET}")
                break

            print(f"\n{BRIGHT_RED}Thought: {plan['thought']}{RESET}")
            action = plan["action"]


            else:
                print(f"{BOLD_CYAN}\nAgent ➔ Unknown action.{RESET}")
                break

if __name__ == "__main__":
    main()
