from backend.agents.intake_agent import IncidentIntakeAgent
from backend.agents.risk_agent import RiskEvaluationAgent
from backend.agents.response_agent import ResponsePlanningAgent
from backend.agents.audit_agent import TrustAuditAgent

from backend.core.config_loader import CampusConfigLoader

DEFAULT_CAMPUS_CONFIG = "backend/config/gla_university.json"


class CoordinatorAgent:
    """
    Orchestrates the full multi-agent campus safety pipeline.
    """

    def __init__(self, campus_config_path: str = DEFAULT_CAMPUS_CONFIG):
        self.config_loader = CampusConfigLoader(campus_config_path)
        self.campus_config = self.config_loader.get_full_config()

        self.intake_agent = IncidentIntakeAgent()
        self.risk_agent = RiskEvaluationAgent()
        self.response_agent = ResponsePlanningAgent()
        self.audit_agent = TrustAuditAgent()

    def process_incident(self, payload: dict):
        intake_result = self.intake_agent.handle_incident(
            payload, campus_config=self.campus_config
        )

        risk_result = self.risk_agent.evaluate_risk(
            intake_result, campus_config=self.campus_config
        )

        response_result = self.response_agent.plan_response(
            intake_result, risk_result, campus_config=self.campus_config
        )

        audit_result = self.audit_agent.audit_decision(
            intake_result,
            risk_result,
            response_result,
            campus_config=self.campus_config
        )

        return audit_result


def run_pipeline(incident_text: str, location: str, user_role: str):
    coordinator = CoordinatorAgent()

    payload = {
        "source": user_role,
        "description": incident_text,
        "location": location,
        "anonymous": False,
    }

    audit_result = coordinator.process_incident(payload)

    return {
        "final": audit_result,
        "campus": coordinator.config_loader.get_campus_name(),
        "emergency_contacts": coordinator.config_loader.get_emergency_contacts(),
    }
