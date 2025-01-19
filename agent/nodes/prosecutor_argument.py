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
system_prompt = """You are a prosecutor arguing in favor of the topic. 
Your goal is to present strong, logical arguments to support your position."""

prosecutor_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "Topic: {topic}"),
])

def prosecutor_argument(state: DebateState) -> DebateState:
    """
    Generates an argument in favor of the topic using the GROQ API.
    """
    # Initialize state if needed
    if "prosecutor_arguments" not in state:
        state["prosecutor_arguments"] = []
    if "metadata" not in state:
        state["metadata"] = {"round": 0, "current_speaker": "prosecutor"}

    # Generate the argument
    chain = prosecutor_prompt | llm
    argument_content = chain.invoke({"topic": state["topic"]}).content

    # Create a DebateMessage
    argument = DebateMessage(
        content=argument_content,
        speaker="prosecutor",
        confidence=0.8,  # Default confidence
        timestamp=datetime.now().isoformat()
    )

    # Add the argument to the state
    state["prosecutor_arguments"].append(argument)
    state["metadata"]["current_speaker"] = "defendant"
    state["metadata"]["round"] += 1
    
    return state