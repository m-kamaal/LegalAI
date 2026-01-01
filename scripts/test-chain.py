#For script run
import sys
import os
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm_chain.chains import llm_with_context_chain, LLM_WITH_CONTEXT_CHAIN
from src.retrieval.content_retriever import content_retriever

query = input("You: ")

contexts = content_retriever(query)

#result = llm_with_context_chain(query, contexts)

result = LLM_WITH_CONTEXT_CHAIN.invoke({"user_query":query, "contexts":contexts})

print(result)