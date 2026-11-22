"""
Script 2: verify_downloads.py
Audits integrity of downloaded raw datasets against metadata/checksums.json.
Generates audit/download_audit.json.
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[3]
CAREER_TRANS_DIR = BASE_DIR / "datasets" / "career_transition"
METADATA_DIR = CAREER_TRANS_DIR / "metadata"
AUDIT_DIR = CAREER_TRANS_DIR / "audit"
RAW_DIR = CAREER_TRANS_DIR / "raw"


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192 * 16):
            h.update(chunk)
    return h.hexdigest()


def main():
    print("=" * 80)
    print("VERIFY DOWNLOADS AUDIT")
    print("=" * 80)

    checksum_file = METADATA_DIR / "checksums.json"
    if not checksum_file.exists():
        print("Missing checksums.json!")
        sys.exit(1)

    with open(checksum_file, "r") as f:
        expected_checksums = json.load(f)

    audit_results = {
        "timestamp": datetime.now().isoformat(),
        "total_files": len(expected_checksums),
        "verified_files": 0,
        "failed_files": 0,
        "missing_files": 0,
        "details": []
    }

    for filename, expected_hash in expected_checksums.items():
        # Search for file in raw dir
        matches = list(RAW_DIR.rglob(filename))
        if not matches:
            audit_results["missing_files"] += 1
            audit_results["details"].append({
                "file": filename,
                "status": "MISSING",
                "expected_hash": expected_hash
            })
            print(f"  [MISSING] {filename}")
            continue

        actual_file = matches[0]
        actual_hash = compute_sha256(actual_file)
        if actual_hash == expected_hash:
            audit_results["verified_files"] += 1
            audit_results["details"].append({
                "file": filename,
                "path": str(actual_file.relative_to(BASE_DIR)),
                "size_bytes": actual_file.stat().st_size,
                "status": "VERIFIED_OK",
                "sha256": actual_hash
            })
            print(f"  [VERIFIED] {filename} ({actual_file.stat().st_size / (1024*1024):.2f} MB)")
        else:
            audit_results["failed_files"] += 1
            audit_results["details"].append({
                "file": filename,
                "status": "CHECKSUM_MISMATCH",
                "expected": expected_hash,
                "actual": actual_hash
            })
            print(f"  [FAILED] {filename} Hash Mismatch!")

    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = AUDIT_DIR / "download_audit.json"
    with open(out_file, "w") as f:
        json.dump(audit_results, f, indent=2)

    print(f"\nAudit complete: {audit_results['verified_files']}/{audit_results['total_files']} files verified. Saved to {out_file.name}")
    sys.exit(0 if audit_results["failed_files"] == 0 and audit_results["missing_files"] == 0 else 1)


if __name__ == "__main__":
    main()
