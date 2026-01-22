#-------------------------- For script run ----------------------------------
import sys
import os
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#----------------------------------------------------------------------------

import requests, os
from dotenv import load_dotenv
import numpy as np

load_dotenv()
embdding_key=os.getenv("EURON_KEY")
generate_embedding_url = os.getenv("GENERATE_EMBEDDING_API_URL")


def generate_single_embedding(text: str):

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
    json_data = response.json()
    embedding = np.array(json_data['data'][0]['embedding'])
    
    return embedding

resp = generate_single_embedding("")
print(resp)