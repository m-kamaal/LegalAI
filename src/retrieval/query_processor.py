"""Responsible for:
trimming query
normalizing text
validating query
preparing filters

If query is too big, we need to convert it into meaningful chunks before embedding it. so the embedding of user query retreive most accurate content from vdb"""

from src.data_preprocessing.text_cleaning import cleaner_pipeline
from src.embeddings.embedding_service import generate_single_embedding

#clean the 
def user_query_processor(user_query):
    '''Cleans the raw query text given by user'''
    return cleaner_pipeline(user_query)

#need to have a method that enhances the query too befor embedding it

def embedd_user_query(user_query:str ):
    """This method return embedding of cleaned query in form of a list for the user query"""
    return generate_single_embedding(user_query)


#one pipleine method for user query that can be called iside the tool

def query_processing_pipeline(user_query):
    query = cleaner_pipeline(user_query)
    output_embedding = embedd_user_query(query)
    return output_embedding


