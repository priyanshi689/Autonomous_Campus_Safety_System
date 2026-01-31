from agents.intake_agent import IncidentIntakeAgent
from agents.risk_agent import RiskEvaluationAgent
from agents.response_agent import ResponsePlanningAgent
from agents.audit_agent import TrustAuditAgent

from core.config_loader import CampusConfigLoader


# 🔒 Single-point deployment switch
DEFAULT_CAMPUS_CONFIG = "config/gla_university.json"


class CoordinatorAgent:
    """
    CoordinatorAgent
    ----------------
    Orchestrates the full multi-agent campus safety pipeline.

    Responsibilities:
    - Load campus configuration once
    - Inject configuration into all agents
    - Maintain standardized AI core behavior
    """

    def __init__(self, campus_config_path: str = DEFAULT_CAMPUS_CONFIG):
        # Load campus configuration (deployment layer)
        self.config_loader = CampusConfigLoader(campus_config_path)
        self.campus_config = self.config_loader.get_full_config()

        # Initialize standardized AI agents (core logic)
        self.intake_agent = IncidentIntakeAgent()
        self.risk_agent = RiskEvaluationAgent()
        self.response_agent = ResponsePlanningAgent()
        self.audit_agent = TrustAuditAgent()

    def process_incident(self, payload: dict):
        """
        Executes the complete AI pipeline for a single incident.
        """

        # 1️⃣ Incident Intake (privacy + structure)
        intake_result = self.intake_agent.handle_incident(
            payload,
            campus_config=self.campus_config
        )

        # 2️⃣ Risk Evaluation (config-driven risk zones & timing)
        risk_result = self.risk_agent.evaluate_risk(
            intake_result,
            campus_config=self.campus_config
        )

        # 3️⃣ Response Planning (policy-driven escalation)
        response_result = self.response_agent.plan_response(
            intake_result,
            risk_result,
            campus_config=self.campus_config
        )

        # 4️⃣ Trust & Audit (governance & explainability)
        audit_result = self.audit_agent.audit_decision(
            intake_result,
            risk_result,
            response_result,
            campus_config=self.campus_config
        )

        return audit_result


# 🔌 UI / API wrapper (used by Streamlit or other frontends)
def run_pipeline(incident_text: str, location: str, user_role: str):
    """
    Entry point for UI or API.
    Keeps UI completely decoupled from AI internals.
    """

    coordinator = CoordinatorAgent()

    payload = {
        "source": user_role,
        "description": incident_text,
        "location": location,
        "anonymous": False  # UI can toggle this later if needed
    }

    audit_result = coordinator.process_incident(payload)

    return {
        "final": audit_result,
        "campus": coordinator.config_loader.get_campus_name(),
        "emergency_contacts": coordinator.config_loader.get_emergency_contacts()
    }


# 🧪 Optional CLI demo (for testing without Streamlit)
def demo_run():
    coordinator = CoordinatorAgent()

    sample_payload = {
        "source": "Student",
        "description": "Someone is following me near the girls hostel at night",
        "location": "Girls Hostel A",
        "anonymous": True
    }

    result = coordinator.process_incident(sample_payload)

    print("\n===== FINAL AI OUTPUT =====")
    print("Decision      :", result.final_decision)
    print("Risk Level    :", result.risk_level)
    print("Confidence    :", result.confidence_level)
    print("Escalation    :", result.escalation_chain)
    print("Explanation   :", result.explanation)
