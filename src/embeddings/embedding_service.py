import os
import logging
import requests
import numpy as np
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

embedding_key = os.getenv("EURON_KEY")
generate_embedding_url = os.getenv("GENERATE_EMBEDDING_API_URL")


def generate_single_embedding(text: str):
    """
    Fundamental text to embedding converter
    """

    logger.debug("generate_single_embedding | start | text_length=%d", len(text))

    url = generate_embedding_url
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {embedding_key}"
    }
    payload = {
        "input": text,
        "model": "text-embedding-3-small"
    }

    try:
        logger.debug("Embedding API call | sending request")
        response = requests.post(url, headers=headers, json=payload)
        logger.debug("Embedding API response | status_code=%s", response.status_code)
    except Exception as e:
        logger.exception("Embedding API call failed")
        return None

    try:
        response_json = response.json()
    except Exception:
        logger.error("Embedding API response is not valid JSON")
        return None

    # Validate response structure BEFORE indexing
    if "data" not in response_json:
        logger.error(
            "Embedding API response missing 'data' key | keys=%s",
            list(response_json.keys())
        )
        return None

    if not response_json["data"]:
        logger.error("Embedding API response 'data' is empty")
        return None

    if "embedding" not in response_json["data"][0]:
        logger.error(
            "Embedding missing in response | data_keys=%s",
            list(response_json["data"][0].keys())
        )
        return None

    embedding = np.array(response_json["data"][0]["embedding"])
    logger.debug("Embedding generated | vector_size=%d", embedding.shape[0])

    return embedding


def generate_embeddings(document_content_list: list):
    """
    Takes list of document chunks and returns list of embeddings
    """

    logger.info(
        "generate_embeddings | start | num_chunks=%d",
        len(document_content_list)
    )

    list_of_embeddings = []

    for idx, item in enumerate(document_content_list):
        text = item.get("text", "").strip()

        if not text:
            logger.debug("Chunk %d skipped | empty text", idx)
            continue

        logger.debug(
            "Processing chunk %d | text_length=%d",
            idx,
            len(text)
        )

        emb = generate_single_embedding(text)

        if emb is not None:
            list_of_embeddings.append(emb)
        else:
            logger.warning("Embedding failed for chunk %d", idx)

    logger.info(
        "generate_embeddings | completed | success=%d",
        len(list_of_embeddings)
    )

    return list_of_embeddings