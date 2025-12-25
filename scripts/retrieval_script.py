#For script run
import sys
import os
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.retrieval.content_retriever import content_retriever

text = "eight lakhs only"

ans = content_retriever(text, 3)

print(ans)