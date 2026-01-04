#For script run
import sys
import os
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.clarifier_agent.graph import build_clarifier_agent_graph
from src.schema.state_schema import StateSchema


user_query = input("You: ")

state = StateSchema(ambiguity_reason=None,
                    ambiguity_score=0.0,
                    clarification_need=False,
                    clarifications_asked_count=0,
                    consolidated_query=None,
                    conversation_history=[],
                    original_user_query=user_query,
                    stop_reason=None
                    )



agent = build_clarifier_agent_graph()

final_state = agent.invoke(state)

print(final_state)