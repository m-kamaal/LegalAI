from langchain.agents import initialize_agent, create_react_agent
from src.llm_chain.llm_builder import get_llm_model


llm_model = get_llm_model()

agent = create_react_agent()