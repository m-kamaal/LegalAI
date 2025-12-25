#For script run
import sys
import os
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_indexing.chroma_database import get_collection
from src.embeddings.embedding_service import generate_single_embedding

collection = get_collection()

query = "What visitation rights were given to the father?"
query_emb = generate_single_embedding(query)

resp = collection.query(query_emb, n_results=2)

print(resp)

