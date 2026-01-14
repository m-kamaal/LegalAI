YELLOW = "\033[93m"
RESET = "\033[0m"

from src.llm_chain.chains import (_ambiguity_checker_chain,
                                  _clarifiaction_ques_generation_chain,
                                  _query_consolidator_chain,
                                  _llm_with_context_chain,
                                  _retrieval_required_checker_chain,
                                   _llm_without_context_chain )
from src.schema.state_schema import StateSchema
from src.retrieval.content_retriever import content_retriever
from logger import log_node
from langchain_core.messages import AIMessage

# -------- NODE 2 ------------
@log_node("node_ambiguity_check")
def node_ambiguity_check(state:StateSchema):

    response = _ambiguity_checker_chain(state['conversation_history'])

    return {
        "clarification_need": response["clarification_need"],
        "ambiguity_reason": response["ambiguity_reason"],
        "ambiguity_score": response["ambiguity_score"],
        "stop_reason": response["stop_reason"]
    }

# -------- NODE 3 ------------
@log_node("node_clarification_ques_gen")
def node_clarification_ques_gen(state: StateSchema):

    response = _clarifiaction_ques_generation_chain(state['conversation_history'],
                                         state['ambiguity_reason'],
                                         state['clarifications_asked_count'])
    
    print(f"{YELLOW}Legal AI : {response}{RESET}")
 
    return {'conversation_history':[AIMessage(content=response)],
            'clarifications_asked_count': state['clarifications_asked_count'] + 1}

# -------- NODE 4 ------------
@log_node("node_simple_llm_call")
def node_simple_llm_call(state: StateSchema):
    
    response = _llm_without_context_chain(state['original_user_query'])

    print(f"{YELLOW}Legal AI : {response}{RESET}")

    return{
        "conversation_history": AIMessage(content=response)
    }

# -------- Node 5 ------------
@log_node("node_retrieve_data")
def node_retrieve_data(state: StateSchema):

    response =  content_retriever(state['consolidated_query']) #this response is a list

    return {
        'retrieved_data': [response]
        }


# -------- NODE 6 ------------
@log_node("node_generate_llm_response_with_retrieved_context")
def node_generate_llm_response_with_retrieved_context(state: StateSchema):

    response= _llm_with_context_chain(state["conversation_history"], state['retrieved_data'])

    print(f"{YELLOW}Legal AI : {response}{RESET}")

    return {
        'conversation_history':AIMessage(content=response)
        }

# -------- NODE 7 ------------
@log_node("node_consolidator")
def node_consolidator(state: StateSchema):

    response = _query_consolidator_chain(state['original_user_query'], state['conversation_history'])

    return {
        "consolidated_query": response
    }

# -------- NODE 8 ------------
@log_node("node_retrieval_decider")
def node_retrieval_decider(state: StateSchema):
    response = _retrieval_required_checker_chain(state["conversation_history"], state['retrieved_data'])

    return {
        "retrieval_needed": response['decision'],
        "retreival_reasoning": response['reasoning']
    }


# ---------- FUNCTION ------------
@log_node("check_stop_condition")
def check_stop_condition(state: StateSchema):

    if state['clarifications_asked_count'] >=3:
        {'clarification_need': "No",
         'stop_reason': "max_count_reached"}
    
    if state['clarification_need'] == "No":
        return True
    
    else: return False

# ---------- FUNCTION ------------
@log_node("retrieval_router")
def retrieval_router(state: StateSchema):

    if state['retrieval_needed'] == "RETRIEVE":
        return "RETRIEVE"
    else: 
        return "DONT_RETRIEVE"
    

    