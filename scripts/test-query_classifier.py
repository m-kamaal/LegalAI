#For script run
import sys
import os
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.query_classifier import query_classification_for_retrieval
from src.llm_chain.llm_builder import get_llm_model

query = "tax avnoor correctly?"
response = query_classification_for_retrieval(query)

print(response['decision'])
print(response['confidence_score'])
print(response['reasoning'])
