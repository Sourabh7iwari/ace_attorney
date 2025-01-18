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
system_prompt = """You are a judge evaluating a debate between a prosecutor and a defendant. 
Your goal is to evaluate the arguments and deliver a fair verdict."""

judge_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "Topic: {topic}\n\nProsecutor Arguments: {prosecutor_arguments}\n\nDefendant Arguments: {defendant_arguments}"),
])

def judge_evaluation(state: DebateState) -> DebateState:
    """
    Evaluates the arguments and delivers a verdict using the GROQ API.
    """
    # Prepare the input for the judge
    input_data = {
        "topic": state["topic"],
        "prosecutor_arguments": "\n".join(state["prosecutor_arguments"]),
        "defendant_arguments": "\n".join(state["defendant_arguments"]),
    }

    # Generate the verdict
    chain = judge_prompt | llm
    verdict = chain.invoke(input_data).content

    # Add the verdict to the state
    state["judgment"] = verdict
    return state