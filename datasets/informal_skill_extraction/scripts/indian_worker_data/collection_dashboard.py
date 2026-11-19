#!/usr/bin/env python3
"""
ELEVATE X AI — FIELD WORKER DATA COLLECTION DASHBOARD & SERVER
Phase 1: 100 Genuine Informal Worker Pilot across 4 Occupations:
- TRD-01: Tailor and Garment Worker (25 workers)
- TRD-02: Electrician (25 workers)
- TRD-03: Plumber (25 workers)
- TRD-04: Motor Mechanic (25 workers)

Provides a lightweight, full-featured local web dashboard:
1. Collection Progress Overview (100 target, occupation & language progress)
2. New Interview Form (pseudonym generator, DPDP consent, 4 trade modules, multi-task capture)
3. Record & Draft Management (in-browser skill span annotator with exact offset verification)
4. Quality & Audit Dashboard (real-time offset, schema, duplicate, and consent checks)
5. Consent & DPDP Ethics Protocol (bilingual Hindi & English consent forms)
"""

import os
import sys
import json
import csv
import io
import re
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Project Paths
BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "raw" / "indian_worker_data"
INTERIM_DIR = BASE_DIR / "interim" / "indian_worker_data"
PROCESSED_DIR = BASE_DIR / "processed" / "indian_worker_data"
REPORTS_DIR = BASE_DIR / "reports" / "indian_worker_data"

REAL_DATA_DIR = RAW_DIR / "real"
DRAFTS_DIR = INTERIM_DIR / "drafts"
GENUINE_PROC_DIR = PROCESSED_DIR / "genuine_worker_data"

for d in [REAL_DATA_DIR, DRAFTS_DIR, GENUINE_PROC_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# 4 Target Occupations for Phase 1
PHASE1_OCCUPATIONS = {
    "TRD-01": {
        "title": "Tailor and Garment Worker",
        "batch_file": "pilot_tailor_batch1.jsonl",
        "proc_dir": "tailor",
        "target": 25,
        "topics": [
            "Body measurement with inch tape and ease allowances",
            "Fabric behavior (cotton, rayon, chiffon, denim, stretch)",
            "Pattern drafting, chalk marking, and fabric shear cutting",
            "Single-needle lockstitch machine assembly (seam pacing)",
            "Overlock serger operation (3-thread/5-thread seam edging)",
            "Fusible interlining (bakram) iron pressing and collar attachment",
            "Sleeve crown drafting, armhole setting, and side seam stitching",
            "Garment alteration, loosening/tightening, and dart placement",
            "Machine maintenance: bobbin tension, needle swap, daily oiling",
            "Troubleshooting skipped stitches, thread breakage, fabric puckering"
        ]
    },
    "TRD-02": {
        "title": "Electrician",
        "batch_file": "pilot_electrician_batch1.jsonl",
        "proc_dir": "electrician",
        "target": 25,
        "topics": [
            "Concealed wall conduit chasing (jhirri kaatna) and PVC pipe laying",
            "Cable pulling using steel fish tape / wire puller",
            "MCB distribution board installation (6A, 16A, 32A load sizing)",
            "Modular switchboard socket and regulator connection",
            "Earthing pit installation (copper/GI plate, charcoal, salt)",
            "Earth resistance measurement and earthing continuity testing",
            "Digital multimeter and test lamp phase-neutral diagnostics",
            "Short-circuit fault isolation and tripping MCB troubleshooting",
            "Inverter and backup battery wiring installation",
            "Electrical safety protocols (1000V insulated tools, main supply isolation)"
        ]
    },
    "TRD-03": {
        "title": "Plumber",
        "batch_file": "pilot_plumber_batch1.jsonl",
        "proc_dir": "plumber",
        "target": 25,
        "topics": [
            "Pipe cutting using wheel cutter / hacksaw (CPVC, UPVC, PVC, GI)",
            "Solvent cement chemical jointing and curing time discipline",
            "GI pipe threading using manual ratchet die stock and thread seal tape",
            "Concealed wall diverter body installation and horizontal leveling",
            "Shower mixer, pillar tap, angle valve, and bibcock installation",
            "Drainage P-trap, S-trap, and Nahani floor trap slope alignment",
            "Flush cistern float valve calibration and siphon leak testing",
            "Hydrostatic pressure leak test on newly completed water lines",
            "Clogged line cleaning using drain auger / manual clearing wire",
            "Overhead water tank connection (inlet, outlet, overflow, scour valve)"
        ]
    },
    "TRD-04": {
        "title": "Motor Mechanic",
        "batch_file": "pilot_motor_mechanic_batch1.jsonl",
        "proc_dir": "motor_mechanic",
        "target": 25,
        "topics": [
            "Visual and acoustic vehicle diagnostic check (engine knocking/tappet noise)",
            "Engine oil draining, replacement, and oil filter installation",
            "Spark plug cleaning, gap calibration with feeler gauge",
            "Hydraulic disc brake pad inspection, caliper clean, fluid bleeding",
            "Drum brake shoe replacement and manual brake cable adjustment",
            "Clutch plate and pressure plate wear inspection and free-play setting",
            "Multimeter battery terminal voltage testing (open-circuit vs charging)",
            "Carburetor jet cleaning and air-fuel mixture adjustment",
            "Front telescopic fork oil seal replacement and fluid topping",
            "Chain sprocket set inspection, tensioning, and lubrication"
        ]
    }
}

VALID_CONTEXTS = [
    "independent_repair_shop",
    "micro_workshop",
    "customer_site",
    "construction_site",
    "industrial_cluster",
    "home_based",
    "street_vendor",
    "service_center",
    "other"
]

VALID_CATEGORIES = [
    "tool_operation",
    "technical_tactile",
    "measurement_planning",
    "troubleshooting_repair",
    "safety_compliance",
    "quality_inspection",
    "material_handling",
    "domain_concept"
]

# Load Canonical Skills
def load_canonical_skills() -> List[Dict[str, Any]]:
    cat_file = PROCESSED_DIR / "canonical_skill_catalogue.json"
    if cat_file.exists():
        with open(cat_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else data.get("skills", [])
    return []

CANONICAL_SKILLS = load_canonical_skills()

# FastAPI Application
app = FastAPI(
    title="Elevate X AI — Field Data Collection Console",
    description="Local web workstation for genuine Indian informal worker interview collection.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Helper Utilities
def get_genuine_records() -> List[Dict[str, Any]]:
    records = []
    for t_id, t_info in PHASE1_OCCUPATIONS.items():
        batch_path = REAL_DATA_DIR / t_info["batch_file"]
        if batch_path.exists():
            with open(batch_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        r = json.loads(line)
                        if r.get("source_type") == "real_field_interview":
                            records.append(r)
    return records

def get_draft_records() -> List[Dict[str, Any]]:
    drafts = []
    for df in DRAFTS_DIR.glob("*.json"):
        try:
            with open(df, "r", encoding="utf-8") as f:
                drafts.append(json.load(f))
        except Exception:
            pass
    return drafts

def get_next_record_id(occupation_id: str) -> str:
    code_map = {"TRD-01": "TLR", "TRD-02": "ELC", "TRD-03": "PLM", "TRD-04": "MEC"}
    short_code = code_map.get(occupation_id, "WRK")
    existing = get_genuine_records()
    max_num = 0
    pattern = re.compile(rf"^IND-{short_code}-(\d{{4,6}})$")
    for r in existing:
        m = pattern.match(r.get("record_id", ""))
        if m:
            num = int(m.group(1))
            if num > max_num:
                max_num = num
    return f"IND-{short_code}-{max_num + 1:04d}"

# Pydantic Schemas for Requests
class SkillSpanItem(BaseModel):
    span_id: str
    extracted_skill: str
    start_offset: int
    end_offset: int
    skill_category: str
    canonical_skill: str
    alternative_skill_names: List[str] = Field(default_factory=list)
    confidence_score: float = 1.0
    mapping_status: str = "mapped"
    is_unmapped_skill: bool = False
    esco_uri: Optional[str] = None
    onet_soc_code: Optional[str] = None
    nsqf_reference: Optional[str] = None

class TaskItem(BaseModel):
    task_id: str
    task_title: Optional[str] = None
    description: str
    skill_spans: List[SkillSpanItem] = Field(default_factory=list)

class InterviewSubmission(BaseModel):
    worker_id: str
    occupation_id: str
    region: str
    experience_years: float
    work_context: str
    original_language: str
    script_type: str
    tasks: List[TaskItem]
    consent_text_confirmed: bool
    consent_audio_confirmed: bool = False
    consent_photo_confirmed: bool = False
    interviewer_id: Optional[str] = "INT-FIELD-01"
    notes: Optional[str] = None
    source_reference: Optional[str] = "field_pilot_phase1"

class DraftSaveRequest(BaseModel):
    worker_id: str
    occupation_id: str
    region: Optional[str] = ""
    experience_years: Optional[float] = 0.0
    work_context: Optional[str] = "micro_workshop"
    original_language: Optional[str] = "hinglish"
    script_type: Optional[str] = "latin"
    tasks: List[Dict[str, Any]] = Field(default_factory=list)
    consent_text_confirmed: bool = False
    consent_audio_confirmed: bool = False
    consent_photo_confirmed: bool = False
    notes: Optional[str] = None

class StatusUpdateRequest(BaseModel):
    record_id: str
    new_status: str
    reviewer_status: Optional[str] = "pending"
    reviewer_id: Optional[str] = None

# ==============================================================================
# REST API ENDPOINTS
# ==============================================================================

@app.get("/api/overview")
def api_overview():
    records = get_genuine_records()
    drafts = get_draft_records()
    
    # Calculate unique genuine workers
    unique_workers = set()
    spans_count = 0
    trade_counts = {tid: 0 for tid in PHASE1_OCCUPATIONS}
    lang_counts = {"hindi": 0, "hinglish": 0, "english": 0, "other": 0}
    status_counts = {
        "drafts": len(drafts),
        "collected": 0,
        "transcribed": 0,
        "annotation_pending": 0,
        "annotated": 0,
        "reviewed": 0,
        "approved": 0
    }
    
    for r in records:
        w_id = r.get("worker_id")
        if w_id:
            unique_workers.add(w_id)
        spans_count += len(r.get("skill_spans", []))
        
        tid = r.get("occupation_id")
        if tid in trade_counts:
            trade_counts[tid] += 1
            
        lang = r.get("original_language", "other")
        if lang in lang_counts:
            lang_counts[lang] += 1
        else:
            lang_counts["other"] += 1
            
        st = r.get("annotation_status", "collected").lower()
        if st in status_counts:
            status_counts[st] += 1
        elif r.get("reviewer_status") == "approved":
            status_counts["approved"] += 1
            
    total_genuine_workers = len(unique_workers)
    target_total = 100
    remaining_target = max(0, target_total - total_genuine_workers)
    
    trade_progress = []
    for tid, info in PHASE1_OCCUPATIONS.items():
        # count unique workers for this trade
        w_in_trade = len(set(r.get("worker_id") for r in records if r.get("occupation_id") == tid and r.get("worker_id")))
        trade_progress.append({
            "occupation_id": tid,
            "title": info["title"],
            "target": info["target"],
            "collected_workers": w_in_trade,
            "collected_tasks": sum(1 for r in records if r.get("occupation_id") == tid),
            "percentage": round((w_in_trade / info["target"]) * 100, 1)
        })
        
    return {
        "target_total_workers": target_total,
        "total_genuine_workers": total_genuine_workers,
        "remaining_workers": remaining_target,
        "completion_percentage": round((total_genuine_workers / target_total) * 100, 1),
        "total_task_records": len(records),
        "total_skill_spans": spans_count,
        "drafts_count": len(drafts),
        "trade_progress": trade_progress,
        "language_distribution": lang_counts,
        "pipeline_stages": status_counts,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/taxonomy")
def api_taxonomy():
    return {
        "occupations": PHASE1_OCCUPATIONS,
        "contexts": VALID_CONTEXTS,
        "categories": VALID_CATEGORIES,
        "canonical_skills": CANONICAL_SKILLS
    }

@app.get("/api/records")
def api_list_records():
    records = get_genuine_records()
    drafts = get_draft_records()
    return {
        "total_genuine_records": len(records),
        "records": records,
        "total_drafts": len(drafts),
        "drafts": drafts
    }

@app.post("/api/draft")
def api_save_draft(draft: DraftSaveRequest):
    if not draft.worker_id:
        raise HTTPException(status_code=400, detail="Worker ID is required to save a draft.")
        
    draft_dict = draft.model_dump()
    draft_dict["updated_at"] = datetime.now().isoformat()
    draft_path = DRAFTS_DIR / f"{draft.worker_id}_draft.json"
    
    with open(draft_path, "w", encoding="utf-8") as f:
        json.dump(draft_dict, f, ensure_ascii=False, indent=2)
        
    return {"status": "success", "message": f"Draft saved successfully for worker {draft.worker_id}", "draft_id": draft.worker_id}

@app.get("/api/drafts")
def api_list_drafts():
    return get_draft_records()

@app.delete("/api/drafts/{worker_id}")
def api_delete_draft(worker_id: str):
    draft_path = DRAFTS_DIR / f"{worker_id}_draft.json"
    if draft_path.exists():
        draft_path.unlink()
        return {"status": "success", "message": f"Draft {worker_id} deleted."}
    raise HTTPException(status_code=404, detail=f"Draft {worker_id} not found.")

@app.post("/api/interview/submit")
def api_submit_interview(payload: InterviewSubmission):
    # 1. Enforce DPDP Act affirmative consent check
    if not payload.consent_text_confirmed:
        raise HTTPException(
            status_code=400,
            detail="DPDP Consent Required: Real worker interview cannot be submitted without affirmative text interview consent."
        )
        
    if payload.occupation_id not in PHASE1_OCCUPATIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid occupation_id '{payload.occupation_id}'. Must be one of {list(PHASE1_OCCUPATIONS.keys())}."
        )
        
    if not payload.tasks:
        raise HTTPException(status_code=400, detail="At least one task description is required.")
        
    occ_info = PHASE1_OCCUPATIONS[payload.occupation_id]
    created_records = []
    
    for t_idx, t in enumerate(payload.tasks):
        desc = t.description.strip()
        if not desc:
            raise HTTPException(status_code=400, detail=f"Task {t_idx + 1} description cannot be empty.")
            
        # Verify any attached skill spans
        for sp in t.skill_spans:
            s = sp.start_offset
            e = sp.end_offset
            sub = sp.extracted_skill
            if desc[s:e] != sub:
                raise HTTPException(
                    status_code=400,
                    detail=f"Character offset mismatch in Task {t_idx + 1} for span '{sub}': text[{s}:{e}] == '{desc[s:e]}'"
                )
                
        rec_id = get_next_record_id(payload.occupation_id)
        
        # Build strict schema-compliant record
        record = {
            "record_id": rec_id,
            "worker_id": payload.worker_id,
            "worker_description": desc,
            "original_language": payload.original_language,
            "script_type": payload.script_type,
            "region": payload.region or "Delhi NCR",
            "occupation_id": payload.occupation_id,
            "occupation": occ_info["title"],
            "secondary_occupations": [],
            "experience_years": payload.experience_years,
            "work_context": payload.work_context,
            "collection_date": datetime.now().strftime("%Y-%m-%d"),
            "skill_spans": [s.model_dump() for s in t.skill_spans],
            "ambiguity_flag": False,
            "notes": payload.notes,
            "annotation_source": "field_interviewer",
            "annotation_status": "annotated" if t.skill_spans else "transcribed",
            "source_type": "real_field_interview",
            "source_reference": payload.source_reference or "field_pilot_phase1",
            "annotator_id": payload.interviewer_id,
            "reviewer_id": None,
            "reviewer_status": "pending",
            "consent_status": "confirmed_dpdp_signed"
        }
        
        # Save to real raw batch file
        batch_path = REAL_DATA_DIR / occ_info["batch_file"]
        with open(batch_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            
        created_records.append(record)
        
    # If a draft existed for this worker, remove it
    draft_path = DRAFTS_DIR / f"{payload.worker_id}_draft.json"
    if draft_path.exists():
        draft_path.unlink()
        
    return {
        "status": "success",
        "message": f"Successfully submitted {len(created_records)} task records for worker {payload.worker_id}.",
        "records": created_records
    }

@app.post("/api/records/{record_id}/annotate")
def api_annotate_record(record_id: str, spans: List[SkillSpanItem]):
    # Locate record in real files
    found = False
    target_file = None
    all_lines = []
    updated_rec = None
    
    for t_id, t_info in PHASE1_OCCUPATIONS.items():
        batch_path = REAL_DATA_DIR / t_info["batch_file"]
        if batch_path.exists():
            with open(batch_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
                
            for idx, l in enumerate(lines):
                rec = json.loads(l)
                if rec.get("record_id") == record_id:
                    # Validate new spans against verbatim description
                    text = rec.get("worker_description", "")
                    for sp in spans:
                        if text[sp.start_offset:sp.end_offset] != sp.extracted_skill:
                            raise HTTPException(
                                status_code=400,
                                detail=f"Offset mismatch for span '{sp.extracted_skill}': text[{sp.start_offset}:{sp.end_offset}] == '{text[sp.start_offset:sp.end_offset]}'"
                            )
                    rec["skill_spans"] = [s.model_dump() for s in spans]
                    rec["annotation_status"] = "annotated"
                    lines[idx] = json.dumps(rec, ensure_ascii=False)
                    updated_rec = rec
                    found = True
                    target_file = batch_path
                    all_lines = lines
                    break
        if found:
            break
            
    if not found:
        raise HTTPException(status_code=404, detail=f"Record {record_id} not found in real batches.")
        
    # Write back
    with open(target_file, "w", encoding="utf-8") as f:
        for l in all_lines:
            f.write(l + "\n")
            
    return {"status": "success", "message": f"Updated {len(spans)} spans for {record_id}", "record": updated_rec}

@app.post("/api/records/{record_id}/status")
def api_update_record_status(payload: StatusUpdateRequest):
    found = False
    target_file = None
    all_lines = []
    updated_rec = None
    
    for t_id, t_info in PHASE1_OCCUPATIONS.items():
        batch_path = REAL_DATA_DIR / t_info["batch_file"]
        if batch_path.exists():
            with open(batch_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
                
            for idx, l in enumerate(lines):
                rec = json.loads(l)
                if rec.get("record_id") == payload.record_id:
                    rec["annotation_status"] = payload.new_status
                    if payload.reviewer_status:
                        rec["reviewer_status"] = payload.reviewer_status
                    if payload.reviewer_id:
                        rec["reviewer_id"] = payload.reviewer_id
                    lines[idx] = json.dumps(rec, ensure_ascii=False)
                    updated_rec = rec
                    found = True
                    target_file = batch_path
                    all_lines = lines
                    break
        if found:
            break
            
    if not found:
        raise HTTPException(status_code=404, detail=f"Record {payload.record_id} not found in real batches.")
        
    with open(target_file, "w", encoding="utf-8") as f:
        for l in all_lines:
            f.write(l + "\n")
            
    return {"status": "success", "record": updated_rec}

@app.get("/api/quality")
def api_quality_audit():
    records = get_genuine_records()
    drafts = get_draft_records()
    
    offset_errors = []
    duplicate_records = 0
    duplicate_workers = 0
    missing_consent = 0
    unannotated_records = 0
    
    seen_rec_ids = set()
    seen_texts = set()
    
    for r in records:
        r_id = r.get("record_id")
        text = r.get("worker_description", "")
        
        if r_id in seen_rec_ids:
            duplicate_records += 1
        seen_rec_ids.add(r_id)
        
        if text in seen_texts:
            duplicate_records += 1
        seen_texts.add(text)
        
        if r.get("consent_status") not in ["confirmed_dpdp_signed", "confirmed_dpdp_audio"]:
            missing_consent += 1
            
        spans = r.get("skill_spans", [])
        if not spans:
            unannotated_records += 1
            
        for sp in spans:
            st = sp.get("start_offset")
            en = sp.get("end_offset")
            sub = sp.get("extracted_skill")
            if text[st:en] != sub:
                offset_errors.append({
                    "record_id": r_id,
                    "expected": sub,
                    "actual": text[st:en],
                    "span": (st, en)
                })
                
    return {
        "total_records_audited": len(records),
        "offset_errors_count": len(offset_errors),
        "offset_errors": offset_errors,
        "duplicate_records_count": duplicate_records,
        "missing_consent_count": missing_consent,
        "unannotated_records_count": unannotated_records,
        "audit_passed": len(offset_errors) == 0 and duplicate_records == 0 and missing_consent == 0
    }

@app.get("/api/export/jsonl")
def api_export_jsonl(occupation_id: Optional[str] = None):
    records = get_genuine_records()
    if occupation_id:
        records = [r for r in records if r.get("occupation_id") == occupation_id]
        
    out = io.StringIO()
    for r in records:
        out.write(json.dumps(r, ensure_ascii=False) + "\n")
        
    filename = f"genuine_{occupation_id or 'all_trades'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    return Response(
        content=out.getvalue(),
        media_type="application/x-jsonlines",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.get("/api/export/csv")
def api_export_csv():
    records = get_genuine_records()
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow([
        "record_id", "worker_id", "occupation_id", "occupation",
        "language", "experience_years", "work_context", "date",
        "skill_spans_count", "annotation_status", "consent_status", "description_preview"
    ])
    for r in records:
        writer.writerow([
            r.get("record_id"),
            r.get("worker_id"),
            r.get("occupation_id"),
            r.get("occupation"),
            r.get("original_language"),
            r.get("experience_years"),
            r.get("work_context"),
            r.get("collection_date"),
            len(r.get("skill_spans", [])),
            r.get("annotation_status"),
            r.get("consent_status"),
            (r.get("worker_description", "")[:60] + "...") if len(r.get("worker_description", "")) > 60 else r.get("worker_description", "")
        ])
    filename = f"genuine_interviews_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return Response(
        content=out.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# ==============================================================================
# EMBEDDED SINGLE-PAGE WEB INTERFACE (HTML5 / Tailwind CSS / Vanilla JS)
# ==============================================================================

@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Elevate X AI — Field Data Collection Console</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+Devanagari:wght@400;600&display=swap');
    body { font-family: 'Inter', 'Noto Sans Devanagari', sans-serif; }
    .badge-devanagari { font-family: 'Noto Sans Devanagari', sans-serif; }
  </style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen flex flex-col">

  <!-- TOP HEADER NAVBAR -->
  <header class="bg-indigo-900 text-white shadow-md sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-lg bg-indigo-600 flex items-center justify-center text-white shadow">
            <i class="fa-solid fa-screwdriver-wrench text-lg"></i>
          </div>
          <div>
            <div class="flex items-center space-x-2">
              <span class="font-bold text-lg tracking-tight">ELEVATE X AI</span>
              <span class="text-xs bg-indigo-700 text-indigo-200 px-2 py-0.5 rounded-full font-medium">Dataset 4 Console</span>
            </div>
            <p class="text-xs text-indigo-300">Phase 1: 100 Real Worker Pilot Field Station</p>
          </div>
        </div>

        <!-- NAVIGATION TABS -->
        <nav class="flex space-x-1 sm:space-x-2 text-sm font-medium">
          <button onclick="switchTab('overview')" id="tab-btn-overview" class="tab-btn px-3 py-2 rounded-md bg-indigo-800 text-white hover:bg-indigo-700 transition">
            <i class="fa-solid fa-chart-pie mr-1.5"></i> Overview
          </button>
          <button onclick="switchTab('interview')" id="tab-btn-interview" class="tab-btn px-3 py-2 rounded-md text-indigo-200 hover:bg-indigo-800 hover:text-white transition">
            <i class="fa-solid fa-circle-plus mr-1.5"></i> New Interview
          </button>
          <button onclick="switchTab('records')" id="tab-btn-records" class="tab-btn px-3 py-2 rounded-md text-indigo-200 hover:bg-indigo-800 hover:text-white transition">
            <i class="fa-solid fa-folder-open mr-1.5"></i> Records & Annotator
          </button>
          <button onclick="switchTab('quality')" id="tab-btn-quality" class="tab-btn px-3 py-2 rounded-md text-indigo-200 hover:bg-indigo-800 hover:text-white transition">
            <i class="fa-solid fa-shield-halved mr-1.5"></i> Quality & Offsets
          </button>
          <button onclick="switchTab('consent')" id="tab-btn-consent" class="tab-btn px-3 py-2 rounded-md text-indigo-200 hover:bg-indigo-800 hover:text-white transition">
            <i class="fa-solid fa-file-contract mr-1.5"></i> Consent & DPDP
          </button>
        </nav>
      </div>
    </div>
  </header>

  <!-- MAIN CONTAINER -->
  <main class="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">

    <!-- TAB 1: OVERVIEW -->
    <div id="tab-overview" class="space-y-6">
      <!-- HERO TARGET BANNER -->
      <div class="bg-gradient-to-r from-indigo-700 via-indigo-800 to-slate-900 rounded-2xl p-6 text-white shadow-xl flex flex-col md:flex-row items-center justify-between gap-6">
        <div class="space-y-2 max-w-2xl">
          <div class="inline-flex items-center space-x-2 bg-indigo-500/30 px-3 py-1 rounded-full text-xs font-semibold text-indigo-200">
            <i class="fa-solid fa-bullseye"></i>
            <span>PILOT TARGET: 100 GENUINE WORKERS (25 PER TRADE)</span>
          </div>
          <h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight">Real Indian Informal Worker Data Collection</h1>
          <p class="text-sm text-indigo-200 leading-relaxed">
            Direct field recording station for artisanal knowledge extraction. Captures verbatim narratives in Hindi, Hinglish, and English with DPDP Act 2023 informed consent.
          </p>
        </div>
        <div class="flex items-center space-x-6 bg-white/10 backdrop-blur-md px-6 py-4 rounded-xl border border-white/20">
          <div class="text-center">
            <div id="hero-collected-count" class="text-3xl font-black text-amber-400">0</div>
            <div class="text-xs text-indigo-200 uppercase font-semibold">Collected</div>
          </div>
          <div class="h-10 w-px bg-white/20"></div>
          <div class="text-center">
            <div class="text-3xl font-black text-white">100</div>
            <div class="text-xs text-indigo-200 uppercase font-semibold">Goal</div>
          </div>
          <div class="h-10 w-px bg-white/20"></div>
          <div class="text-center">
            <div id="hero-progress-pct" class="text-3xl font-black text-emerald-400">0.0%</div>
            <div class="text-xs text-indigo-200 uppercase font-semibold">Progress</div>
          </div>
        </div>
      </div>

      <!-- KEY METRIC CARDS -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center space-x-4">
          <div class="w-12 h-12 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center text-xl">
            <i class="fa-solid fa-users"></i>
          </div>
          <div>
            <div class="text-xs font-semibold uppercase text-slate-500">Genuine Workers</div>
            <div id="metric-workers" class="text-2xl font-bold text-slate-800">0</div>
            <div class="text-xs text-slate-400">Target: 100 workers</div>
          </div>
        </div>

        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center space-x-4">
          <div class="w-12 h-12 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center text-xl">
            <i class="fa-solid fa-list-check"></i>
          </div>
          <div>
            <div class="text-xs font-semibold uppercase text-slate-500">Task Descriptions</div>
            <div id="metric-tasks" class="text-2xl font-bold text-slate-800">0</div>
            <div class="text-xs text-emerald-600">Multi-task capture</div>
          </div>
        </div>

        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center space-x-4">
          <div class="w-12 h-12 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center text-xl">
            <i class="fa-solid fa-tags"></i>
          </div>
          <div>
            <div class="text-xs font-semibold uppercase text-slate-500">Annotated Spans</div>
            <div id="metric-spans" class="text-2xl font-bold text-slate-800">0</div>
            <div class="text-xs text-slate-400">Exact character offsets</div>
          </div>
        </div>

        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center space-x-4">
          <div class="w-12 h-12 rounded-lg bg-purple-50 text-purple-600 flex items-center justify-center text-xl">
            <i class="fa-solid fa-pen-ruler"></i>
          </div>
          <div>
            <div class="text-xs font-semibold uppercase text-slate-500">Drafts in Progress</div>
            <div id="metric-drafts" class="text-2xl font-bold text-slate-800">0</div>
            <div class="text-xs text-purple-600">In interim workspace</div>
          </div>
        </div>
      </div>

      <!-- 4 OCCUPATIONS PROGRESS GRIDS -->
      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div class="flex items-center justify-between border-b pb-3">
          <div>
            <h2 class="text-lg font-bold text-slate-800">Phase 1 Four-Occupation Balance (25 Workers Each)</h2>
            <p class="text-xs text-slate-500">Worker quota must be balanced across all four informal trades</p>
          </div>
          <button onclick="switchTab('interview')" class="bg-indigo-600 text-white text-xs px-3 py-1.5 rounded-lg hover:bg-indigo-700 transition font-medium">
            <i class="fa-solid fa-plus mr-1"></i> Collect Interview
          </button>
        </div>

        <div id="trades-progress-container" class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Populated dynamically via JS -->
        </div>
      </div>

      <!-- LINGUISTIC & PIPELINE BREAKDOWN -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h3 class="font-bold text-slate-800 text-sm uppercase tracking-wider text-slate-500">Linguistic Diversity</h3>
          <div class="space-y-3" id="languages-container">
            <!-- Populated via JS -->
          </div>
        </div>

        <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h3 class="font-bold text-slate-800 text-sm uppercase tracking-wider text-slate-500">Annotation & Review Stages</h3>
          <div class="space-y-2" id="stages-container">
            <!-- Populated via JS -->
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: NEW INTERVIEW FORM -->
    <div id="tab-interview" class="hidden space-y-6">
      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
        <div class="flex items-center justify-between border-b pb-4">
          <div>
            <h2 class="text-xl font-bold text-slate-900">New Genuine Worker Interview Collection</h2>
            <p class="text-xs text-slate-500">Record natural work descriptions from informal workers. Minimum 1 detailed task required.</p>
          </div>
          <div class="flex items-center space-x-2">
            <button onclick="saveDraft()" class="px-3.5 py-1.5 border border-slate-300 rounded-lg text-xs font-semibold text-slate-700 hover:bg-slate-50 transition">
              <i class="fa-solid fa-floppy-disk mr-1"></i> Save Draft
            </button>
            <button onclick="submitInterview()" class="px-4 py-1.5 bg-emerald-600 text-white rounded-lg text-xs font-semibold hover:bg-emerald-700 transition shadow">
              <i class="fa-solid fa-check-double mr-1"></i> Submit Interview
            </button>
          </div>
        </div>

        <!-- STEP 1: DEMOGRAPHICS & PSEUDONYM -->
        <div class="space-y-4">
          <h3 class="text-sm font-bold uppercase tracking-wider text-indigo-700 flex items-center space-x-2">
            <span class="w-5 h-5 rounded-full bg-indigo-100 text-indigo-700 flex items-center justify-center text-xs">1</span>
            <span>Worker Demographics & Pseudonym</span>
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1">Occupation <span class="text-red-500">*</span></label>
              <select id="form-occupation" onchange="onOccupationChange()" class="w-full text-sm border border-slate-300 rounded-lg p-2.5 bg-slate-50 focus:ring-2 focus:ring-indigo-500 focus:outline-none">
                <option value="TRD-01">TRD-01: Tailor and Garment Worker</option>
                <option value="TRD-02">TRD-02: Electrician</option>
                <option value="TRD-03">TRD-03: Plumber</option>
                <option value="TRD-04">TRD-04: Motor Mechanic</option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1">Worker Pseudonym ID <span class="text-red-500">*</span></label>
              <div class="flex space-x-1">
                <input id="form-worker-id" type="text" class="w-full text-sm font-mono border border-slate-300 rounded-lg p-2 bg-slate-50" value="WRK-DEL-TLR-001" />
                <button onclick="generateWorkerId()" title="Regenerate Pseudonym" class="px-2.5 py-1 bg-slate-100 border border-slate-300 rounded-lg text-slate-600 hover:bg-slate-200">
                  <i class="fa-solid fa-arrows-rotate text-xs"></i>
                </button>
              </div>
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1">Experience (Years) <span class="text-red-500">*</span></label>
              <input id="form-experience" type="number" step="0.5" min="0" max="60" value="5.0" class="w-full text-sm border border-slate-300 rounded-lg p-2.5 bg-slate-50" />
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1">Region / Cluster</label>
              <input id="form-region" type="text" placeholder="e.g. Karol Bagh Delhi" value="Karol Bagh Delhi" class="w-full text-sm border border-slate-300 rounded-lg p-2.5 bg-slate-50" />
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1">Work Context</label>
              <select id="form-context" class="w-full text-sm border border-slate-300 rounded-lg p-2.5 bg-slate-50">
                <option value="micro_workshop">Micro-Workshop / Karigari Shop</option>
                <option value="independent_repair_shop">Independent Repair Shop</option>
                <option value="customer_site">Customer On-Site / Field Visit</option>
                <option value="construction_site">Construction / Project Site</option>
                <option value="home_based">Home-Based Artisan</option>
                <option value="service_center">Authorized Service Center</option>
                <option value="industrial_cluster">Industrial / Mandi Cluster</option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1">Spoken Language Mode</label>
              <select id="form-language" class="w-full text-sm border border-slate-300 rounded-lg p-2.5 bg-slate-50">
                <option value="hinglish">Hinglish (Colloquial Hindi-English Mix)</option>
                <option value="hindi">Hindi (Pure Vernacular / Regional Hindi)</option>
                <option value="english">English (Technical English)</option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1">Script System</label>
              <select id="form-script" class="w-full text-sm border border-slate-300 rounded-lg p-2.5 bg-slate-50">
                <option value="latin">Latin / Roman Alphabet</option>
                <option value="devanagari">Devanagari (देवनागरी लिपि)</option>
                <option value="mixed">Mixed Latin-Devanagari</option>
              </select>
            </div>
          </div>
        </div>

        <!-- STEP 2: INFORMED CONSENT & PRIVACY (DPDP ACT 2023) -->
        <div class="space-y-3 p-4 bg-amber-50/70 border border-amber-200 rounded-xl">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold uppercase tracking-wider text-amber-900 flex items-center space-x-2">
              <span class="w-5 h-5 rounded-full bg-amber-200 text-amber-900 flex items-center justify-center text-xs">2</span>
              <span>DPDP Act 2023 Informed Consent Protocol</span>
            </h3>
            <span class="text-xs bg-amber-200 text-amber-800 px-2 py-0.5 rounded font-semibold">Strict Anonymity</span>
          </div>

          <p class="text-xs text-amber-800">
            Explain the research purpose to the worker. No Aadhaar, PAN, bank details, or residential addresses will ever be collected.
          </p>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2">
            <label class="flex items-start space-x-2 text-xs text-slate-800 cursor-pointer p-2 bg-white rounded-lg border border-amber-200">
              <input type="checkbox" id="consent-text" class="mt-0.5 rounded text-indigo-600 focus:ring-indigo-500" checked />
              <div>
                <span class="font-bold text-slate-900">1. Text Interview Consent</span> <span class="text-red-500 font-bold">*Mandatory</span>
                <p class="text-slate-500 text-[11px]">Consents to transcription and skill extraction research.</p>
              </div>
            </label>

            <label class="flex items-start space-x-2 text-xs text-slate-800 cursor-pointer p-2 bg-white rounded-lg border border-amber-200">
              <input type="checkbox" id="consent-audio" class="mt-0.5 rounded text-indigo-600 focus:ring-indigo-500" />
              <div>
                <span class="font-bold text-slate-900">2. Audio Recording (Optional)</span>
                <p class="text-slate-500 text-[11px]">Consents to spoken audio record for phonetic analysis.</p>
              </div>
            </label>

            <label class="flex items-start space-x-2 text-xs text-slate-800 cursor-pointer p-2 bg-white rounded-lg border border-amber-200">
              <input type="checkbox" id="consent-photo" class="mt-0.5 rounded text-indigo-600 focus:ring-indigo-500" />
              <div>
                <span class="font-bold text-slate-900">3. Workplace Photos (Optional)</span>
                <p class="text-slate-500 text-[11px]">Consents to tool demonstration photos (face obscured).</p>
              </div>
            </label>
          </div>
        </div>

        <!-- STEP 3: OCCUPATION INTERVIEW TOPIC GUIDE -->
        <div class="space-y-3 p-4 bg-slate-50 border border-slate-200 rounded-xl">
          <h3 class="text-sm font-bold uppercase tracking-wider text-slate-700 flex items-center space-x-2">
            <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-800 flex items-center justify-center text-xs">3</span>
            <span id="guide-occupation-title">Trade-Specific Interview Guide: Tailor and Garment Worker</span>
          </h3>
          <p class="text-xs text-slate-500">Ask the worker open-ended prompts based on these core trade competencies:</p>
          <div id="topics-list" class="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs text-slate-700">
            <!-- Populated via JS -->
          </div>
        </div>

        <!-- STEP 4: DETAILED TASK DESCRIPTIONS (MULTIPLE TASKS) -->
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold uppercase tracking-wider text-indigo-700 flex items-center space-x-2">
              <span class="w-5 h-5 rounded-full bg-indigo-100 text-indigo-700 flex items-center justify-center text-xs">4</span>
              <span>Verbatim Task Narratives (Multi-Task Capture)</span>
            </h3>
            <button onclick="addTaskBlock()" class="text-xs bg-indigo-50 text-indigo-700 hover:bg-indigo-100 px-3 py-1.5 rounded-lg border border-indigo-200 font-semibold transition">
              <i class="fa-solid fa-plus mr-1"></i> Add Another Task
            </button>
          </div>

          <div id="tasks-container" class="space-y-4">
            <!-- Task Block 1 (Default) -->
            <div class="task-card bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-3" data-task-idx="0">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-slate-700 uppercase tracking-wide">
                  <i class="fa-solid fa-wrench mr-1 text-indigo-600"></i> Task #1 Narrative
                </span>
                <span class="text-xs text-slate-400">Verbatim Speech Transcript</span>
              </div>
              <textarea rows="4" class="task-description w-full p-3 text-sm rounded-lg border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:outline-none" placeholder="Enter verbatim description in Hindi, Hinglish, or English. E.g. 'Main customer ka inch tape se naap lekar fabric cutting karta hu aur overlock machine se kinari banata hu.'"></textarea>
              <div class="text-[11px] text-slate-500 flex items-center justify-between">
                <span>Capture: Work performed, tools used, materials handled, troubleshooting fix, and quality check.</span>
                <span class="task-char-count font-mono text-slate-400">0 chars</span>
              </div>
            </div>
          </div>
        </div>

        <!-- FORM SUBMISSION FOOTER -->
        <div class="pt-4 border-t flex items-center justify-between">
          <div class="text-xs text-slate-500">
            <i class="fa-solid fa-lock text-slate-400 mr-1"></i> Records saved directly to <code class="bg-slate-100 px-1 py-0.5 rounded">raw/indian_worker_data/real/</code>
          </div>
          <div class="flex items-center space-x-3">
            <button onclick="saveDraft()" class="px-4 py-2 border border-slate-300 rounded-lg text-xs font-semibold text-slate-700 hover:bg-slate-50 transition">
              <i class="fa-solid fa-floppy-disk mr-1"></i> Save Incomplete Draft
            </button>
            <button onclick="submitInterview()" class="px-5 py-2 bg-emerald-600 text-white rounded-lg text-xs font-semibold hover:bg-emerald-700 transition shadow">
              <i class="fa-solid fa-check-double mr-1"></i> Validate & Submit Interview
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 3: RECORDS & IN-APP ANNOTATOR -->
    <div id="tab-records" class="hidden space-y-6">
      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b pb-4">
          <div>
            <h2 class="text-xl font-bold text-slate-900">Genuine Worker Records & Annotator</h2>
            <p class="text-xs text-slate-500">Inspect verbatim narratives, tag skill spans, and export batches.</p>
          </div>
          <div class="flex items-center space-x-2">
            <button onclick="exportJsonl()" class="px-3 py-1.5 bg-slate-100 text-slate-700 border border-slate-300 rounded-lg text-xs font-medium hover:bg-slate-200 transition">
              <i class="fa-solid fa-file-code mr-1"></i> Export JSONL
            </button>
            <button onclick="exportCsv()" class="px-3 py-1.5 bg-slate-100 text-slate-700 border border-slate-300 rounded-lg text-xs font-medium hover:bg-slate-200 transition">
              <i class="fa-solid fa-file-csv mr-1"></i> Export CSV
            </button>
          </div>
        </div>

        <!-- FILTER BAR -->
        <div class="flex flex-wrap items-center gap-3 bg-slate-50 p-3 rounded-xl border border-slate-200 text-xs">
          <div class="font-semibold text-slate-600">Filter By:</div>
          <select id="filter-occupation" onchange="renderRecordsTable()" class="border border-slate-300 rounded-lg px-2.5 py-1.5 bg-white">
            <option value="ALL">All Occupations</option>
            <option value="TRD-01">TRD-01: Tailor</option>
            <option value="TRD-02">TRD-02: Electrician</option>
            <option value="TRD-03">TRD-03: Plumber</option>
            <option value="TRD-04">TRD-04: Motor Mechanic</option>
          </select>
          <select id="filter-status" onchange="renderRecordsTable()" class="border border-slate-300 rounded-lg px-2.5 py-1.5 bg-white">
            <option value="ALL">All Statuses</option>
            <option value="transcribed">Transcribed</option>
            <option value="annotated">Annotated</option>
            <option value="reviewed">Reviewed</option>
            <option value="approved">Approved</option>
          </select>
          <button onclick="loadAllData()" class="ml-auto text-indigo-600 font-semibold hover:underline">
            <i class="fa-solid fa-arrows-rotate mr-1"></i> Refresh Table
          </button>
        </div>

        <!-- RECORDS TABLE -->
        <div class="overflow-x-auto border border-slate-200 rounded-xl">
          <table class="w-full text-left text-xs text-slate-600">
            <thead class="bg-slate-100 text-slate-700 uppercase font-semibold text-[11px] border-b">
              <tr>
                <th class="p-3">Record ID</th>
                <th class="p-3">Worker ID</th>
                <th class="p-3">Trade</th>
                <th class="p-3">Lang</th>
                <th class="p-3">Description Preview</th>
                <th class="p-3">Spans</th>
                <th class="p-3">Status</th>
                <th class="p-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody id="records-tbody" class="divide-y divide-slate-200">
              <!-- Populated via JS -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- IN-BROWSER ANNOTATION MODAL -->
      <div id="annotator-modal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
        <div class="bg-white rounded-2xl max-w-3xl w-full p-6 shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto">
          <div class="flex items-center justify-between border-b pb-3">
            <div>
              <h3 class="font-bold text-slate-900 text-lg">In-App Skill Span Annotator</h3>
              <p class="text-xs text-slate-500" id="modal-record-title">Record ID: IND-TLR-0001</p>
            </div>
            <button onclick="closeAnnotatorModal()" class="text-slate-400 hover:text-slate-600">
              <i class="fa-solid fa-xmark text-lg"></i>
            </button>
          </div>

          <!-- VERBATIM TEXT DISPLAY & SELECTION -->
          <div class="space-y-2">
            <label class="block text-xs font-semibold text-slate-700">Verbatim Worker Narrative (Highlight text with mouse):</label>
            <div id="modal-verbatim-text" onmouseup="captureSelection()" class="p-4 bg-slate-50 border border-slate-200 rounded-xl text-sm leading-relaxed select-text font-normal text-slate-800">
              <!-- Verbatim text injected here -->
            </div>
          </div>

          <!-- SELECTION DETAIL & CANONICAL MAPPING -->
          <div class="bg-indigo-50/60 border border-indigo-100 p-4 rounded-xl space-y-3">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-semibold text-indigo-900 mb-1">Selected Extracted Skill Substring:</label>
                <input id="selected-substring" type="text" readonly class="w-full text-xs font-mono p-2 border border-indigo-200 rounded-lg bg-white text-indigo-900 font-bold" />
              </div>
              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="block text-xs font-semibold text-indigo-900 mb-1">Start Offset</label>
                  <input id="selected-start" type="number" readonly class="w-full text-xs font-mono p-2 border border-indigo-200 rounded-lg bg-white" />
                </div>
                <div>
                  <label class="block text-xs font-semibold text-indigo-900 mb-1">End Offset</label>
                  <input id="selected-end" type="number" readonly class="w-full text-xs font-mono p-2 border border-indigo-200 rounded-lg bg-white" />
                </div>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-semibold text-indigo-900 mb-1">Skill Category</label>
                <select id="selected-category" class="w-full text-xs p-2 border border-indigo-200 rounded-lg bg-white">
                  <option value="tool_operation">Tool Operation</option>
                  <option value="technical_tactile">Technical / Tactile</option>
                  <option value="measurement_planning">Measurement & Planning</option>
                  <option value="troubleshooting_repair">Troubleshooting & Repair</option>
                  <option value="safety_compliance">Safety Compliance</option>
                  <option value="quality_inspection">Quality Inspection</option>
                  <option value="material_handling">Material Handling</option>
                  <option value="domain_concept">Domain Concept</option>
                </select>
              </div>

              <div>
                <label class="block text-xs font-semibold text-indigo-900 mb-1">Canonical Skill (32-Skill Catalogue)</label>
                <select id="selected-canonical" class="w-full text-xs p-2 border border-indigo-200 rounded-lg bg-white">
                  <!-- Populated via JS -->
                </select>
              </div>
            </div>

            <div class="flex justify-end pt-1">
              <button onclick="addSelectedSpan()" class="px-3.5 py-1.5 bg-indigo-600 text-white rounded-lg text-xs font-semibold hover:bg-indigo-700 transition">
                <i class="fa-solid fa-plus mr-1"></i> Add Tagged Span
              </button>
            </div>
          </div>

          <!-- CURRENT SPANS LIST -->
          <div class="space-y-2">
            <h4 class="text-xs font-bold uppercase tracking-wider text-slate-700">Tagged Skill Spans for this Record</h4>
            <div id="modal-spans-list" class="space-y-2 max-h-48 overflow-y-auto">
              <!-- Populated via JS -->
            </div>
          </div>

          <!-- MODAL ACTIONS -->
          <div class="flex items-center justify-between border-t pt-3">
            <div class="flex items-center space-x-2">
              <button onclick="updateRecordStage('reviewed')" class="px-3 py-1.5 bg-purple-50 text-purple-700 border border-purple-200 rounded-lg text-xs font-medium hover:bg-purple-100">
                Mark Reviewed
              </button>
              <button onclick="updateRecordStage('approved')" class="px-3 py-1.5 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-lg text-xs font-medium hover:bg-emerald-100">
                Mark Approved
              </button>
            </div>
            <button onclick="saveRecordAnnotations()" class="px-4 py-2 bg-indigo-600 text-white rounded-lg text-xs font-semibold hover:bg-indigo-700 transition">
              Save Annotations
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: QUALITY & VALIDATION -->
    <div id="tab-quality" class="hidden space-y-6">
      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
        <div class="flex items-center justify-between border-b pb-4">
          <div>
            <h2 class="text-xl font-bold text-slate-900">Quality Assurance & Offset Validator</h2>
            <p class="text-xs text-slate-500">Real-time integrity auditing across character slices, DPDP consent, and duplicates.</p>
          </div>
          <button onclick="runQualityAudit()" class="px-4 py-2 bg-indigo-600 text-white rounded-lg text-xs font-semibold hover:bg-indigo-700 transition">
            <i class="fa-solid fa-stethoscope mr-1"></i> Run Live Audit
          </button>
        </div>

        <div id="quality-audit-results" class="space-y-4">
          <!-- Populated via JS -->
        </div>
      </div>
    </div>

    <!-- TAB 5: CONSENT & DPDP PROTOCOL -->
    <div id="tab-consent" class="hidden space-y-6">
      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
        <div class="border-b pb-4">
          <h2 class="text-xl font-bold text-slate-900">Informed Consent Protocol (DPDP Act 2023)</h2>
          <p class="text-xs text-slate-500">Legal and ethical guidelines for human enumerators conducting field interviews.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- ENGLISH PROTOCOL -->
          <div class="p-5 bg-slate-50 rounded-xl border border-slate-200 space-y-3">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-slate-800 text-sm">English Informed Consent Notice</h3>
              <span class="text-xs bg-slate-200 text-slate-700 px-2 py-0.5 rounded">Standard</span>
            </div>
            <div class="text-xs text-slate-600 space-y-2 leading-relaxed">
              <p><strong>1. Purpose:</strong> Research initiative by Elevate X AI to map informal worker experiential speech into recognized National (NSQF) and International (ESCO, O*NET) skill competencies.</p>
              <p><strong>2. Voluntary:</strong> Participation is 100% voluntary. The worker can decline or terminate at any time without consequence.</p>
              <p><strong>3. Absolute Privacy:</strong> No Aadhaar numbers, PAN, bank accounts, or residential addresses are collected. Only pseudonymous codes (e.g. <code>WRK-DEL-TLR-001</code>) are recorded.</p>
              <p><strong>4. Right to Withdraw:</strong> Under DPDP Act 2023, the participant can request complete erasure of their recorded description at any time.</p>
            </div>
          </div>

          <!-- HINDI PROTOCOL -->
          <div class="p-5 bg-amber-50/70 rounded-xl border border-amber-200 space-y-3">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-amber-900 text-sm badge-devanagari">कामगार सूचित सहमति प्रपत्र (Hindi)</h3>
              <span class="text-xs bg-amber-200 text-amber-800 px-2 py-0.5 rounded">देवनागरी</span>
            </div>
            <div class="text-xs text-amber-900 space-y-2 leading-relaxed badge-devanagari">
              <p><strong>1. उद्देश्य:</strong> 'एलिवेट एक्स एआई' एक शोध पहल है जिसका उद्देश्य अनौपचारिक कारीगरों (दर्ज़ी, इलेक्ट्रीशियन, प्लंबर, मैकेनिक) के मौखिक काम के अनुभव को राष्ट्रीय एवं अंतर्राष्ट्रीय कौशल मानकों के साथ जोड़ना है।</p>
              <p><strong>2. स्वैच्छिक:</strong> इस बातचीत में भाग लेना पूरी तरह से आपकी इच्छा पर निर्भर है। आप किसी भी प्रश्न का उत्तर देने से मना कर सकते हैं।</p>
              <p><strong>3. पूर्ण गोपनीयता:</strong> आपका नाम, फोन नंबर, आधार कार्ड, बैंक खाता या घर का पता कभी भी सार्वजनिक नहीं किया जाएगा। आपको एक गोपनीय कोड दिया जाएगा।</p>
              <p><strong>4. सहमति वापसी:</strong> आप साक्षात्कार के बाद कभी भी अपना विवरण हटाने का अनुरोध कर सकते हैं।</p>
            </div>
          </div>
        </div>
      </div>
    </div>

  </main>

  <!-- JAVASCRIPT APPLICATION LOGIC -->
  <script>
    let globalOverview = null;
    let globalTaxonomy = null;
    let globalRecords = [];
    let globalDrafts = [];
    let activeAnnotatingRecord = null;
    let currentRecordSpans = [];

    // Tab Switching
    function switchTab(tabId) {
      document.querySelectorAll('main > div').forEach(el => el.classList.add('hidden'));
      document.getElementById('tab-' + tabId).classList.remove('hidden');

      document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('bg-indigo-800', 'text-white');
        btn.classList.add('text-indigo-200');
      });
      document.getElementById('tab-btn-' + tabId).classList.add('bg-indigo-800', 'text-white');
      document.getElementById('tab-btn-' + tabId).classList.remove('text-indigo-200');

      if (tabId === 'overview') loadOverview();
      if (tabId === 'records') loadRecords();
      if (tabId === 'quality') runQualityAudit();
    }

    // Load Taxonomy
    async function loadTaxonomy() {
      try {
        const res = await fetch('/api/taxonomy');
        globalTaxonomy = await res.json();
        onOccupationChange();
        populateCanonicalDropdown();
      } catch (err) {
        console.error("Failed to load taxonomy:", err);
      }
    }

    // Populate Canonical Skills Dropdown
    function populateCanonicalDropdown() {
      const select = document.getElementById('selected-canonical');
      if (!select || !globalTaxonomy) return;
      select.innerHTML = '';
      (globalTaxonomy.canonical_skills || []).forEach(sk => {
        const opt = document.createElement('option');
        opt.value = sk.canonical_skill_name;
        opt.textContent = `[${sk.occupation_id}] ${sk.canonical_skill_name}`;
        select.appendChild(opt);
      });
    }

    // On Occupation Change in Form
    function onOccupationChange() {
      const occId = document.getElementById('form-occupation').value;
      if (!globalTaxonomy || !globalTaxonomy.occupations) return;

      const occ = globalTaxonomy.occupations[occId];
      if (occ) {
        document.getElementById('guide-occupation-title').textContent = `Trade-Specific Interview Guide: ${occ.title}`;
        const container = document.getElementById('topics-list');
        container.innerHTML = '';
        (occ.topics || []).forEach(t => {
          const div = document.createElement('div');
          div.className = 'flex items-start space-x-1.5';
          div.innerHTML = `<i class="fa-solid fa-check text-indigo-500 mt-0.5 text-[10px]"></i><span>${t}</span>`;
          container.appendChild(div);
        });
      }
      generateWorkerId();
    }

    // Generate Worker ID Pseudonym
    function generateWorkerId() {
      const occId = document.getElementById('form-occupation').value;
      const codeMap = {"TRD-01": "TLR", "TRD-02": "ELC", "TRD-03": "PLM", "TRD-04": "MEC"};
      const shortCode = codeMap[occId] || "WRK";
      const randomNum = Math.floor(100 + Math.random() * 900);
      document.getElementById('form-worker-id').value = `WRK-DEL-${shortCode}-${randomNum}`;
    }

    // Add Task Block
    function addTaskBlock() {
      const container = document.getElementById('tasks-container');
      const idx = container.querySelectorAll('.task-card').length;
      const div = document.createElement('div');
      div.className = 'task-card bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-3';
      div.dataset.taskIdx = idx;
      div.innerHTML = `
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-slate-700 uppercase tracking-wide">
            <i class="fa-solid fa-wrench mr-1 text-indigo-600"></i> Task #${idx + 1} Narrative
          </span>
          <button onclick="this.closest('.task-card').remove()" class="text-xs text-red-500 hover:underline">
            <i class="fa-solid fa-trash-can mr-1"></i> Remove
          </button>
        </div>
        <textarea rows="4" class="task-description w-full p-3 text-sm rounded-lg border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:outline-none" placeholder="Describe the second task performed by this worker..."></textarea>
        <div class="text-[11px] text-slate-500 flex items-center justify-between">
          <span>Capture: Tools used, sequence of actions, and how they inspect their work.</span>
          <span class="task-char-count font-mono text-slate-400">0 chars</span>
        </div>
      `;
      container.appendChild(div);
    }

    // Load Overview Data
    async function loadOverview() {
      try {
        const res = await fetch('/api/overview');
        globalOverview = await res.json();

        document.getElementById('hero-collected-count').textContent = globalOverview.total_genuine_workers;
        document.getElementById('hero-progress-pct').textContent = `${globalOverview.completion_percentage}%`;
        document.getElementById('metric-workers').textContent = `${globalOverview.total_genuine_workers} / ${globalOverview.target_total_workers}`;
        document.getElementById('metric-tasks').textContent = globalOverview.total_task_records;
        document.getElementById('metric-spans').textContent = globalOverview.total_skill_spans;
        document.getElementById('metric-drafts').textContent = globalOverview.drafts_count;

        // Render Trade Progress
        const tContainer = document.getElementById('trades-progress-container');
        tContainer.innerHTML = '';
        (globalOverview.trade_progress || []).forEach(tp => {
          const card = document.createElement('div');
          card.className = 'p-4 rounded-xl border border-slate-200 bg-slate-50 space-y-2';
          card.innerHTML = `
            <div class="flex items-center justify-between text-xs">
              <span class="font-bold text-slate-800">[${tp.occupation_id}] ${tp.title}</span>
              <span class="font-semibold text-indigo-600">${tp.collected_workers} / ${tp.target} Workers</span>
            </div>
            <div class="w-full bg-slate-200 h-2.5 rounded-full overflow-hidden">
              <div class="bg-indigo-600 h-2.5 rounded-full transition-all duration-500" style="width: ${Math.min(100, tp.percentage)}%"></div>
            </div>
            <div class="flex items-center justify-between text-[11px] text-slate-500">
              <span>${tp.collected_tasks} task descriptions collected</span>
              <span>${tp.percentage}% Complete</span>
            </div>
          `;
          tContainer.appendChild(card);
        });

        // Languages
        const lContainer = document.getElementById('languages-container');
        lContainer.innerHTML = '';
        const langs = globalOverview.language_distribution || {};
        const totalL = Object.values(langs).reduce((a, b) => a + b, 0) || 1;
        for (const [lang, count] of Object.entries(langs)) {
          const pct = Math.round((count / totalL) * 100);
          lContainer.innerHTML += `
            <div class="space-y-1">
              <div class="flex justify-between text-xs">
                <span class="capitalize font-semibold text-slate-700">${lang}</span>
                <span class="text-slate-500">${count} records (${pct}%)</span>
              </div>
              <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                <div class="bg-indigo-500 h-2 rounded-full" style="width: ${pct}%"></div>
              </div>
            </div>
          `;
        }

        // Pipeline Stages
        const sContainer = document.getElementById('stages-container');
        sContainer.innerHTML = '';
        const stages = globalOverview.pipeline_stages || {};
        for (const [st, count] of Object.entries(stages)) {
          sContainer.innerHTML += `
            <div class="flex items-center justify-between p-2 rounded-lg bg-slate-50 border border-slate-100 text-xs">
              <span class="capitalize font-medium text-slate-700">${st.replace('_', ' ')}</span>
              <span class="font-bold px-2 py-0.5 rounded bg-white border border-slate-200 text-slate-800">${count}</span>
            </div>
          `;
        }

      } catch (err) {
        console.error("Failed to load overview:", err);
      }
    }

    // Save Incomplete Draft
    async function saveDraft() {
      const workerId = document.getElementById('form-worker-id').value.trim();
      const occId = document.getElementById('form-occupation').value;
      const exp = parseFloat(document.getElementById('form-experience').value) || 0;
      const reg = document.getElementById('form-region').value.trim();
      const ctx = document.getElementById('form-context').value;
      const lang = document.getElementById('form-language').value;
      const script = document.getElementById('form-script').value;

      const tasks = [];
      document.querySelectorAll('#tasks-container .task-card').forEach((card, i) => {
        const text = card.querySelector('.task-description').value;
        tasks.push({ task_id: `TSK-${i+1:02d}`, description: text });
      });

      const payload = {
        worker_id: workerId,
        occupation_id: occId,
        experience_years: exp,
        region: reg,
        work_context: ctx,
        original_language: lang,
        script_type: script,
        tasks: tasks,
        consent_text_confirmed: document.getElementById('consent-text').checked,
        consent_audio_confirmed: document.getElementById('consent-audio').checked,
        consent_photo_confirmed: document.getElementById('consent-photo').checked
      };

      try {
        const res = await fetch('/api/draft', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (res.ok) {
          alert(`Draft saved successfully for worker ${workerId}!`);
        } else {
          alert(`Error saving draft: ${data.detail || 'Unknown error'}`);
        }
      } catch (err) {
        alert(`Network error saving draft: ${err.message}`);
      }
    }

    // Submit Complete Genuine Interview
    async function submitInterview() {
      const workerId = document.getElementById('form-worker-id').value.trim();
      const occId = document.getElementById('form-occupation').value;
      const exp = parseFloat(document.getElementById('form-experience').value) || 0;
      const reg = document.getElementById('form-region').value.trim();
      const ctx = document.getElementById('form-context').value;
      const lang = document.getElementById('form-language').value;
      const script = document.getElementById('form-script').value;
      const consentText = document.getElementById('consent-text').checked;

      if (!consentText) {
        alert("DPDP Consent Required: Please tick the Text Interview Consent box after receiving the worker's affirmative consent.");
        return;
      }

      const tasks = [];
      let emptyCount = 0;
      document.querySelectorAll('#tasks-container .task-card').forEach((card, i) => {
        const text = card.querySelector('.task-description').value.trim();
        if (text) {
          tasks.push({
            task_id: `TSK-${i+1:02d}`,
            description: text,
            skill_spans: []
          });
        } else {
          emptyCount++;
        }
      });

      if (tasks.length === 0) {
        alert("Please enter at least one detailed task description before submitting.");
        return;
      }

      const payload = {
        worker_id: workerId,
        occupation_id: occId,
        experience_years: exp,
        region: reg,
        work_context: ctx,
        original_language: lang,
        script_type: script,
        tasks: tasks,
        consent_text_confirmed: consentText,
        consent_audio_confirmed: document.getElementById('consent-audio').checked,
        consent_photo_confirmed: document.getElementById('consent-photo').checked,
        interviewer_id: "INT-FIELD-01",
        source_reference: "delhi_karol_bagh_pilot_b1"
      };

      try {
        const res = await fetch('/api/interview/submit', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (res.ok) {
          alert(`Success! Created ${data.records.length} genuine interview task records for worker ${workerId}.`);
          // Clear inputs
          document.querySelectorAll('#tasks-container .task-description').forEach(ta => ta.value = '');
          generateWorkerId();
          switchTab('records');
        } else {
          alert(`Submission validation failed: ${data.detail || 'Unknown error'}`);
        }
      } catch (err) {
        alert(`Network error submitting interview: ${err.message}`);
      }
    }

    // Load Records
    async function loadRecords() {
      try {
        const res = await fetch('/api/records');
        const data = await res.json();
        globalRecords = data.records || [];
        globalDrafts = data.drafts || [];
        renderRecordsTable();
      } catch (err) {
        console.error("Failed to load records:", err);
      }
    }

    // Render Records Table
    function renderRecordsTable() {
      const tbody = document.getElementById('records-tbody');
      tbody.innerHTML = '';

      const fOcc = document.getElementById('filter-occupation').value;
      const fStatus = document.getElementById('filter-status').value;

      const filtered = globalRecords.filter(r => {
        if (fOcc !== 'ALL' && r.occupation_id !== fOcc) return false;
        if (fStatus !== 'ALL' && r.annotation_status !== fStatus) return false;
        return true;
      });

      if (filtered.length === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="8" class="p-8 text-center text-slate-400">
              <i class="fa-solid fa-inbox text-3xl mb-2 text-slate-300"></i>
              <p class="font-medium text-slate-600">No genuine worker records submitted yet.</p>
              <p class="text-[11px] text-slate-400">Use the 'New Interview' tab to collect your first real worker description.</p>
            </td>
          </tr>
        `;
        return;
      }

      filtered.forEach(r => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-50 transition border-b';
        tr.innerHTML = `
          <td class="p-3 font-mono font-bold text-slate-900">${r.record_id}</td>
          <td class="p-3 font-mono text-indigo-700">${r.worker_id}</td>
          <td class="p-3">
            <span class="bg-indigo-50 text-indigo-700 font-semibold px-2 py-0.5 rounded text-[11px]">${r.occupation_id}</span>
          </td>
          <td class="p-3 uppercase text-[11px] font-bold text-slate-500">${r.original_language}</td>
          <td class="p-3 max-w-xs truncate" title="${r.worker_description}">${r.worker_description}</td>
          <td class="p-3">
            <span class="bg-amber-100 text-amber-800 font-bold px-2 py-0.5 rounded text-[11px]">${(r.skill_spans || []).length} spans</span>
          </td>
          <td class="p-3">
            <span class="capitalize px-2 py-0.5 rounded text-[11px] font-semibold bg-emerald-100 text-emerald-800">${r.annotation_status}</span>
          </td>
          <td class="p-3 text-right space-x-1">
            <button onclick="openAnnotatorModal('${r.record_id}')" class="px-2.5 py-1 bg-indigo-50 text-indigo-700 rounded hover:bg-indigo-100 font-semibold text-[11px]">
              <i class="fa-solid fa-pen-nib mr-1"></i> Annotate
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    // Open Annotator Modal
    function openAnnotatorModal(recId) {
      const rec = globalRecords.find(r => r.record_id === recId);
      if (!rec) return;
      activeAnnotatingRecord = rec;
      currentRecordSpans = [...(rec.skill_spans || [])];

      document.getElementById('modal-record-title').textContent = `Record: ${rec.record_id} (${rec.occupation}) | Worker: ${rec.worker_id}`;
      document.getElementById('modal-verbatim-text').textContent = rec.worker_description;

      document.getElementById('selected-substring').value = '';
      document.getElementById('selected-start').value = '';
      document.getElementById('selected-end').value = '';

      renderCurrentSpansList();
      document.getElementById('annotator-modal').classList.remove('hidden');
    }

    function closeAnnotatorModal() {
      document.getElementById('annotator-modal').classList.add('hidden');
      activeAnnotatingRecord = null;
    }

    // Capture Selection
    function captureSelection() {
      const sel = window.getSelection();
      const sub = sel.toString().trim();
      if (!sub || !activeAnnotatingRecord) return;

      const fullText = activeAnnotatingRecord.worker_description;
      const start = fullText.indexOf(sub);
      if (start !== -1) {
        const end = start + sub.length;
        document.getElementById('selected-substring').value = sub;
        document.getElementById('selected-start').value = start;
        document.getElementById('selected-end').value = end;
      }
    }

    // Add Selected Span
    function addSelectedSpan() {
      const sub = document.getElementById('selected-substring').value.trim();
      const start = parseInt(document.getElementById('selected-start').value);
      const end = parseInt(document.getElementById('selected-end').value);
      const cat = document.getElementById('selected-category').value;
      const can = document.getElementById('selected-canonical').value;

      if (!sub || isNaN(start) || isNaN(end)) {
        alert("Please highlight a valid phrase from the description first.");
        return;
      }

      const spanId = `SP-${currentRecordSpans.length + 1:02d}`;
      currentRecordSpans.push({
        span_id: spanId,
        extracted_skill: sub,
        start_offset: start,
        end_offset: end,
        skill_category: cat,
        canonical_skill: can,
        alternative_skill_names: [sub],
        confidence_score: 1.0,
        mapping_status: "mapped",
        is_unmapped_skill: false
      });

      renderCurrentSpansList();
      document.getElementById('selected-substring').value = '';
      document.getElementById('selected-start').value = '';
      document.getElementById('selected-end').value = '';
    }

    function renderCurrentSpansList() {
      const container = document.getElementById('modal-spans-list');
      container.innerHTML = '';
      if (currentRecordSpans.length === 0) {
        container.innerHTML = '<p class="text-xs text-slate-400 italic">No spans annotated yet.</p>';
        return;
      }
      currentRecordSpans.forEach((sp, idx) => {
        const div = document.createElement('div');
        div.className = 'flex items-center justify-between p-2 bg-slate-50 border border-slate-200 rounded-lg text-xs';
        div.innerHTML = `
          <div>
            <span class="font-bold text-indigo-700">${sp.span_id}:</span>
            <span class="font-semibold text-slate-900">"${sp.extracted_skill}"</span>
            <span class="text-slate-400 font-mono text-[10px] ml-1">[${sp.start_offset}:${sp.end_offset}]</span>
            <span class="bg-indigo-100 text-indigo-800 text-[10px] font-semibold px-1.5 py-0.5 rounded ml-1">${sp.skill_category}</span>
            <div class="text-[11px] text-slate-500 mt-0.5">Canonical: ${sp.canonical_skill}</div>
          </div>
          <button onclick="removeSpan(${idx})" class="text-red-500 hover:text-red-700 p-1">
            <i class="fa-solid fa-trash-can"></i>
          </button>
        `;
        container.appendChild(div);
      });
    }

    function removeSpan(idx) {
      currentRecordSpans.splice(idx, 1);
      renderCurrentSpansList();
    }

    // Save Record Annotations to Server
    async function saveRecordAnnotations() {
      if (!activeAnnotatingRecord) return;
      try {
        const res = await fetch(`/api/records/${activeAnnotatingRecord.record_id}/annotate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(currentRecordSpans)
        });
        const data = await res.json();
        if (res.ok) {
          alert("Annotations saved successfully!");
          closeAnnotatorModal();
          loadRecords();
        } else {
          alert(`Error saving annotations: ${data.detail}`);
        }
      } catch (err) {
        alert(`Network error saving annotations: ${err.message}`);
      }
    }

    // Update Record Stage
    async function updateRecordStage(newStatus) {
      if (!activeAnnotatingRecord) return;
      try {
        const res = await fetch(`/api/records/${activeAnnotatingRecord.record_id}/status`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            record_id: activeAnnotatingRecord.record_id,
            new_status: newStatus,
            reviewer_status: newStatus === 'approved' ? 'approved' : 'pending',
            reviewer_id: "REV-HUMAN-01"
          })
        });
        const data = await res.json();
        if (res.ok) {
          alert(`Record marked as ${newStatus}!`);
          closeAnnotatorModal();
          loadRecords();
        } else {
          alert(`Error updating status: ${data.detail}`);
        }
      } catch (err) {
        alert(`Network error: ${err.message}`);
      }
    }

    // Run Quality Audit
    async function runQualityAudit() {
      const container = document.getElementById('quality-audit-results');
      container.innerHTML = '<p class="text-xs text-slate-500">Auditing genuine records for offset mismatches and duplicates...</p>';
      try {
        const res = await fetch('/api/quality');
        const audit = await res.json();

        container.innerHTML = `
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="p-4 rounded-xl border ${audit.offset_errors_count === 0 ? 'bg-emerald-50 border-emerald-200' : 'bg-red-50 border-red-200'}">
              <div class="text-xs font-semibold uppercase text-slate-500">Offset Errors</div>
              <div class="text-2xl font-bold ${audit.offset_errors_count === 0 ? 'text-emerald-700' : 'text-red-700'}">${audit.offset_errors_count}</div>
              <div class="text-[11px] text-slate-500">text[start:end] == span</div>
            </div>

            <div class="p-4 rounded-xl border ${audit.duplicate_records_count === 0 ? 'bg-emerald-50 border-emerald-200' : 'bg-red-50 border-red-200'}">
              <div class="text-xs font-semibold uppercase text-slate-500">Duplicate Narratives</div>
              <div class="text-2xl font-bold ${audit.duplicate_records_count === 0 ? 'text-emerald-700' : 'text-red-700'}">${audit.duplicate_records_count}</div>
              <div class="text-[11px] text-slate-500">Zero duplicate policy</div>
            </div>

            <div class="p-4 rounded-xl border ${audit.missing_consent_count === 0 ? 'bg-emerald-50 border-emerald-200' : 'bg-red-50 border-red-200'}">
              <div class="text-xs font-semibold uppercase text-slate-500">Missing DPDP Consent</div>
              <div class="text-2xl font-bold ${audit.missing_consent_count === 0 ? 'text-emerald-700' : 'text-red-700'}">${audit.missing_consent_count}</div>
              <div class="text-[11px] text-slate-500">Strict legal gating</div>
            </div>

            <div class="p-4 rounded-xl border bg-slate-50 border-slate-200">
              <div class="text-xs font-semibold uppercase text-slate-500">Audited Genuine Records</div>
              <div class="text-2xl font-bold text-slate-800">${audit.total_records_audited}</div>
              <div class="text-[11px] text-slate-500">Real field batches</div>
            </div>
          </div>
        `;

        if (audit.offset_errors && audit.offset_errors.length > 0) {
          container.innerHTML += `
            <div class="p-4 bg-red-50 border border-red-200 rounded-xl space-y-2">
              <h4 class="text-xs font-bold text-red-800 uppercase">Offset Mismatches Detected:</h4>
              <ul class="text-xs text-red-700 space-y-1 font-mono">
                ${audit.offset_errors.map(e => `<li>${e.record_id}: Expected '${e.expected}', Found '${e.actual}'</li>`).join('')}
              </ul>
            </div>
          `;
        } else {
          container.innerHTML += `
            <div class="p-4 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center space-x-3 text-emerald-800 text-xs">
              <i class="fa-solid fa-circle-check text-lg"></i>
              <span><strong>100% Quality Verification Passed:</strong> All character slices match verbatim text and DPDP consent is verified.</span>
            </div>
          `;
        }
      } catch (err) {
        container.innerHTML = `<p class="text-xs text-red-600">Failed to run audit: ${err.message}</p>`;
      }
    }

    // Export Helpers
    function exportJsonl() {
      window.location.href = '/api/export/jsonl';
    }

    function exportCsv() {
      window.location.href = '/api/export/csv';
    }

    // Initialize
    window.addEventListener('DOMContentLoaded', () => {
      loadTaxonomy();
      loadOverview();
    });
  </script>
</body>
</html>
"""
    return HTMLResponse(content=html_content)

def main():
    import uvicorn
    port = int(os.environ.get("COLLECTION_PORT", "8501"))
    print("=" * 65)
    print("ELEVATE X AI — FIELD WORKER DATA COLLECTION WORKSTATION")
    print("=" * 65)
    print(f"Target Occupations: Tailor, Electrician, Plumber, Motor Mechanic (25 each)")
    print(f"Local Console URL:  http://localhost:{port}")
    print(f"Swagger API Docs:   http://localhost:{port}/docs")
    print("=" * 65)
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

if __name__ == "__main__":
    main()

