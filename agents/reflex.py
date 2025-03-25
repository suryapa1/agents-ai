import asyncio
import ollama

# Define a simple reflex agent
async def simple_reflex_agent(inventory_level):
    print(f"Current inventory level: {inventory_level}")
    
    if inventory_level < 50:
        print("Inventory level is low. Placing an order...")
        client = ollama.AsyncClient()
        try:
            message = {
                "role": "user",
                "content": "Pretend to have ordered 100 widgets automatically from the supplier."
            }
            response = await client.chat(
                model="llama3.2",
                messages=[message],
                stream=False
            )
            print("Order placed:", response["message"]["content"])
        finally:
            pass

# Example usage
async def main():
    inventory_level = int(input("Enter the current inventory level: "))
    await simple_reflex_agent(inventory_level)

asyncio.run(main())
