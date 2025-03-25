import asyncio
import ollama
import random

# Define a learning agent
class LearningAgent:
    def __init__(self):
        self.historical_data = []
    
    async def learn(self, inventory_level, sales):
        print(f"Current inventory level: {inventory_level}, Recent sales: {sales}")
        
        self.historical_data.append((inventory_level, sales))
        
        # Simplified learning logic: adjust order quantity based on recent sales
        if len(self.historical_data) > 5:
            recent_sales = sum([data[1] for data in self.historical_data[-5:]])
            if recent_sales > 50:
                order_quantity = 150
            else:
                order_quantity = 100
        else:
            order_quantity = 100
        
        print(f"Ordering {order_quantity} units based on recent sales trends...")
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

# Example usage
async def main():
    agent = LearningAgent()
    inventory_level = int(input("Enter the current inventory level: "))
    sales = int(input("Enter recent sales: "))
    await agent.learn(inventory_level, sales)

asyncio.run(main())
