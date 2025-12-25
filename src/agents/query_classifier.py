""" To classify wether the given user query requires agent to call retrival tool or not"""
"""improve query classifier logic with this solution: https://chatgpt.com/share/6939ab5f-cf9c-800b-b75c-f8467db1f380"""

from src.llm_chain.prompt_template import retrieval_use_hint
import json
from src.data_preprocessing.text_cleaning import cleaner_pipeline
from src.llm_chain.llm_builder import get_llm_model, get_llm_response

def query_classification_for_retrieval(user_query):

    cleaned_query = cleaner_pipeline(user_query)
    final_query = retrieval_use_hint.invoke({"user_query": cleaned_query})

    llm_model = get_llm_model(temp = 0.3)
    llm_response = get_llm_response(llm_model,final_query)
    
    json_body = json.loads(llm_response)

    final_decision = json_body["decision"]
    confidence_score = json_body["confidence"]
    reasoning = json_body["reasoning"]

    return {"decision" : final_decision, 
            "confidence_score" : confidence_score, 
            "reasoning" : reasoning}
                                

if __name__ == "__main__":

    from src.llm_chain.llm_builder import get_llm

    print(query_classification_for_retrieval("give me details and summary of harry potter in 3 words"))