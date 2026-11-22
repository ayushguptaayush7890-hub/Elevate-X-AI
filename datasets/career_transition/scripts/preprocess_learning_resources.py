"""
Script 9: preprocess_learning_resources.py
Validates and structures authentic learning resources from raw catalog.
Generates:
- processed/learning_resources/verified_resources.json
"""

import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
RAW_FILE = BASE_DIR / "datasets" / "career_transition" / "raw" / "learning_resources" / "verified_resource_catalog.json"
PROC_DIR = BASE_DIR / "datasets" / "career_transition" / "processed" / "learning_resources"


def main():
    print("=" * 80)
    print("PREPROCESS VERIFIED LEARNING RESOURCES")
    print("=" * 80)

    if not RAW_FILE.exists():
        print("Missing raw learning resources catalog!")
        sys.exit(1)

    with open(RAW_FILE, "r", encoding="utf-8") as f:
        resources = json.load(f)

    print(f"Loaded {len(resources)} verified learning resources.")
    for r in resources:
        assert r.get("url"), f"Missing URL in resource {r.get('id')}"
        assert r.get("title"), f"Missing title in resource {r.get('id')}"

    PROC_DIR.mkdir(parents=True, exist_ok=True)
    out_file = PROC_DIR / "verified_resources.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(resources, f, indent=2)

    print(f"[SUCCESS] Saved {len(resources)} verified resources to {out_file.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
