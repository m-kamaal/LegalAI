# agents/clarifier_agent/graph.py

from langgraph.graph import StateGraph, END

from src.schema.state_schema import StateSchema
from src.agents.clarifier_agent.nodes import (
    ambiguity_checker,
    clarification_ques_generator,
    wait_for_user,
    check_for_stop,
    intent_consolidator
)

# Node name constants
AMBIGUITY_CHECKER = "ambiguity_checker"
CLARIFIER_QUES_GEN = "clarification_ques_generator"
WAIT_FOR_USER = "wait_for_user"
CHECK_FOR_STOP = "check_for_stop"
CONSOLIDATOR = "intent_consolidator"

# ---------------------------------------------------------
# Routing functions (PURE logic, no LLM)
# ---------------------------------------------------------

def route_after_ambiguity(state: StateSchema) -> str:
    """
    Decide whether to ask a clarification question
    or move towards stopping logic.
    """
    if state["clarification_need"]:
        return CLARIFIER_QUES_GEN
    return CHECK_FOR_STOP


def route_after_stop_check(state: StateSchema) -> str:
    """
    Decide whether to stop and consolidate
    or loop back for further clarification.
    """
    if state["stop_reason"] is not None:
        return CONSOLIDATOR
    return AMBIGUITY_CHECKER

# ---------------------------------------------------------
# Graph builder
# ---------------------------------------------------------

def build_clarifier_agent_graph(llm):
    graph = StateGraph(StateSchema)

    # ---- Register nodes ----
    graph.add_node(
        AMBIGUITY_CHECKER,
        lambda state: ambiguity_checker(state, llm),
    )

    graph.add_node(
        CLARIFIER_QUES_GEN,
        lambda state: clarification_ques_generator(state, llm),
    )

    graph.add_node(
        WAIT_FOR_USER,
        wait_for_user,  # called externally with user input
    )

    graph.add_node(
        CHECK_FOR_STOP,
        check_for_stop,
    )

    graph.add_node(
        CONSOLIDATOR,
        lambda state: intent_consolidator(state, llm),
    )

    # ---- Entry point ----
    graph.set_entry_point(AMBIGUITY_CHECKER)

    # ---- Conditional edges ----
    graph.add_conditional_edges(
        AMBIGUITY_CHECKER,
        route_after_ambiguity,
    )

    graph.add_edge(
        CLARIFIER_QUES_GEN,
        WAIT_FOR_USER,
    )

    graph.add_edge(
        WAIT_FOR_USER,
        AMBIGUITY_CHECKER,
    )

    graph.add_conditional_edges(
        CHECK_FOR_STOP,
        route_after_stop_check,
    )

    graph.add_edge(
        CONSOLIDATOR,
        END,
    )

    return graph.compile()
