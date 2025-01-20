from agent.state import DebateState, DebateMessage
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize the GROQ client
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

# Define the prompt template
system_prompt = """You are a calm and compose defense attorney arguing against the topic. 
Your goal is to present strong, logical counter-arguments to challenge the prosecutor's position.
Argument should not be more than 3 sentences."""

defendant_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", """Topic: {topic}
Prosecutor's Argument: {prosecutor_argument}

Please provide a strong counter-argument."""),
])

def defendant_argument(state: DebateState) -> DebateState:
    """
    Generates a counter-argument against the topic using the GROQ API.
    """
    # Initialize state if needed
    if "defendant_arguments" not in state:
        state["defendant_arguments"] = []
    if "metadata" not in state:
        state["metadata"] = {"round": 0, "current_speaker": "defendant"}

    # Get the latest prosecutor argument
    latest_prosecutor_arg = state["prosecutor_arguments"][-1].content if state["prosecutor_arguments"] else "No prosecutor argument provided."

    # Generate the counter-argument
    chain = defendant_prompt | llm
    argument_content = chain.invoke({
        "topic": state["topic"],
        "prosecutor_argument": latest_prosecutor_arg,
    }).content

    # Create a DebateMessage
    argument = DebateMessage(
        content=argument_content,
        speaker="defendant",
        confidence=0.8,  # Default confidence
        timestamp=datetime.now().isoformat()
    )

    # Add the argument to the state
    state["defendant_arguments"].append(argument)
    state["metadata"]["current_speaker"] = "judge"
    
    return state