import json
import os


class CampusConfigLoader:
    """
    Campus Configuration Loader
    ---------------------------
    Loads university-specific configuration files
    and exposes them to the AI core in a safe manner.
    """

    def __init__(self, config_path: str):
        self.config_path = config_path
        self._config = self._load_config()

    def _load_config(self) -> dict:
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                f"Campus configuration file not found: {self.config_path}"
            )

        with open(self.config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        self._basic_validation(config)
        return config

    def _basic_validation(self, config: dict):
        """
        Minimal validation to ensure required top-level keys exist.
        """
        required_keys = [
            "campus",
            "infrastructure",
            "risk_zones",
            "emergency_contacts",
            "incident_policies",
            "user_roles",
            "privacy_rules",
            "governance"
        ]

        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required config section: {key}")

    # ---------------- PUBLIC ACCESS METHODS ----------------

    def get_campus_name(self) -> str:
        return self._config["campus"]["name"]

    def get_operating_hours(self) -> dict:
        return self._config["campus"]["operating_hours"]

    def get_risk_zones(self) -> dict:
        return self._config["risk_zones"]

    def get_emergency_contacts(self) -> dict:
        return self._config["emergency_contacts"]

    def get_incident_policies(self) -> dict:
        return self._config["incident_policies"]

    def get_privacy_rules(self) -> dict:
        return self._config["privacy_rules"]

    def get_governance(self) -> dict:
        return self._config["governance"]

    def get_full_config(self) -> dict:
        """
        Use this only if absolutely needed.
        Prefer specific getters.
        """
        return self._config
