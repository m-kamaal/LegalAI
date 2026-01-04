from src.schema.state_schema import StateSchema

from src.llm_chain.chains import (_clarifiaction_ques_generation_chain,
                                  _ambiguity_checker_chain,
                                  _query_consolidator_chain,
                                  _retrieval_required_checker_chain)

from langchain_core.output_parsers import JsonOutputParser




#---------------
#NODE creation
#---------------
#NODE 1
def ambiguity_check_node(state:StateSchema):

    response = _ambiguity_checker_chain(state["conversation_history"])

    state["clarification_need"] = response["clarification_need"]
    state["ambiguity_reason"] = response["ambiguity_reason"]
    state["ambiguity_score"] = response["ambiguity_score"]

    return state

#NODE 2
def clarification_ques_gen_node(state: StateSchema):

    response = _clarifiaction_ques_generation_chain(state["conversation_history"],
                                         state["ambiguity_reason"],
                                         state["clarifications_asked_count"])
    
    state["clarifications_asked_count"] +=1
    state["conversation_history"].append({"assistant":response})

    return state

#NODE 3
def retrieval_checker_node(state: StateSchema):

    response = _retrieval_required_checker_chain(state["conversation_history"])
    state["retrieval_needed"] = response["decision"]

    return response["decision"]