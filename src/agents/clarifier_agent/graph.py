# agents/clarifier_agent/graph.py

from langgraph.graph import StateGraph, END, START

from src.schema.state_schema import StateSchema
from src.agents.clarifier_agent.nodes import (
    ambiguity_checker,
    clarification_ques_generator,
    wait_for_user,
    check_for_stop,
    intent_consolidator
)

# Node name constants
_AMBIGUITY_CHECKER = "ambiguity_checker"
_CLARIFIER_QUES_GEN = "clarification_ques_generator"
_WAIT_FOR_USER = "wait_for_user"
_CHECK_FOR_STOP = "check_for_stop"
_CONSOLIDATOR = "intent_consolidator"

# ---------------------------------------------------------
# Routing functions (PURE logic, no LLM)
# ---------------------------------------------------------

def route_after_ambiguity(state: StateSchema) -> str:
    """
    Decide whether to ask a clarification question
    or move towards stopping logic.
    """
    if state["clarification_need"]:
        return _CLARIFIER_QUES_GEN
    return _CHECK_FOR_STOP


def route_after_stop_check(state: StateSchema) -> str:
    """
    Decide whether to stop and consolidate
    or loop back for further clarification.
    """
    if state["stop_reason"] is not None:
        return _CONSOLIDATOR
    return _AMBIGUITY_CHECKER

# ---------------------------------------------------------
# Graph builder
# ---------------------------------------------------------

def build_clarifier_agent_graph():
    
    graph = StateGraph(StateSchema)

    # ---- Register nodes ----
    graph.add_node(
        _AMBIGUITY_CHECKER,
        lambda state: ambiguity_checker(state),
    )

    graph.add_node(
        _CLARIFIER_QUES_GEN,
        lambda state: clarification_ques_generator(state),
    )

    graph.add_node(
        _WAIT_FOR_USER,
        wait_for_user,  # called externally with user input
    )

    graph.add_node(
        _CHECK_FOR_STOP,
        check_for_stop,
    )

    graph.add_node(
        _CONSOLIDATOR,
        lambda state: intent_consolidator(state),
    )

    # ---- Entry point ----
    graph.set_entry_point(_AMBIGUITY_CHECKER)

    # ---- Conditional edges ----
    graph.add_conditional_edges(
        _AMBIGUITY_CHECKER,
        route_after_ambiguity,
    )

    graph.add_edge(
        _CLARIFIER_QUES_GEN,
        _WAIT_FOR_USER,
    )

    graph.add_edge(
        _WAIT_FOR_USER,
        _AMBIGUITY_CHECKER,
    )

    graph.add_conditional_edges(
        _CHECK_FOR_STOP,
        route_after_stop_check,
    )

    graph.add_edge(
        _CONSOLIDATOR,
        END,
    )

    return graph.compile()
