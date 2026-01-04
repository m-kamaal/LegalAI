from typing import TypedDict, Literal

class ConversationHistoryMessage(TypedDict):

    role:Literal["user","assistant"]
    message: str



