import json
import sys
import os
from pathlib import Path


#Extract data from docling object
#def extract_data_from_docling


def read_data_to_process(stored_json_file_path: str):
    """This method reads the JSON content from a given file path and returns the content of a file
    Args:
        stored_json_file_path: file path of the json file
    Returns:
        data: It's a python dictionary"""
    
    with open(stored_json_file_path, 'r' ) as f:
        data = json.load(f)

    return data


def store_json_in_new_file(directory_path: str, data, file_prefix:str = None):
    """
    This method allows user to define a directory, name the file and store the JSON data inside defined file
    Args:
        directory_path (str): define deirectory where you want to create and store file containing yoru data
        data : The actual data to be stored inside the file. Data must be JSON
        file_prefix (str): any prefix you want to keep in your file name
    """
    if (file_prefix):
        file_name = f"{file_prefix}{data['doc_info']['doc_name'].strip()}.json"
    else:
        file_name = f"{data['doc_info']['doc_name'].strip()}.json" 
    
    file_path = f"{directory_path}/{file_name}"

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)