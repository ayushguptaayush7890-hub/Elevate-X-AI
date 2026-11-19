"""
Career Roadmap & Learning Recommendation Service.
Generates structured, step-by-step technical learning milestones based on assessed skill gaps.
"""

from typing import Dict, List, Any
import uuid

# Curated reference resources by skill domain to prevent URL hallucinations
RESOURCE_REGISTRY = {
    "Data Structures & Algorithms": {
        "title": "NeetCode 150 & MIT OpenCourseWare 6.006",
        "type": "Interactive Course & Problem Bank",
        "url": "https://neetcode.io/practice"
    },
    "Object-Oriented & Functional Design Patterns": {
        "title": "Refactoring Guru: Design Patterns Catalogue",
        "type": "Technical Architecture Guide",
        "url": "https://refactoring.guru/design-patterns"
    },
    "Concurrency, Multithreading & Memory Management": {
        "title": "Java Concurrency in Practice & Rust Nomicon",
        "type": "Systems Book & Reference",
        "url": "https://doc.rust-lang.org/nomicon/"
    },
    "Database Systems & Transaction Isolation": {
        "title": "Use The Index, Luke! & Designing Data-Intensive Applications",
        "type": "Database Engineering Manual",
        "url": "https://use-the-index-luke.com/"
    },
    "API Architecture & Distributed RPC": {
        "title": "Google Cloud API Design Guide & gRPC Documentation",
        "type": "Standard Architecture Guidelines",
        "url": "https://cloud.google.com/apis/design"
    },
    "Machine Learning Foundations & Regularization": {
        "title": "Stanford CS229: Machine Learning Course Materials",
        "type": "University Course",
        "url": "https://cs229.stanford.edu/"
    },
    "Deep Learning Architectures (CNN, RNN, Transformers)": {
        "title": "The Illustrated Transformer & DeepLearning.AI Specialization",
        "type": "Interactive Tutorial",
        "url": "https://jalammar.github.io/illustrated-transformer/"
    },
    "NLP & LLM Engineering": {
        "title": "Hugging Face NLP Course & Transformer Documentation",
        "type": "Hands-on Practical Course",
        "url": "https://huggingface.co/learn/nlp-course"
    },
    "Computer Vision & Feature Extraction": {
        "title": "PyImageSearch OpenCV & Stanford CS231n",
        "type": "Computer Vision Curriculum",
        "url": "https://cs231n.github.io/"
    },
    "MLOps, Model Serving & Drift Monitoring": {
        "title": "Full Stack Deep Learning MLOps Curriculum",
        "type": "Engineering Course",
        "url": "https://fullstackdeeplearning.com/"
    },
    "Core JavaScript/TypeScript & Browser Runtime": {
        "title": "JavaScript.info & TypeScript Official Handbook",
        "type": "Language Specification Guide",
        "url": "https://javascript.info/"
    },
    "Modern UI Frameworks (React, Reconciliation, State)": {
        "title": "React.dev Documentation: Managing State & Escape Hatches",
        "type": "Official Documentation",
        "url": "https://react.dev/learn"
    },
    "Web Performance, Caching & Rendering Optimization": {
        "title": "Google Web.dev: Fast Load Times & Core Web Vitals",
        "type": "Performance Engineering Guide",
        "url": "https://web.dev/fast/"
    },
    "Linux System Administration & Shell Scripting": {
        "title": "Linux Journey & The Linux Command Line",
        "type": "Systems Tutorial",
        "url": "https://linuxjourney.com/"
    },
    "Containerization & Image Optimization (Docker)": {
        "title": "Docker Official Deep Dive & Best Practices",
        "type": "Container Reference",
        "url": "https://docs.docker.com/develop/develop-images/dockerfile_best-practices/"
    },
    "Container Orchestration (Kubernetes)": {
        "title": "Kubernetes.io Official Tutorials & The Children's Illustrated Guide",
        "type": "Platform Architecture Docs",
        "url": "https://kubernetes.io/docs/tutorials/"
    },
    "Web Application Security & OWASP Top 10": {
        "title": "OWASP Top 10 Security Project & PortSwigger Web Security Academy",
        "type": "Hands-on Security Labs",
        "url": "https://portswigger.net/web-security"
    },
    "Cloud Infrastructure & Virtual Networks (VPC, Subnets)": {
        "title": "AWS Well-Architected Framework: Reliability & Security Pillars",
        "type": "Cloud Architecture Guide",
        "url": "https://aws.amazon.com/architecture/well-architected/"
    }
}

DEFAULT_RESOURCE = {
    "title": "Elevate X AI Technical Competency Workshop",
    "type": "Curated Engineering Module",
    "url": "https://github.com"
}

class RoadmapService:
    @classmethod
    def generate_roadmap(
        cls,
        target_role_id: str,
        target_role_title: str,
        skill_gaps: List[Dict[str, Any]],
        overall_score: float
    ) -> Dict[str, Any]:
        milestones = []
        
        # Sort gaps by priority
        for idx, gap in enumerate(skill_gaps, 1):
            sname = gap["skill_name"]
            res = RESOURCE_REGISTRY.get(sname, DEFAULT_RESOURCE)
            delta = gap["gap_delta"]
            
            # Formulate actionable milestone
            milestones.append({
                "milestone_id": f"M-{idx:02d}",
                "order_index": idx,
                "skill_id": gap["skill_id"],
                "skill_name": sname,
                "priority": gap["priority"],
                "current_mastery": gap["current_level"],
                "target_mastery": gap["target_level"],
                "gap_delta": delta,
                "estimated_hours": 10 if delta < 25 else (20 if delta < 50 else 35),
                "reason": f"Assessed at {gap['current_level']}%, requiring a +{delta}% capability increase to meet {target_role_title} production expectations.",
                "learning_objective": f"Master core technical concepts, avoid common antipatterns, and implement production solutions in {sname}.",
                "hands_on_task": f"Build a tested implementation of {sname} resolving common edge cases and benchmark performance under load.",
                "resource_title": res["title"],
                "resource_type": res["type"],
                "resource_url": res["url"],
                "status": "pending"
            })
            
        total_hours = sum(m["estimated_hours"] for m in milestones)
        
        return {
            "roadmap_id": str(uuid.uuid4()),
            "target_role_id": target_role_id,
            "target_role_title": target_role_title,
            "overall_assessed_score": overall_score,
            "total_milestones": len(milestones),
            "estimated_completion_hours": total_hours,
            "milestones": milestones
        }

# Singleton
roadmap_service = RoadmapService()

