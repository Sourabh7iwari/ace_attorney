from fastapi import FastAPI
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from state import DebateState
from nodes import prosecutor_argument, defendant_argument, judge_evaluation
from edges import decide_prosecutor_argument, decide_defendant_argument, decide_judge_verdict
from workflow import graph  # Import the compiled workflow
import uvicorn
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Initialize FastAPI app
app = FastAPI()

# Define the agent
class AceAttorneyAgent:
    def __init__(self):
        """
        Initializes the Ace Attorney agent with the compiled workflow.
        """
        self.workflow = graph

    async def run(self, topic: str) -> DebateState:
        """
        Runs the Ace Attorney workflow for a given topic.

        Args:
            topic: The topic of the debate (e.g., "Should AI be regulated?").

        Returns:
            The final state of the debate, including arguments and judgment.
        """
        # Initialize the state
        state: DebateState = {
            "topic": topic,
            "prosecutor_arguments": [],
            "defendant_arguments": [],
            "judgment": "",
            "messages": [],
        }

        # Run the workflow
        final_state = await self.workflow.arun(state)
        return final_state

# Initialize the agent
agent = AceAttorneyAgent()

# Define FastAPI endpoints
@app.post("/debate")
async def debate(topic: str):
    """
    Endpoint to start a debate on a given topic.

    Args:
        topic: The topic of the debate (e.g., "Should AI be regulated?").

    Returns:
        The final state of the debate, including arguments and judgment.
    """
    result = await agent.run(topic)
    return result

# Run the FastAPI server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)