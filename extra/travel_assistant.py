"""
Travel Assistant implemented with AutoGen

Prerequisites:
    pip install pyautogen openai chromadb pdfplumber sentence_transformers requests

Before running, start Ollama with an OpenAI-compatible endpoint, for example:
    ollama run llama3:8b --port 11434
"""

import math
import requests
import pdfplumber
import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions

# AutoGen imports
from autogen import AssistantAgent, UserProxyAgent
from autogen.tools import tool

# ----------------------- LLM configuration -----------------------
LLM_CONFIG = {
    "model": "llama3.2",                 # model served by Ollama
    "base_url": "http://localhost:11434/v1",  # Ollama's OpenAI-compatible endpoint
    "api_key": "ollama",                  # dummy key (ignored by Ollama)
    "temperature": 0.2,
}

# ----------------------- Constants -----------------------
CURRENT_LAT = 35.7796  # Raleigh, NC
CURRENT_LON = -78.6382

# ----------------------- Build vector store -----------------------
print("\nBuilding vector DB from offices.pdf ...")
pdf_path = "../data/offices.pdf"
pdf_text = ""
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        pdf_text += page.extract_text() + "\n"

embedding_model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(embedding_model_name)

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(
    name="office_docs",
    embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=embedding_model_name
    ),
)

docs = [line.strip() for line in pdf_text.split("\n") if len(line.strip()) > 20]
ids = [f"doc_{i}" for i in range(len(docs))]
# Avoid duplicate adds if the script is re-run
if collection.count() == 0:
    collection.add(documents=docs, ids=ids)
print(f"Indexed {len(docs)} snippets.\n")


# ----------------------- Helper functions (Tools) -----------------------
@tool
def search_office_docs(query: str) -> list[str]:
    """Retrieve up to 3 office snippets relevant to the given query."""
    results = collection.query(query_texts=[query], n_results=3)
    return results["documents"][0] if results["documents"] else []


@tool
def calculate_distance_tool(destination_query: str) -> dict:
    """Calculate the great-circle (haversine) distance in miles between Raleigh, NC and the destination."""

    def geocode_location(location_query: str):
        headers = {"User-Agent": "TravelAssistant/1.0"}
        url = (
            "https://nominatim.openstreetmap.org/search"
            f"?q={location_query}&format=json"
        )
        try:
            geo = requests.get(url, headers=headers, timeout=10).json()
            if geo:
                return float(geo[0]["lat"]), float(geo[0]["lon"])
        except Exception:
            pass
        return None, None

    def haversine_distance(lat1, lon1, lat2, lon2):
        R = 3958.8  # Earth radius in miles
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    lat2, lon2 = geocode_location(destination_query)
    if lat2 is None or lon2 is None:
        return {"destination": destination_query, "distance_miles": "unknown"}

    miles = haversine_distance(CURRENT_LAT, CURRENT_LON, lat2, lon2)
    return {"destination": destination_query, "distance_miles": round(miles, 2)}


# ----------------------- Agents -----------------------
SYSTEM_PROMPT = (
    "You are a helpful travel assistant.\n"
    "Your tasks:\n"
    "  1. Use `search_office_docs` to present office facts from internal documents (if any).\n"
    "  2. Provide exactly 3 interesting facts about the city using your own knowledge.\n"
    "  3. Use `calculate_distance_tool` to report the distance from Raleigh, NC.\n\n"
    "When responding, combine the information into a clear answer with bullet points."
)

assistant = AssistantAgent(
    name="travel_assistant",
    llm_config=LLM_CONFIG,
    system_message=SYSTEM_PROMPT,
    tools=[search_office_docs, calculate_distance_tool],
)

user_proxy = UserProxyAgent(
    name="user",
    code_execution_config=False,  # no Python execution within messages
)


# ----------------------- REPL Loop -----------------------
print("Travel Assistant ready! (type 'exit' to quit)\n")

while True:
    query = input("User ➜ ")
    if query.lower().strip() == "exit":
        print("Goodbye!")
        break

    user_proxy.initiate_chat(
        assistant,
        message=query,
        summary_style="none",  # show full conversation
    )
