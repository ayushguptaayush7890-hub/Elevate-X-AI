# ELEVATE X AI — VOCATIONAL ONTOLOGY & SKILL MAPPING QUALITY REPORT
## Crosswalk Analysis: Indian Qualification Standards (NCVET/NSDC) ↔ International Ontologies (ESCO v1.2.1 & O*NET)
### Version 2.0 (November 2026) | Elevate X AI Career Intelligence Data Layer

---

## 1. Executive Summary & Mapping Integrity

Elevate X AI bridges colloquial, experiential work narratives from India's informal labor market into formal competency frameworks. To prevent hallucinated or forced crosswalks, the pipeline establishes a **three-way crosswalk architecture**:

```
[Verbatim Worker Utterance] ──► [Canonical Trade Skill]
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        ▼                               ▼                               ▼
 [NCVET / NSDC QP]               [ESCO v1.2.1]                    [O*NET-SOC]
 Official Indian NQR             European Skills Pillar          US Occupational Code
 (e.g. AMH/Q1947:NOS-101)        (e.g. esco/skill/08d51185...)   (e.g. 51-6052.00)
```

> [!IMPORTANT]
> **Strict Non-Forced Mapping Policy**: In natural vocational environments, unique indigenous craftsmanship techniques (e.g., *lime ghoontai plastering*, *traditional zardozi embroidery*, *ayurvedic soil preparation*) have **no direct European or American counterpart**. Under Elevate X AI governance rules, annotators must **never** force an inaccurate ESCO or O*NET link. Such competencies are assigned `mapping_status: "unmapped"` and `is_unmapped_skill: true`, preserving their cultural and technical authenticity for expert human evaluation.

---

## 2. Official Indian Vocational Standard Sources Audit

The official sources catalogued in `source_catalog.csv` were verified against public NCVET, NQR, and Sector Skill Council registries:

| Trade ID | Sector Skill Council (SSC) | Official Qualification Pack (QP) | NSQF Level | Verified Competency Module |
|---|---|---|---|---|
| `TRD-01` | Apparel, Made-Ups & Home Furnishings (AMHSSC) | `AMH/Q1947` (Self Employed Tailor) | Level 4 | Single-needle lockstitch, drafting, cutting, overlocking, fitting |
| `TRD-02` | Electronics Sector Skills Council of India (ESSCI) | `ELE/Q3104` (Field Tech - Home Appliances) | Level 4 | Concealed conduits, cable pulling, DB dressing, multimeter testing |
| `TRD-03` | Indian Plumbing Skills Council (IPSSC) | `PSC/Q0104` (Plumber General) | Level 4 | CPVC/UPVC solvent jointing, GI threading, concealed diverters |
| `TRD-04` | Automotive Skills Development Council (ASDC) | `ASC/Q1402` (Four Wheeler Service Technician) | Level 4 | Hydraulic brake bleeding, valve clearance, clutch overhaul |
| `TRD-05` | Furniture & Fittings Skill Council (FFSC) | `FFS/Q0103` (General Carpenter) | Level 4 | Plywood sizing, sunmica laminate pressing, mortise-tenon joinery |
| `TRD-06` | Capital Goods Skill Council (CGSC) | `CSC/Q0204` (Manual Metal Arc Welder) | Level 3 | E6013 electrode welding, slag chipping, bevel grinding, gas cutting |
| `TRD-07` | Construction Skill Development Council (CSDCI) | `CON/Q0103` (Mason General) | Level 4 | Bricklaying (1:4 mortar), sahul plumb bob, clear water tube level |
| `TRD-08` | Construction Skill Development Council (CSDCI) | `CON/Q0501` (Construction Painter) | Level 3 | Double-coat wall putty blade application, regmar sanding, priming |
| `TRD-09` | Agriculture Skill Council of India (ASCI) | `AGR/Q1002` (Micro Irrigation Technician) | Level 4 | Drip lateral layout, inline emitters, disc filter backwash, venturi |
| `TRD-10` | Electronics Sector Skills Council of India (ESSCI) | `ELE/Q8104` (Mobile Phone Hardware Tech) | Level 4 | SMD hot air desoldering, charging port soldering, PCB jumper bypass |

---

## 3. ESCO v1.2.1 and O*NET SOC Alignment Verification

Every mapped canonical skill in the pipeline test suite was audited against our local processed classifications:
- **ESCO Skills Cleaned**: `datasets/informal_skill_extraction/processed/esco/esco_skills_cleaned.csv` (13,939 unique skill concepts).
- **O*NET Essential Skills**: `datasets/informal_skill_extraction/processed/essential_skills_cleaned.csv` (910 SOC occupations).

### Exemplary Crosswalk Matrix

| Local Vernacular Phrase | Canonical Trade Competency | NSQF Reference | ESCO Skill Concept URI | O*NET SOC Code |
|---|---|---|---|---|
| *single needle machine par pant shirt ki silai* | Single-Needle Lockstitch Garment Assembly | `AMH/Q1947:NOS-101` | `http://data.europa.eu/esco/skill/08d51185-df0e-4360-aee8-2a210f968be8` | `51-6052.00` |
| *deewar mein jhirri kaat kar PVC conduit daalta hu* | Concealed Wall Conduit Chasing and Installation | `ELE/Q3104:NOS-201` | `http://data.europa.eu/esco/skill/3d3d82d9-e932-430b-9df0-e3ebc707db9e` | `47-2111.00` |
| *CPVC pipe mein solvent lagakar fitting karta hu* | CPVC Pipe Solvent Cement Jointing | `PSC/Q0104:NOS-101` | `http://data.europa.eu/esco/skill/b5e28a52-c80f-48d6-9430-c3dcfdcfda98` | `47-2152.00` |
| *feeler gauge se tappet setting karta hu* | Engine Valve Tappet Clearance Calibration | `ASC/Q1411:NOS-102` | `http://data.europa.eu/esco/skill/96253c55-6b83-4a12-87f5-201ea1815e45` | `49-3023.00` |
| *fevicol lagakar sunmica press karta hu* | Adhesive Application & Laminate Sheet Pressing | `FFS/Q0103:NOS-102` | `http://data.europa.eu/esco/skill/474c10a4-e7fa-42f0-a29d-439ea8ba0784` | `47-2031.00` |
| *sahul lagakar deewar ki seedh dekhta hu* | Plumb Bob Vertical Alignment Verification | `CON/Q0103:NOS-101` | `http://data.europa.eu/esco/skill/3035f299-4458-45ec-9f5b-6f0a67cf4798` | `47-2061.00` |
| *SMD blower se charging port nikal kar naya CC pin solder karta hu* | SMD Hot Air Desoldering & Micro-Soldering | `ELE/Q8104:NOS-101` | `http://data.europa.eu/esco/skill/8f220311-bf12-4217-b6f1-a1d2931db26e` | `49-2022.00` |

---

## 4. Unmapped Skill Handling Protocol

When an informal worker describes a task unique to Indian operating conditions:
1. The primary annotator tags the exact string (`extracted_skill`) and functional category (`skill_category`).
2. A formal English title is assigned in `canonical_skill`.
3. If no exact concept exists in ESCO v1.2.1, `esco_uri` is set to `null` and `mapping_status` is marked `"unmapped"`.
4. `is_unmapped_skill` is set to `true`.
5. These records are aggregated into an **Indigenous Skills Register** for review by certified vocational master trainers.

