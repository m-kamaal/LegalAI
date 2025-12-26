from src.llm_chain.llm_builder import get_llm_model, get_llm_response
from src.prompt_tempaltes.prompt_template import llm_answer_prompt, clarification_ques
from src.data_preprocessing.text_cleaning import cleaner_pipeline

#simple and direct llm call 
def run_llm_without_context(query):
    model = get_llm_model()
    response = get_llm_response(model, query)
    return response


#llm call by passing user question and retreived data
def run_llm_with_context(query, contexts):

    cleaned_query = cleaner_pipeline(query)
    updated_query = llm_answer_prompt.invoke({"user_query":cleaned_query, "contexts":contexts})
    
    model = get_llm_model()
    response = get_llm_response(model, updated_query)

    return response

def clarification_chain(query):

    cleaned_query = cleaner_pipeline(query)
    updated_query = clarification_ques.invoke({"user_query":cleaned_query})

    model = get_llm_model()
    response = get_llm_response(model, updated_query)

    return response