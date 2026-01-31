from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.core.coordinator import run_pipeline

app = FastAPI(
    title="Campus Safety AI API",
    description="API for Autonomous Campus Safety Intelligence System",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class IncidentRequest(BaseModel):
    incident_type: str
    description: str
    location: str
    user_role: str
    panic: bool


@app.get("/")
def health_check():
    return {
        "status": "API running",
        "message": "Campus Safety AI backend is live"
    }


@app.post("/api/report-incident")
def report_incident(data: IncidentRequest):

    text = f"{data.incident_type}. {data.description}"
    if data.panic:
        text = "EMERGENCY. " + text

    result = run_pipeline(
        incident_text=text,
        location=data.location,
        user_role=data.user_role
    )

    audit = result["final"]

    return {
        "campus": result["campus"],
        "risk_level": audit.risk_level,
        "confidence": audit.confidence_level,
        "decision": audit.final_decision,
        "escalation_chain": audit.escalation_chain,
        "explanation": audit.explanation,
        "emergency_contacts": result["emergency_contacts"]
    }
