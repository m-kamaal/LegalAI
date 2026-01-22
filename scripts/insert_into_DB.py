# For script run
import sys
import os
import logging

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_indexing.chroma_database import add_or_update_data
from src.data_indexing.collection_dataset_builder import dataset_builder
from logger import setup_logging

logger = logging.getLogger(__name__)


def main():
    setup_logging()
    file_path = (
        "/Users/workpc/Legalai/project_data/cleaned_data_after_ingestion/"
        "cleaned_Landmark judgements of supreme court.json"
    )

    logger.info("Ingestion script started")
    logger.info("Processing file | path=%s", file_path)

    # Build dataset
    response = dataset_builder(file_path)

    if not response:
        logger.error("Dataset builder failed | aborting ingestion")
        return

    logger.info(
        "Dataset built | ids=%d | embeddings=%d | documents=%d",
        len(response["ids"]),
        len(response["embeddings"]),
        len(response["documents"]),
    )

    # Insert into ChromaDB
    try:
        logger.info("Inserting data into ChromaDB")
        add_or_update_data(
            response["ids"],
            response["embeddings"],
            response["documents"],
            response["metadatas"],
        )
        logger.info("ChromaDB insertion completed successfully")
    except Exception:
        logger.exception("Failed to insert data into ChromaDB")


if __name__ == "__main__":
    main()