"""Service catalog for Civic Saathi.

Add or edit services here. The sidebar, quick lookup selector, and
service suggestions can reuse this single catalog.
"""

from typing import Dict, List


SERVICE_CATALOG: List[Dict[str, str]] = [
    {
        "name": "Aadhaar",
        "icon": "🪪",
        "short": "ID",
        "category": "Identity",
        "prompt": "Tell me about Aadhaar services, eligibility, required documents, and application steps.",
    },
    {
        "name": "PAN",
        "icon": "💳",
        "short": "PAN",
        "category": "Identity",
        "prompt": "Tell me about PAN card services, required documents, eligibility, and application steps.",
    },
    {
        "name": "Income Certificate",
        "icon": "📄",
        "short": "INC",
        "category": "Certificates",
        "prompt": "Tell me about Income Certificate requirements, eligibility, documents, and application steps.",
    },
    {
        "name": "PM Kisan",
        "icon": "🌾",
        "short": "K",
        "category": "Agriculture",
        "prompt": "Tell me about PM-KISAN eligibility, required documents, and application steps.",
    },
    {
        "name": "Ayushman Bharat",
        "icon": "🏥",
        "short": "AB",
        "category": "Healthcare",
        "prompt": "Tell me about Ayushman Bharat eligibility, required documents, and application steps.",
    },
    {
        "name": "e-Shram",
        "icon": "👷",
        "short": "ES",
        "category": "Employment",
        "prompt": "Tell me about e-Shram registration, eligibility, required documents, and application steps.",
    },
    {
        "name": "PM Awas Yojana",
        "icon": "🏠",
        "short": "HOME",
        "category": "Housing",
        "prompt": "Tell me about PM Awas Yojana eligibility, required documents, and application steps.",
    },
    {
        "name": "PM Jan Dhan Yojana",
        "icon": "🏦",
        "short": "JD",
        "category": "Banking",
        "prompt": "Tell me about PM Jan Dhan Yojana eligibility, required documents, and application steps.",
    },
    {
        "name": "Atal Pension Yojana",
        "icon": "👴",
        "short": "APY",
        "category": "Pension",
        "prompt": "Tell me about Atal Pension Yojana eligibility, required documents, and application steps.",
    },
    {
        "name": "Passport",
        "icon": "📘",
        "short": "PASS",
        "category": "Travel",
        "prompt": "Tell me about passport application requirements, documents, eligibility, and steps.",
    },
    {
        "name": "Driving Licence",
        "icon": "🚗",
        "short": "DL",
        "category": "Transport",
        "prompt": "Tell me about driving licence application requirements, documents, eligibility, and steps.",
    },
    {
        "name": "Ration Card",
        "icon": "🛒",
        "short": "RC",
        "category": "Food",
        "prompt": "Tell me about ration card services, eligibility, required documents, and application steps.",
    },
    {
        "name": "PM Fasal Bima Yojana",
        "icon": "🌱",
        "short": "PMFBY",
        "category": "Agriculture",
        "prompt": "Tell me about PM Fasal Bima Yojana eligibility, documents, and application steps.",
    },
    {
        "name": "Voter ID",
        "icon": "🗳️",
        "short": "VOTE",
        "category": "Identity",
        "prompt": "Tell me about Voter ID registration, eligibility, required documents, and application steps.",
    },
]


def service_names() -> List[str]:
    return [service["name"] for service in SERVICE_CATALOG]


def get_service(name: str) -> Dict[str, str]:
    for service in SERVICE_CATALOG:
        if service["name"] == name:
            return service
    return {}


def get_service_prompt(name: str) -> str:
    service = get_service(name)
    return service.get("prompt", f"Tell me about {name}.")