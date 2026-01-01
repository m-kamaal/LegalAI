"""The central brain:
accpts query text
calls embedding service
calls vector DB
gets raw resultss

call formatter also and format and return the finall formatted content that will be passed to LLM

here i this file, the content is searched, sent to formatter and that entire flow is retreiverpipeline"""


from src.data_indexing.chroma_database import get_collection, search_topk
from src.retrieval.query_processor import query_processing_pipeline
from src.data_indexing.chroma_database import search_topk
from src.retrieval.utils import retreived_doc_formatter



def content_retriever(user_query, k= 5):
    '''Inputs embedding of user query and gets results of top k similar content from stored documents and returns fomrated content to be passed to LLM'''

    emb = query_processing_pipeline(user_query)
    doc_content = search_topk(emb, k)
    result = retreived_doc_formatter(doc_content)

    return result






