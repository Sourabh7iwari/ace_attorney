from typing import Literal
from agent.state import DebateState

def decide_prosecutor_argument(state: DebateState) -> Literal["defendant_argument", "prosecutor_argument"]:
    """
    Decides whether the prosecutor's argument is strong enough to proceed.
    """
    # Example logic: If the prosecutor has presented at least one argument, proceed to the defendant.
    if len(state["prosecutor_arguments"]) > 0:
        return "defendant_argument"
    else:
        return "prosecutor_argument"