from src.utilities.file_handling import read_data_to_process
from src.utilities.misc_utilities import create_docID_for_vectorDB
from src.embeddings.embedding_service import generate_embeddings

def dataset_builder(datafile_path, ):

    data = read_data_to_process(datafile_path)
    
    doc_name = data['doc_info']['doc_name']

    #create list of index of each data block inside the cleaned data to be vectorised
    indices = [data['doc_content'].index(i) for i in data['doc_content']]

    # #create lits of document ids to be used in chromadb
    _ids = create_docID_for_vectorDB(doc_name, indices)

    # #create list of all embeddings of respective text blocks
    _embeddings = generate_embeddings(data['doc_content'])

    #create a list of original texts of each respective text block
    _texts = [i['metadata']['orig_text'] for i in data['doc_content']]

    #create a list of metadatas for respective text block
    _metadatas = [{'document name':data['doc_info']['doc_name'], 'document version': data['doc_info']['doc_version'], 'page number': i['metadata']['page_number']} for i in data['doc_content']]

    return {
        'ids' :_ids,
        'embeddings': _embeddings,
        'documents': _texts,
        'metadatas': _metadatas
    }