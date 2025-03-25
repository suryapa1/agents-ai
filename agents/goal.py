import asyncio
import ollama

# Define a goal-based agent
async def goal_based_agent(inventory_level, target_range):
    print(f"Current inventory level: {inventory_level}, Target range: {target_range}")
    
    if inventory_level < target_range[0]:
        order_quantity = target_range[0] - inventory_level
        print(f"Inventory level is below target. Ordering {order_quantity} units...")
        client = ollama.AsyncClient()
        try:
            message = {
                "role": "user",
                "content": f"Pretend to have ordered {order_quantity} widgets automatically from the supplier. You can make up any missing values except {order_quantity}."
            }
            response = await client.chat(
                model="llama3.2",
                messages=[message],
                stream=False
            )
            print("Order placed:", response["message"]["content"])
        finally:
            pass
    elif inventory_level > target_range[1]:
        excess_quantity = inventory_level - target_range[1]
        print(f"Inventory level is above target. Discounting {excess_quantity} units...")
        client = ollama.AsyncClient()
        try:
            message = {
                "role": "user",
                "content": f"Create a sales ad for a discount on {excess_quantity} widgets. Mention a limited-time offer and a discount price."
            }
            response = await client.chat(
                model="llama3.2",
                messages=[message],
                stream=False
            )
            print("Sales Ad:", response["message"]["content"])
        finally:
            pass
    else:
        print("Inventory level is within target range. No action needed.")

# Example usage
async def main():
    inventory_level = int(input("Enter the current inventory level: "))
    target_range = (int(input("Enter the lower bound of the target range: ")), int(input("Enter the upper bound of the target range: ")))
    await goal_based_agent(inventory_level, target_range)

asyncio.run(main())
