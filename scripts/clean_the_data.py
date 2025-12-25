#For script run
import sys
import os
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


#Actual method imports to use in this script
from src.data_preprocessing.text_cleaning import cleaner_pipeline , read_data_to_process
from src.utilities.file_handling import store_json_in_new_file




file_to_be_cleaned = "/Users/workpc/Legalai/data/data_extracted_from_raw_file/shaina450062024_2025-09-10.json"
json_data = read_data_to_process(file_to_be_cleaned)

#run the cleaning process for each text block of the data chunks inside the json data
for i in json_data["doc_content"]:
    i['text'] = cleaner_pipeline(i['text'])

#store the cleaned data in a new file 
store_json_in_new_file("/Users/workpc/Legalai/data/cleaned_data_from_extracted", json_data, "cleaned_")


