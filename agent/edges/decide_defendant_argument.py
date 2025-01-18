from typing import Literal
from agent.state import DebateState

def decide_defendant_argument(state: DebateState) -> Literal["judge_evaluation", "defendant_argument"]:
    """
    Decides whether the defendant's counter-argument is strong enough to proceed.
    """
    # Example logic: If the defendant has presented at least one counter-argument, proceed to the judge.
    if len(state["defendant_arguments"]) > 0:
        return "judge_evaluation"
    else:
        return "defendant_argument"