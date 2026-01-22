import logging
from src.utilities.file_handling import read_data_to_process
from src.utilities.misc_utilities import create_docID_for_vectorDB
from src.embeddings.embedding_service import generate_embeddings

logger = logging.getLogger(__name__)


def dataset_builder(source):
    """
    Creates dictionary of lists for vector DB ingestion
    """
    logger.info(
        "dataset_builder | start | input_type=%s",
        type(source).__name__
    )
    

    # Normalize input into _content
    if isinstance(source, dict):
        logger.info("dataset_builder | using provided JSON content directly")
        _content = source

    elif isinstance(source, str):
        logger.info("dataset_builder | reading content from file | path=%s", source)
        _content = read_data_to_process(source)

    if source is None:
        logger.error("dataset_builder | no file path provided")
        return None


    if not _content:
        logger.error("dataset_builder | no content returned from file reader")
        return None

    # Extract document info
    doc_info = _content.get("doc_info", {})
    doc_name = doc_info.get("doc_name")

    logger.debug("Document info | name=%s", doc_name)

    # Validate content blocks
    doc_content = _content.get("doc_content", [])

    if not doc_content:
        logger.error("dataset_builder | no document content blocks found")
        return None

    logger.info(
        "Preparing dataset | num_blocks=%d",
        len(doc_content)
    )

        # Generate embeddings
    logger.info("Generating embeddings")
    _embeddings = generate_embeddings(doc_content)

    logger.info(
        "Embeddings generated | count=%d",
        len(_embeddings)
    )

    if _embeddings:
        # Create indices for vector DB
        indices = list(range(len(doc_content)))
        logger.debug("Generated indices | count=%d", len(indices))

        # Create document IDs
        _ids = create_docID_for_vectorDB(doc_name, indices)
        logger.debug("Generated document IDs | count=%d", len(_ids))

        # Create documents list
        _texts = [i["metadata"]["orig_text"] for i in doc_content]

        # Create metadatas list
        _metadatas = [
            {
                "document name": doc_info.get("doc_name"),
                "document version": doc_info.get("doc_version"),
                "page number": i["metadata"]["page_number"],
            }
            for i in doc_content
        ]
        
    else:
        logger.error("dataset_builder | embeddings generation failed or returned empty")
        return None

    logger.info("dataset_builder | completed successfully")

    return {
        "ids": _ids,
        "embeddings": _embeddings,
        "documents": _texts,
        "metadatas": _metadatas,
    }