"""https://chatgpt.com/share/695171c4-9920-800b-b22a-f2b68c9b8e54"""


from src.schema.state_schema import StateSchema

from src.llm_chain.chains import (_clarifiaction_ques_generation_chain,
                                  _ambiguity_checker_chain,
                                  _query_consolidator_chain)

from langchain_core.output_parsers import JsonOutputParser


# ---------------------------------------------------------
# Utility
# ---------------------------------------------------------

def format_conversation(history: list[dict]) -> str:
    """
    Converts conversation history into a readable string
    """
    return "\n".join(
        f"{msg['role'].upper()}: {msg['message']}"
        for msg in history
    )

# ---------------------------------------------------------
# Node 1: Ambiguity Checker
# ---------------------------------------------------------

def ambiguity_checker(state: StateSchema) -> StateSchema:
    parser = JsonOutputParser()

    response = _ambiguity_checker_chain(format_conversation(state["conversation_history"]))

    state["clarification_need"] = response["clarification_need"]
    state["ambiguity_reason"] = response["ambiguity_reason"]
    state["ambiguity_score"] = response["ambiguity_score"]

    return state

# ---------------------------------------------------------
# Node 2: Clarification Question Generator
# ---------------------------------------------------------

def clarification_ques_generator(state: StateSchema) -> StateSchema:
    
    ques = _clarifiaction_ques_generation_chain(format_conversation(state["conversation_history"]), 
                                                state["ambiguity_reason"], 
                                                state["clarifications_asked_count"])

    state["conversation_history"].append({"role":"assistant","message":ques})                                       

    state["clarifications_asked_count"] += 1

    return state

# ---------------------------------------------------------
# Node 3: Wait for User (human-in-the-loop)
# ---------------------------------------------------------

def wait_for_user(state: StateSchema, user_input: str) -> StateSchema:
    state["conversation_history"].append({
        "role": "user",
        "message": user_input
    })
    return state

# ---------------------------------------------------------
# Node 4: Stop Condition Checker (NO LLM)
# ---------------------------------------------------------

def check_for_stop(state: StateSchema) -> StateSchema:
    if state["clarification_need"] is False:
        state["stop_reason"] = "intent_clear"
        return state

    if state["clarifications_asked_count"] >= 3:
        state["stop_reason"] = "max_clarifications_reached"
        return state

    state["stop_reason"] = None
    return state


# ---------------------------------------------------------
# Node 5: Intent Consolidator
# ---------------------------------------------------------

def intent_consolidator(state: StateSchema) -> StateSchema:

    response = _query_consolidator_chain(state["original_user_query"],
                                         format_conversation(state["conversation_history"]))

    state["consolidated_query"] = response["consolidated_query"]
    state["stop_reason"] = response["stop_reason"]

    return state