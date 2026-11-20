"""Azure Policy, RBAC, and Resource Lock Compliance Checker (Weeks 4 and 5)."""

from typing import Dict, List, Any

ALLOWED_REGIONS = {"centralindia", "southindia"}
REQUIRED_TAGS = {"Environment", "CostCenter", "Owner"}


def evaluate_deployment(payload: Dict[str, Any]) -> Dict[str, Any]:
    violations: List[str] = []
    recommendations: List[str] = []

    region = str(payload.get("region", "")).lower().replace(" ", "")
    environment = str(payload.get("environment", "dev")).lower()
    tags = payload.get("tags") or {}
    role = str(payload.get("requested_role", "Contributor"))
    has_lock = bool(payload.get("resource_lock", False))
    public_db = bool(payload.get("public_database_access", False))

    # 1. Azure Policy: Allowed Locations
    if region not in ALLOWED_REGIONS:
        violations.append(
            f"Azure Policy [Deny]: Region '{region}' is outside allowed India geography regions ({sorted(ALLOWED_REGIONS)})."
        )

    # 2. Azure Policy: Required Tags for Cost Management
    missing_tags = sorted(REQUIRED_TAGS - set(tags.keys()))
    if missing_tags:
        violations.append(
            f"Azure Policy [Audit/Deny]: Missing required cost-allocation tags: {', '.join(missing_tags)}."
        )

    # 3. Resource Locks for Production
    if environment == "production" and not has_lock:
        violations.append(
            "Governance Check: Production resources must have a 'CanNotDelete' resource lock enabled."
        )

    # 4. Zero Trust / Network Security (NSG & Private Endpoints)
    if public_db:
        violations.append(
            "Defense in Depth / Zero Trust: Database tier should not be publicly accessible; use a Private Endpoint and NSG rules."
        )

    # 5. RBAC Least Privilege
    if role == "Owner" and environment != "sandbox":
        recommendations.append(
            "RBAC Least Privilege: Prefer 'Contributor' or 'Reader' scoped to a Resource Group instead of 'Owner'."
        )
    if environment == "production":
        recommendations.append(
            "Monitoring: Enable Azure Monitor alerts, Log Analytics, and Microsoft Defender for Cloud."
        )

    return {
        "compliant": len(violations) == 0,
        "violations": violations,
        "recommendations": recommendations,
    }
