
from typing import TypedDict, Literal, Annotated, List, Optional
from langgraph.graph.message import BaseMessage, add_messages

class RetrievedChunk(TypedDict):
    document: str
    metadata: dict
    distance: float

def merge_retrieved_data(left: List[RetrievedChunk], right: List[RetrievedChunk]) -> List[RetrievedChunk]:
    if not left: left = []
    if not right: right = []
    return left + right

class StateSchema(TypedDict):
    original_user_query: str #fixed value throughout state
    conversation_history: Annotated[list[BaseMessage], add_messages] #appends and merges upcoming new values, no override
    
    
    clarifications_asked_count: int # old value is updated here
    consolidated_query: str | None #created just ones
    
    clarification_need: Literal["Yes", "No"] #overrides and keeps either of them as value
    ambiguity_reason: str #add only once, not used multiple times, no override and no append
    ambiguity_score: float


    stop_reason: str
    
    retrieval_needed: Literal["RETRIEVE", "DONT_RETRIEVE"] #decided once for one iteration
    retreival_reasoning: str
    retrieved_data: Annotated[List[RetrievedChunk], merge_retrieved_data]


