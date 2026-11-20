# AZ-900 Cloud Architecture & Governance Toolkit

A lightweight, modular Python + FastAPI mini-project and Infrastructure as Code (IaC) showcase built around the **Microsoft Azure Fundamentals (AZ-900)** syllabus.

## AZ-900 Concepts Demonstrated
- **Week 1 (Cloud Concepts):** Shared Responsibility Model across IaaS, PaaS, and SaaS; CapEx vs. OpEx consumption pricing.
- **Weeks 2–4 (Architecture, Compute, Storage & Security):** Azure regions, Availability Zones, compute selection (VMs, AKS, ACI, App Service, Azure Functions), storage access tiers (Hot/Cool/Cold/Archive), redundancy (LRS/ZRS/GRS/GZRS), RBAC, and Zero Trust.
- **Week 5 (Cost & Governance):** Monthly cost estimator (region, SKU, storage redundancy, egress bandwidth, reserved-instance discounts), tagging, resource locks (`CanNotDelete`), and a custom Azure Policy (`infra/policy-allowed-regions.json`).
- **Week 6 (Management & IaC):** Declarative Azure Bicep template (`infra/main.bicep`) to deploy an App Service web app and a ZRS Storage Account with governance tags.

## Project Structure
```text
az900-cloud-toolkit/
├── app/
│   ├── main.py                  # FastAPI routes & static UI
│   ├── services/
│   │   ├── advisor.py           # Compute, storage & shared-responsibility logic
│   │   ├── cost_estimator.py    # Monthly & annual Azure cost estimator
│   │   └── governance.py        # Policy, RBAC & resource-lock validator
│   └── static/index.html        # Interactive single-page web UI
├── infra/
│   ├── main.bicep               # Bicep IaC template (App Service + Storage)
│   └── policy-allowed-regions.json
├── tests/
│   └── test_api.py              # Pytest endpoint tests
└── requirements.txt
```

## Run Locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open `http://127.0.0.1:8000` in your browser (or `/docs` for Swagger UI).

## Run Tests
```bash
pytest -v
```
