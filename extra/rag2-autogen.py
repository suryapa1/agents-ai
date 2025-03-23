import os
from pathlib import Path
from datasets import load_dataset
from dotenv import load_dotenv
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen.agentchat.assistant_agent import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen.agentchat.contrib.vectordb.chromadb import ChromaVectorDB
import asyncio

# Load environment variables (e.g., API keys)
load_dotenv()

# Ollama configuration for the LLM
ollama_client = OllamaChatCompletionClient(
    model="llama3.2:latest",  # Specify the Llama 3.2 model
    base_url="http://localhost:11434/v1",  # Local Ollama server URL
)

# Step 1: Load the MedQuad dataset and preprocess it
dataset = load_dataset("keivalya/MedQuad-MedicalQnADataset", split="train")
data = dataset.to_pandas()  # Convert to Pandas DataFrame for easier handling

# Select a subset of the dataset for demonstration (e.g., first 100 rows)
data = data.head(100)

# Save the dataset to text files for ingestion into the vector database
docs_path = "documents"
Path(docs_path).mkdir(exist_ok=True, parents=True)  # Ensure folder exists

for idx, row in data.iterrows():
    doc_path = os.path.join(docs_path, f"doc_{idx}.txt")
    with open(doc_path, "w") as f:
        f.write(f"Question: {row['Question']}\nAnswer: {row['Answer']}")

# Step 2: Initialize Chroma vector database and create a collection
vector_db = ChromaVectorDB(path="vdb_data/")

# Create or get a collection explicitly (fixes the collection_name issue)
collection_name = "medical_qa"
vector_db.client.get_or_create_collection(collection_name)

# Function to validate document format
def validate_document(doc):
    """
    Validates if a document has the required fields for ChromaVectorDB.
    
    Args:
        doc: Document object to validate
        
    Returns:
        bool: True if document is valid, False otherwise
    """
    # Check if document has the required fields
    if not isinstance(doc, dict):
        print(f"Error: Document must be a dictionary, got {type(doc)}")
        return False
        
    if 'id' not in doc:
        print(f"Error: Document missing required 'id' field")
        return False
        
    if 'content' not in doc:
        print(f"Error: Document missing required 'content' field")
        return False
        
    if not doc['content'] or not isinstance(doc['content'], str):
        print(f"Error: Document 'content' field must be a non-empty string")
        return False
        
    return True

# Create a list of valid documents as dictionaries with 'content'
valid_documents = []
invalid_count = 0

for idx, row in data.iterrows():
    try:
        # Create a dictionary for the document with 'content'
        doc = {
            "id": f"doc_{idx}",  # Unique ID for the document
            "content": f"Question: {row['Question']}\nAnswer: {row['Answer']}",  # Required content field
            "metadata": {"source": f"doc_{idx}.txt", "type": "medical_qa"}  # Optional metadata
        }
        
        # Validate the document
        if validate_document(doc):
            valid_documents.append(doc)
        else:
            invalid_count += 1
            print(f"Skipping invalid document {idx}")
    except Exception as e:
        invalid_count += 1
        print(f"Error processing document {idx}: {str(e)}")

print(f"Processed {len(data)} documents: {len(valid_documents)} valid, {invalid_count} invalid")

# Insert only valid documents into the vector database collection
if valid_documents:
    try:
        vector_db.insert_docs(valid_documents, collection_name=collection_name)
        print(f"Successfully inserted {len(valid_documents)} documents into the vector database")
        
        # Persist the vector database for future use (optional)
        # vector_db.client.persist()
    except Exception as e:
        print(f"Error inserting documents into vector database: {str(e)}")
else:
    print("No valid documents to insert into the vector database")

# Step 3: Initialize the RetrieveUserProxyAgent for document retrieval
ragproxyagent = RetrieveUserProxyAgent(
    name="ragproxyagent",
    retrieve_config={
        "task": "qa",  # Task type: question-answering or code generation
        "docs_path": docs_path,  # Path to document collection
        "chunk_token_size": 1250,  # Chunk size for splitting documents
        "vector_db": vector_db,  # Vector database instance
        "overwrite": False,
        "get_or_create": True,
    },
)

# Step 4: Initialize the AssistantAgent (Replacing deprecated RetrieveAssistantAgent)
assistant = AssistantAgent(
    name="assistant",
    system_message="You are a helpful assistant that provides answers based on retrieved medical documents.",
)

# Register Ollama client with AssistantAgent (to use Llama3.2 model)
assistant.client = ollama_client

# Step 5: Initiate Chat with Retrieval Augmentation using `a_send`
problem_statement = """I have a patient that can have Botulism, how can I confirm the diagnosis?"""

To-do: figure out correct syntax here.
assistant.reset()
ragproxyagent.initiate_chat(assistant, problem="What is the workflow in docGPT?", n_results=2)
