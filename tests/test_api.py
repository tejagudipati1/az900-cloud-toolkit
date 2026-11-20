from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_advisor_serverless():
    r = client.post("/api/advisor", json={"event_driven": True, "access_frequency": "archival", "resilience": "max"})
    assert r.status_code == 200
    data = r.json()
    assert data["compute"]["service"] == "Azure Functions"
    assert data["storage"]["access_tier"] == "Archive"
    assert "GZRS" in data["storage"]["redundancy"]


def test_cost_estimator_reserved_discount():
    payg = client.post("/api/cost", json={"compute_sku": "vm_d2s_v3", "commitment": "pay_as_you_go"}).json()
    res3 = client.post("/api/cost", json={"compute_sku": "vm_d2s_v3", "commitment": "3_year_reserved"}).json()
    assert res3["breakdown_usd"]["compute"] < payg["breakdown_usd"]["compute"]


def test_governance_blocks_non_india_region():
    r = client.post("/api/governance", json={"region": "eastus", "environment": "production", "resource_lock": False})
    assert r.status_code == 200
    data = r.json()
    assert data["compliant"] is False
    assert len(data["violations"]) >= 2
