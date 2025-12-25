from langchain.tools import tool
from langchain_core.tools import Tool

from src.retrieval.content_retriever import content_retriever


@tool("Retriever_for_rag")
def retrieve_context(user_query:str, k:int):
    '''Search indexed documents and return top-k chunks based on the userquery given in a fomrat to be passed to LLM'''

    return content_retriever()