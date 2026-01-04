
from typing import TypedDict, Literal
from src.schema.message_schema import ConversationHistoryMessage

class StateSchema(TypedDict):
    original_user_query: str
    conversation_history: list[ConversationHistoryMessage]
    clarification_need: Literal["Yes", "No"]
    ambiguity_reason: str
    clarifications_asked_count: int
    consolidated_query: str | None
    ambiguity_score: float
    stop_reason: Literal["max_count_reached", "user_not_willing", "intent_clear"]
    
    retrieval_needed: Literal["RETRIEVE", "DONT_RETRIEVE"]
