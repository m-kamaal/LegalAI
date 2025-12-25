"""Need to add csv later
this   """

from pypdf import PdfReader
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.text import partition_text
from docling.document_converter import DocumentConverter


class DocumentLoader:

    @staticmethod
    def load_doc_docling(file_path: str):
        """"
        This method generates a docling doc object out of a given file from which later we will extract data

        Args:
            file_path (str): this is the path of the file from which we need to extract information

        Retruns:
            doc (Docling doc object): 

        """

        source = file_path  # file path or URL ex: https://arxiv.org/pdf/2408.09869
        converter = DocumentConverter()
        doc = converter.convert(source).document

        return doc

        #print(doc.export_to_markdown())  # output: "### Docling Technical Report[...]"

    @staticmethod
    def extract_data_from_doclingdocument(doc):
        """
        This method helps in extracting texts and metadata from the docling file along with the details of the document

        Args:
            doc (Docling doc):

        Returns:
            result (Dict) : Dictionary containing document metadata and  respective blocks metadata alogn with its text
        """

        result = {}

        result["doc_info"] = {
            "doc_name": doc.name,
            "doc_type": getattr(doc.origin, 'mimetype'),
            "doc_version": doc.version
        }

        result["doc_content"] = []

        for item in doc.texts:
            text = getattr(item, "text", "").strip()

            if text:
                meta = {
                    "page_number": item.prov[0].page_no if item.prov else None,
                    "content_label": getattr(item, "label", None).name if getattr(item, "label", None) else None,
                    # "bbox": item.prov[0].bbox if item.prov else None,
                    # "char_span": item.prov[0].charspan if item.prov else None,
                    "orig_text": getattr(item, "orig", ""),
                    "level": getattr(item, "level", None),  # section header level if present
                }
                result["doc_content"].append({"text": text, "metadata": meta})
                
        return result

@staticmethod
def extract_data_from_source_document(file_path):
    """
    This method takes raw file source like PDF and gives Json formatted content back
    Args:
        file_path: absolute file path of source file
    Returns:
        JSON formatted data containg content and metadata from the source file
    """
    docling_doc_obj = DocumentLoader.load_doc_docling(file_path)
    extracted_data_with_metadata = DocumentLoader.extract_data_from_doclingdocument(docling_doc_obj)
    return extracted_data_with_metadata



if __name__ == "__main__":
    # import json

    # doclingdoc = DocumentLoader.load_doc_docling("/Users/workpc/Legalai/raw data/Finance_Bill_2025.pdf")
    # data_blocks = DocumentLoader.extract_data_from_doclingdocument(doclingdoc)

    # print(data_blocks['document_info'])
    
    # with open("/Users/workpc/Legalai/app/data_preprocessing/storedjson.json", "w") as f:
    #     json.dump(data_blocks, f, indent=4)



    """ ---------------- JUNK CODE BELOW ---------------- """

# @staticmethod
# def load_doc_pypdf(file_path: str)-> str:
#     """Load document based on file type
#     Args:
#         file_path (str): path to document in string format
#     Returns:
#         str: text extracted from document in a single string
#     Raises:
#         ValueError: if file type is not supported (not yet)
#     """
#     text=""
#     if file_path.endswith(".pdf"):
#         reader = PdfReader(file_path)
#         for page in reader.pages:
#             text+= page.extract_text()
#     elif file_path.endswith(".txt"):
#         with open(file_path, "r") as f:
#             text = f.read()
#     else:
#         raise ValueError(f"Unsupported file type other than pdf or txt")

#     return text

# def load_doc_unstructured(file_path:str):

#     """ This method identifies the type of file then extracts data from file, performs partitioning 
#     Args:
#         file_path (str): path of your file
#     Returns:
#         elements: A list of elements that contain text and metadata from the file including page number
            
#     """
#     #Identification of file type
#     file_type_extension= None
#     if(file_path.endswith(".pdf")):
#         file_type_extension = "pdf"
#     elif(file_path.endswith(".txt")):
#         file_path_extension = "txt"
    

#     #Match case to call relevant functions
#     elements = []
#     match file_type_extension:
#         case "pdf":
#             elements = partition_pdf(file_path)
#         case "txt":
#             elements = partition_text(file_path)

#     return elements


    

    
    
