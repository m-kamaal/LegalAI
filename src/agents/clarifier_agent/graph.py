from langgraph.graph import StateGraph
from langgraph.graph import START, END
from langgraph.checkpoint.memory import InMemorySaver
from src.schema.state_schema import StateSchema

from src.agents.clarifier_agent.nodes import (node_retrieval_decider,
                                              node_consolidator,
                                              node_ambiguity_check,
                                              node_clarification_ques_gen,
                                              node_generate_llm_response_with_retrieved_context,
                                              node_retrieve_data,
                                              node_simple_llm_call,
                                              check_stop_condition,
                                              retrieval_router
)

graph = StateGraph(StateSchema)
checkpointer = InMemorySaver()

#Add nodes in graph
#graph.add_node("user_input_node", node_take_user_input)
graph.add_node("ambiguity_checker", node_ambiguity_check)
graph.add_node("clarification_ques_gen", node_clarification_ques_gen)
graph.add_node("retrieval_decider", node_retrieval_decider)
graph.add_node("retrieve_data", node_retrieve_data)
graph.add_node("generate_with_retrieved_data", node_generate_llm_response_with_retrieved_context)
graph.add_node("simple_llm_call", node_simple_llm_call)
graph.add_node("consolidator", node_consolidator)

#Add Edges
#graph.add_edge(START, "user_input_node")
graph.add_edge(START, "ambiguity_checker")
graph.add_conditional_edges("ambiguity_checker", check_stop_condition, path_map={False:"clarification_ques_gen", True:"retrieval_decider"})
#graph.add_edge("clarification_ques_gen", "user_input_node")
graph.add_conditional_edges("retrieval_decider", retrieval_router, {"RETRIEVE": "consolidator", "DONT_RETRIEVE": "simple_llm_call"})
graph.add_edge("consolidator", "retrieve_data")
graph.add_edge("retrieve_data", "generate_with_retrieved_data")

def agent_graph_compiler():

    return graph.compile(checkpointer=checkpointer)