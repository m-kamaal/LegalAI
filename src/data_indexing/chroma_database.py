import os
import chromadb
from dotenv import load_dotenv
from langchain.tools import tool

#Fetch env variables
load_dotenv()
chroma_persistent_db_path = os.getenv("CHROMA_PERSISTENT_DB_PATH")
collection_name = os.getenv("CHROMADB_COLLECTION_NAME")



# Create persistent client (connects to existing data or creates new)
_client = chromadb.PersistentClient(path = chroma_persistent_db_path)

# Get existing collection or create if doesn't exist
_collection = _client.get_or_create_collection(name = collection_name)

def get_client():
    """Returns the singleton ChromaDB client."""
    return _client


def get_collection():
    """Returns the singleton collection for direct access."""
    return _collection

def insert_new_data(_ids, _embeddings, _documents, _metadatas):
    """This methods inserts new data into chroma DB. All arguments in List format
    Args:
        _documents : List of text chunks corresponding to the vectors
    """
    _collection.add(
    ids= _ids,
    embeddings= _embeddings,
    documents= _documents,
    metadatas= _metadatas,
    )

def add_or_update_data(_ids, _embeddings, _documents, _metadatas):
    """This methods inserts new data into chroma DB. All arguments in List format
Args:
    _documents : List of text chunks corresponding to the vectors
"""
    _collection.upsert(
    ids= _ids,
    embeddings= _embeddings,
    documents= _documents,
    metadatas= _metadatas,
    )
    
def search_topk(_embeddings, k: int = 5):
    """This method returns the n (default 5) closest data blocks including metadata and distance
    Args:
        embeddings: embedding of user query that gets match against strored embeddings of content in vector db
        k: top k most relevant content in which we can seek answers of the user query
    Returns:
            QueryResult: A QueryResult object containing metadata, document and distance from vector chromadb."""
    return _collection.query(query_embeddings=_embeddings, n_results=k, include=["metadatas", "documents", "distances"] )
