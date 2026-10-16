# graph.py
# LangGraph state machine orchestrating the clinical workflow
# ZENIK.AI — Computational Epidemiology Portfolio

from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from agents import (
    retrieval_agent,
    reasoning_agent,
    validation_agent,
    recommendation_agent
)

# ── What this does ──────────────────────────────────────────────────────────
# StateGraph defines the workflow as a directed graph.
# Each node is an agent. Edges define the flow between agents.
# A conditional edge routes to human review or directly to recommendation
# based on the validation agent's safety assessment.
# ────────────────────────────────────────────────────────────────────────────

class ClinicalState(TypedDict):
    """The state object passed between all agents."""
    patient_input: str
    retrieved_guidelines: str
    differential_diagnosis: str
    validation_result: str
    requires_human_review: bool
    final_recommendation: str
    human_review_note: str
    agent_trace: List[str]


def human_review_node(state: ClinicalState) -> ClinicalState:
    """
    Human-in-the-loop gate.
    In production this would pause and wait for a physician.
    In this demo it flags the case and adds a review note.
    """
    print("[Human Review Gate] Case flagged for physician review.")
    return {
        **state,
        "human_review_note": (
            "FLAGGED FOR PHYSICIAN REVIEW: This case contains red flag symptoms "
            "or high-risk features requiring senior clinical oversight before "
            "any management decisions are made."
        ),
        "agent_trace": state.get("agent_trace", []) + ["human_review_gate triggered"]
    }


def should_escalate(state: ClinicalState) -> str:
    """
    Conditional routing function.
    Returns 'escalate' if human review needed, 'recommend' otherwise.
    """
    if state.get("requires_human_review", False):
        return "escalate"
    return "recommend"


def build_clinical_graph():
    """Build and compile the clinical workflow graph."""
    
    workflow = StateGraph(ClinicalState)
    
    # Add nodes — each node is one agent
    workflow.add_node("retrieval", retrieval_agent)
    workflow.add_node("reasoning", reasoning_agent)
    workflow.add_node("validation", validation_agent)
    workflow.add_node("human_review", human_review_node)
    workflow.add_node("recommendation", recommendation_agent)
    
    # Define the flow
    workflow.set_entry_point("retrieval")
    workflow.add_edge("retrieval", "reasoning")
    workflow.add_edge("reasoning", "validation")
    
    # Conditional routing after validation
    workflow.add_conditional_edges(
        "validation",
        should_escalate,
        {
            "escalate": "human_review",
            "recommend": "recommendation"
        }
    )
    
    # Both paths lead to recommendation
    workflow.add_edge("human_review", "recommendation")
    workflow.add_edge("recommendation", END)
    
    graph = workflow.compile()
    print("Clinical workflow graph compiled successfully.")
    return graph


if __name__ == "__main__":
    graph = build_clinical_graph()
    
    # Test with a sample clinical scenario
    test_input = {
        "patient_input": (
            "A 4-year-old child in Kisumu County presents with 3 days of fever "
            "reaching 39.5 degrees Celsius, poor feeding, and lethargy. "
            "The mother reports no bed net use. No prior malaria treatment. "
            "Child appears pale and mildly dehydrated on examination."
        ),
        "retrieved_guidelines": "",
        "differential_diagnosis": "",
        "validation_result": "",
        "requires_human_review": False,
        "final_recommendation": "",
        "human_review_note": "",
        "agent_trace": []
    }
    
    print("\nRunning clinical workflow...")
    print("="*60)
    
    result = graph.invoke(test_input)
    
    print("\n" + "="*60)
    print("AGENT TRACE:")
    for step in result["agent_trace"]:
        print(f"  → {step}")
    
    print("\nFINAL RECOMMENDATION:")
    print(result["final_recommendation"])
    
    print("\nGraph test complete.")