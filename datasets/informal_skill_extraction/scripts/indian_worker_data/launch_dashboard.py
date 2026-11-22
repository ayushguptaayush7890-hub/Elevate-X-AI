#!/usr/bin/env python3
"""
ELEVATE X AI — LAUNCH FIELD DATA COLLECTION DASHBOARD
Quick launcher for the Phase 1 Real Indian Informal Worker Data Collection Console.

Usage:
    python launch_dashboard.py [--port 8501] [--host 0.0.0.0]
"""

import sys
import argparse
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(BASE_DIR))

from datasets.informal_skill_extraction.scripts.indian_worker_data.collection_dashboard import app, main
import uvicorn

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch Elevate X AI Field Worker Data Collection Dashboard")
    parser.add_argument("--port", type=int, default=8501, help="Port to run the dashboard on (default: 8501)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host interface (default: 0.0.0.0)")
    args = parser.parse_args()

    print("=" * 70)
    print("ELEVATE X AI — PHASE 1: REAL INFORMAL WORKER DATA COLLECTION STATION")
    print("=" * 70)
    print(f"Target Occupations: 100 Real Workers across 4 Trades (25 each):")
    print(f"  1. TRD-01: Tailor and Garment Worker (25 workers)")
    print(f"  2. TRD-02: Electrician (25 workers)")
    print(f"  3. TRD-03: Plumber (25 workers)")
    print(f"  4. TRD-04: Motor Mechanic (25 workers)")
    print(f"\nLocal Web URL:     http://localhost:{args.port}")
    print(f"API Documentation: http://localhost:{args.port}/docs")
    print("Press Ctrl+C to stop the field collection server.")
    print("=" * 70)

    uvicorn.run(app, host=args.host, port=args.port, log_level="info")

