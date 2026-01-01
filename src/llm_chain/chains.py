from src.llm_chain.llm_builder import get_llm_model, get_llm_response
from src.prompt_templates.prompt_template import llm_answer_prompt, clarification_ques
from src.data_preprocessing.text_cleaning import cleaner_pipeline

from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

"""Chain is supposed to use LCEL and pipe operator i.e langchain runnablesequence() only"""

string_output = StrOutputParser()

#simple and direct llm call 
def run_llm_without_context(query):
    model = get_llm_model()
    
    simple_llm_generation = query | model | string_output
    
    return simple_llm_generation.invoke(query)


#llm call by passing user question and retreived data

"""
run_llm_with_context = prompt | LLM | Output pydantic schema

query cleaning and all not required
"""

def run_llm_with_context(query, contexts):

    cleaned_query = cleaner_pipeline(query)
    model = get_llm_model()

    run_llm_with_context_chain = llm_answer_prompt | model | string_output

    return run_llm_with_context_chain.invoke({"user_query":cleaned_query, "contexts":contexts})

