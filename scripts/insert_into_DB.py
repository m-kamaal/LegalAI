#For script run
import sys
import os
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_indexing.chroma_database import add_or_update_data
from src.data_indexing.collection_dataset_builder import dataset_builder

file_path = "/Users/workpc/Legalai/data/cleaned_data_after_ingestion/cleaned_shaina450062024_2025-09-10.json"

response = dataset_builder(file_path)

#Insert te data into chromadb
add_or_update_data(response['ids'], response['embeddings'], response['documents'], response['metadatas'])

# for i in response['embeddings']:
#     print(len(i))







