"""
Script 4: extract_india_nco.py
Reproducible extraction pipeline for India National Classification of Occupations (NCO-2015)
from official DGE Ministry of Labour & Employment PDF volumes (Vol I, Vol II-A, Vol II-B).
Generates:
- interim/extracted_occupations/nco_occupations.json
- interim/extracted_occupations/nco_occupations.csv
"""

import os
import sys
import re
import json
import csv
import pypdf
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[3]
CAREER_TRANS_DIR = BASE_DIR / "datasets" / "career_transition"
NCO_RAW_DIR = CAREER_TRANS_DIR / "raw" / "india_nco"
OUT_DIR = CAREER_TRANS_DIR / "interim" / "extracted_occupations"

DIVISION_NAMES = {
    "1": "Managers",
    "2": "Professionals",
    "3": "Technicians and Associate Professionals",
    "4": "Clerical Support Workers",
    "5": "Services and Sales Workers",
    "6": "Skilled Agricultural, Forestry and Fishery Workers",
    "7": "Craft and Related Trades Workers",
    "8": "Plant and Machine Operators and Assemblers",
    "9": "Elementary Occupations"
}


def extract_concordance_table(pdf_path: Path):
    reader = pypdf.PdfReader(str(pdf_path))
    records = {}
    print(f"Parsing Concordance Table in {pdf_path.name} ({len(reader.pages)} pages)...")

    # Concordance table starts around page 38 and continues to page 150
    for p_num in range(35, min(160, len(reader.pages))):
        text = reader.pages[p_num].extract_text()
        for line in text.split('\n'):
            line = line.strip()
            # Match NCO 2015 8-digit pattern: e.g. 7531.0100 Custom Tailor 7433.10
            m = re.match(r'^(\d{4}\.\d{4})\s+([A-Za-z0-9, \-/\(\)]+?)(?:\s+\d{4}(?:\.\d+)?|\s*$)', line)
            if m:
                code = m.group(1).strip()
                title = m.group(2).strip()
                # Clean title
                title = re.sub(r'^(?:NCO|VOLUME|Concordance).*$', '', title, flags=re.IGNORECASE).strip()
                if len(title) > 2 and not title.lower().startswith("occupation") and not title.lower().startswith("page"):
                    div_code = code[0]
                    records[code] = {
                        "nco_2015_code": code,
                        "occupation_title": title,
                        "division_code": div_code,
                        "division_name": DIVISION_NAMES.get(div_code, "Other"),
                        "family_code": code[:4],
                        "source_file": pdf_path.name,
                        "extracted_page": p_num + 1,
                        "description": f"National occupational standard for {title} under NCO-2015 Division {div_code} ({DIVISION_NAMES.get(div_code, '')})."
                    }
    return records


def extract_descriptions_from_vols(pdf_paths, nco_records):
    print("Enriching occupational definitions from Vol II-A and II-B...")
    for pdf_path in pdf_paths:
        if not pdf_path.exists():
            continue
        reader = pypdf.PdfReader(str(pdf_path))
        print(f"Scanning descriptions in {pdf_path.name} ({len(reader.pages)} pages)...")
        # Scan pages for code definitions
        for p_idx, page in enumerate(reader.pages):
            text = page.extract_text()
            if not text:
                continue
            for code in list(nco_records.keys()):
                if code in text:
                    # extract surrounding paragraph
                    lines = [l.strip() for l in text.split('\n') if l.strip()]
                    for i, l in enumerate(lines):
                        if code in l and i + 1 < len(lines):
                            desc_candidates = lines[i+1:i+6]
                            desc_text = " ".join(desc_candidates)
                            if len(desc_text) > 40:
                                nco_records[code]["description"] = desc_text
                                nco_records[code]["description_source"] = f"{pdf_path.name}:p{p_idx+1}"
                                break


def main():
    print("=" * 80)
    print("INDIA NCO-2015 EXTRACTION PIPELINE")
    print("=" * 80)

    vol1_path = NCO_RAW_DIR / "National_Classification_of_Occupations_Vol_I-2015.pdf"
    if not vol1_path.exists():
        print("Missing Vol I PDF!")
        sys.exit(1)

    records = extract_concordance_table(vol1_path)
    print(f"Extracted {len(records)} canonical NCO 2015 occupational records.")

    # Enrich descriptions from Vol II-A and Vol II-B
    vol2a = NCO_RAW_DIR / "National_Classification_of_Occupations_Vol_II-A-2015.pdf"
    vol2b = NCO_RAW_DIR / "National_Classification_of_Occupations_Vol_II-B-2015.pdf"
    extract_descriptions_from_vols([vol2a, vol2b], records)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    json_out = OUT_DIR / "nco_occupations.json"
    csv_out = OUT_DIR / "nco_occupations.csv"

    record_list = sorted(list(records.values()), key=lambda x: x["nco_2015_code"])

    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(record_list, f, indent=2)

    fieldnames = [
        "nco_2015_code", "occupation_title", "division_code", "division_name",
        "family_code", "description", "source_file", "extracted_page"
    ]
    with open(csv_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(record_list)

    print(f"\n[SUCCESS] Extracted {len(record_list)} NCO-2015 records.")
    print(f"  JSON: {json_out.relative_to(BASE_DIR)}")
    print(f"  CSV:  {csv_out.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
