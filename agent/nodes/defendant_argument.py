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
system_prompt = """You are a defendant arguing against the topic. 
Your goal is to present strong, logical counter-arguments to oppose the prosecutor's position."""

defendant_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "Topic: {topic}"),
])

def defendant_argument(state: DebateState) -> DebateState:
    """
    Generates a counter-argument against the topic using the GROQ API.
    """
    # Generate the counter-argument
    chain = defendant_prompt | llm
    argument = chain.invoke({"topic": state["topic"]}).content

    # Add the counter-argument to the state
    state["defendant_arguments"].append(argument)
    return state