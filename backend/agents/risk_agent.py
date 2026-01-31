from dataclasses import dataclass
from typing import Any
from datetime import datetime


@dataclass
class RiskResult:
    risk_score: int
    risk_level: str
    reason: str


class RiskEvaluationAgent:
    """
    Risk Evaluation Agent (Planner)
    -------------------------------
    Risk logic is standardized.
    Campus-specific behavior is driven by configuration.
    """

    def __init__(self, agent_name: str = "RiskEvaluationAgent"):
        self.agent_name = agent_name

    def evaluate_risk(self, incident_result: Any, campus_config: dict) -> RiskResult:
        description = incident_result.description.lower()

        # -------------------------------------------------
        # 🔴 SAFETY-FIRST OVERRIDE (GLOBAL)
        # -------------------------------------------------
        critical_keywords = [
            "fire", "smoke", "burn",
            "fainted", "unconscious", "medical", "bleeding",
            "ambulance", "help",
            "following", "stalking", "harassment",
            "attack", "assault"
        ]

        if any(word in description for word in critical_keywords):
            return RiskResult(
                risk_score=9,
                risk_level="High",
                reason="Critical safety keywords detected requiring immediate action"
            )

        # -------------------------------------------------
        # 🧠 CONFIG-DRIVEN CONTEXTUAL SCORING
        # -------------------------------------------------
        score = 0
        reasons = []

        # 1️⃣ Risk zone sensitivity (CONFIG)
        risk_zones = campus_config.get("risk_zones", {})
        location = incident_result.location.lower()

        if any(zone.lower() in location for zone in risk_zones.get("high", [])):
            score += 3
            reasons.append("Incident occurred in a high-risk campus zone")
        elif any(zone.lower() in location for zone in risk_zones.get("medium", [])):
            score += 2
            reasons.append("Incident occurred in a medium-risk campus zone")
        else:
            score += 1
            reasons.append("Incident occurred in a low-risk campus zone")

        # 2️⃣ Time-based risk (CONFIG)
        campus_hours = campus_config["campus"]["operating_hours"]
        night_start = int(campus_hours["night_start"].split(":")[0])

        try:
            incident_hour = int(incident_result.timestamp[11:13])
            if incident_hour >= night_start:
                score += 2
                reasons.append("Incident occurred during campus night hours")
        except Exception:
            pass

        # 3️⃣ Input confidence (STANDARDIZED)
        if incident_result.confidence_level == "High":
            score += 2
            reasons.append("High confidence incident source")
        elif incident_result.confidence_level == "Medium":
            score += 1
            reasons.append("Medium confidence incident source")

        # -------------------------------------------------
        # 🔢 SCORE → RISK LEVEL (STANDARD)
        # -------------------------------------------------
        if score >= 7:
            risk_level = "High"
        elif score >= 4:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        return RiskResult(
            risk_score=score,
            risk_level=risk_level,
            reason="; ".join(reasons)
        )

