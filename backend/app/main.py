from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.agent import IncidentInvestigator
from app.models import Incident, InvestigationState


app = FastAPI(
    title="AI Incident Investigator",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post(
    "/investigations",
    response_model=InvestigationState,
    status_code=status.HTTP_200_OK,
)
def create_investigation(incident: Incident) -> InvestigationState:
    state = InvestigationState(incident=incident)

    try:
        investigator = IncidentInvestigator()
        return investigator.investigate(state)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Investigation failed.",
        ) from exc