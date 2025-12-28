"""
Direct retrieval and ans should be generated
"""

from src.retrieval.content_retriever import content_retriever #returns document content in json
from src.prompt_templates.prompt_template import llm_answer_prompt
from src.llm_chain.llm_builder import get_llm_model, get_llm_response

def simple_agent(user_input):

    retreived_content = content_retriever(user_input, 4)

    final_query = llm_answer_prompt.invoke({"contexts": retreived_content, "user_query": user_input})


    model = get_llm_model()

    final_response = get_llm_response(model, final_query)

    return final_response


