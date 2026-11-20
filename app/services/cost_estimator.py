"""Simplified Azure Cost & CapEx/OpEx Estimator (Weeks 1 and 5)."""

from typing import Dict, Any

REGION_MULTIPLIER = {
    "centralindia": 1.00,
    "southindia": 1.02,
    "eastus": 0.95,
    "westeurope": 1.08,
}

COMPUTE_MONTHLY_USD = {
    "app_service_b1": 13.14,
    "app_service_s1": 69.35,
    "vm_b2s": 30.37,
    "vm_d2s_v3": 70.08,
    "functions_consumption": 2.50,
}

REDUNDANCY_USD_PER_GB = {
    "LRS": 0.018,
    "ZRS": 0.023,
    "GRS": 0.036,
    "GZRS": 0.046,
}

COMMITMENT_DISCOUNT = {
    "pay_as_you_go": 0.0,
    "1_year_reserved": 0.30,
    "3_year_reserved": 0.50,
}


def estimate_monthly_cost(
    region: str,
    compute_sku: str,
    instances: int,
    storage_gb: float,
    redundancy: str,
    egress_gb: float,
    commitment: str = "pay_as_you_go",
) -> Dict[str, Any]:
    reg_mult = REGION_MULTIPLIER.get(region, 1.0)
    discount = COMMITMENT_DISCOUNT.get(commitment, 0.0)

    base_compute = COMPUTE_MONTHLY_USD.get(compute_sku, 13.14) * max(1, instances) * reg_mult
    compute_cost = round(base_compute * (1.0 - discount), 2)

    storage_rate = REDUNDANCY_USD_PER_GB.get(redundancy, 0.018) * reg_mult
    storage_cost = round(max(0.0, storage_gb) * storage_rate, 2)

    # First 100 GB outbound data transfer is typically free; ~$0.087/GB thereafter
    billable_egress = max(0.0, egress_gb - 100.0)
    bandwidth_cost = round(billable_egress * 0.087, 2)

    total = round(compute_cost + storage_cost + bandwidth_cost, 2)
    return {
        "region": region,
        "commitment": commitment,
        "breakdown_usd": {
            "compute": compute_cost,
            "storage": storage_cost,
            "outbound_bandwidth": bandwidth_cost,
        },
        "estimated_monthly_usd": total,
        "estimated_annual_usd": round(total * 12, 2),
        "notes": "Inbound data transfer to Azure is free; outbound bandwidth is billed after the free tier.",
    }
