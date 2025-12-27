#For script run
import sys
import os
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.simple_direct_retrieve_agent import simple_agent

user_input = input("Enter your query: ")

ans = simple_agent(user_input)

print(ans)
