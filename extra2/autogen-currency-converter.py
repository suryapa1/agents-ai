#!/usr/bin/env python
# ag_cur.py  — fast currency converter (reflect-on-tool version)

import asyncio, httpx, re, importlib
from typing import Annotated, Optional, AsyncIterator

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.ui import Console

from autogen_core.tools import FunctionTool
from autogen_core.memory import ListMemory, MemoryContent, MemoryMimeType
from autogen_ext.models.ollama import OllamaChatCompletionClient

# ── 1. Currency-conversion coroutine + tiny cache ───────────────────────
_cache: dict[tuple[str, str, float], str] = {}

async def convert_currency(
    from_currency: Annotated[str, "ISO-4217 code, e.g. USD"],
    to_currency:   Annotated[str, "ISO-4217 code, e.g. EUR"],
    amount:        Annotated[float, "Amount to convert"],
) -> str:
    key = (from_currency, to_currency, amount)
    if key in _cache:
        return _cache[key]

    url = (f"https://api.frankfurter.app/latest"
           f"?from={from_currency}&to={to_currency}&amount={amount}")
    async with httpx.AsyncClient(timeout=8) as c:
        r = await c.get(url)
        r.raise_for_status()
        rate = r.json()["rates"][to_currency]
        result = f"{amount} {from_currency} = {rate} {to_currency}"
        _cache[key] = result
        return result

convert_tool = FunctionTool(
    convert_currency,
    name="convert_currency",
    description="Convert an amount between two ISO-4217 currencies."
)

# ── 2. Hide noisy events no matter where they live ───────────────────────
NOISY = {"MemoryQueryEvent", "ToolCallRequestEvent"}
hidden = set()
for mod in ("autogen_core.events",
            "autogen_agentchat.events",
            "autogen.events"):
    try:
        m = importlib.import_module(mod)
        hidden |= {getattr(m, c) for c in NOISY if hasattr(m, c)}
    except ModuleNotFoundError:
        pass

async def filter_events(source) -> AsyncIterator:
    async for ev in source:
        if ev.__class__ not in hidden:
            yield ev

# ── 3. Main async loop ───────────────────────────────────────────────────
async def main() -> None:
    # initial preference
    prefs = ListMemory()
    await prefs.add(MemoryContent(
        content="Preferred target currency: EUR",
        mime_type=MemoryMimeType.TEXT
    ))

    # local Ollama model that supports function calling
    ollama = OllamaChatCompletionClient(
        model="qwen2.5:7b",            # pull this tag first
        generate_kwargs={"options": {"stream": False}}
    )

    assistant = AssistantAgent(
        name="currency_bot",
        model_client=ollama,
        tools=[convert_tool],
        memory=[prefs],
        reflect_on_tool_use=True,             # tool → reflection → answer
        model_client_stream=False,            # no token streaming
        system_message=(
            "You are a currency-conversion assistant. "
            "If the user omits the target currency, read the most recent "
            "'Preferred target currency' from memory, call the tool, "
            "reply with the result and end with TERMINATE."
        ),
    )

    num_re   = re.compile(r"^\d+(\.\d+)?$")
    alpha_re = re.compile(r"^[A-Za-z]+$")

    last_amt: Optional[str] = None

    while True:
        usr = input("💬  ").strip()
        if usr.lower() in {"exit", "quit"}:
            break

        # shorthand handling
        if num_re.fullmatch(usr):
            last_amt = usr
            prompt = f"Convert {usr} USD to my preferred currency"

        elif alpha_re.fullmatch(usr):
            if last_amt is None:
                print("↪️  Enter an amount first.")
                continue
            await prefs.add(MemoryContent(
                content=f"Preferred target currency: {usr.upper()}",
                mime_type=MemoryMimeType.TEXT
            ))
            prompt = f"Convert {last_amt} USD to my preferred currency"

        else:
            prompt = usr

        team = RoundRobinGroupChat(
            [assistant],
            termination_condition=MaxMessageTermination(3)  # user + 2 bot msgs
        )

        await Console(filter_events(team.run_stream(task=prompt)))

    await ollama.close()

if __name__ == "__main__":
    asyncio.run(main())
