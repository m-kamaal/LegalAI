#For script run
import sys
import os
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm_chain.chains import run_llm_with_context
from src.retrieval.content_retriever import content_retriever

query = input("You: ")

contexts = content_retriever(query)

result = run_llm_with_context(query, contexts)

print(result)