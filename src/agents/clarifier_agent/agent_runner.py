import logging
from langchain_core.messages import HumanMessage
from src.agents.clarifier_agent.graph import agent_graph_compiler

YELLOW = "\033[93m"
RESET = "\033[0m"

stop_words = {"bye", "stop", "exit"}
thread_id = "1"


def run():
    logger = logging.getLogger("langgraph.runner")

    while True:
        user_input = input("").strip()
        print(f"{YELLOW}You : {user_input}{RESET}")

        if user_input in stop_words:
            break

        my_chat_state = {
            "conversation_history": HumanMessage(content=user_input),
            "clarifications_asked_count": 0,
            "original_user_query": user_input,
        }

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        workflow = agent_graph_compiler()
        resp = workflow.invoke(my_chat_state, config=config)

        logger.info("FINAL GRAPH STATE: %s", resp)
