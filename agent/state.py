from typing import List, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class DebateState(TypedDict):
    """
    Represents the state of the Ace Attorney workflow.

    Attributes:
        topic: The topic of the debate.
        prosecutor_arguments: List of arguments from the prosecutor.
        defendant_arguments: List of arguments from the defendant.
        judgment: The final judgment from the judge.
        messages: List of messages for context (used for LangGraph message passing).
    """
    topic: str  # The topic of the debate (e.g., "Should AI be regulated?")
    prosecutor_arguments: List[str]  # Arguments presented by the prosecutor
    defendant_arguments: List[str]  # Counter-arguments presented by the defendant
    judgment: str  # The final verdict delivered by the judge
    messages: List[BaseMessage]  # List of messages for context (used by LangGraph)