import asyncio
import ollama

# Define a model-based reflex agent
async def model_based_reflex_agent(inventory_level, sales_trend):
    print(f"Current inventory level: {inventory_level}, Sales trend: {sales_trend}")
    
    if sales_trend == "increasing":
        order_quantity = 100
    else:
        order_quantity = 50
    
    print(f"Ordering {order_quantity} widgets based on sales trend...")
    client = ollama.AsyncClient()
    try:
        message = {
            "role": "user",
            "content": "Pretend to have ordered widgets automatically from the supplier. You can make up any missing values except {order_quantity}."
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
    sales_trend = input("Enter the sales trend (increasing/decreasing): ")
    await model_based_reflex_agent(inventory_level, sales_trend)

asyncio.run(main())
