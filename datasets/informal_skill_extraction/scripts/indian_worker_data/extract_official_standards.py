#!/usr/bin/env python3
"""
ELEVATE X AI — OFFICIAL VOCATIONAL STANDARDS EXTRACTION ENGINE
Parses downloaded DGT CTS trade directories, NQR indexes, and open Indic NLP manifests.
Extracts structured trade competencies, NSQF levels, eligibility criteria, and durations.
Outputs:
- processed/indian_worker_data/official_reference_data/dgt_cts_extracted_trades.json
- processed/indian_worker_data/official_reference_data/dgt_cts_extracted_trades.csv
- processed/indian_worker_data/external_research_data/ai4bharat_indic_nlp_summary.json
"""

import re
import json
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_OFFICIAL_DIR = BASE_DIR / "raw" / "indian_worker_data" / "official_standards"
RAW_EXTERNAL_DIR = BASE_DIR / "raw" / "indian_worker_data" / "external_sources"
PROC_OFFICIAL_DIR = BASE_DIR / "processed" / "indian_worker_data" / "official_reference_data"
PROC_EXTERNAL_DIR = BASE_DIR / "processed" / "indian_worker_data" / "external_research_data"

PROC_OFFICIAL_DIR.mkdir(parents=True, exist_ok=True)
PROC_EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)

TRADE_KEYWORDS = {
    "TRD-01": ["सिलाई", "दर्जी", "कपड़े", "sewing", "dress", "apparel", "garment", "fashion"],
    "TRD-02": ["इलेक्ट्रीशियन", "वायरमैन", "बिजली", "electrician", "wireman", "electrical"],
    "TRD-03": ["प्लंबर", "नल", "पाइप", "plumber", "plumbing", "pipe"],
    "TRD-04": ["मैकेनिक", "ऑटो", "मोटर", "गाड़ी", "mechanic", "motor", "vehicle", "diesel", "automobile"],
    "TRD-05": ["बढ़ई", "कारपेंटर", "फर्नीचर", "carpenter", "wood", "furniture"],
    "TRD-06": ["वेल्डर", "वेल्डिंग", "welder", "welding", "fabrication"],
    "TRD-07": ["राज मिस्त्री", "चुनाई", "मेसन", "mason", "building", "construction"],
    "TRD-08": ["पेंटर", "रंग", "पुट्टी", "painter", "painting"],
    "TRD-09": ["कृषि", "ड्रिप", "सिंचाई", "agriculture", "horticulture", "irrigation", "tractor", "floriculture"],
    "TRD-10": ["मोबाइल", "इलेक्ट्रॉनिक्स", "हार्डवेयर", "mobile", "electronics", "hardware"]
}

def clean_html(text: str) -> str:
    cleaned = re.sub(r"<[^>]+>", " ", text)
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"&amp;", "&", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned

def extract_dgt_trades():
    html_path = RAW_OFFICIAL_DIR / "dgt_cts_trade_directory.html"
    if not html_path.exists():
        print(f"File not found: {html_path}")
        return []

    print(f"Parsing DGT CTS trade directory: {html_path.name}...")
    html_content = html_path.read_text(encoding="utf-8", errors="ignore")
    
    # Extract table rows
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html_content, re.DOTALL)
    print(f"Total rows found: {len(rows)}")

    extracted_records = []
    
    # Skip header row
    for r_idx, row in enumerate(rows[1:], start=1):
        cols = re.findall(r"<td[^>]*>(.*?)</td>", row, re.DOTALL)
        if len(cols) < 5:
            continue
            
        sno = clean_html(cols[0])
        sector = clean_html(cols[1])
        trade_name = clean_html(cols[2])
        syllabus = clean_html(cols[3])
        eligibility = clean_html(cols[4])
        trade_type = clean_html(cols[5]) if len(cols) > 5 else "Unknown"
        batch_size = clean_html(cols[6]) if len(cols) > 6 else ""
        nsqf_level = clean_html(cols[7]) if len(cols) > 7 else ""
        duration = clean_html(cols[8]) if len(cols) > 8 else ""
        approval_year = clean_html(cols[9]) if len(cols) > 9 else ""

        # Map to our 10 trades
        mapped_trade_id = None
        for t_id, kws in TRADE_KEYWORDS.items():
            combined_text = f"{sector} {trade_name} {syllabus}".lower()
            if any(kw.lower() in combined_text for kw in kws):
                mapped_trade_id = t_id
                break

        rec = {
            "dgt_record_id": f"DGT-CTS-{r_idx:04d}",
            "serial_no": sno,
            "sector_name": sector,
            "trade_name": trade_name,
            "curriculum_title": syllabus,
            "minimum_eligibility": eligibility,
            "trade_type": trade_type,
            "batch_size": batch_size,
            "nsqf_level": nsqf_level,
            "duration": duration,
            "nsqf_approval_year": approval_year,
            "mapped_elevatex_trade_id": mapped_trade_id,
            "source_origin": "https://dgt.gov.in/cts-details",
            "provenance": "Official DGT CTS Curriculum Directory (Govt of India)"
        }
        extracted_records.append(rec)

    print(f"Successfully extracted {len(extracted_records)} official DGT CTS trade qualifications.")
    
    # Save JSON
    json_out = PROC_OFFICIAL_DIR / "dgt_cts_extracted_trades.json"
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(extracted_records, f, indent=2, ensure_ascii=False)
    print(f"Saved extracted DGT records to {json_out}")

    # Save CSV
    csv_out = PROC_OFFICIAL_DIR / "dgt_cts_extracted_trades.csv"
    if extracted_records:
        with open(csv_out, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(extracted_records[0].keys()))
            writer.writeheader()
            writer.writerows(extracted_records)
        print(f"Saved extracted DGT CSV to {csv_out}")

    return extracted_records

def extract_indicbert_research():
    readme_path = RAW_EXTERNAL_DIR / "ai4bharat_indicbert_readme.md"
    if not readme_path.exists():
        return
        
    print(f"Processing AI4Bharat IndicBERT research manifest: {readme_path.name}...")
    content = readme_path.read_text(encoding="utf-8", errors="ignore")
    
    lines = content.splitlines()
    summary = {
        "resource_name": "AI4Bharat IndicBERT / IndicCorp Reference",
        "publisher": "AI4Bharat / IIT Madras",
        "license": "MIT Open Source",
        "supported_languages": ["Hindi", "Bengali", "Gujarati", "Marathi", "Tamil", "Telugu", "Kannada", "Malayalam", "Punjabi", "Odia", "Assamese"],
        "relevance_to_elevatex": "Informs phonetic script tokenization, Hindi Romanization handling, and transformer backbone selection for Indic trade text.",
        "char_count": len(content),
        "source_url": "https://raw.githubusercontent.com/AI4Bharat/IndicBERT/main/README.md"
    }
    
    out_path = PROC_EXTERNAL_DIR / "ai4bharat_indic_nlp_summary.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"Saved Indic research summary to {out_path}")

def main():
    extract_dgt_trades()
    extract_indicbert_research()

if __name__ == "__main__":
    main()

