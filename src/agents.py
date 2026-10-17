# agents.py
# Individual agent definitions for the Clinical Workflow Orchestrator
# ZENIK.AI — Computational Epidemiology Portfolio

import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()


def get_llm(temperature=0.1):
    """Initialise the LLM used by all agents."""
    return ChatOpenAI(
        model="gpt-4o",
        temperature=temperature,
        api_key=os.getenv("OPENAI_API_KEY")
    )


def retrieval_agent(state: dict) -> dict:
    """Retrieves relevant clinical guidelines based on patient symptoms."""
    llm = get_llm()

    messages = [
        SystemMessage(content="""You are a clinical guidelines retrieval specialist
        for East African health systems. Your job is to identify and summarise
        the most relevant clinical guidelines, WHO protocols, and KEMRI recommendations
        for the symptoms presented. Focus on:
        - Relevant disease possibilities based on symptoms
        - Standard diagnostic criteria used in Kenya
        - First-line investigation protocols
        Format your response as structured clinical context."""),
        HumanMessage(content=f"Patient presentation: {state['patient_input']}\n\nRetrieve relevant clinical guidelines.")
    ]

    response = llm.invoke(messages)
    print(f"[Retrieval Agent] Guidelines retrieved.")

    return {
        **state,
        "retrieved_guidelines": response.content,
        "agent_trace": state.get("agent_trace", []) + ["retrieval_agent completed"]
    }


def reasoning_agent(state: dict) -> dict:
    """Synthesises guidelines into a differential diagnosis."""
    llm = get_llm()

    messages = [
        SystemMessage(content="""You are a clinical reasoning specialist working
        in an East African health context. Based on the patient presentation and
        retrieved guidelines, generate a differential diagnosis. For each condition:
        - State the probability (high, moderate, low)
        - List the supporting clinical features
        - Identify what additional information would change the probability
        Format as a structured differential diagnosis list."""),
        HumanMessage(content=f"""Patient presentation: {state['patient_input']}

Clinical guidelines: {state['retrieved_guidelines']}

Generate a differential diagnosis.""")
    ]

    response = llm.invoke(messages)
    print(f"[Reasoning Agent] Differential diagnosis generated.")

    return {
        **state,
        "differential_diagnosis": response.content,
        "agent_trace": state.get("agent_trace", []) + ["reasoning_agent completed"]
    }


def validation_agent(state: dict) -> dict:
    """Checks for contraindications, safety issues, and flags high-risk cases."""
    llm = get_llm()

    messages = [
        SystemMessage(content="""You are a clinical safety validation specialist.
        Your role is to:
        1. Check for any red flag symptoms requiring immediate escalation
        2. Identify potential contraindications in the proposed differential
        3. Flag cases requiring human physician review
        4. Assess whether the case is safe to handle at primary care level

        Respond with:
        SAFETY_LEVEL: [SAFE / CAUTION / ESCALATE]
        RED_FLAGS: [list any red flag symptoms]
        CONTRAINDICATIONS: [list any concerns]
        RECOMMENDATION: [brief recommendation]
        REQUIRES_HUMAN_REVIEW: [YES / NO]"""),
        HumanMessage(content=f"""Patient presentation: {state['patient_input']}

Differential diagnosis: {state['differential_diagnosis']}

Perform safety validation.""")
    ]

    response = llm.invoke(messages)
    requires_review = "REQUIRES_HUMAN_REVIEW: YES" in response.content.upper()
    print(f"[Validation Agent] Safety check complete. Human review required: {requires_review}")

    return {
        **state,
        "validation_result": response.content,
        "requires_human_review": requires_review,
        "agent_trace": state.get("agent_trace", []) + ["validation_agent completed"]
    }


def recommendation_agent(state: dict) -> dict:
    """Generates final clinical recommendation with case-specific medication guidance."""
    llm = get_llm()

    messages = [
        SystemMessage(content="""You are a clinical recommendation specialist
        for primary and secondary care in Kenya. Generate a final structured
        clinical recommendation that includes:

        1. Most likely diagnosis with confidence level
        2. Recommended investigations (with availability in Kenya context)
        3. First-line treatment options following Kenya Standard Treatment Guidelines 2022
        4. Possible medications suited to this specific case
           - List medications from the Kenya Standard Treatment Guidelines
           - Include typical dosage ranges for the patient's age and weight where relevant
           - Note any case-specific factors that influence medication choice
             (e.g. age under 5, pregnancy, HIV status, severity indicators)
           - End this section with: "Medication selection, exact dosage, and
             duration must be confirmed by a licensed clinician based on full
             patient assessment."
        5. Referral criteria
        6. Follow-up plan
        7. Patient and caregiver education points

        Always cite the Kenya Standard Treatment Guidelines or relevant WHO
        protocol as the source for each medication mentioned.
        Format professionally for a clinical handover document."""),
        HumanMessage(content=f"""Patient presentation: {state['patient_input']}

Guidelines consulted: {state['retrieved_guidelines'][:500]}...

Differential diagnosis: {state['differential_diagnosis'][:500]}...

Safety validation: {state['validation_result']}

Generate final clinical recommendation with case-specific medication guidance.""")
    ]

    response = llm.invoke(messages)
    print(f"[Recommendation Agent] Final recommendation with medication guidance generated.")

    return {
        **state,
        "final_recommendation": response.content,
        "agent_trace": state.get("agent_trace", []) + ["recommendation_agent completed"]
    }