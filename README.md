# 🛡️ Autonomous Campus Safety Intelligence System

A **config-driven, multi-agent AI system** designed to enhance **campus safety** through intelligent incident intake, risk evaluation, response planning, and governance-aware auditing.

This project was built for **AGENT-A-THON (AI for Safety Track)** and focuses on **Campus Incident Reporting & Risk Evaluation**.

---

## 🚀 Key Highlights

- **Multi-Agent Architecture**
  - Incident Intake Agent
  - Risk Evaluation Agent
  - Response Planning Agent
  - Trust & Audit Agent

- **Config-Driven Design**
  - Campus-specific behavior controlled via JSON configuration
  - Same AI core can adapt to different universities **without code changes**

- **Human-in-the-Loop Safety**
  - AI provides decision support
  - Final authority remains with human responders

- **Explainable AI**
  - Clear reasoning for every decision
  - Transparent escalation logic

- **Demo-Ready UI**
  - Dark-mode Streamlit dashboard
  - Real-time agent flow visualization
  - Emergency actions highlighted for high-risk cases

---

## 🧠 System Architecture
User Input
↓
Incident Intake Agent
↓
Risk Evaluation Agent
↓
Response Planning Agent
↓
Trust & Audit Agent
↓
Final Decision + Explanation

## 🗂️ Project Structure
Agentathon/
├── app/
│ └── streamlit_app.py # Streamlit UI (final demo)
│
├── backend/
│ ├── agents/ # Autonomous agents
│ │ ├── intake_agent.py
│ │ ├── risk_agent.py
│ │ ├── response_agent.py
│ │ └── audit_agent.py
│ │
│ ├── core/ # Orchestration & config loading
│ │ ├── coordinator.py
│ │ └── config_loader.py
│ │
│ ├── config/ # Campus configuration (JSON)
│ │ └── gla_university.json
│ │
│ └── tests/ # Basic pipeline tests
│
├── requirements.txt
└── README.md

