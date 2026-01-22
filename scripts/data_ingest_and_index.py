#-------------------------- For script run ----------------------------------
import sys
import os
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#----------------------------------------------------------------------------

from langchain_core import runnables
from src.data_preprocessing.doc_ingestion import extract_data_from_source_document
from src.data_preprocessing.text_cleaning import cleaner_pipeline
from src.data_indexing.chroma_database import add_or_update_data
from src.data_indexing.collection_dataset_builder import dataset_builder
from src.utilities.file_handling import store_json_in_new_file, read_data_to_process
import logging
from logger import setup_logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def ingest_and_index(uploaded_file_path):
    setup_logging()

    logger.info("Step 1: extracting data from raw file")
    ingested_data = extract_data_from_source_document(uploaded_file_path) #creates a json output


    # logger.info("Step 2: cleaning the extracted json data content of the file")
    # #run the cleaning process for each text block of the data chunks inside the json data
    # for i in ingested_data["doc_content"]:
    #     i['text'] = cleaner_pipeline(i['text'])

    #store the cleaned data in a new file 
    logger.info("Step 3: storing cleaned data in local")
    store_json_in_new_file("/Users/workpc/Legalai/project_data/cleaned_data_after_ingestion", ingested_data, "cleaned_")

    logger.info("Step 4: building dataset to get indexed in chromaDB")
    indexed_data = dataset_builder(ingested_data) #returns a dictionary of lists

    print(indexed_data)

    logger.info("Step 5: storing the indexed data to chromadb")
    add_or_update_data(indexed_data['ids'], indexed_data['embeddings'], indexed_data['documents'], indexed_data['metadatas'])

    return ("Success fully extracted data from raw file and stored inside the ChromaDB")




# ------------ Run ------------------

uploaded_file_path = "/Users/workpc/Legalai/project_data/raw data/water_tank_cleaning_circular.pdf"
ingest_and_index(uploaded_file_path)
