from typing import TypedDict, Literal

class ConversationHistoryMessage:

    role:Literal["user","assistant"]
    message: str



