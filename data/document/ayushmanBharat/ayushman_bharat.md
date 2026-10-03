# Ayushman Bharat — Pradhan Mantri Jan Arogya Yojana (PM-JAY)

> **Note:** This is a paraphrased summary for testing the Civic Saathi RAG pipeline.
> It is NOT the official government document. Scheme rules, cover amounts, and
> portals are revised periodically — before production use, verify against and
> ideally replace this with content pulled directly from **pmjay.gov.in** and
> **beneficiary.nha.gov.in**.

## What is PM-JAY?

Ayushman Bharat PM-JAY is the Government of India's flagship health assurance
scheme, run by the **National Health Authority (NHA)** under the **Ministry of
Health & Family Welfare**. It aims to provide cashless and paperless access to
hospital care for economically weaker and vulnerable families, in line with
the National Health Policy 2017's goal of Universal Health Coverage.

## Benefit

- **₹5 lakh per family per year**, covering secondary and tertiary
  hospitalization at empanelled public and private hospitals across India.
- No cap on family size, age, or gender.
- Pre-existing conditions are covered from day one.
- Cover is portable — usable anywhere in India, not just the beneficiary's
  home state.
- Fully cashless and paperless at the point of treatment.

## Eligibility

There are **two separate eligibility routes**:

### 1. Base scheme (deprivation/occupational criteria)
Eligibility is drawn from the **Socio-Economic Caste Census (SECC) 2011**
deprivation and occupational categories, which identify poor and vulnerable
households in both rural and urban India. There is **no income-based
self-declaration** — eligibility depends on whether the household appears in
the SECC database, or holds specific ration card categories linked to it.

**Important for guided-flow design:** most users will not know off-hand
whether their household is in the SECC database. The assistant should treat
this as something to be *checked*, not something the user can self-report
with confidence — route them to the official "Am I Eligible" check rather
than inferring yes/no from income alone.

### 2. Senior citizens aged 70+ (Ayushman Vay Vandana Card)
Since the scheme's 2024 expansion, **every Indian citizen aged 70 and above
is eligible for ₹5 lakh/year cover, regardless of income**, via the Ayushman
Vay Vandana Card.
- Seniors already covered under a family PM-JAY entry get an **additional**
  ₹5 lakh top-up for themselves, on top of the family's shared cover.
- Seniors not otherwise covered get ₹5 lakh on an individual/family basis.
- Seniors already enrolled in **CGHS, ECHS, or Ayushman CAPF** must choose
  between that scheme and PM-JAY — they cannot hold both simultaneously.
- Having private health insurance or ESI membership does **not** disqualify
  a person from PM-JAY.

## How to Check Eligibility

1. Visit the official portal (**pmjay.gov.in**) or the **Ayushman App**.
2. Use the "Am I Eligible" feature, entering mobile number, state, and
   ration card / Aadhaar / mobile number as prompted.
3. Alternatively, visit a nearby **Common Service Centre (CSC)** for
   assisted eligibility checks.

## How to Get the Ayushman Card

1. Confirm eligibility via the portal, app, or CSC.
2. Complete **Aadhaar e-KYC** (one-time identity verification).
3. Download the digital Ayushman card (PDF) from **beneficiary.nha.gov.in**,
   or collect a physical card via CSC/empanelled hospital Arogya Mitra desk.
4. **This process is completely free.** Do not pay anyone for "card making" —
   there is no official charge for enrollment or card issuance.

There is **no separate application form** to fill for the base scheme —
eligible families are automatically identified from the SECC database; the
user's task is verification and card issuance, not "applying" in the
traditional sense.

## Required Documents

- Aadhaar card (primary, generally mandatory for e-KYC)
- Ration card (used to cross-check SECC-linked eligibility)
- Mobile number linked for OTP verification
- Any additional government ID requested during verification

## At the Hospital (Using the Benefit)

1. Report to the PM-JAY / Ayushman Bharat Cell at the empanelled hospital,
   ideally at admission (within 3 days if not done immediately).
2. Identity is confirmed via **biometric authentication**.
3. Treating doctor fills a pre-authorization form with the relevant
   procedure/package code.
4. The hospital submits pre-authorization documents online for NHA approval.
5. Once approved, cashless treatment proceeds — **no upfront payment**
   required from the beneficiary for covered procedures.
6. In genuine emergencies, treatment may start immediately, with
   post-approval intimation to the PM-JAY Cell within 24 hours.

## Common "Missing Information" Triggers for the Assistant

Flag these to the user as needing external verification rather than
guessing eligibility:
- Whether their household appears in the SECC 2011 database
- Their exact ration card category/type
- Whether they already hold CGHS/ECHS/CAPF cover (relevant only for 70+ route)

## Official Sources (verify before use)

- Official PM-JAY portal: https://pmjay.gov.in
- Beneficiary card portal / e-KYC: https://beneficiary.nha.gov.in
- National Health Authority: https://nha.gov.in

---
*Ingestion metadata (for embedding_pipeline.py): scheme_name="Ayushman Bharat PM-JAY",
category="central", ministry="Ministry of Health & Family Welfare",
eligibility_type="database_dependent" (not purely self-declared — good test
case for missing-information / insufficient-information flows).*
