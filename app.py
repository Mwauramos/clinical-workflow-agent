# app.py
# Streamlit UI for Clinical Workflow Orchestrator
# ZENIK.AI — Computational Epidemiology Portfolio

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

st.set_page_config(
    page_title="Clinical Workflow Orchestrator",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Clinical Workflow Orchestrator")
st.markdown(
    "A multi-agent AI system for clinical decision support in East African "
    "health contexts. Four specialised agents collaborate to retrieve guidelines, "
    "generate differential diagnoses, validate safety, and produce recommendations."
)
st.divider()

# Agent flow diagram
st.markdown("### Agent Workflow")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.info("🔍 Retrieval\nAgent")
with col2:
    st.info("🧠 Reasoning\nAgent")
with col3:
    st.info("✅ Validation\nAgent")
with col4:
    st.warning("👨‍⚕️ Human Review\nGate")
with col5:
    st.success("📋 Recommendation\nAgent")

st.divider()

@st.cache_resource
def load_graph():
    from graph import build_clinical_graph
    return build_clinical_graph()

with st.spinner("Loading clinical workflow graph..."):
    graph = load_graph()

st.success("Clinical workflow ready.")

# Sample cases
SAMPLE_CASES = {
    "Paediatric Malaria — Kisumu": (
        "A 4-year-old child in Kisumu County presents with 3 days of fever "
        "reaching 39.5 degrees Celsius, poor feeding, and lethargy. "
        "The mother reports no bed net use. No prior malaria treatment. "
        "Child appears pale and mildly dehydrated on examination."
    ),
    "TB Suspect — Nairobi": (
        "A 32-year-old man from Kibera, Nairobi presents with 3 weeks of "
        "productive cough, night sweats, and 5kg weight loss over 2 months. "
        "He is HIV positive on ART. Sputum is blood-tinged. "
        "He lives with 6 family members in a single room."
    ),
    "Maternal Emergency — Rural Kenya": (
        "A 24-year-old woman at 36 weeks gestation presents to a rural health "
        "centre in Turkana County with sudden onset severe headache, visual "
        "disturbances, and upper abdominal pain. Blood pressure is 160/110. "
        "No antenatal care received. Nearest referral hospital is 80km away."
    )
}

st.markdown("**Select a sample case or describe your own:**")
sample = st.selectbox("Sample cases:", ["Describe my own"] + list(SAMPLE_CASES.keys()))

if sample != "Describe my own":
    default_text = SAMPLE_CASES[sample]
else:
    default_text = ""

patient_input = st.text_area(
    "Patient presentation:",
    value=default_text,
    height=150,
    placeholder="Describe the patient's symptoms, age, location, and relevant history..."
)

if st.button("Run Clinical Workflow", type="primary") and patient_input:

    initial_state = {
        "patient_input": patient_input,
        "retrieved_guidelines": "",
        "differential_diagnosis": "",
        "validation_result": "",
        "requires_human_review": False,
        "final_recommendation": "",
        "human_review_note": "",
        "agent_trace": []
    }

    with st.spinner("Running multi-agent clinical workflow..."):
        result = graph.invoke(initial_state)

    st.divider()

    # Agent trace
    st.markdown("### Agent Execution Trace")
    for step in result["agent_trace"]:
        if "human_review" in step:
            st.warning(f"⚠️ {step}")
        else:
            st.success(f"✅ {step}")

    # Human review flag
    if result.get("requires_human_review"):
        st.error(
            "⚠️ HUMAN REVIEW REQUIRED: This case has been flagged for "
            "physician review before any management decisions are made."
        )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Differential Diagnosis")
        st.markdown(result["differential_diagnosis"])

    with col2:
        st.markdown("### Safety Validation")
        st.markdown(result["validation_result"])

    st.markdown("### Final Clinical Recommendation")
    st.markdown(result["final_recommendation"])

    st.divider()
    st.caption(
        "ZENIK.AI · Clinical Workflow Orchestrator · "
        "For research and educational purposes only · "
        "Not for clinical decision-making without physician oversight"
    )