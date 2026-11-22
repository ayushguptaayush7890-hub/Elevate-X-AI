#!/usr/bin/env python3
"""
ELEVATE X AI — SOURCE PROVENANCE & DATA AUTHENTICITY AUDITOR
Ensures strict provenance compliance across all Dataset 4 records:
1. Every record has a traceable source_reference.
2. Synthetic records never claim to be 'real_field_interview'.
3. Real records have verified DPDP consent status.
4. No synthetic record exists in real data partitions.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "raw" / "indian_worker_data"
PROCESSED_DIR = BASE_DIR / "processed" / "indian_worker_data"

def audit_provenance():
    print("Auditing source provenance and authenticity tags across Dataset 4...")
    
    violations = []
    total_records = 0
    provenance_dist = {}
    
    # Check all jsonl files
    jsonl_files = list(RAW_DIR.rglob("*.jsonl")) + list(PROCESSED_DIR.rglob("*.jsonl"))
    jsonl_files = sorted(list(set(jsonl_files)))
    
    for f in jsonl_files:
        is_real_partition = ("/real/" in str(f) or "/genuine_worker_data/" in str(f))
        
        with open(f, "r", encoding="utf-8") as fp:
            for line_num, line in enumerate(fp, 1):
                if not line.strip():
                    continue
                total_records += 1
                try:
                    rec = json.loads(line)
                except Exception as e:
                    violations.append((str(f), line_num, "JSON_CORRUPTION", str(e)))
                    continue
                    
                rec_id = rec.get("record_id", f"LINE-{line_num}")
                src_type = rec.get("source_type")
                src_ref = rec.get("source_reference")
                consent = rec.get("consent_status")
                
                provenance_dist[src_type] = provenance_dist.get(src_type, 0) + 1
                
                # Check 1: Missing source_reference
                if not src_ref:
                    violations.append((str(f), line_num, "UNTRACEABLE_SOURCE", f"Record {rec_id} has empty source_reference"))
                    
                # Check 2: Synthetic in real partition
                if is_real_partition and src_type != "real_field_interview":
                    violations.append((str(f), line_num, "PARTITION_CONTAMINATION", f"Synthetic record {rec_id} found in real partition: {f.name}"))
                    
                # Check 3: Synthetic claiming real_field_interview
                if ("SYN" in rec_id or "STUB" in rec_id or "synthetic" in str(src_ref).lower()) and src_type == "real_field_interview":
                    violations.append((str(f), line_num, "FALSE_AUTHENTICITY_CLAIM", f"Synthetic record {rec_id} falsely marked as 'real_field_interview'"))
                    
                # Check 4: Missing consent in real record
                if src_type == "real_field_interview" and consent not in ["confirmed_dpdp_signed", "confirmed_dpdp_audio"]:
                    violations.append((str(f), line_num, "MISSING_DPDP_CONSENT", f"Real record {rec_id} missing affirmative consent"))

    print(f"Total records audited for provenance: {total_records:,}")
    print(f"Provenance distribution: {provenance_dist}")
    
    if not violations:
        print("Provenance Audit Status: PASSED (100% Provenance Traceability & Zero Partition Contamination)")
    else:
        print(f"Provenance Audit Status: FAILED ({len(violations)} violations detected)")
        for v in violations[:10]:
            print(f"  {v[0]}:{v[1]} - {v[2]}: {v[3]}")
            
    return len(violations) == 0

if __name__ == "__main__":
    audit_provenance()

