from core.coordinator import CoordinatorAgent


def main():
    coordinator = CoordinatorAgent()

    # Demo input (what judges see)
    incident_payload = {
        "source": "CCTV",
        "description": "Suspicious movement detected near girls hostel at night",
        "location": "Girls Hostel Gate"
    }

    result = coordinator.process_incident(incident_payload)

    print("\n===== FINAL SYSTEM OUTPUT =====")
    print(f"Decision      : {result.final_decision}")
    print(f"Risk Level    : {result.risk_level}")
    print(f"Confidence    : {result.confidence_level}")
    print(f"Explanation   : {result.explanation}")


if __name__ == "__main__":
    main()
