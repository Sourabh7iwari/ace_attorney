from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from agent.state import DebateState
from agent.nodes import prosecutor_argument, defendant_argument, judge_evaluation
from agent.edges import decide_prosecutor_argument, decide_defendant_argument, decide_judge_verdict

# Define the workflow
workflow = StateGraph(DebateState)

# Add nodes
workflow.add_node("prosecutor_argument", prosecutor_argument)
workflow.add_node("defendant_argument", defendant_argument)
workflow.add_node("judge_evaluation", judge_evaluation)

# Add edges
workflow.add_conditional_edges(
    "prosecutor_argument",
    decide_prosecutor_argument,
    {
        "defendant_argument": "defendant_argument",  # Proceed to defendant if prosecutor's argument is strong
        "prosecutor_argument": "prosecutor_argument",  # Retry prosecutor's argument if weak
    },
)

workflow.add_conditional_edges(
    "defendant_argument",
    decide_defendant_argument,
    {
        "judge_evaluation": "judge_evaluation",  # Proceed to judge if defendant's argument is strong
        "defendant_argument": "defendant_argument",  # Retry defendant's argument if weak
    },
)

workflow.add_conditional_edges(
    "judge_evaluation",
    decide_judge_verdict,
    {
        "end_debate": END,  # End the debate if the judge delivers a verdict
        "prosecutor_argument": "prosecutor_argument",  # Restart the debate if the verdict is unclear
    },
)

# Set the entry point
workflow.set_entry_point("prosecutor_argument")

# Compile the workflow
graph = workflow.compile(checkpointer=MemorySaver())