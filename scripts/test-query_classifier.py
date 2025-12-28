#For script run
import sys
import os
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.classifiers.retrieval_classifier import query_classification_for_retrieval


query = "how avnoor kaur's child can celebrate diwali"
response = query_classification_for_retrieval(query)

print(response['decision'])
print(response['confidence_score'])
print(response['reasoning'])
