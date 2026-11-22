# Elevate X AI — Career Transition API Documentation

## Base URL
`http://localhost:8000/api/v1/career-transitions`

All endpoints are protected by standard Bearer JWT authorization (`Authorization: Bearer <token>`).

---

## 1. Search Occupations
- **Endpoint:** `GET /occupations`
- **Query Parameters:**
  - `q` (string, optional): Search keyword (title, clean title, or canonical ID).
  - `limit` (integer, default: 15): Number of results to return (max 50).
  - `taxonomy` (string, optional): Filter by `ESCO`, `ONET`, or `NCO`.
- **Response `200 OK`:**
```json
[
  {
    "canonical_id": "ESCO:7411.1",
    "title": "electrician",
    "source": "ESCO v1.2.1",
    "code": "http://data.europa.eu/esco/occupation/...",
    "description": "Electricians install, maintain, and repair electrical wiring...",
    "isco_group": "7411"
  }
]
```

---

## 2. Get Occupation Details & Requirements
- **Endpoint:** `GET /occupations/{occupation_id}`
- **Path Parameters:**
  - `occupation_id` (string): Canonical ID, URI, or title.
- **Response `200 OK`:**
```json
{
  "occupation": {
    "canonical_id": "ESCO:7411.1",
    "occupation_title": "electrician",
    "source": "ESCO v1.2.1",
    "isco_group": "7411"
  },
  "skills": [
    {
      "skill_id": "http://data.europa.eu/esco/skill/...",
      "name": "install electrical wiring",
      "weight": 1.0,
      "relation_type": "essential"
    }
  ],
  "market": {
    "salary_range": "Authentic Industry Range (Based on 45 active postings)",
    "demand_level": "High",
    "sample_postings_count": 45
  }
}
```

---

## 3. Career Transition Recommendations
- **Endpoint:** `POST /recommendations`
- **Request Body:**
```json
{
  "current_occupation": "Electrician",
  "candidate_skills": ["wiring", "electrical safety", "circuit design"],
  "limit": 6
}
```
- **Response `200 OK`:**
```json
[
  {
    "target_occupation_id": "ESCO:7411.2",
    "target_title": "building electrician",
    "target_source": "ESCO v1.2.1",
    "fit_percentage": 78.5,
    "transition_delta": 21.5,
    "difficulty_category": "Low Friction",
    "estimated_months": 3,
    "salary_range": "Authentic Industry Range (Based on 18 active postings)",
    "demand_level": "High",
    "demand_postings_count": 25,
    "transferable_skills_count": 14,
    "bridgeable_skills_count": 3,
    "missing_skills_count": 2,
    "transferable_competencies_preview": ["electrical safety", "wiring", "power tools"],
    "bridgeable_competencies_preview": ["smart home wiring", "energy efficiency"]
  }
]
```

---

## 4. Deep Transferability Analysis
- **Endpoint:** `POST /analyze`
- **Request Body:**
```json
{
  "from_occupation": "Electrician",
  "to_occupation": "Solar Photovoltaic Installer",
  "candidate_skills": ["wiring", "electrical safety"]
}
```
- **Response `200 OK`:**
```json
{
  "from_occupation_id": "ESCO:7411.1",
  "from_occupation_title": "electrician",
  "to_occupation_id": "ESCO:7411.3",
  "to_occupation_title": "solar photovoltaic installer",
  "to_taxonomy": "ESCO v1.2.1",
  "fit_percentage": 78.5,
  "transition_delta": 21.5,
  "difficulty_category": "Low Friction",
  "estimated_months": 3,
  "salary_range": "$52,000 - $78,000 / year",
  "demand_level": "High",
  "transferable_competencies": [
    {
      "name": "install electrical wiring",
      "skill_id": "...",
      "evidence_state": "practically_demonstrated",
      "evidence_score": 0.9,
      "importance": "essential",
      "notes": "Demonstrated in work experience as Electrician"
    }
  ],
  "bridgeable_competencies": [],
  "missing_competencies": []
}
```

---

## 5. Transition Bridge Blueprint
- **Endpoint:** `POST /blueprint`
- **Request Body:**
```json
{
  "from_occupation": "Electrician",
  "to_occupation": "Solar Photovoltaic Installer"
}
```
- **Response `200 OK`:**
```json
{
  "transition_id": "550e8400-e29b-41d4-a716-446655440000",
  "from_occupation": "electrician",
  "target_occupation": "solar photovoltaic installer",
  "overall_fit": 78.5,
  "total_estimated_weeks": 16,
  "stages": [
    {
      "stage_number": 1,
      "stage_name": "Foundational Bridge & Diagnostics",
      "timeframe": "Weeks 1-3",
      "objective": "Bridge prior expertise with destination principles.",
      "milestones": ["Baseline Diagnostic Assessment", "Safety Certification"],
      "tasks": ["Complete diagnostic self-assessment", "Review mandatory safety standards"],
      "recommended_resources": [
        {
          "title": "Solar Photovoltaic Energy Systems",
          "provider": "NPTEL",
          "url": "https://nptel.ac.in/courses/108105058",
          "type": "Course"
        }
      ]
    }
  ],
  "generated_by": "Elevate X AI Dynamic Transition Engine",
  "model_used": "PyTorch Graph Embeddings + Grounded Blueprint Generator"
}
```

---

## 6. Adopt as Career Goal
- **Endpoint:** `POST /adopt-goal`
- **Request Body:**
```json
{
  "from_occupation_title": "Electrician",
  "target_occupation_id": "ESCO:solar-pv-installer",
  "target_occupation_title": "Solar Photovoltaic Installer",
  "fit_percentage": 78.5,
  "transition_delta": 21.5,
  "difficulty_category": "Low Friction",
  "blueprint": { ... }
}
```
- **Response `200 OK`:**
```json
{
  "success": true,
  "goal_id": "d7e01070-9747-418a-812f-5e0093dda631",
  "message": "Successfully adopted Solar Photovoltaic Installer as your active career transition goal.",
  "roadmap_id": "4b9fa350-2f98-4c07-bfd3-0511f5ccbc81"
}
```

---

## 7. Get User Transition Progress
- **Endpoint:** `GET /progress`
- **Response `200 OK`:**
```json
[
  {
    "goal_id": "d7e01070-9747-418a-812f-5e0093dda631",
    "from_occupation_title": "Electrician",
    "target_occupation_title": "Solar Photovoltaic Installer",
    "fit_percentage": 78.5,
    "difficulty_category": "Low Friction",
    "status": "active",
    "progress_percentage": 0.0,
    "created_at": "2026-11-22T00:50:32"
  }
]
```
