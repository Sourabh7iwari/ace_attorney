from langgraph.graph import StateGraph
from agent.state import create_initial_state, DebateState
from agent.nodes.prosecutor_argument import prosecutor_argument
from agent.nodes.defendant_argument import defendant_argument
from agent.nodes.judge import judge
from typing import Dict, Any, Annotated, TypedDict
from datetime import datetime

def should_continue(state: Dict[str, Any]) -> str:
    """Determine if we should continue the debate."""
    # Continue if we haven't reached a judgment
    if not state.get("judgment"):
        if state["metadata"]["round"] < 3:  # Maximum 3 rounds
            return "continue"
        else:
            return "judge"
    return "end"

def continue_or_judge(state: Dict[str, Any]) -> Dict[str, Any]:
    """Node that decides whether to continue the debate or move to judgment."""
    return state

def create_debate_graph() -> StateGraph:
    """Create the debate workflow graph."""
    
    # Create graph with state type annotation
    workflow = StateGraph(state_schema=DebateState)
    
    # Add nodes
    workflow.add_node("prosecutor", prosecutor_argument)
    workflow.add_node("defendant", defendant_argument)
    workflow.add_node("judge", judge)
    workflow.add_node("continue_or_judge", continue_or_judge)
    workflow.add_node("end", lambda x: x)
    
    # Add edges
    workflow.add_edge("prosecutor", "defendant")
    workflow.add_edge("defendant", "continue_or_judge")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "continue_or_judge",
        should_continue,
        {
            "continue": "prosecutor",
            "judge": "judge",
            "end": "end"
        }
    )
    
    # Set entry point
    workflow.set_entry_point("prosecutor")
    
    return workflow.compile()

# Create the graph
graph = create_debate_graph()

def start_debate(topic: str) -> Dict[str, Any]:
    """Start a new debate with the given topic."""
    try:
        # Create initial state
        initial_state = create_initial_state(topic)
        
        # Run the graph
        final_state = graph.invoke(initial_state)
        
        return {
            "topic": topic,
            "prosecutor_arguments": final_state["prosecutor_arguments"],
            "defendant_arguments": final_state["defendant_arguments"],
            "judgment": final_state.get("judgment"),
            "metadata": final_state["metadata"]
        }
    except Exception as e:
        print(f"Error in debate workflow: {str(e)}")
        raise