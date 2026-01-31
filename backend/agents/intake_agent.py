from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any
import uuid


@dataclass
class IncidentResult:
    incident_id: str
    timestamp: str
    location: str
    incident_type: str
    source: str
    description: str
    confidence_level: str
    anonymous: bool
    raw_payload: Dict[str, Any]


class IncidentIntakeAgent:
    """
    Incident Intake Agent
    ---------------------
    Collects and structures incident data
    while enforcing campus privacy rules.
    """

    def __init__(self, agent_name: str = "IncidentIntakeAgent"):
        self.agent_name = agent_name

    def handle_incident(
        self,
        payload: Dict[str, Any],
        campus_config: dict
    ) -> IncidentResult:

        privacy = campus_config.get("privacy_rules", {})
        anonymous_allowed = privacy.get("anonymous_reporting", False)

        anonymous = payload.get("anonymous", False) and anonymous_allowed

        incident_id = f"INC_{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.utcnow().isoformat()

        incident_type = self._classify_incident(payload)
        confidence = self._assign_confidence(payload.get("source", ""))

        source = "Anonymous" if anonymous else payload.get("source", "Unknown")

        return IncidentResult(
            incident_id=incident_id,
            timestamp=timestamp,
            location=payload.get("location", "Unknown"),
            incident_type=incident_type,
            source=source,
            description=payload.get("description", ""),
            confidence_level=confidence,
            anonymous=anonymous,
            raw_payload=payload
        )

    # ---------------- INTERNAL HELPERS ----------------

    def _classify_incident(self, payload: Dict[str, Any]) -> str:
        text = payload.get("description", "").lower()

        if any(w in text for w in ["fire", "smoke", "burn"]):
            return "Fire"
        if any(w in text for w in ["medical", "fainted", "injured"]):
            return "Medical Emergency"
        if any(w in text for w in ["follow", "harass", "stalk"]):
            return "Harassment"
        if any(w in text for w in ["theft", "stolen"]):
            return "Theft"
        if any(w in text for w in ["lab", "chemical"]):
            return "Lab Hazard"

        return "General Incident"

    def _assign_confidence(self, source: str) -> str:
        source = source.lower()

        if source in ["security"]:
            return "High"
        if source in ["faculty", "staff"]:
            return "Medium"
        if source in ["student", "anonymous"]:
            return "Low"

        return "Low"
