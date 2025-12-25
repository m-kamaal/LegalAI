



def create_docID_for_vectorDB(source_doc_name: str, indices):
    """This methods takes name of the document and the list of indices of the text blocks.
    concatenates first 10 characters of file name with respective index to create a document id for chromadb
    Args:
        source_doc_name (str): full name of the original document
        indices (List of numbers): index list of respective text blocks
        
    Returns: 
        generated_ids (List of strings): These are respective ids of all text blocks
        """


    generated_ids = [f"{source_doc_name[:10]}_{index}" for index in indices]

    return generated_ids