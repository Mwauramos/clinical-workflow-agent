# Clinical Workflow Orchestrator

A multi-agent AI system for clinical decision support in East African health contexts. Four specialised agents collaborate using LangGraph to handle complete clinical scenarios from symptom intake to final recommendation with citations.

## Live Demo
https://clinical-workflow-agent-rxzywwzktk23ebkbpnjscc.streamlit.app/

## Agent Architecture

Patient Symptom Input
↓
Retrieval Agent searches clinical guidelines and WHO protocols
↓
Reasoning Agent generates structured differential diagnosis
↓
Validation Agent performs safety check and flags high-risk cases
↓
Human Review Gate escalates cases requiring physician oversight
↓
Recommendation Agent produces clinical handover document with citations


## What Each Agent Does

Retrieval Agent searches clinical guidelines, WHO protocols, and KEMRI recommendations relevant to the patient presentation. It provides structured clinical context grounded in East African health systems.

Reasoning Agent synthesises the retrieved guidelines into a differential diagnosis. For each condition it states probability, supporting clinical features, and what additional information would change the probability.

Validation Agent performs a safety check on the differential diagnosis. It identifies red flag symptoms, contraindications, and determines whether the case requires immediate physician review before any management decisions.

Human Review Gate is triggered when the validation agent flags a high-risk case. In production this node would pause the workflow and wait for a physician. In this demo it adds a review flag to the output.

Recommendation Agent generates a structured clinical handover document including most likely diagnosis, recommended investigations available in Kenya, first-line treatment per Kenya clinical guidelines, referral criteria, follow-up plan, and patient education points.

## Sample Cases Included

Paediatric malaria in Kisumu County — 4-year-old with fever, lethargy, pallor, no bed net use

TB suspect in Nairobi informal settlement — 32-year-old with cough, night sweats, weight loss, HIV positive

Maternal emergency in rural Turkana — 36-week pregnancy with severe headache, hypertension, 80km from referral hospital

## Tech Stack

LangGraph for stateful multi-agent orchestration
LangChain and LangChain OpenAI for LLM integration
OpenAI GPT-4o as the reasoning engine
Streamlit for the web interface
Python 3.11

## Responsible AI Statement

This system is for research and educational purposes only. It is not intended for clinical decision-making without physician oversight. Every case flagged as high-risk by the validation agent requires human physician review before any management decisions are made. The system does not replace clinical judgment.

## Portfolio Context

Project 5 of 12 in a Computational Epidemiology and Health Data Science portfolio under ZENIK.AI. This project demonstrates production-grade agentic AI architecture applied to East African health systems.

GitHub: github.com/Mwauramos | Contact: mwauramos.n@gmail.com