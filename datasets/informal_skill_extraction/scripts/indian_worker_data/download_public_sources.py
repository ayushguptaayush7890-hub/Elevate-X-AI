#!/usr/bin/env python3
"""
ELEVATE X AI — AUTOMATED PUBLIC VOCATIONAL SOURCE ACQUISITION ENGINE
Downloads permitted, public open-access qualification standards,
CTS curriculum syllabi listings, and open research references.
Computes SHA-256 checksums, preserves raw original files, and records provenance.
"""

import os
import json
import ssl
import hashlib
import urllib.request
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[2]
OFFICIAL_DIR = BASE_DIR / "raw" / "indian_worker_data" / "official_standards"
EXTERNAL_DIR = BASE_DIR / "raw" / "indian_worker_data" / "external_sources"

OFFICIAL_DIR.mkdir(parents=True, exist_ok=True)
EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)

SOURCES = [
    {
        "source_id": "SRC-DGT-CTS-01",
        "title": "DGT Craftsmen Training Scheme (CTS) Official Trade Syllabi Directory",
        "url": "https://dgt.gov.in/cts-details",
        "destination_dir": OFFICIAL_DIR,
        "filename": "dgt_cts_trade_directory.html",
        "format": "HTML",
        "category": "Official Vocational Standard Listing",
        "publisher": "Directorate General of Training (DGT), Ministry of Skill Development",
        "license": "Government Open Data / Public Information (Govt of India)",
        "occupations": ["All 10 Trades", "CTS ITI Engineering & Non-Engineering Crafts"]
    },
    {
        "source_id": "SRC-NQR-PORTAL-01",
        "title": "National Qualifications Register (NQR) Official Qualification Catalog Index",
        "url": "https://nqr.gov.in/",
        "destination_dir": OFFICIAL_DIR,
        "filename": "nqr_portal_index.html",
        "format": "HTML",
        "category": "Official National Repository",
        "publisher": "NCVET / National Qualifications Register (NQR)",
        "license": "Government Open Access / Public Information (Govt of India)",
        "occupations": ["All National Occupational Standards (NOS)", "Qualification Packs (QPs)"]
    },
    {
        "source_id": "SRC-AI4BHARAT-INDIC-01",
        "title": "AI4Bharat IndicBERT Multilingual Language Architecture Specification",
        "url": "https://raw.githubusercontent.com/AI4Bharat/IndicBERT/main/README.md",
        "destination_dir": EXTERNAL_DIR,
        "filename": "ai4bharat_indicbert_readme.md",
        "format": "MD",
        "category": "Open Research Dataset Reference",
        "publisher": "AI4Bharat / IIT Madras",
        "license": "MIT Open Source License",
        "occupations": ["Multilingual Indic NLP", "Hindi / Roman Script Processing"]
    }
]

def compute_sha256(filepath: Path) -> str:
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest()

def download_sources():
    print("Starting Automated Public Vocational Source Acquisition...")
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    manifest = []
    
    for src in SOURCES:
        dest_file = src["destination_dir"] / src["filename"]
        print(f"\nProcessing {src['source_id']}: {src['title']}")
        print(f"  URL: {src['url']}")
        print(f"  Target: {dest_file}")
        
        status = "unknown"
        error_msg = None
        size_bytes = 0
        sha = None
        
        # Check if already downloaded and valid
        if dest_file.exists() and dest_file.stat().st_size > 1000:
            print("  File already exists. Verifying existing file...")
            size_bytes = dest_file.stat().st_size
            sha = compute_sha256(dest_file)
            status = "already_downloaded_verified"
        else:
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ElevateX-Research-Bot/1.0"}
                req = urllib.request.Request(src["url"], headers=headers)
                with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
                    content = resp.read()
                    with open(dest_file, "wb") as f:
                        f.write(content)
                size_bytes = len(content)
                sha = compute_sha256(dest_file)
                status = "download_success"
                print(f"  Download successful ({size_bytes:,} bytes, SHA-256: {sha[:12]}...)")
            except Exception as e:
                status = "download_failed"
                error_msg = str(e)
                print(f"  Download failed: {e}")
                
        record = {
            "source_id": src["source_id"],
            "title": src["title"],
            "url": src["url"],
            "local_path": str(dest_file.relative_to(BASE_DIR.parent.parent)),
            "format": src["format"],
            "category": src["category"],
            "publisher": src["publisher"],
            "license": src["license"],
            "occupations": src["occupations"],
            "download_status": status,
            "error_message": error_msg,
            "size_bytes": size_bytes,
            "sha256": sha,
            "retrieval_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        manifest.append(record)
        
    manifest_path = OFFICIAL_DIR / "download_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"\nSource acquisition manifest written to {manifest_path}")

if __name__ == "__main__":
    download_sources()

