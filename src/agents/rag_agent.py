
from src.llm_chain.chains import run_llm_without_context, run_llm_with_context
from src.tools.retreiver_tool import retrieve_context #@Tool
from src.agents.query_classifier import query_classification_for_retrieval
from src.agents.clarification_classifier import clarification_classifier

class QueryRoutingAgent:

    def __init__(self, top_k=3):
        self.top_k = top_k

    def run(self, user_query: str):

        # 1. Decide retrieve vs no-retrieve
        retrieval_result = query_classification_for_retrieval(user_query)
        retrieve_decision = retrieval_result["decision"]


        # 2. Decide clarification vs answer
        clarification_result = clarification_classifier(user_query)
        needs_clarification = clarification_result["needs_clarification"]

        if needs_clarification:
            return clarification_result["clarification_question"]

        # 3. Execute tools in correct order
        if retrieve_decision == "RETRIEVE":

            documents = retrieve_context(
                user_query=user_query,
                k=self.top_k
            )

            return run_llm_with_context(
                user_query=user_query,
                context=documents
            )

        return run_llm_without_context(user_query)



