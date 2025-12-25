"""
Store the output after cleaning metadata and text into a JSONL format that can later be vectorised and uploaded in vectordb
"""

    #-------------------------------------------------------------------------------
    #https://chatgpt.com/share/68ebe7d4-cc1c-800b-816f-23ab8998a91c
    #should different cleaning teqniques be different methods? or all in one method?

import unicodedata
import re


class TextCleaner:

    '''
    Data pipline to be built under this
    '''

    #to lowercase
    def convert_to_lowercase(text_data):
        return text_data.lower()

    #normalise the text as per unicode
    def unicode_normalize(text_data):
        return unicodedata.normalize('NFKC', text_data)
        
    #change non standard symbols to standard symbols
    def symbol_normalize(text_data):
        
        symbol_replacements = {        
            '“': '"', '”': '"', '‘': "'", '’': "'",
            '–': '-', '—': '-', '−': '-', 
            '…': '...', '•': '', '·': '', '►': '',
            'ﬁ': 'fi', 'ﬂ': 'fl'
        }

        for old, new in symbol_replacements.items():
            upated_text_data = text_data.replace(old,new)

        return upated_text_data

    #replace patterns
    def structurual_cleanup(text_data):
        
        # Remove non-printable characters
        text_data = re.sub(r'[^\x09\x0A\x0D\x20-\x7E]', '', text_data)
        
        # Remove page numbers like "Page 12" or "12 of 100"
        text_data = re.sub(r'Page\s*\d+(\s*of\s*\d+)?', '', text_data, flags=re.IGNORECASE)
        
        # Remove excessive line breaks
        text_data = re.sub(r'\n+', '\n', text_data)
        
        # Remove hyphenation at line breaks
        text_data = re.sub(r'-\n', '', text_data)
        
        # Replace multiple spaces/tabs with single space
        text_data = re.sub(r'\s+', ' ', text_data).strip()

        # Replace patterns like "O R D E R" → "ORDER"
        re.sub(r'(?<!\w)([A-Z](?:\s[A-Z])+)(?!\w)',
                  lambda m: m.group(0).replace(' ', ''),
                  text_data)
        
        return text_data


def cleaner_pipeline(text):
    """
    This method cleans the text passed into it and returns back the cleaned text
    Args:
        text: text that needs to be cleaned
    """
    text = TextCleaner.convert_to_lowercase(text)
    text = TextCleaner.unicode_normalize(text)
    text = TextCleaner.symbol_normalize(text)
    text = TextCleaner.structurual_cleanup(text)
    return text



        


