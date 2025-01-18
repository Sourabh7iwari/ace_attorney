from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from agent.state import DebateState
import os

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
    # Generate the argument
    chain = prosecutor_prompt | llm
    argument = chain.invoke({"topic": state["topic"]}).content

    # Add the argument to the state
    state["prosecutor_arguments"].append(argument)
    return state