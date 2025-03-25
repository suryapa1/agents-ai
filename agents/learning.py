import asyncio
import ollama
import random

# Define a learning agent
class LearningAgent:
    def __init__(self):
        self.historical_data = []
        self.optimal_inventory_level = 200  # Example optimal level
    
    async def learn(self, inventory_level, sales):
        """
        This method represents the learning logic of the agent, adjusting order quantities based on recent sales trends and historical data.
        
        Parameters:
        - inventory_level: The current level of inventory.
        - sales: The recent sales data.
        """
        
        print(f"Current inventory level: {inventory_level}, Recent sales: {sales}")
        
        self.historical_data.append((inventory_level, sales))
        
        # Calculate recent sales trend
        if len(self.historical_data) > 5:
            recent_sales = sum([data[1] for data in self.historical_data[-5:]])
            if recent_sales > 50:
                projected_demand = recent_sales / 5  # Average demand per period
            else:
                projected_demand = 10  # Default demand if recent sales are low
        else:
            projected_demand = 10  # Default demand if not enough historical data
        
        # Determine order quantity based on projected demand and current inventory
        order_quantity = max(0, self.optimal_inventory_level - inventory_level + projected_demand)
        
        # Limit order quantity to a reasonable amount based on recent sales
        if len(self.historical_data) > 5:
            max_order_quantity = int(recent_sales * 1.5)  # Limit to 150% of recent sales
            order_quantity = min(order_quantity, max_order_quantity)
        
        if order_quantity > 0:
            print(f"Ordering {order_quantity} units based on recent sales trends and projected demand...")
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
            print("No order needed. Inventory level is sufficient.")

# Example usage
async def main():
    agent = LearningAgent()
    
    while True:
        user_input = input("Enter 'exit' to stop or press Enter to continue. Enter the current inventory level and recent sales (comma-separated): ")
        
        if user_input.lower() == 'exit':
            print("Exiting the program.")
            break
        
        try:
            inputs = user_input.split(',')
            if len(inputs) != 2:
                print("Please enter two values separated by a comma.")
                continue
            
            # Remove leading/trailing whitespace from inputs
            inputs = [input.strip() for input in inputs]
            
            inventory_level = int(inputs[0])
            sales = int(inputs[1])
            
            await agent.learn(inventory_level, sales)
        except ValueError:
            print("Invalid input. Please enter numeric values for inventory level and sales.")

asyncio.run(main())

