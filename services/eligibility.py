"""
Service: rule-based eligibility checks for specific schemes, using the
applicant data columns from data/synthetic_data/applicants/*.csv.
 
For schemes with a hardcoded rule below, we check applicant data directly
(fast, exact, no LLM call, no hallucination risk). For any other scheme
name, we fall back to the RAG+LLM pipeline and return a text explanation.
 
NAMING CONVENTION (keep this consistent for every new scheme you add):
  - has_identity_proof        : Yes/No
  - has_address_proof         : Yes/No
  - age                       : integer (raw age; each rule applies its
                                 own threshold instead of relying on a
                                 precomputed is_age_eligible flag)
  - is_minor_needs_guardian   : Yes/No (derived from age < 18, but some
                                 CSVs may also provide it directly)
"""
from typing import Dict, Optional
 
from rag.retriever import get_retriever
from llm.response_generator import generate_response
from utils.helpers import extract_section
 
 
# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
 
def _is_yes(value) -> bool:
    """Case/whitespace-insensitive check for a 'Yes' flag in CSV data."""
    return str(value).strip().lower() == "yes"
 
 
def _get_age(applicant: Dict) -> Optional[int]:
    raw = applicant.get("age")
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None
 
 
# ---------------------------------------------------------------------------
# Hardcoded rules — one function per scheme, matching the columns in
# data/synthetic_data/applicants/<scheme>_applicants.csv
# ---------------------------------------------------------------------------
 
def _check_aadhar(applicant: Dict) -> bool:
    if _is_yes(applicant.get("is_minor_needs_guardian")):
        return False
    return (
        _is_yes(applicant.get("has_identity_proof"))
        and _is_yes(applicant.get("has_address_proof"))
    )
 
 
def _check_pan(applicant: Dict) -> bool:
    if _is_yes(applicant.get("already_has_pan")):
        return False
    return (
        _is_yes(applicant.get("has_identity_proof"))
        and _is_yes(applicant.get("has_address_proof"))
        and _is_yes(applicant.get("has_date_of_birth_proof"))
    )
 
 
def _check_ayushman_bharat(applicant: Dict) -> bool:
    # PM-JAY eligibility is primarily driven by SECC 2011 deprivation
    # criteria, represented here as is_secc_listed.
    return _is_yes(applicant.get("is_secc_listed"))
 
 
def _check_income_certificate(applicant: Dict) -> bool:
    try:
        residency_years = float(applicant.get("residency_years", 0))
    except (TypeError, ValueError):
        residency_years = 0
    return (
        _is_yes(applicant.get("has_address_proof"))
        and _is_yes(applicant.get("has_identity_proof"))
        and residency_years >= 3
    )
 
 
def _check_pm_kisan(applicant: Dict) -> bool:
    return (
        _is_yes(applicant.get("owns_agricultural_land"))
        and not _is_yes(applicant.get("is_income_tax_payer"))
        and not _is_yes(applicant.get("is_government_employee"))
    )
 
 
def _check_voter_id(applicant: Dict) -> bool:
    age = _get_age(applicant)
    return (
        _is_yes(applicant.get("is_indian_citizen"))
        and age is not None and age >= 18
    )
 
 
def _check_eshram_card(applicant: Dict) -> bool:
    age = _get_age(applicant)
    return (
        _is_yes(applicant.get("is_unorganised_worker"))
        and not _is_yes(applicant.get("is_epfo_or_govt_employee"))
        and age is not None and 16 <= age <= 59
    )
 
 
def _check_pm_awas_yojana(applicant: Dict) -> bool:
    return (
        _is_yes(applicant.get("is_eligible_household"))
        and not _is_yes(applicant.get("owns_pucca_house"))
    )
 
 
def _check_pm_jan_dhan_yojana(applicant: Dict) -> bool:
    # Eligible if the applicant does NOT already have a bank account.
    return not _is_yes(applicant.get("has_bank_account"))
 
 
def _check_atal_pension_yojana(applicant: Dict) -> bool:
    age = _get_age(applicant)
    return (
        age is not None and 18 <= age <= 40
        and _is_yes(applicant.get("has_bank_account"))
        and not _is_yes(applicant.get("is_income_tax_payer"))
    )
 
 
def _check_passport(applicant: Dict) -> bool:
    if _is_yes(applicant.get("has_pending_criminal_case")):
        return False
    return (
        _is_yes(applicant.get("has_identity_proof"))
        and _is_yes(applicant.get("has_address_proof"))
    )
 
 
def _check_driving_license(applicant: Dict) -> bool:
    age = _get_age(applicant)
    if age is None:
        return False
    if age >= 18:
        return True
    # 16-17 year olds are only eligible for a gearless-vehicle (50cc)
    # learner's license with guardian consent.
    return age >= 16 and _is_yes(applicant.get("is_minor_needs_guardian"))
 
 
def _check_ration_card(applicant: Dict) -> bool:
    if _is_yes(applicant.get("has_existing_ration_card_elsewhere")):
        return False
    return (
        _is_yes(applicant.get("has_identity_proof"))
        and _is_yes(applicant.get("has_address_proof"))
    )
 
 
def _check_pm_fasal_bima_yojana(applicant: Dict) -> bool:
    return (
        _is_yes(applicant.get("is_farmer"))
        and _is_yes(applicant.get("has_land_record_or_tenancy"))
    )
 
 
# Map scheme name (lowercased, spaces/dashes/underscores stripped) -> rule fn.
# Add new entries here as you add more schemes.
SCHEME_RULES = {
    "aadhar": _check_aadhar,
    "aadhaar": _check_aadhar,
 
    "pan": _check_pan,
    "pancard": _check_pan,
 
    "ayushmanbharat": _check_ayushman_bharat,
    "ayushman": _check_ayushman_bharat,
 
    "incomecertificate": _check_income_certificate,
 
    "pmkisan": _check_pm_kisan,
 
    "eshramcard": _check_eshram_card,
    "eshram": _check_eshram_card,
 
    "pmawasyojana": _check_pm_awas_yojana,
    "pmay": _check_pm_awas_yojana,
 
    "pmjandhanyojana": _check_pm_jan_dhan_yojana,
    "jandhan": _check_pm_jan_dhan_yojana,
 
    "atalpensionyojana": _check_atal_pension_yojana,
    "atalpension": _check_atal_pension_yojana,
    "apy": _check_atal_pension_yojana,
 
    "passport": _check_passport,
 
    "drivinglicense": _check_driving_license,
    "drivinglicence": _check_driving_license,
 
    "rationcard": _check_ration_card,
 
    "pmfasalbimayojana": _check_pm_fasal_bima_yojana,
    "pmfby": _check_pm_fasal_bima_yojana,
 
    "voterid": _check_voter_id,
    "voter": _check_voter_id,
}
 
 
def _normalize(scheme_name: str) -> str:
    return scheme_name.lower().replace(" ", "").replace("-", "").replace("_", "")
 
 
# ---------------------------------------------------------------------------
# RAG fallback — used only when a scheme has no hardcoded rule above
# ---------------------------------------------------------------------------
 
def _get_eligibility_via_rag(scheme_name: str, applicant_details: str = "") -> str:
    retriever = get_retriever()
 
    if applicant_details:
        question = (
            f"Is a person with these details eligible for {scheme_name}? "
            f"Details: {applicant_details}"
        )
    else:
        question = f"What are the eligibility criteria for {scheme_name}?"
 
    results = retriever.retrieve(question, k=5, min_score=0.3)
    full_answer = generate_response(question, results)
 
    answer = extract_section(full_answer, "Answer")
    important = extract_section(full_answer, "Important")
    combined = "\n\n".join(part for part in [answer, important] if part)
    return combined if combined else full_answer
 
 
# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------
 
def check_eligibility(scheme_name: str, applicant: Optional[Dict] = None, applicant_details: str = ""):
    """
    If `applicant` (a dict matching that scheme's CSV columns) is given and
    a hardcoded rule exists for this scheme -> returns True/False.
    Otherwise falls back to the RAG+LLM pipeline and returns a text answer.
    """
    rule_fn = SCHEME_RULES.get(_normalize(scheme_name))
 
    if rule_fn and applicant is not None:
        return rule_fn(applicant)
 
    return _get_eligibility_via_rag(scheme_name, applicant_details)
 
 
if __name__ == "__main__":
    import csv
 
    scheme = input(
        "Enter scheme/service name "
        "(aadhar/pan/ayushman_bharat/income_certificate/pm_kisan/"
        "eshram_card/pm_awas_yojana/pm_jan_dhan_yojana/"
        "atal_pension_yojana/passport/driving_license/ration_card/"
        "pm_fasal_bima_yojana/voter_id): "
    )
    csv_path = input("Path to that scheme's applicants CSV (or press Enter to skip): ").strip()
 
    print("\n" + "=" * 60)
    print(f"ELIGIBILITY — {scheme}")
    print("=" * 60)
 
    if csv_path:
        # Batch mode: check every row in the CSV and compare against the
        # is_eligible ground-truth column, so you can see how accurate
        # the rule is.
        correct = 0
        total = 0
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                result = check_eligibility(scheme, applicant=row)
                expected = _is_yes(row.get("is_eligible", ""))
                match = "PASS" if result == expected else "FAIL"
                label = row.get("name", row.get("applicant_id"))
                print(f"[{match}] {label}: predicted={result}, expected={expected}")
                total += 1
                correct += int(result == expected)
        print(f"\nAccuracy: {correct}/{total}")
    else:
        # Single free-text check via RAG fallback
        details = input("Enter applicant details in plain words: ")
        print(check_eligibility(scheme, applicant_details=details))