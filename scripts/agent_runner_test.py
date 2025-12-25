#For script run
import sys
import os
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from src.agents.rag_agent import create_agent

agent = create_agent()


result = agent.invoke(
    {"messages": [{"role": "user", "content": "who is avnoor kaur?"}]}
)