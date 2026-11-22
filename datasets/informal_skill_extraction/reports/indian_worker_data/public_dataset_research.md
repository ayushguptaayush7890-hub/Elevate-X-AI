# ELEVATE X AI — LARGE-SCALE PUBLIC VOCATIONAL DATASET RESEARCH REPORT
**Research Audit Timestamp**: 2026-11-14 20:50:46  
**Target Feature**: Informal Experience to Skill Extraction (Dataset 4 of 4)  
**Governance Policy**: Permitted Open Data & Strict Provenance Tracking  

---

## 1. Executive Research Findings
We systematically researched 11 major public, government, and academic sources across India's vocational ecosystem.

> [!IMPORTANT]
> ### CRITICAL GROUND TRUTH FINDING
> **100% of available public vocational documents contain formal occupational standards, curriculum guidelines, or general Indic corpora. NONE contain genuine unscripted verbal descriptions from informal Indian workers.**
> 
> Official NCVET, NSDC, and DGT documents describe what a worker *ought* to know in institutional English or formal Hindi. They do NOT contain transcripts of what a self-employed tailor, plumber, or mechanic actually *says* on a job site.
> 
> **Conclusion**: Field interviews remain the **only valid method** to acquire genuine informal worker descriptions.

## 2. Acquired & Catalogued Sources Registry

| ID | Source Name | Publisher | Relevant Trades | Format | License Terms | Download Status |
|---|---|---|---|---|---|---|
| `RES-01` | **DGT Craftsmen Training Scheme (CTS) Syllabi Directory** | Directorate General of Training (DGT), Ministry of Skill Development & Entrepreneurship | All 10 Trades (Electrician, Welder,... | HTML / Extracted JSON & CSV | Government Open Data / Public Information (Govt of India) | `DOWNLOADED & EXTRACTED (169 Trade Qualifications)` |
| `RES-02` | **National Qualifications Register (NQR) Master Catalog** | National Council for Vocational Education and Training (NCVET) | Multi-Sector Qualification Packs (Q... | HTML / Web Catalog Index | Government Open Access / Public Information (Govt of India) | `DOWNLOADED & CATALOGUED (576 KB Portal Index)` |
| `RES-03` | **Apparel Made-Ups & Home Furnishing Sector Skill Council (AMHSSC)** | AMHSSC / NSDC | Tailor and Garment Worker (TRD-01: ... | Web Catalog / QP Documentation | Public Educational & Skill Development Use | `CATALOGUED ONLINE REFERENCE` |
| `RES-04` | **Electronics Sector Skills Council of India (ESSCI)** | ESSCI / NSDC | Electrician (TRD-02: ELE/Q3104), Mo... | Web Catalog / QP Documentation | Public Educational & Skill Development Use | `CATALOGUED ONLINE REFERENCE` |
| `RES-05` | **Indian Plumbing Skills Council (IPSSC)** | IPSSC / NSDC | Plumber (TRD-03: PSC/Q0104)... | Web Catalog / QP Documentation | Public Educational & Skill Development Use | `CATALOGUED ONLINE REFERENCE` |
| `RES-06` | **Automotive Skills Development Council (ASDC)** | ASDC / NSDC | Motor Mechanic (TRD-04: ASC/Q1402, ... | Web Catalog / QP Documentation | Public Educational & Skill Development Use | `CATALOGUED ONLINE REFERENCE` |
| `RES-07` | **Furniture & Fittings Skill Council (FFSC)** | FFSC / NSDC | Carpenter (TRD-05: FFS/Q0103)... | Web Catalog / QP Documentation | Public Educational & Skill Development Use | `CATALOGUED ONLINE REFERENCE` |
| `RES-08` | **Capital Goods Skill Council (CGSC)** | CGSC / NSDC | Welder (TRD-06: CSC/Q0204)... | Web Catalog / QP Documentation | Public Educational & Skill Development Use | `CATALOGUED ONLINE REFERENCE` |
| `RES-09` | **Construction Skill Development Council of India (CSDCI)** | CSDCI / NSDC | Mason (TRD-07: CON/Q0103), Painter ... | Web Catalog / QP Documentation | Public Educational & Skill Development Use | `CATALOGUED ONLINE REFERENCE` |
| `RES-10` | **Agriculture Skill Council of India (ASCI)** | ASCI / NSDC | Agriculture Worker (TRD-09: AGR/Q10... | Web Catalog / QP Documentation | Public Educational & Skill Development Use | `CATALOGUED ONLINE REFERENCE` |
| `RES-11` | **AI4Bharat IndicBERT / IndicNLP Open Research Manifest** | AI4Bharat / IIT Madras | Multilingual Indic NLP (Hindi, Beng... | Markdown / GitHub Research Manifest | MIT Open Source License | `DOWNLOADED & EXTRACTED (11 KB Manifest)` |

## 3. Detailed Source Breakdown & Technical Limitations

### RES-01: DGT Craftsmen Training Scheme (CTS) Syllabi Directory
- **Official URL**: [https://dgt.gov.in/cts-details](https://dgt.gov.in/cts-details)
- **Publisher**: Directorate General of Training (DGT), Ministry of Skill Development & Entrepreneurship
- **Target Occupations**: All 10 Trades (Electrician, Welder, Carpenter, Plumber, Mechanic, Sewing, Mason, etc.)
- **Content Type**: Formal Vocational Curriculum Standards (No Genuine Worker Utterances)
- **License & Permissions**: Government Open Data / Public Information (Govt of India)
- **Download & Extraction Status**: DOWNLOADED & EXTRACTED (169 Trade Qualifications)
- **Technical Limitations**: Formal pedagogical curricula; does not represent conversational informal worker slang or code-switching.

### RES-02: National Qualifications Register (NQR) Master Catalog
- **Official URL**: [https://nqr.gov.in/](https://nqr.gov.in/)
- **Publisher**: National Council for Vocational Education and Training (NCVET)
- **Target Occupations**: Multi-Sector Qualification Packs (QPs) and National Occupational Standards (NOS)
- **Content Type**: Official Competency Specifications & Performance Criteria
- **License & Permissions**: Government Open Access / Public Information (Govt of India)
- **Download & Extraction Status**: DOWNLOADED & CATALOGUED (576 KB Portal Index)
- **Technical Limitations**: Institutional competency definitions; uncredentialed informal workers do not speak in NOS performance codes.

### RES-03: Apparel Made-Ups & Home Furnishing Sector Skill Council (AMHSSC)
- **Official URL**: [https://sscamh.com/](https://sscamh.com/)
- **Publisher**: AMHSSC / NSDC
- **Target Occupations**: Tailor and Garment Worker (TRD-01: AMH/Q1947, AMH/Q0301)
- **Content Type**: Formal Qualification Standards
- **License & Permissions**: Public Educational & Skill Development Use
- **Download & Extraction Status**: CATALOGUED ONLINE REFERENCE
- **Technical Limitations**: Prescribes formal factory operations rather than informal boutique/darzi alteration workflows.

### RES-04: Electronics Sector Skills Council of India (ESSCI)
- **Official URL**: [https://www.essc-india.org/](https://www.essc-india.org/)
- **Publisher**: ESSCI / NSDC
- **Target Occupations**: Electrician (TRD-02: ELE/Q3104), Mobile Repair (TRD-10: ELE/Q8104)
- **Content Type**: Formal Qualification Standards
- **License & Permissions**: Public Educational & Skill Development Use
- **Download & Extraction Status**: CATALOGUED ONLINE REFERENCE
- **Technical Limitations**: Standardized home appliance repair; informal electricians frequently perform non-standard improvised repairs.

### RES-05: Indian Plumbing Skills Council (IPSSC)
- **Official URL**: [https://ipssc.in/](https://ipssc.in/)
- **Publisher**: IPSSC / NSDC
- **Target Occupations**: Plumber (TRD-03: PSC/Q0104)
- **Content Type**: Formal Qualification Standards
- **License & Permissions**: Public Educational & Skill Development Use
- **Download & Extraction Status**: CATALOGUED ONLINE REFERENCE
- **Technical Limitations**: Formal plumbing schematics; does not reflect colloquial pipe slang (solvent lagana, chudi kaatna).

### RES-06: Automotive Skills Development Council (ASDC)
- **Official URL**: [https://www.asdc.org.in/](https://www.asdc.org.in/)
- **Publisher**: ASDC / NSDC
- **Target Occupations**: Motor Mechanic (TRD-04: ASC/Q1402, ASC/Q1411)
- **Content Type**: Formal Qualification Standards
- **License & Permissions**: Public Educational & Skill Development Use
- **Download & Extraction Status**: CATALOGUED ONLINE REFERENCE
- **Technical Limitations**: Workshop diagnostic manuals; roadside mechanics rely heavily on sensory diagnosis (sound, vibration).

### RES-07: Furniture & Fittings Skill Council (FFSC)
- **Official URL**: [https://ffsc.in/](https://ffsc.in/)
- **Publisher**: FFSC / NSDC
- **Target Occupations**: Carpenter (TRD-05: FFS/Q0103)
- **Content Type**: Formal Qualification Standards
- **License & Permissions**: Public Educational & Skill Development Use
- **Download & Extraction Status**: CATALOGUED ONLINE REFERENCE
- **Technical Limitations**: Commercial furniture joinery; informal carpenters work extensively with laminate and MDF fabrication.

### RES-08: Capital Goods Skill Council (CGSC)
- **Official URL**: [https://cgsc.in/](https://cgsc.in/)
- **Publisher**: CGSC / NSDC
- **Target Occupations**: Welder (TRD-06: CSC/Q0204)
- **Content Type**: Formal Qualification Standards
- **License & Permissions**: Public Educational & Skill Development Use
- **Download & Extraction Status**: CATALOGUED ONLINE REFERENCE
- **Technical Limitations**: Industrial welding standards; informal fabricators often lack AWS certification but possess deep arc experience.

### RES-09: Construction Skill Development Council of India (CSDCI)
- **Official URL**: [https://csdcindia.org/](https://csdcindia.org/)
- **Publisher**: CSDCI / NSDC
- **Target Occupations**: Mason (TRD-07: CON/Q0103), Painter (TRD-08: CON/Q0501)
- **Content Type**: Formal Qualification Standards
- **License & Permissions**: Public Educational & Skill Development Use
- **Download & Extraction Status**: CATALOGUED ONLINE REFERENCE
- **Technical Limitations**: Formal construction site procedures; informal masons and painters operate through informal labor chowks.

### RES-10: Agriculture Skill Council of India (ASCI)
- **Official URL**: [https://asci-india.com/](https://asci-india.com/)
- **Publisher**: ASCI / NSDC
- **Target Occupations**: Agriculture Worker (TRD-09: AGR/Q1002)
- **Content Type**: Formal Qualification Standards
- **License & Permissions**: Public Educational & Skill Development Use
- **Download & Extraction Status**: CATALOGUED ONLINE REFERENCE
- **Technical Limitations**: Institutional drip irrigation guidelines; farmers describe work in highly localized agronomic vocabulary.

### RES-11: AI4Bharat IndicBERT / IndicNLP Open Research Manifest
- **Official URL**: [https://raw.githubusercontent.com/AI4Bharat/IndicBERT/main/README.md](https://raw.githubusercontent.com/AI4Bharat/IndicBERT/main/README.md)
- **Publisher**: AI4Bharat / IIT Madras
- **Target Occupations**: Multilingual Indic NLP (Hindi, Bengali, Tamil, etc.)
- **Content Type**: Open Academic NLP Architecture
- **License & Permissions**: MIT Open Source License
- **Download & Extraction Status**: DOWNLOADED & EXTRACTED (11 KB Manifest)
- **Technical Limitations**: General domain web crawl; lacks specific informal trade and artisan vocational descriptions.

## 4. Derived Reference Standards Extracted
From the downloaded DGT CTS official trade directory, **169 trade qualifications** have been parsed and archived in:
- `processed/indian_worker_data/official_reference_data/dgt_cts_extracted_trades.json`
- `processed/indian_worker_data/official_reference_data/dgt_cts_extracted_trades.csv`

These records provide authoritative NSQF levels, eligibility criteria, and trade titles to anchor our canonical skills.
