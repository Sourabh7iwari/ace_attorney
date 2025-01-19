from typing import List, TypedDict, Optional, Dict, Any
from langchain_core.messages import BaseMessage
from pydantic import BaseModel
from datetime import datetime

class DebateMessage(BaseModel):
    """Single debate message with metadata"""
    content: str
    speaker: str
    confidence: float
    timestamp: str = datetime.now().isoformat()
    references: Optional[List[str]] = None

class DebateState(TypedDict):
    """
    Represents the state of the Ace Attorney workflow.

    Attributes:
        topic: The topic of the debate.
        prosecutor_arguments: List of arguments from the prosecutor.
        defendant_arguments: List of arguments from the defendant.
        judgment: The final judgment from the judge.
        messages: List of messages for context.
        metadata: Additional debate metadata.
    """
    topic: str
    prosecutor_arguments: List[DebateMessage]
    defendant_arguments: List[DebateMessage]
    judgment: Optional[str]
    messages: List[BaseMessage]
    metadata: Dict[str, Any]  # For tracking debate progress, rounds, etc.

def create_initial_state(topic: str) -> DebateState:
    """Create an initial debate state with the given topic."""
    return {
        "topic": topic,
        "prosecutor_arguments": [],
        "defendant_arguments": [],
        "judgment": None,
        "messages": [],
        "metadata": {
            "round": 0,
            "current_speaker": "prosecutor",
            "start_time": datetime.now().isoformat(),
            "status": "in_progress"
        }
    }