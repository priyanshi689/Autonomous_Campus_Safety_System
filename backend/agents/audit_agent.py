from dataclasses import dataclass
from typing import Any, List


@dataclass
class AuditResult:
    final_decision: str
    risk_level: str
    confidence_level: str
    escalation_chain: List[str]
    explanation: str


class TrustAuditAgent:
    """
    Trust & Audit Agent (Evaluator)
    -------------------------------
    Ensures transparency, governance compliance,
    and human accountability.
    """

    def __init__(self, agent_name: str = "TrustAuditAgent"):
        self.agent_name = agent_name

    def audit_decision(
        self,
        incident_result: Any,
        risk_result: Any,
        response_result: Any,
        campus_config: dict
    ) -> AuditResult:

        governance = campus_config.get("governance", {})

        explanation = (
            f"Incident '{incident_result.incident_type}' was reported at "
            f"'{incident_result.location}'. "
            f"The system assessed the risk as '{risk_result.risk_level}' based on "
            f"campus-defined risk zones, operating hours, and input confidence. "
            f"According to university safety policy, the following authorities "
            f"are responsible for handling this incident: "
            f"{', '.join(response_result.escalation_chain)}. "
            f"Final responsibility and action remain with designated "
            f"university officials and emergency responders."
        )

        return AuditResult(
            final_decision=response_result.recommended_action,
            risk_level=risk_result.risk_level,
            confidence_level=incident_result.confidence_level,
            escalation_chain=response_result.escalation_chain,
            explanation=explanation
        )
