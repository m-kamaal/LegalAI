#For script run
import sys
import os
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_indexing.chroma_database import get_client, get_collection

collection = get_collection()

resp = collection.get("shaina4500_3", include=["documents", "metadatas", "embeddings"])

print(resp)