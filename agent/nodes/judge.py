from agent.state import DebateState
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
system_prompt = """You are a judge evaluating a debate. Your goal is to analyze both sides' arguments and provide a fair, well-reasoned judgment.
Consider the strength of arguments, logic, and evidence presented by both sides."""

judge_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", """Topic: {topic}

Prosecutor's Arguments:
{prosecutor_arguments}

Defendant's Arguments:
{defendant_arguments}

Please provide your judgment on this debate, considering the strength of both sides' arguments in not more than 5 to 6 sentences."""),
])

def judge(state: DebateState) -> DebateState:
    """
    Evaluates the debate and provides a judgment using the GROQ API.
    """
    # Format arguments for the prompt
    prosecutor_args = "\n".join([
        f"- {arg.content}" for arg in state["prosecutor_arguments"]
    ])
    defendant_args = "\n".join([
        f"- {arg.content}" for arg in state["defendant_arguments"]
    ])

    # Generate the judgment
    chain = judge_prompt | llm
    judgment = chain.invoke({
        "topic": state["topic"],
        "prosecutor_arguments": prosecutor_args,
        "defendant_arguments": defendant_args,
    }).content

    # Add the judgment to the state
    state["judgment"] = judgment
    state["metadata"]["current_speaker"] = "end"
    state["metadata"]["status"] = "completed"
    
    return state
