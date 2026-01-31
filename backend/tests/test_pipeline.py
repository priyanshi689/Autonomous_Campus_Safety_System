import unittest

from core.coordinator import CoordinatorAgent


class TestCampusSafetyPipeline(unittest.TestCase):

    def setUp(self):
        self.coordinator = CoordinatorAgent(
            campus_config_path="config/gla_university.json"
        )

    def test_config_loading(self):
        """Campus config should load correctly"""
        campus_name = self.coordinator.config_loader.get_campus_name()
        self.assertEqual(campus_name, "GLA University")

    def test_high_risk_incident(self):
        """Critical incidents should escalate to HIGH risk"""
        payload = {
            "source": "Student",
            "description": "Fire reported in chemistry lab",
            "location": "Chemistry Lab",
            "anonymous": True
        }

        result = self.coordinator.process_incident(payload)

        self.assertEqual(result.risk_level, "High")
        self.assertTrue(len(result.escalation_chain) > 0)

    def test_non_emergency_incident(self):
        """Non-critical incidents should not panic"""
        payload = {
            "source": "Student",
            "description": "Noise complaint in library",
            "location": "Library",
            "anonymous": False
        }

        result = self.coordinator.process_incident(payload)

        self.assertIn(result.risk_level, ["Low", "Medium"])


if __name__ == "__main__":
    unittest.main()
