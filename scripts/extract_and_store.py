#For script run
import sys
import os
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


#actual imports for the following code
from src.data_preprocessing.doc_ingestion import extract_data_from_source_document
import json
from pathlib import Path
from src.utilities.file_handling import store_json_in_new_file

#raw file that is under ingestion
raw_file_path = "/Users/workpc/Legalai/data/raw data/Web-Based To-Do List Application – Requirements Document.pdf"

#extract data and metadata from raw file
extracted_data_metadata = extract_data_from_source_document(raw_file_path)

#Store the extracted data and metadata in a json file inside
store_json_in_new_file("/Users/workpc/Legalai/data/data_extracted_from_raw_file", extracted_data_metadata)


