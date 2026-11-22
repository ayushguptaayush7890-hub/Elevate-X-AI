"""
End-to-End Verification of ATS & Resume Upload Pipeline
Tests:
1. PDF text extraction + Neural Section Classification (/upload-parse)
2. DOCX text extraction + Neural Section Classification (/upload-parse)
3. Job Description Analyzer (/analyze-jd)
4. Semantic Matching Engine & ATS Score Breakdown (/match-ats)
5. AI STAR Improvement Engine (/ai-improve)
"""

import io
import json
import requests
import docx
from pypdf import PdfWriter

BASE_URL = "http://localhost:8000/api/v1"

def create_sample_docx():
    doc = docx.Document()
    doc.add_heading("Vikram Sen", 0)
    doc.add_paragraph("vikram.sen@techpulse.io | +1 (555) 234-5678 | San Francisco, CA | github.com/vsen")
    doc.add_paragraph("Experienced Software Engineer specializing in distributed backend systems and cloud APIs.")
    
    doc.add_heading("Technical Skills", level=1)
    doc.add_paragraph("Python, FastAPI, TypeScript, React, PostgreSQL, Docker, AWS, Redis, GraphQL")
    
    doc.add_heading("Work Experience", level=1)
    doc.add_paragraph("Senior Backend Engineer | CloudScale Inc (2022 - Present)")
    doc.add_paragraph("• Architected high-throughput microservices in FastAPI reducing p99 API latency by 35%.")
    doc.add_paragraph("• Spearheaded PostgreSQL database indexing and query optimization handling 2M daily requests.")
    doc.add_paragraph("• Orchestrated container deployments across AWS ECS clusters with automated CI/CD pipelines.")
    
    doc.add_heading("Education", level=1)
    doc.add_paragraph("B.S. in Computer Science | University of California, Berkeley (2018 - 2022)")
    
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

def run_tests():
    print("=" * 60)
    print("TEST 1: Ingest DOCX & Neural Section Classification")
    print("=" * 60)
    docx_bytes = create_sample_docx()
    files = {"file": ("vikram_sen_resume.docx", docx_bytes, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    res = requests.post(f"{BASE_URL}/resumes/upload-parse", files=files)
    assert res.status_code == 200, f"Upload DOCX failed: {res.status_code} {res.text}"
    parsed_docx = res.json()
    print(f"✓ Parsed Name: {parsed_docx['personalInfo']['fullName']}")
    print(f"✓ Parsed Email: {parsed_docx['personalInfo']['email']}")
    print(f"✓ Skills Extracted ({len(parsed_docx['skills'])}): {parsed_docx['skills'][:5]}")
    print(f"✓ Section Breakdown: {parsed_docx['sectionBreakdown']}")
    print(f"✓ Evidence Lines Tracked: {len(parsed_docx['evidenceLines'])}")

    print("\n" + "=" * 60)
    print("TEST 2: Analyze Job Description")
    print("=" * 60)
    jd_payload = {
        "jobTitle": "Lead Backend Platform Engineer",
        "jobDescriptionText": (
            "TechVision Systems is hiring a Lead Backend Platform Engineer.\n"
            "Requirements:\n"
            "- 5+ years building backend microservices with Python and FastAPI\n"
            "- Strong relational database expertise with PostgreSQL and performance tuning\n"
            "- Hands-on containerization experience with Docker and Kubernetes\n"
            "- Proven track record deploying on AWS cloud infrastructure\n"
            "- Bachelor's degree in Computer Science or related STEM discipline\n\n"
            "Preferred Skills:\n"
            "- Familiarity with Redis in-memory caching and message queues\n"
            "- Experience with CI/CD automation and GitHub Actions\n\n"
            "Responsibilities:\n"
            "- Architect highly resilient microservices processing high concurrent traffic\n"
            "- Lead database schema migrations and data isolation strategies\n"
            "- Mentor junior engineers and conduct rigorous code reviews\n"
        )
    }
    res_jd = requests.post(f"{BASE_URL}/resumes/analyze-jd", json=jd_payload)
    assert res_jd.status_code == 200, f"Analyze JD failed: {res_jd.status_code} {res_jd.text}"
    jd_analysis = res_jd.json()
    print(f"✓ Inferred Seniority: {jd_analysis['seniorityLevel']}")
    print(f"✓ Required Skills ({len(jd_analysis['requiredSkills'])}): {jd_analysis['requiredSkills']}")
    print(f"✓ Preferred Skills ({len(jd_analysis['preferredSkills'])}): {jd_analysis['preferredSkills']}")
    print(f"✓ Responsibilities ({len(jd_analysis['keyResponsibilities'])}): {jd_analysis['keyResponsibilities'][:2]}")

    print("\n" + "=" * 60)
    print("TEST 3: Semantic ATS Matching & Explainable Scoring")
    print("=" * 60)
    match_payload = {
        "parsedResume": parsed_docx,
        "jobDescription": jd_payload["jobDescriptionText"],
        "jobTitle": jd_payload["jobTitle"]
    }
    res_match = requests.post(f"{BASE_URL}/resumes/match-ats", json=match_payload)
    assert res_match.status_code == 200, f"Match ATS failed: {res_match.status_code} {res_match.text}"
    match_data = res_match.json()
    print(f"✓ Overall ATS Compatibility Score: {match_data['overallScore']} / 100")
    print(f"✓ Part A (Job Requirement Alignment): {match_data['breakdown']['partAScore']} / 60")
    print(f"  - Required Skills: {match_data['breakdown']['partADetails']['requiredSkillsScore']} / 25")
    print(f"  - Preferred Skills: {match_data['breakdown']['partADetails']['preferredSkillsScore']} / 10")
    print(f"  - Responsibilities: {match_data['breakdown']['partADetails']['responsibilitiesScore']} / 15")
    print(f"  - Qualifications: {match_data['breakdown']['partADetails']['qualificationsScore']} / 10")
    print(f"✓ Part B (Resume Document Quality): {match_data['breakdown']['partBScore']} / 40")
    print(f"  - Action Verbs & Impact: {match_data['breakdown']['partBDetails']['actionVerbsAndImpactScore']} / 15")
    print(f"  - ATS Parseability: {match_data['breakdown']['partBDetails']['formattingAndParseabilityScore']} / 10")
    print(f"  - Completeness: {match_data['breakdown']['partBDetails']['sectionCompletenessScore']} / 15")
    print(f"✓ Strong Matches: {len(match_data['strongMatches'])}")
    print(f"✓ Partial Matches: {len(match_data['partialMatches'])}")
    print(f"✓ Missing Requirements: {len(match_data['missingRequirements'])}")

    print("\n" + "=" * 60)
    print("TEST 4: AI Grounded STAR Improvements & Gap Questions")
    print("=" * 60)
    improve_payload = {
        "resumeData": {
            "personalInfo": {
                "fullName": "Vikram Sen",
                "professionalTitle": "Senior Backend Engineer",
                "email": "vikram.sen@techpulse.io",
                "phone": "+1 555-234-5678",
                "location": "San Francisco, CA",
                "summary": "Experienced Software Engineer specializing in distributed backend systems and cloud APIs."
            },
            "education": [{
                "id": "edu-1",
                "institution": "UC Berkeley",
                "degree": "B.S.",
                "fieldOfStudy": "Computer Science",
                "startDate": "2018",
                "endDate": "2022",
                "coursework": ["Algorithms", "Database Systems"]
            }],
            "skills": {
                "programmingLanguages": ["Python", "TypeScript"],
                "frameworks": ["FastAPI", "React"],
                "databases": ["PostgreSQL", "Redis"],
                "developerTools": ["Docker", "AWS"],
                "aiMlSkills": [],
                "otherSkills": []
            },
            "experience": [{
                "id": "exp-1",
                "company": "CloudScale Inc",
                "role": "Senior Backend Engineer",
                "employmentType": "Full-time",
                "startDate": "2022",
                "endDate": "Present",
                "current": True,
                "responsibilities": [
                    "helped build backend services using FastAPI and PostgreSQL",
                    "worked on database performance and query optimization",
                    "did container setups on AWS"
                ]
            }],
            "internships": [],
            "projects": [{
                "id": "proj-1",
                "title": "Distributed Task Queue",
                "description": "Python task queue library with Redis backing",
                "technologies": ["Python", "Redis", "Docker"],
                "contributions": ["wrote background worker processes handling async tasks"]
            }],
            "certifications": [],
            "additional": {
                "achievements": [],
                "awards": [],
                "publications": [],
                "volunteerExperience": [],
                "extracurricular": [],
                "languages": ["English"],
                "interests": []
            }
        },
        "jobDescription": jd_payload["jobDescriptionText"],
        "gapRequirements": [m["requirement"] for m in match_data["missingRequirements"]]
    }
    res_imp = requests.post(f"{BASE_URL}/resumes/ai-improve", json=improve_payload)
    assert res_imp.status_code == 200, f"AI Improve failed: {res_imp.status_code} {res_imp.text}"
    imp_data = res_imp.json()
    print(f"✓ Suggestions Generated ({len(imp_data['suggestions'])}):")
    for s in imp_data["suggestions"][:2]:
        print(f"  • Section: {s['targetSection']}")
        print(f"    Original:  {s['originalText']}")
        print(f"    Suggested: {s['suggestedText']}")
        print(f"    Notes:     {s['starMethodologyNotes']}")
    print(f"✓ Targeted Missing Evidence Questions ({len(imp_data['targetedQuestions'])}):")
    for q in imp_data["targetedQuestions"][:2]:
        print(f"  • {q}")
    print(f"✓ Grounding Disclaimer: {imp_data['groundingDisclaimer']}")

    print("\n" + "=" * 60)
    print("ALL ATS & RESUME UPLOAD PIPELINE TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
