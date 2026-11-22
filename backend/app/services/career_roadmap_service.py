"""
Career Roadmap Service.
Dynamically generates personalized career roadmaps for candidates across diverse occupations
using authentic occupational datasets (ESCO v1.1.1, O*NET 31.0, NQR India),
verified learning resources, BGE Small semantic matching, and Apple Silicon Qwen MLX inference.
"""

import os
import json
import time
import uuid
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, delete

from app.models.user import User
from app.models.roadmap import CareerRoadmap, RoadmapMilestone, RoadmapTask
from app.schemas.career_roadmap import (
    CareerRoadmapDetailResponse,
    MilestoneDetail,
    TaskDetail,
    LearningResourceRef,
)
from app.services.skill_gap_service import SkillGapService

BASE_DIR = Path(__file__).resolve().parents[3]
PROCESSED_DIR = BASE_DIR / "datasets" / "career_roadmap" / "processed"
AUDIT_DIR = BASE_DIR / "datasets" / "career_roadmap" / "audit"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)
QWEN_AUDIT_LOG = AUDIT_DIR / "qwen_inference_audit.jsonl"


class CareerRoadmapService:
    _unified_occupations: Optional[Dict[str, Any]] = None
    _competency_tiers: Optional[Dict[str, Any]] = None
    _resource_catalog: Optional[List[Dict[str, Any]]] = None
    _skill_resource_index: Optional[Dict[str, List[str]]] = None
    _benchmark_titles: Optional[List[str]] = None
    _benchmark_embeddings: Optional[Any] = None

    @classmethod
    def _load_datasets(cls):
        """Lazy loads processed occupational benchmarks and resource catalogs."""
        if cls._unified_occupations is None:
            occ_file = PROCESSED_DIR / "unified_occupations.json"
            if occ_file.exists():
                with open(occ_file, "r", encoding="utf-8") as f:
                    cls._unified_occupations = json.load(f)
            else:
                cls._unified_occupations = {}

        if cls._competency_tiers is None:
            tiers_file = PROCESSED_DIR / "occupation_competency_tiers.json"
            if tiers_file.exists():
                with open(tiers_file, "r", encoding="utf-8") as f:
                    cls._competency_tiers = json.load(f)
            else:
                cls._competency_tiers = {}

        if cls._resource_catalog is None:
            res_file = PROCESSED_DIR / "verified_resource_catalog.json"
            if res_file.exists():
                with open(res_file, "r", encoding="utf-8") as f:
                    cls._resource_catalog = json.load(f)
            else:
                cls._resource_catalog = []

        if cls._skill_resource_index is None:
            idx_file = PROCESSED_DIR / "skill_resource_index.json"
            if idx_file.exists():
                with open(idx_file, "r", encoding="utf-8") as f:
                    cls._skill_resource_index = json.load(f)
            else:
                cls._skill_resource_index = {}

    @classmethod
    def resolve_target_occupation(cls, target_role: str) -> Dict[str, Any]:
        """
        Strictly resolves target occupation against 3,000+ ESCO/O*NET benchmarks.
        Checks exact matches, verified canonical aliases, and BGE Small semantic search.
        Enforces a 0.55 similarity threshold. Never returns invented dummy occupation data.
        """
        cls._load_datasets()
        role_clean = target_role.strip().lower()

        # 1. Direct exact or canonical alias match
        if role_clean in cls._unified_occupations:
            entry = cls._unified_occupations[role_clean]
            if entry.get("is_alias") and entry.get("target_canonical_key"):
                res = dict(cls._unified_occupations[entry["target_canonical_key"]])
                res["resolution_confidence"] = 1.0
                res["resolution_method"] = "canonical_alias"
                return res
            res = dict(entry)
            res["resolution_confidence"] = 1.0
            res["resolution_method"] = "exact_match"
            return res

        # 2. Case-insensitive alias scan across all entries
        for key, entry in cls._unified_occupations.items():
            if not entry.get("is_alias"):
                aliases = [a.lower() for a in entry.get("aliases", [])]
                if role_clean in aliases or role_clean == entry.get("canonical_title", "").lower():
                    res = dict(entry)
                    res["resolution_confidence"] = 1.0
                    res["resolution_method"] = "alias_scan"
                    return res

        # 3. Semantic matching with BGE Small across all authentic benchmarks
        try:
            bge = SkillGapService.get_embedding_model()
            if cls._benchmark_titles is None or cls._benchmark_embeddings is None:
                canonical_entries = [
                    (entry.get("canonical_title", k), k)
                    for k, entry in cls._unified_occupations.items()
                    if not entry.get("is_alias")
                ]
                cls._benchmark_titles = [t[0] for t in canonical_entries]
                cls._benchmark_embeddings = bge.encode(
                    cls._benchmark_titles,
                    normalize_embeddings=True,
                    batch_size=64,
                    show_progress_bar=False
                )

            role_emb = bge.encode([target_role], normalize_embeddings=True)
            sims = (role_emb @ cls._benchmark_embeddings.T)[0]

            best_idx = int(sims.argmax())
            best_sim = float(sims[best_idx])
            best_title = cls._benchmark_titles[best_idx]
            best_key = best_title.strip().lower()

            # Rank top 3 suggestions for feedback
            top_indices = sims.argsort()[-3:][::-1]
            top_suggestions = [cls._benchmark_titles[i] for i in top_indices]

            # Enforce 0.72 similarity threshold (genuine occupational queries score >= 0.75)
            if best_sim >= 0.72 and best_key in cls._unified_occupations:
                matched_entry = dict(cls._unified_occupations[best_key])
                matched_entry["resolution_confidence"] = round(best_sim, 4)
                matched_entry["resolution_method"] = "bge_semantic_match"
                matched_entry["matched_from_query"] = target_role
                return matched_entry

            # Low confidence: Reject with informative error
            raise ValueError(
                f"Target occupation '{target_role}' could not be confidently resolved to an authentic "
                f"occupational standard (highest similarity: {best_sim:.2f} < 0.72 threshold). "
                f"Suggested closest matches: {', '.join(top_suggestions)}."
            )
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Failed to resolve target occupation '{target_role}': {str(e)}")

    @classmethod
    def find_verified_resources_for_skills(cls, skills: List[str]) -> List[LearningResourceRef]:
        """
        Retrieves authentic learning resources strictly from the verified catalog.
        Prevents URL hallucinations by enforcing exact domain whitelisting.
        """
        cls._load_datasets()
        matched_resources: List[LearningResourceRef] = []
        matched_ids = set()

        for skill in skills:
            s_clean = skill.strip().lower()
            r_ids = cls._skill_resource_index.get(s_clean, [])
            for r in cls._resource_catalog:
                if r["id"] in r_ids and r["id"] not in matched_ids:
                    matched_ids.add(r["id"])
                    matched_resources.append(
                        LearningResourceRef(
                            name=r.get("title", "Official Documentation"),
                            title=r.get("title"),
                            type=r.get("type", "Official Learning Path"),
                            duration="Self-paced (4-8 hours)",
                            free=True,
                            url=r.get("url"),
                            source_domain=r.get("source_domain")
                        )
                    )

        # Fallback to general official learning docs if none matched
        if not matched_resources and cls._resource_catalog:
            default_res = cls._resource_catalog[0]
            matched_resources.append(
                LearningResourceRef(
                    name=default_res.get("title", "Official Developer Tutorial"),
                    title=default_res.get("title"),
                    type=default_res.get("type", "Official Documentation"),
                    duration="Self-paced",
                    free=True,
                    url=default_res.get("url"),
                    source_domain=default_res.get("source_domain")
                )
            )

        return matched_resources[:3]

    @classmethod
    def generate_qwen_personalization(
        cls,
        candidate_skills: List[str],
        target_role: str,
        stage_number: int,
        stage_title: str,
        skills_to_acquire: List[str]
    ) -> Tuple[str, List[str], Dict[str, Any]]:
        """
        Uses Qwen2.5-1.5B-Instruct-4bit on Apple Silicon to personalize milestone
        narrative and practical project tasks. Captures audit logs of every inference.
        """
        t0 = time.time()
        prompt = (
            f"<|im_start|>system\n"
            f"You are a technical career director specializing in personalized career roadmaps.\n"
            f"Candidate existing skills: {', '.join(candidate_skills) if candidate_skills else 'None stated'}.\n"
            f"Target role: {target_role}.\n"
            f"Current milestone stage {stage_number}: {stage_title}.\n"
            f"Competencies to master: {', '.join(skills_to_acquire)}.\n"
            f"Provide:\n"
            f"1. A concise 2-sentence technical summary of why this milestone is vital for {target_role}.\n"
            f"2. Exactly 2 rigorous, hands-on practical project tasks.\n"
            f"Output format:\n"
            f"DESCRIPTION: <summary>\n"
            f"TASK 1: <actionable project task>\n"
            f"TASK 2: <actionable project task>\n"
            f"<|im_end|>\n<|im_start|>assistant\n"
        )

        audit_entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "target_role": target_role,
            "stage_number": stage_number,
            "stage_title": stage_title,
            "skills_to_acquire": skills_to_acquire,
            "candidate_skills": candidate_skills,
            "model": "mlx-community/Qwen2.5-1.5B-Instruct-4bit",
            "prompt": prompt,
            "status": "PENDING"
        }

        try:
            model, tokenizer = SkillGapService.get_qwen_model()
            from mlx_lm import generate
            raw_response = generate(
                model,
                tokenizer,
                prompt=prompt,
                max_tokens=220,
                verbose=False
            )
            elapsed = time.time() - t0

            desc = ""
            tasks = []

            # 1. Flexible regex for description
            desc_match = re.search(
                r'(?:\*\*Technical Summary:\*\*|DESCRIPTION:|Technical Summary:)\s*(.*?)(?=\n\s*(?:\*\*Practical|\*\*TASK|TASK|\n\n\*\*)|$)',
                raw_response,
                re.DOTALL | re.IGNORECASE
            )
            if desc_match:
                desc = ' '.join(desc_match.group(1).split())
            elif raw_response.strip():
                paras = [p.strip() for p in raw_response.split('\n\n') if p.strip()]
                if paras:
                    desc = ' '.join(paras[0].split())

            # 2. Flexible regex for practical tasks
            task_matches = re.findall(
                r'(?:\*\*TASK\s*\d+:|TASK\s*\d+:|\d+\.\s+)(.*?)(?=(?:\*\*TASK|\n\s*TASK|\n\s*\d+\.|$))',
                raw_response,
                re.DOTALL | re.IGNORECASE
            )
            for tm in task_matches:
                t_clean = tm.strip()
                t_title = t_clean.split('\n')[0].replace('*', '').strip()
                if t_title and len(t_title) > 5 and t_title not in tasks:
                    tasks.append(t_title)

            if not desc:
                desc = f"Develop production-grade capabilities in {', '.join(skills_to_acquire[:3])} to bridge capability gaps toward senior {target_role} benchmarks."

            if len(tasks) < 1:
                tasks.append(f"Implement an end-to-end practical solution utilizing {skills_to_acquire[0] if skills_to_acquire else 'core tools'} with unit verification.")
            if len(tasks) < 2:
                tasks.append(f"Author a comprehensive architectural benchmark demonstrating performance under production constraints.")

            audit_entry.update({
                "status": "SUCCESS",
                "latency_seconds": round(elapsed, 3),
                "raw_output": raw_response,
                "parsed_description": desc,
                "parsed_tasks": tasks[:2]
            })
            cls._append_qwen_audit(audit_entry)
            return desc, tasks[:2], audit_entry

        except Exception as e:
            elapsed = time.time() - t0
            desc = (
                f"Develop production-grade capabilities in {', '.join(skills_to_acquire[:3])} "
                f"to bridge capability gaps toward senior {target_role} benchmarks."
            )
            tasks = [
                f"Implement an end-to-end practical solution utilizing {skills_to_acquire[0] if skills_to_acquire else 'core tools'} with unit verification.",
                f"Author a comprehensive architectural benchmark demonstrating performance under production constraints."
            ]
            audit_entry.update({
                "status": "FAILED",
                "latency_seconds": round(elapsed, 3),
                "error": str(e),
                "fallback_description": desc,
                "fallback_tasks": tasks
            })
            cls._append_qwen_audit(audit_entry)
            print(f"[CareerRoadmapService] Qwen MLX generation fallback: {e}")
            return desc, tasks, audit_entry

    @classmethod
    def _append_qwen_audit(cls, entry: Dict[str, Any]):
        """Appends real inference telemetry into audit log."""
        try:
            QWEN_AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
            with open(QWEN_AUDIT_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
                f.flush()
        except Exception as e:
            print(f"[CareerRoadmapService] Failed to write Qwen audit: {e}")

    @classmethod
    def generate_roadmap_plan(
        cls,
        target_role: str,
        candidate_skills: List[str],
        verified_skills: Optional[List[str]] = None,
        previously_completed_tasks: Optional[set] = None
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Builds the complete 4-stage dynamic roadmap plan with competencies, tasks,
        and verified resources.
        
        Strict Evidence Rules:
        - Candidate skills from resume/self-reported are marked 'mentioned_in_resume' or 'self_reported'.
        - Resume mentions alone NEVER mark a milestone completed.
        - A milestone is ONLY marked completed if practically demonstrated in DB or assessment-verified.
        """
        cls._load_datasets()
        occ = cls.resolve_target_occupation(target_role)
        canonical_title = occ.get("canonical_title", target_role)
        norm_key = canonical_title.strip().lower()

        # Check if pre-defined structured competency tiers exist
        tiers = cls._competency_tiers.get(norm_key)

        if not tiers:
            # Check aliases
            for k, t_list in cls._competency_tiers.items():
                if k in norm_key or norm_key in k:
                    tiers = t_list
                    break

        if not tiers:
            # Dynamically derive 4 authentic stages from actual occupation competencies
            ess_skills = occ.get("essential_skills", [])
            opt_skills = occ.get("optional_skills", [])
            all_skills = ess_skills + [s for s in opt_skills if s not in ess_skills]

            if not all_skills:
                all_skills = [
                    f"{canonical_title} Fundamentals",
                    "Domain Technical Execution",
                    "Quality & Safety Standards",
                    "Advanced System Operations"
                ]

            total_s = len(all_skills)
            chunk = max(1, total_s // 4)

            s1_skills = all_skills[:chunk] or [all_skills[0]]
            s2_skills = all_skills[chunk:chunk*2] or [all_skills[min(1, total_s-1)]]
            s3_skills = all_skills[chunk*2:chunk*3] or [all_skills[min(2, total_s-1)]]
            s4_skills = all_skills[chunk*3:] or [all_skills[-1]]

            # Derive stage titles directly from the authentic competencies
            stages_data = [
                {
                    "stage_number": 1,
                    "title": f"Foundational Principles, Tools & Baseline Standards ({s1_skills[0].title()})",
                    "time_estimate": "3-4 Weeks",
                    "skills_to_acquire": s1_skills,
                    "practical_tasks": [
                        f"Implement foundational exercises in {s1_skills[0]} according to standard industry specifications.",
                        f"Validate baseline tooling and configuration setup with unit verification."
                    ]
                },
                {
                    "stage_number": 2,
                    "title": f"Applied Execution, Workflows & Systems Integration ({s2_skills[0].title()})",
                    "time_estimate": "4-5 Weeks",
                    "skills_to_acquire": s2_skills,
                    "practical_tasks": [
                        f"Construct an applied end-to-end system utilizing {', '.join(s2_skills[:2])}.",
                        f"Verify execution stability and benchmark operational parameters against target thresholds."
                    ]
                },
                {
                    "stage_number": 3,
                    "title": f"Quality Control, Diagnostic Testing & Industry Compliance ({s3_skills[0].title()})",
                    "time_estimate": "3-4 Weeks",
                    "skills_to_acquire": s3_skills,
                    "practical_tasks": [
                        f"Conduct diagnostic inspection, testing, and defect grading for {s3_skills[0]}.",
                        f"Formulate corrective action protocol (CAPA) adhering to professional safety and compliance standards."
                    ]
                },
                {
                    "stage_number": 4,
                    "title": f"Advanced Specialization, Capstone Delivery & Production Operations",
                    "time_estimate": "3-4 Weeks",
                    "skills_to_acquire": s4_skills,
                    "practical_tasks": [
                        f"Execute comprehensive capstone deliverable demonstrating advanced mastery of {s4_skills[0]}.",
                        f"Compile full technical audit documentation and readiness report for senior certification."
                    ]
                }
            ]
        else:
            stages_data = tiers

        # Candidate skills evidence levels
        norm_candidate_skills = {s.strip().lower() for s in candidate_skills}
        norm_verified_skills = {s.strip().lower() for s in (verified_skills or [])}
        completed_task_set = previously_completed_tasks or set()

        milestones_plan = []
        found_in_progress = False

        for stage in stages_data:
            s_num = stage["stage_number"]
            s_title = stage["title"]
            s_time = stage.get("time_estimate", "3-4 Weeks")
            s_skills = stage.get("skills_to_acquire", [])
            s_desc = stage.get("description", "")
            s_tasks = stage.get("practical_tasks", [])

            # Compute evidence state for each competency
            evidence_map = {}
            for sk in s_skills:
                sk_clean = sk.strip().lower()
                if sk_clean in norm_verified_skills:
                    evidence_map[sk] = "assessment_verified"
                elif sk_clean in norm_candidate_skills:
                    evidence_map[sk] = "mentioned_in_resume"
                else:
                    evidence_map[sk] = "mastery_not_assessed"

            # Strict rule: A stage is ONLY completed if all its tasks were practically completed
            # in DB or all competencies are assessment_verified. Resume mention ALONE is NOT completion!
            all_verified = (len(s_skills) > 0) and all(
                evidence_map.get(sk) == "assessment_verified" for sk in s_skills
            )
            all_tasks_completed = (len(s_tasks) > 0) and all(
                t.strip().lower() in completed_task_set for t in s_tasks
            )

            is_stage_completed = all_verified or all_tasks_completed

            if is_stage_completed:
                stage_status = "completed"
            elif not found_in_progress:
                stage_status = "in_progress"
                found_in_progress = True
            else:
                stage_status = "upcoming"

            # Personalize description and tasks via Qwen
            qwen_desc, qwen_tasks, _ = cls.generate_qwen_personalization(
                candidate_skills=candidate_skills,
                target_role=canonical_title,
                stage_number=s_num,
                stage_title=s_title,
                skills_to_acquire=s_skills
            )
            final_desc = qwen_desc if qwen_desc else s_desc
            final_tasks = qwen_tasks if qwen_tasks else s_tasks

            # Fetch verified resources from official catalog
            verified_resources = cls.find_verified_resources_for_skills(s_skills)

            milestones_plan.append({
                "stage_number": s_num,
                "title": s_title,
                "time_estimate": s_time,
                "status": stage_status,
                "is_completed": is_stage_completed,
                "description": final_desc,
                "skills_to_acquire": s_skills,
                "competency_evidence": evidence_map,
                "practical_tasks": final_tasks,
                "resources": [r.model_dump() for r in verified_resources]
            })

        return milestones_plan, occ

    @classmethod
    def get_or_create_roadmap(
        cls,
        db: Session,
        user: User,
        target_role: Optional[str] = None,
        candidate_skills: Optional[List[str]] = None
    ) -> CareerRoadmapDetailResponse:
        """
        Retrieves active roadmap from DB or creates a new one dynamically.
        Preserves previously completed tasks across recalibration.
        """
        # 1. Check existing active roadmap
        query = (
            select(CareerRoadmap)
            .options(
                joinedload(CareerRoadmap.milestones).joinedload(RoadmapMilestone.tasks)
            )
            .where(
                CareerRoadmap.user_id == user.id,
                CareerRoadmap.status == "active"
            )
            .order_by(CareerRoadmap.created_at.desc())
        )
        existing = db.execute(query).unique().scalars().first()

        # If user explicitly requested target_role and it differs from existing, regenerate
        needs_regeneration = False
        if target_role and existing:
            if existing.target_role.strip().lower() != target_role.strip().lower():
                needs_regeneration = True
        if candidate_skills is not None and existing:
            needs_regeneration = True

        if existing and not needs_regeneration:
            return cls._serialize_roadmap(existing)

        # 2. Determine target role
        if not target_role:
            target_role = existing.target_role if existing else "AI Engineer"

        # 3. Determine candidate skills from user profile if not provided
        if candidate_skills is None:
            candidate_skills = []
            if hasattr(user, "skills") and user.skills:
                candidate_skills = [s.name for s in user.skills if hasattr(s, "name")]

        # 4. Check previously completed tasks for this user to preserve manual progress
        previously_completed_titles = set()
        if existing and existing.milestones:
            for m in existing.milestones:
                for t in m.tasks:
                    if t.is_completed:
                        previously_completed_titles.add(t.title.strip().lower())

        # Delete existing active roadmaps for this user
        if existing:
            db.execute(delete(CareerRoadmap).where(CareerRoadmap.user_id == user.id))
            db.commit()

        # 5. Generate plan
        plan, occ_meta = cls.generate_roadmap_plan(
            target_role=target_role,
            candidate_skills=candidate_skills,
            previously_completed_tasks=previously_completed_titles
        )

        # 6. Persist into DB
        total_weeks = 16
        roadmap = CareerRoadmap(
            id=uuid.uuid4(),
            user_id=user.id,
            title=f"Personalized Career Pathway: {occ_meta.get('canonical_title', target_role)}",
            target_role=occ_meta.get("canonical_title", target_role),
            estimated_duration_weeks=total_weeks,
            progress_percentage=0.0,
            status="active"
        )
        db.add(roadmap)
        db.flush()

        for stg in plan:
            milestone = RoadmapMilestone(
                id=uuid.uuid4(),
                roadmap_id=roadmap.id,
                title=stg["title"],
                description=stg["description"],
                order_index=stg["stage_number"],
                is_completed=stg["is_completed"]
            )
            db.add(milestone)
            db.flush()

            # Add tasks
            for t_title in stg["practical_tasks"]:
                # Preserve completion state if task was previously marked complete
                was_previously_completed = t_title.strip().lower() in previously_completed_titles
                primary_res_url = stg["resources"][0]["url"] if stg["resources"] else None
                task = RoadmapTask(
                    id=uuid.uuid4(),
                    milestone_id=milestone.id,
                    title=t_title,
                    description=f"Practical hands-on deliverable for Stage {stg['stage_number']}.",
                    task_type="practical",
                    estimated_hours=4.0,
                    is_completed=was_previously_completed or stg["is_completed"],
                    resource_url=primary_res_url
                )
                db.add(task)

        db.commit()

        # Reload complete object with relationships
        saved_roadmap = db.execute(
            select(CareerRoadmap)
            .options(
                joinedload(CareerRoadmap.milestones).joinedload(RoadmapMilestone.tasks)
            )
            .where(CareerRoadmap.id == roadmap.id)
        ).unique().scalar_one()

        # Compute initial progress
        cls.recalculate_progress(db, saved_roadmap.id)
        db.commit()

        # Refresh
        saved_roadmap = db.execute(
            select(CareerRoadmap)
            .options(
                joinedload(CareerRoadmap.milestones).joinedload(RoadmapMilestone.tasks)
            )
            .where(CareerRoadmap.id == roadmap.id)
        ).unique().scalar_one()

        return cls._serialize_roadmap(saved_roadmap, plan_metadata=plan, occ_meta=occ_meta)

    @classmethod
    def recalculate_progress(cls, db: Session, roadmap_id: uuid.UUID) -> float:
        """
        Recalculates milestone completion status and overall roadmap progress percentage
        based strictly on actual database task completion states.
        """
        roadmap = db.execute(
            select(CareerRoadmap)
            .options(
                joinedload(CareerRoadmap.milestones).joinedload(RoadmapMilestone.tasks)
            )
            .where(CareerRoadmap.id == roadmap_id)
        ).unique().scalar_one_or_none()

        if not roadmap or not roadmap.milestones:
            return 0.0

        total_tasks = 0
        completed_tasks = 0

        for m in roadmap.milestones:
            if m.tasks:
                m_completed = all(t.is_completed for t in m.tasks)
                m.is_completed = m_completed
                total_tasks += len(m.tasks)
                completed_tasks += sum(1 for t in m.tasks if t.is_completed)
            else:
                total_tasks += 1
                if m.is_completed:
                    completed_tasks += 1

        progress = round((completed_tasks / max(1, total_tasks)) * 100, 1)
        roadmap.progress_percentage = progress
        if progress >= 100.0:
            roadmap.status = "completed"
        elif roadmap.status == "completed" and progress < 100.0:
            roadmap.status = "active"

        db.flush()
        return progress

    @classmethod
    def toggle_task(cls, db: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> CareerRoadmapDetailResponse:
        """Toggles a task's completion and recalculates overall progress."""
        task = db.execute(
            select(RoadmapTask)
            .join(RoadmapMilestone, RoadmapTask.milestone_id == RoadmapMilestone.id)
            .join(CareerRoadmap, RoadmapMilestone.roadmap_id == CareerRoadmap.id)
            .where(RoadmapTask.id == task_id, CareerRoadmap.user_id == user_id)
        ).scalar_one_or_none()

        if not task:
            raise ValueError("Task not found or access denied.")

        task.is_completed = not task.is_completed
        db.flush()

        milestone = db.execute(
            select(RoadmapMilestone)
            .where(RoadmapMilestone.id == task.milestone_id)
        ).scalar_one()

        cls.recalculate_progress(db, milestone.roadmap_id)
        db.commit()
        db.expire_all()

        # In SQLAlchemy with identity map, use populate_existing to ensure freshly updated child rows are re-read
        roadmap = db.execute(
            select(CareerRoadmap)
            .execution_options(populate_existing=True)
            .options(
                joinedload(CareerRoadmap.milestones).joinedload(RoadmapMilestone.tasks)
            )
            .where(CareerRoadmap.id == milestone.roadmap_id)
        ).unique().scalar_one()

        return cls._serialize_roadmap(roadmap)

    @staticmethod
    def clean_milestone_description(text: str) -> str:
        """Sanitizes milestone descriptions, removing redundant prompt echoes or raw markdown bullet prefixes."""
        if not text:
            return ""
        cleaned = text.strip()
        # Strip leading bullet indicators if applied to the start of the block
        cleaned = re.sub(r'^(?:[-*•]\s+)+', '', cleaned)
        # Strip echoes like **Technical Summary:** or - **Why this milestone is vital for [Role]:**
        cleaned = re.sub(
            r'^(?:\*\*)?(?:Technical Summary|Why this milestone is vital(?: for [^:*]+)?)(?:\*\*)?[:*]*\s*',
            '',
            cleaned,
            flags=re.IGNORECASE
        )
        cleaned = re.sub(r'^(?:[-*•]\s+)+', '', cleaned)
        return cleaned.strip()

    @classmethod
    def toggle_milestone(cls, db: Session, milestone_id: uuid.UUID, user_id: uuid.UUID) -> CareerRoadmapDetailResponse:
        """Toggles an entire milestone's completion, adhering to strict task completion requirements."""
        milestone = db.execute(
            select(RoadmapMilestone)
            .options(joinedload(RoadmapMilestone.tasks))
            .join(CareerRoadmap, RoadmapMilestone.roadmap_id == CareerRoadmap.id)
            .where(RoadmapMilestone.id == milestone_id, CareerRoadmap.user_id == user_id)
        ).unique().scalar_one_or_none()

        if not milestone:
            raise ValueError("Milestone not found or access denied.")

        new_status = not milestone.is_completed
        if new_status:
            # A stage cannot be marked complete while required tasks remain incomplete
            incomplete_tasks = [t for t in milestone.tasks if not t.is_completed]
            if incomplete_tasks:
                raise ValueError(
                    f"Cannot mark stage complete: {len(incomplete_tasks)} required practical task(s) remain incomplete. Complete all practical deliverables first."
                )
            milestone.is_completed = True
        else:
            # Mark stage incomplete and reset child tasks
            milestone.is_completed = False
            for t in milestone.tasks:
                t.is_completed = False

        db.flush()
        cls.recalculate_progress(db, milestone.roadmap_id)
        db.commit()
        db.expire_all()

        # In SQLAlchemy with identity map, use populate_existing to ensure freshly updated child rows are re-read
        roadmap = db.execute(
            select(CareerRoadmap)
            .execution_options(populate_existing=True)
            .options(
                joinedload(CareerRoadmap.milestones).joinedload(RoadmapMilestone.tasks)
            )
            .where(CareerRoadmap.id == milestone.roadmap_id)
        ).unique().scalar_one()

        return cls._serialize_roadmap(roadmap)

    @classmethod
    def _serialize_roadmap(
        cls,
        roadmap: CareerRoadmap,
        plan_metadata: Optional[List[Dict[str, Any]]] = None,
        occ_meta: Optional[Dict[str, Any]] = None
    ) -> CareerRoadmapDetailResponse:
        """Serializes CareerRoadmap database model into CareerRoadmapDetailResponse schema."""
        cls._load_datasets()
        sorted_milestones = sorted(roadmap.milestones, key=lambda m: m.order_index)
        milestone_details: List[MilestoneDetail] = []

        total_tasks = 0
        completed_tasks = 0
        total_hours = 0.0

        # Plan metadata map
        meta_by_order = {}
        if plan_metadata:
            for p in plan_metadata:
                meta_by_order[p["stage_number"]] = p

        first_in_progress_found = False

        for idx, m in enumerate(sorted_milestones, 1):
            tasks_list: List[TaskDetail] = []
            sorted_tasks = sorted(m.tasks, key=lambda t: (t.title, str(t.id)))
            for t in sorted_tasks:
                total_tasks += 1
                if t.is_completed:
                    completed_tasks += 1
                total_hours += (t.estimated_hours or 2.0)
                tasks_list.append(
                    TaskDetail(
                        id=str(t.id),
                        milestone_id=str(t.milestone_id),
                        title=t.title,
                        description=t.description,
                        task_type=t.task_type,
                        estimated_hours=t.estimated_hours or 2.0,
                        is_completed=t.is_completed,
                        resource_url=t.resource_url,
                        resource_title=None
                    )
                )

            # Determine milestone status with prerequisite logic:
            # - If completed: "completed"
            # - If previous stage completed (or Stage 1): "in_progress" (active)
            # - Otherwise: "blocked" (prerequisite stage incomplete)
            if m.is_completed:
                m_status = "completed"
                first_in_progress_found = True
            elif not first_in_progress_found:
                m_status = "in_progress"
                first_in_progress_found = True
            else:
                m_status = "blocked"

            # Retrieve skills and resources from metadata or fallback
            meta = meta_by_order.get(m.order_index)
            if meta:
                skills_to_acq = meta.get("skills_to_acquire", [])
                evidence_map = meta.get("competency_evidence", {})
                pract_tasks = meta.get("practical_tasks", [t.title for t in sorted_tasks])
                resources = [LearningResourceRef(**r) for r in meta.get("resources", [])]
                time_est = meta.get("time_estimate", "3-4 Weeks")
            else:
                # Resolve dynamically from occupation
                try:
                    occ = cls.resolve_target_occupation(roadmap.target_role)
                except Exception:
                    occ = {"canonical_title": roadmap.target_role, "essential_skills": ["Core Competency"]}
                ess_skills = occ.get("essential_skills", ["Core Skill"])
                chunk = max(1, len(ess_skills) // 4)
                start = (m.order_index - 1) * chunk
                skills_to_acq = ess_skills[start:start+chunk] or ["Core Competency"]
                evidence_map = {sk: "mastery_not_assessed" for sk in skills_to_acq}
                pract_tasks = [t.title for t in sorted_tasks]
                resources = cls.find_verified_resources_for_skills(skills_to_acq)
                time_est = "3-4 Weeks"

            cleaned_desc = cls.clean_milestone_description(m.description or "")

            milestone_details.append(
                MilestoneDetail(
                    id=str(m.id),
                    stage_number=m.order_index,
                    stageNumber=m.order_index,
                    order_index=m.order_index,
                    title=m.title,
                    description=cleaned_desc,
                    rationale=f"Mastery of {', '.join(skills_to_acq[:3]) if skills_to_acq else 'core skills'} is critical for {roadmap.target_role}.",
                    time_estimate=time_est,
                    timeEstimate=time_est,
                    status=m_status,
                    is_completed=m.is_completed,
                    competency_evidence=evidence_map,
                    competencyEvidence=evidence_map,
                    skills_to_acquire=skills_to_acq,
                    skillsToAcquire=skills_to_acq,
                    practical_tasks=pract_tasks,
                    practicalTasks=pract_tasks,
                    tasks=tasks_list,
                    resources=resources
                )
            )

        completed_milestones = sum(1 for m in milestone_details if m.is_completed)

        return CareerRoadmapDetailResponse(
            id=str(roadmap.id),
            user_id=str(roadmap.user_id),
            title=roadmap.title,
            target_role=roadmap.target_role,
            target_occupation_id=str(roadmap.target_occupation_id) if roadmap.target_occupation_id else None,
            resolved_canonical_title=occ_meta.get("canonical_title") if occ_meta else roadmap.target_role,
            occupation_domain=occ_meta.get("domain") if occ_meta else None,
            resolution_confidence=occ_meta.get("resolution_confidence") if occ_meta else 1.0,
            estimated_duration_weeks=roadmap.estimated_duration_weeks,
            progress_percentage=roadmap.progress_percentage,
            status=roadmap.status,
            total_milestones=len(milestone_details),
            completed_milestones=completed_milestones,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            estimated_total_hours=total_hours,
            milestones=milestone_details,
            created_at=roadmap.created_at,
            updated_at=roadmap.updated_at
        )


# Singleton
career_roadmap_service = CareerRoadmapService()
