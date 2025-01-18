from typing import Literal
from agent.state import DebateState

def decide_judge_verdict(state: DebateState) -> Literal["end_debate", "prosecutor_argument"]:
    """
    Decides whether the judge's verdict is final or if the debate needs to continue.
    """
    # Example logic: If the judge has delivered a verdict, end the debate.
    if state["judgment"]:
        return "end_debate"
    else:
        return "prosecutor_argument"