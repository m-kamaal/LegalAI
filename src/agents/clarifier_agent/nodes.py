"""https://chatgpt.com/share/695171c4-9920-800b-b22a-f2b68c9b8e54"""


from state.state_schema import StateSchema
from prompt_templates.prompt_clarifier_agent import ambiguity_check_prompt, clarification_question_generation_prompt, user_query_consolidation_prompt

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda


"""nodes of the graph"""

AMBIGUITY_CHECKER = "ambiguity_checker"
CLASSIFIER_QUES_GEN = "classfier_ques_generator"
CONSOLIDATOR = "intent_consolidator"
WAIT_FOR_USER = "wait_for_user"
CHECK_FOR_STOP = "check_for_stop"

# ---------------------------------------------------------
# Utility
# ---------------------------------------------------------

def format_conversation(history: list[dict]) -> str:
    """
    Converts conversation history into a readable string
    """
    return "\n".join(
        f"{msg['role'].upper()}: {msg['content']}"
        for msg in history
    )

# ---------------------------------------------------------
# Node 1: Ambiguity Checker
# ---------------------------------------------------------

def ambiguity_checker(state: StateSchema, llm) -> StateSchema:
    parser = JsonOutputParser()

    chain = ambiguity_check_prompt | llm | parser

    response = chain.invoke({
        "conversation_history": format_conversation(
            state["conversation_history"]
        )
    })

    state["clarification_need"] = response["clarification_need"]
    state["ambiguity_reason"] = response["ambiguity_reason"]
    state["ambiguity_score"] = response["ambiguity_score"]

    return state

# ---------------------------------------------------------
# Node 2: Clarification Question Generator
# ---------------------------------------------------------

def classfier_ques_generator(state: StateSchema, llm) -> StateSchema:
    chain = clarification_question_generation_prompt | llm

    question = chain.invoke({
        "conversation_history": format_conversation(
            state["conversation_history"]
        ),
        "ambiguity_reason": state["ambiguity_reason"],
        "clarifications_asked_count": state["clarifications_asked_count"],
    })

    state["conversation_history"].append({
        "role": "assistant",
        "content": question.strip(),
    })

    state["clarifications_asked_count"] += 1

    return state

# ---------------------------------------------------------
# Node 3: Wait for User (human-in-the-loop)
# ---------------------------------------------------------

def wait_for_user(state: StateSchema, user_input: str) -> StateSchema:
    state["conversation_history"].append({
        "role": "user",
        "content": user_input,
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

def intent_consolidator(state: StateSchema, llm) -> StateSchema:
    parser = JsonOutputParser()

    chain = user_query_consolidation_prompt | llm | parser

    response = chain.invoke({
        "original_user_query": state["original_user_query"],
        "conversation_history": format_conversation(
            state["conversation_history"]
        ),
    })

    state["consolidated_query"] = response["consolidated_query"]
    state["ambiguity_score"] = response["ambiguity_score"]
    state["stop_reason"] = response["stop_reason"]

    return state