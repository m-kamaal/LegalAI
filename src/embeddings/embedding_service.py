import requests, os
from dotenv import load_dotenv

load_dotenv()
embdding_key=os.getenv("EURON_KEY")
generate_embedding_url = os.getenv("GENERATE_EMBEDDING_API_URL")

#generate embedding
@staticmethod
def generate_single_embedding(text: str):
    
    """
    Fundamental text to embedding convertor
    Args:
        text (str): This is a string that will be converted into a vector
    """

    url = generate_embedding_url
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {embdding_key}"
    }
    payload = {
        "input": text,
        "model": "text-embedding-3-small"
    }
    response = requests.post(url, headers=headers, json=payload)
    embedding = response.json()['data'][0]['embedding']
    
    return embedding

@staticmethod
def generate_embeddings(document_content_list: list):
    """This methods takes list of document content that include text chunks and metadata.
    And returns the list of embeddings for each text chunk in the form of a list"""

    list_of_embeddings=[]

    for item in document_content_list:

        emb = generate_single_embedding(item['text'])
        list_of_embeddings.append(emb)

    return list_of_embeddings