from enum import Enum


class AgentType(str, Enum):
    ZERO_SHORT_REACT_DESCRIPTION = "zero-shot-react-description"
    CHAT_ZERO_SHOT_REACT_DESCRIPTION = "chat-zero-shot-react-description"
    SELF_ASK_WITH_SEARCH = "self-ask-with-search"
    REACT_DOCSTORE = "react-docstore"
    CONVERSATIONAL_REACT_DESCRIPTION = "conversational-react-description"
    CHAT_CONVERSATIONAL_REACT_DESCRIPTION = "chat-conversational-react-description"
