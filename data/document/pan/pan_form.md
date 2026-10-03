# PAN Card Application — Form 49A (Reference Summary)

> **Note:** This is a paraphrased summary for testing the Civic Saathi RAG pipeline.
> It is NOT the official government document. Before production use, replace this
> file with the actual PDF downloaded from the Income Tax Department / Protean
> (formerly NSDL) / UTIITSL official portals.

## What is Form 49A?

Form 49A is the official application form used to request a new Permanent
Account Number (PAN) under Section 139A of the Income Tax Act, 1961, and Rule
114 of the Income Tax Rules, 1962. It is meant for:

- Indian citizens (including those residing outside India)
- Companies and entities incorporated in India
- Unincorporated entities formed within India (partnership firms, HUFs, trusts, etc.)

Foreign citizens and entities incorporated outside India instead use **Form 49AA**.

## Who Should Apply

- Anyone who does not already hold a PAN and needs one for tax filing,
  opening a bank account, high-value financial transactions, or as identity proof.
- Existing PAN holders should **not** file a fresh Form 49A. Holding more than
  one PAN is illegal. Corrections or reprints use the separate "Request for
  New PAN Card or/and Changes or Correction in PAN Data" form instead.

## Eligibility Snapshot

| Applicant Type | Correct Form |
|---|---|
| Indian citizen / NRI | Form 49A |
| Indian company, firm, trust, HUF, AOP, local authority | Form 49A |
| Foreign citizen | Form 49AA |
| Entity incorporated outside India | Form 49AA |

## Required Documents

1. **Proof of Identity** — Aadhaar card, voter ID, passport, driving licence, etc.
2. **Proof of Address** — Aadhaar, utility bill, bank statement, passport, etc.
3. **Proof of Date of Birth** — birth certificate, matriculation certificate, passport.
4. Recent passport-size photograph (for individual applicants).
5. Signature (physical form) or digital signature (for online/paperless applications).

## Key Sections in the Form

1. Assessing Officer (AO) code — area code, range code, AO type, AO number
   (obtained from the Income Tax portal based on your jurisdiction).
2. Full name of applicant.
3. Other names previously used, if any.
4. Gender (for individuals).
5. Date of birth / incorporation / formation.
6. Details of parents (for individual applicants).
7. Address details (residence and office).
8. Address for communication (choice of residence or office).
9. Telephone number and email ID.
10. Status of applicant (Individual, HUF, Company, Firm, Government, AOP,
    Trust, Body of Individuals, Local Authority, etc.).
11. Registration number (for companies/firms, where applicable).
12. Aadhaar number (mandatory linkage for individuals, where applicable).
13. Source of income.
14. Representative Assessee details, if applicable.
15. Documents submitted as proof of identity, address, and date of birth.

## How to Apply

**Online:**
1. Visit the official Protean (formerly NSDL) portal or the UTIITSL portal.
2. Choose "Apply for New PAN — Form 49A" (Indian citizens) or "Form 49AA"
   (foreign citizens).
3. Fill in the required details, upload supporting documents, and pay the
   applicable fee.
4. Submit and note the acknowledgment number for tracking.
5. If required by the mode chosen, courier the signed physical form and
   documents to the address provided on the acknowledgment.

**Offline:**
1. Download and print Form 49A (or 49AA) from the official website, or
   collect it from an authorized PAN/TIN facilitation centre.
2. Fill it in block letters; one character per box; mandatory fields are
   marked with an asterisk.
3. Attach your photograph and signature.
4. Submit the form with supporting documents to your nearest PAN centre.

## Official Sources (verify before use)

- Income Tax Department e-filing portal: https://www.incometax.gov.in
- Protean (formerly NSDL) PAN services: https://tinpan.proteantech.in
- UTIITSL PAN services: https://www.utiitsl.com

---
*Ingestion metadata (for embedding_pipeline.py): scheme_name="PAN Card Application",
category="central", document_type="supporting_document" (not a welfare scheme —
commonly required as supporting ID proof across multiple schemes).*
