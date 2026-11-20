"""AZ-900 Service & Architecture Advisor (Weeks 1, 3, and 4)."""

from typing import Dict, Any


SHARED_RESPONSIBILITY = {
    "IaaS": {
        "customer_manages": ["Data & Info", "Devices", "Accounts & Identities", "Applications", "Network Controls", "Operating System"],
        "microsoft_manages": ["Physical Hosts", "Physical Network", "Physical Datacenter"],
        "shared": ["Identity & Directory Infrastructure"],
    },
    "PaaS": {
        "customer_manages": ["Data & Info", "Devices", "Accounts & Identities"],
        "microsoft_manages": ["Operating System", "Physical Hosts", "Physical Network", "Physical Datacenter"],
        "shared": ["Identity & Directory Infrastructure", "Applications", "Network Controls"],
    },
    "SaaS": {
        "customer_manages": ["Data & Info", "Devices", "Accounts & Identities"],
        "microsoft_manages": ["Applications", "Network Controls", "Operating System", "Physical Hosts", "Physical Network", "Physical Datacenter"],
        "shared": ["Identity & Directory Infrastructure"],
    },
}


def recommend_compute(workload_type: str, os_control: bool, event_driven: bool) -> Dict[str, Any]:
    if event_driven:
        return {
            "service": "Azure Functions",
            "model": "Serverless (PaaS)",
            "billing": "Per execution (Consumption Plan)",
            "reason": "Best for short, event-driven tasks with automatic scaling and zero server management.",
            "responsibility": SHARED_RESPONSIBILITY["PaaS"],
        }
    if os_control:
        return {
            "service": "Azure Virtual Machines / VM Scale Sets",
            "model": "IaaS",
            "billing": "Per second/hour while allocated",
            "reason": "Provides full OS-level control for lift-and-shift workloads or custom system dependencies.",
            "responsibility": SHARED_RESPONSIBILITY["IaaS"],
        }
    if workload_type == "microservices":
        return {
            "service": "Azure Kubernetes Service (AKS)",
            "model": "Managed Containers (PaaS)",
            "billing": "Pay for worker nodes",
            "reason": "Ideal for orchestrating multi-container microservice architectures at scale.",
            "responsibility": SHARED_RESPONSIBILITY["PaaS"],
        }
    if workload_type == "batch_container":
        return {
            "service": "Azure Container Instances (ACI)",
            "model": "Serverless Containers",
            "billing": "Per second of vCPU and memory",
            "reason": "Fastest way to run isolated, short-lived containers without managing orchestrators or VMs.",
            "responsibility": SHARED_RESPONSIBILITY["PaaS"],
        }
    return {
        "service": "Azure App Service",
        "model": "PaaS",
        "billing": "Per App Service Plan tier",
        "reason": "Managed platform for web apps and REST APIs with built-in patching, scaling, and HTTPS.",
        "responsibility": SHARED_RESPONSIBILITY["PaaS"],
    }


def recommend_storage(access_frequency: str, resilience: str) -> Dict[str, Any]:
    tier_map = {
        "frequent": ("Hot", "Lowest access cost, highest storage cost. Ideal for active app data."),
        "monthly": ("Cool", "Lower storage cost, min 30-day retention. Good for short-term backups."),
        "quarterly": ("Cold", "Even lower storage cost, min 90-day retention. Good for rarely accessed data."),
        "archival": ("Archive", "Lowest storage cost, offline tier (hours to rehydrate), min 180-day retention."),
    }
    redundancy_map = {
        "rack": ("LRS (Locally Redundant Storage)", "3 copies within a single datacenter. Lowest cost."),
        "zone": ("ZRS (Zone-Redundant Storage)", "3 copies across 3 Availability Zones in the primary region."),
        "region": ("GRS (Geo-Redundant Storage)", "LRS in primary region + async replication to paired region."),
        "max": ("GZRS (Geo-Zone-Redundant Storage)", "ZRS in primary region + async replication to paired region."),
    }
    tier, tier_note = tier_map.get(access_frequency, tier_map["frequent"])
    red, red_note = redundancy_map.get(resilience, redundancy_map["zone"])
    return {
        "access_tier": tier,
        "tier_reason": tier_note,
        "redundancy": red,
        "redundancy_reason": red_note,
    }
