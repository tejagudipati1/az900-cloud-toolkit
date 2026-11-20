"""FastAPI application for the AZ-900 Cloud Architecture & Governance Toolkit."""

from pathlib import Path
from typing import Dict, Optional
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.services.advisor import recommend_compute, recommend_storage
from app.services.cost_estimator import estimate_monthly_cost
from app.services.governance import evaluate_deployment

app = FastAPI(
    title="AZ-900 Cloud Architecture & Governance Toolkit",
    description="Interactive mini-project demonstrating Microsoft Azure Fundamentals (AZ-900) concepts.",
    version="1.0.0",
)

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class AdvisorRequest(BaseModel):
    workload_type: str = Field(default="web_api", description="web_api | microservices | batch_container")
    os_control: bool = False
    event_driven: bool = False
    access_frequency: str = Field(default="frequent", description="frequent | monthly | quarterly | archival")
    resilience: str = Field(default="zone", description="rack | zone | region | max")


class CostRequest(BaseModel):
    region: str = "centralindia"
    compute_sku: str = "app_service_b1"
    instances: int = Field(default=1, ge=1, le=50)
    storage_gb: float = Field(default=100.0, ge=0)
    redundancy: str = "ZRS"
    egress_gb: float = Field(default=50.0, ge=0)
    commitment: str = "pay_as_you_go"


class GovernanceRequest(BaseModel):
    region: str = "centralindia"
    environment: str = "production"
    tags: Dict[str, str] = Field(default_factory=lambda: {"Environment": "prod", "CostCenter": "AIML-01", "Owner": "vasu"})
    requested_role: str = "Contributor"
    resource_lock: bool = True
    public_database_access: bool = False


@app.get("/")
def serve_home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "az900-cloud-toolkit"}


@app.post("/api/advisor")
def get_advice(req: AdvisorRequest):
    return {
        "compute": recommend_compute(req.workload_type, req.os_control, req.event_driven),
        "storage": recommend_storage(req.access_frequency, req.resilience),
    }


@app.post("/api/cost")
def get_cost(req: CostRequest):
    return estimate_monthly_cost(
        region=req.region,
        compute_sku=req.compute_sku,
        instances=req.instances,
        storage_gb=req.storage_gb,
        redundancy=req.redundancy,
        egress_gb=req.egress_gb,
        commitment=req.commitment,
    )


@app.post("/api/governance")
def check_governance(req: GovernanceRequest):
    return evaluate_deployment(req.model_dump())
