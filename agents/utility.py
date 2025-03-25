import asyncio
import ollama

# Define a utility-based agent
async def utility_based_agent(inventory_level, holding_cost, stockout_cost):
    # holding_cost: This is the cost associated with storing inventory, including expenses like storage space rental, maintenance, insurance, and potential depreciation of goods over time.
    # stockout_cost: This represents the cost of not having enough inventory to meet customer demand, including lost sales, potential loss of customer loyalty, and any additional costs associated with emergency orders or expedited shipping.
    
    print(f"Current inventory level: {inventory_level}, Holding cost: {holding_cost}, Stockout cost: {stockout_cost}")
    
    # Simplified utility function
    # The goal is to minimize the total cost, which is a balance between holding costs (cost of having inventory) and stockout costs (cost of not having enough inventory).
    utility = lambda x: -holding_cost * x - stockout_cost * (100 - x)
    
    # Find optimal inventory level
    optimal_level = 50  # For simplicity, assume this is the optimal level
    
    if inventory_level < optimal_level:
        order_quantity = optimal_level - inventory_level
        print(f"Inventory level is below optimal. Ordering {order_quantity} units...")
    else:
        print("Inventory level is optimal. No action needed.")
        return

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
    holding_cost = float(input("Enter the holding cost per unit (numeric only): "))
    stockout_cost = float(input("Enter the stockout cost per unit (numeric only): "))
    await utility_based_agent(inventory_level, holding_cost, stockout_cost)

asyncio.run(main())
