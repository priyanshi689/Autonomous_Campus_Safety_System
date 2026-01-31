from dataclasses import dataclass
from typing import Any, List


@dataclass
class ResponseResult:
    recommended_action: str
    priority_level: str
    escalation_chain: List[str]


class ResponsePlanningAgent:
    """
    Response Planning Agent (Executor)
    ----------------------------------
    Converts risk + policy into actionable escalation steps.
    """

    def __init__(self, agent_name: str = "ResponsePlanningAgent"):
        self.agent_name = agent_name

    def plan_response(
        self,
        incident_result: Any,
        risk_result: Any,
        campus_config: dict
    ) -> ResponseResult:

        # -------------------------
        # Determine incident category
        # -------------------------
        incident_type = incident_result.incident_type.lower()

        policy_map = campus_config.get("incident_policies", {})

        # Normalize mapping
        if "fire" in incident_type:
            policy_key = "fire"
        elif "harass" in incident_type:
            policy_key = "harassment"
        elif "medical" in incident_type:
            policy_key = "medical"
        elif "unauthorized" in incident_type or "theft" in incident_type:
            policy_key = "theft"
        elif "lab" in incident_type:
            policy_key = "lab_hazard"
        else:
            policy_key = None

        escalation_chain = policy_map.get(policy_key, [])

        # -------------------------
        # Priority based on risk
        # -------------------------
        if risk_result.risk_level == "High":
            priority = "Immediate"
            action = "Immediate escalation as per campus safety policy"
        elif risk_result.risk_level == "Medium":
            priority = "High"
            action = "Notify responsible authorities and monitor"
        else:
            priority = "Normal"
            action = "Log incident and monitor as per policy"

        return ResponseResult(
            recommended_action=action,
            priority_level=priority,
            escalation_chain=escalation_chain
        )
