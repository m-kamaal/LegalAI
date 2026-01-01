
from typing import TypedDict
from src.schema.message_schema import ConversationHistoryMessage

class StateSchema(TypedDict):
    original_user_query: str
    conversation_history: list[ConversationHistoryMessage]
    clarification_need: bool
    ambiguity_reason: str
    clarifications_asked_count: int
    consolidated_query: str | None
    ambiguity_score: float
    stop_reason: str | None
