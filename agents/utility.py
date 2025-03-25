import asyncio
import ollama

# Define a utility-based agent
async def utility_based_agent(inventory_level, holding_cost, stockout_cost):
    """
    This function represents a utility-based agent that decides whether to order more inventory based on a utility function.
    
    Parameters:
    - inventory_level: The current level of inventory.
    - holding_cost: The cost associated with storing inventory.
    - stockout_cost: The cost of not having enough inventory to meet customer demand.
    """
    
    print(f"Current inventory level: {inventory_level}, Holding cost: {holding_cost}, Stockout cost: {stockout_cost}")
    
    # Simplified utility function
    # The goal is to minimize the total cost, which is a balance between holding costs (cost of having inventory) and stockout costs (cost of not having enough inventory).
    utility = lambda x: -holding_cost * x - stockout_cost * (100 - x)
    
    # Calculate utility at current inventory level
    current_utility = utility(inventory_level)
    print(f"Utility at current inventory level: {current_utility}")
    
    # Find optimal inventory level
    optimal_level = 50  # For simplicity, assume this is the optimal level
    
    if inventory_level < optimal_level:
        order_quantity = optimal_level - inventory_level
        
        # Calculate utility if we order to reach the optimal level
        new_inventory_level = inventory_level + order_quantity
        new_utility = utility(new_inventory_level)
        print(f"Utility if we order to reach {new_inventory_level} units: {new_utility}")
        
        # Decide whether to order based on utility comparison
        if new_utility > current_utility:
            print(f"Ordering {order_quantity} units will improve utility. Proceeding with order...")
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
        else:
            print("Ordering will not improve utility. No action needed.")
    else:
        print("Inventory level is optimal. No action needed.")

# Example usage
async def main():
    inventory_level = int(input("Enter the current inventory level: "))
    holding_cost = float(input("Enter the holding cost per unit (numeric only): "))
    stockout_cost = float(input("Enter the stockout cost per unit (numeric only): "))
    await utility_based_agent(inventory_level, holding_cost, stockout_cost)

asyncio.run(main())
