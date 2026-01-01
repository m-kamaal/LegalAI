from src.llm_chain.llm_builder import get_llm_model, get_llm_response
from src.prompt_templates.prompt_template import llm_answer_prompt, clarification_ques
from src.prompt_templates.prompt_clarifier_agent import clarification_question_generation_prompt, ambiguity_check_prompt
from src.data_preprocessing.text_cleaning import cleaner_pipeline

from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

"""Chain is supposed to use LCEL and pipe operator i.e langchain runnablesequence() only"""

string_output = StrOutputParser()
json_output = JsonOutputParser()
model = get_llm_model()

#simple and direct llm call 
def _llm_without_context_chain(query):
    
    chain = query | model | string_output
    
    return chain.invoke(query)


#llm call by passing user question and retreived data

"""
run_llm_with_context = prompt | LLM | Output pydantic schema
query cleaning and all not required
"""

def _llm_with_context_chain(query, contexts):

    _cleaned_query = cleaner_pipeline(query)
    chain = llm_answer_prompt | model | string_output

    return chain.invoke({"user_query":_cleaned_query, "contexts":contexts})


#chain for clarification ques generation
def _clarifiaction_ques_generation_chain(convo_history,
                                   ambiguity_reason,
                                   clarifications_asked_count):

    chain = clarification_question_generation_prompt | model | json_output

    return chain.invoke({"conversation_history":convo_history, 
                         "ambiguity_reason":ambiguity_reason, 
                         "clarifications_asked_count":clarifications_asked_count})

#to check if there is ambiguity in user query or not
def _ambiguity_checker_chain(convo_history):
    """This function returns a json output of llm response in format.
        Args:
            convo_history: str
        Returns:
            clarification_need: boolean
            ambiguity_reason: str
            ambiguity_score: float
    """
    chain = ambiguity_check_prompt | model | json_output

    return chain.invoke(convo_history)

