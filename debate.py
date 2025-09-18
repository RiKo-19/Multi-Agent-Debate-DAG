import logging
import os
import re
from typing import TypedDict, List, Optional

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from graphviz import Digraph

# Load Environment Variables
load_dotenv()
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found. Please set it in your .env file.")

# Setup Logging
logging.basicConfig(
    filename="debate.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

# LLM Setup
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=OPENROUTER_API_KEY,
    base_url=OPENAI_API_BASE,
    temperature=0.7,
    max_tokens=1024
)

# TypedDict Debate State
class DebateState(TypedDict):
    topic: str
    round: int
    history: List[str]
    memory: str
    winner: Optional[str]
    judge_summary: Optional[str]


# Memory Node
def memory_node(state: DebateState) -> DebateState:
    """Update memory with a running summary of debate"""
    history = state.get("history", [])
    if not history:
        state["memory"] = "No debate history yet."
        return state

    debate_text = "\n".join(history)
    prompt = (
        f"Summarize the debate so far in 3–4 sentences, focusing on key points.\n"
        f"Debate so far:\n{debate_text}"
    )
    summary = llm.invoke(prompt).content

    logging.info(f"[Memory] Updated summary: {summary}")
    state["memory"] = summary
    return state


# State Validation Helper
def validate_state(state: DebateState, expected_role: str):
    """Ensure correct turn-taking and no repeated arguments"""
    history = state.get("history", [])
    if history:
        last_speaker = history[-1].split(":")[0]
        if expected_role in last_speaker:
            raise ValueError(f"Invalid turn: {expected_role} spoke twice in a row!")

    if len(history) != len(set(history)):
        raise ValueError("Repeated argument detected in debate history!")


# User Input Node
def user_input_node(state: DebateState) -> DebateState:
    topic = input("Enter topic for debate: ")
    logging.info(f"Debate Topic: {topic}")
    print(f"Starting debate between Scientist and Philosopher on: {topic}\n")

    state.update({
        "topic": topic,
        "round": 0,
        "history": [],
        "memory": "",
        "winner": None,
        "judge_summary": None,
    })
    return state


# Agent Nodes
def agent_a_node(state: DebateState) -> DebateState:
    validate_state(state, "Scientist")

    state["round"] += 1
    round_no = state["round"]

    topic = state["topic"]
    context = state.get("memory", "")

    logging.info(f"--- Scientist speaking (Round {round_no}) ---")
    print(f"--- Round {round_no} ---")

    prompt = PromptTemplate(
        input_variables=["topic", "context"],
        template=(
            "You are a Scientist debating on the topic: {topic}.\n"
            "Argue with facts, evidence, and logic.\n"
            "Context: {context}\n\n"
            "Now give your next argument (1–2 sentences)."
        )
    )
    response = llm.invoke(prompt.format(topic=topic, context=context)).content
    argument = f"[Round {round_no}] Scientist: {response}"

    print(argument)
    logging.info(argument)

    state["history"].append(argument)
    return state

def agent_b_node(state: DebateState) -> DebateState:
    validate_state(state, "Philosopher")

    state["round"] += 1
    round_no = state["round"]

    topic = state["topic"]
    context = state.get("memory", "")

    logging.info(f"--- Philosopher speaking (Round {round_no}) ---")
    print(f"--- Round {round_no} ---")

    prompt = PromptTemplate(
        input_variables=["topic", "context"],
        template=(
            "You are a Philosopher debating on the topic: {topic}.\n"
            "Argue with reasoning, ethics, and philosophy.\n"
            "Context: {context}\n\n"
            "Now give your next counter-argument (1–2 sentences)."
        )
    )
    response = llm.invoke(prompt.format(topic=topic, context=context)).content
    argument = f"[Round {round_no}] Philosopher: {response}"

    print(argument)
    logging.info(argument)

    state["history"].append(argument)
    return state


# Judge Node
def judge_node(state: DebateState) -> DebateState:
    print("\n[Judge] Reviewing debate...")
    logging.info("[Judge] Reviewing debate...")

    debate_text = "\n".join(state["history"])
    topic = state["topic"]

    prompt = (
        f"You are the judge of a debate on '{topic}'.\n"
        "Here is the full debate:\n"
        f"{debate_text}\n\n"
        "Task:\n"
        "1. Summarize the debate.\n"
        "2. Explicitly declare the winner in this format: 'Winner: Scientist' or 'Winner: Philosopher'.\n"
        "3. Justify your decision clearly."
    )
    response = llm.invoke(prompt).content

    print(response)
    logging.info(f"[Judge] {response}")

    match = re.search(r"Winner:\s*(Scientist|Philosopher)", response, re.IGNORECASE)
    if match:
        state["winner"] = match.group(1).capitalize()
    else:
        state["winner"] = "Undecided"

    state["judge_summary"] = response
    return state


# DAG Diagram Generator
def generate_dag_diagram(state: DebateState):
    dot = Digraph()

    dot.node("U", "UserInput")
    dot.node("A", "Agent A (Scientist)")
    dot.node("M", "Memory")
    dot.node("B", "Agent B (Philosopher)")
    dot.node("J", "Judge")

    winner_label = state["winner"] if state.get("winner") else "Undecided"
    dot.node("W", f"Winner: {winner_label}", shape="box", style="filled", color="lightgreen")

    dot.edges([("U", "A"), ("A", "M"), ("M", "B"), ("B", "M"), ("M", "A"), ("A", "J"), ("B", "J")])
    dot.edge("J", "W")

    with open("dag_diagram.dot", "w") as f:
        f.write(dot.source)

    print("\n DAG diagram saved as dag_diagram.dot")


# Graph Construction
def build_graph() -> CompiledStateGraph:
    workflow = StateGraph(DebateState)

    workflow.add_node("UserInput", user_input_node)
    workflow.add_node("AgentA", agent_a_node)
    workflow.add_node("AgentB", agent_b_node)
    workflow.add_node("Memory", memory_node)
    workflow.add_node("Judge", judge_node)

    workflow.set_entry_point("UserInput")
    workflow.add_edge("UserInput", "AgentA")

    workflow.add_conditional_edges(
        "AgentA",
        lambda state: "Judge" if state["round"] >= 8 else "Memory",
        {"Judge": "Judge", "Memory": "Memory"},
    )
    workflow.add_conditional_edges(
        "AgentB",
        lambda state: "Judge" if state["round"] >= 8 else "Memory",
        {"Judge": "Judge", "Memory": "Memory"},
    )

    workflow.add_conditional_edges(
        "Memory",
        lambda state: "AgentB" if state["round"] % 2 == 1 else "AgentA",
        {"AgentA": "AgentA", "AgentB": "AgentB"},
    )

    workflow.add_edge("Judge", END)
    return workflow.compile()


# Main Execution
if __name__ == "__main__":
    graph = build_graph()
    initial_state: DebateState = {
        "topic": "",
        "round": 0,
        "history": [],
        "memory": "",
        "winner": None,
        "judge_summary": None,
    }
    final_state = graph.invoke(initial_state)
    generate_dag_diagram(final_state)