import io
import json
import requests
from docx import Document

BASE_URL = "http://localhost:8000/api/v1/resumes"

def create_sample_docx():
    doc = Document()
    doc.add_heading("AYUSH GUPTA", 0)
    doc.add_paragraph("Senior AI & Software Engineer | ayush.gupta@example.com | +91 98765 43210 | New Delhi, India")
    doc.add_paragraph("linkedin.com/in/ayushgupta | github.com/ayushgupta")
    
    doc.add_heading("PROFESSIONAL SUMMARY", level=1)
    doc.add_paragraph("Senior AI & Software Engineer with 4+ years of production experience in machine learning pipelines, LLM fine-tuning, and scalable backend microservices.")
    
    doc.add_heading("TECHNICAL SKILLS", level=1)
    doc.add_paragraph("Programming Languages: Python, TypeScript, Go, C++, SQL")
    doc.add_paragraph("Frameworks & Libraries: PyTorch, FastAPI, Next.js, React, Docker")
    doc.add_paragraph("Databases: PostgreSQL, Redis, Pinecone, MongoDB")
    doc.add_paragraph("Tools & DevOps: Git, AWS, Kubernetes, GitHub Actions, CI/CD")
    doc.add_paragraph("AI & ML Skills: Hugging Face Transformers, MLX, RAG, LoRA, Vector Search")
    
    doc.add_heading("WORK EXPERIENCE", level=1)
    doc.add_paragraph("Senior AI Engineer | NeuralTech Solutions | July 2022 – Present | New Delhi, India")
    doc.add_paragraph("• Architected low-latency LLM inference pipelines achieving 40% reduction in time-to-first-token.")
    doc.add_paragraph("• Deployed multi-tenant RAG system on Kubernetes handling 50k requests daily with 99.9% uptime.")
    doc.add_paragraph("• Mentored junior engineers and led migration to microservices architecture.")
    
    doc.add_heading("INTERNSHIPS", level=1)
    doc.add_paragraph("Machine Learning Research Intern | CloudScale Systems | January 2022 – June 2022")
    doc.add_paragraph("• Benchmarked transformer attention variants and quantized models for edge deployment.")
    
    doc.add_heading("EDUCATION", level=1)
    doc.add_paragraph("Delhi Technological University (DTU) | Bachelor of Technology in Computer Science | 2018 – 2022 | GPA: 8.9/10")
    
    doc.add_heading("PROJECTS", level=1)
    doc.add_paragraph("Elevate X AI Platform")
    doc.add_paragraph("• Built autonomous multi-agent skill assessment and career copilot using Next.js and FastAPI.")
    doc.add_paragraph("• Implemented high-throughput resume parser and semantic ATS intelligence engine.")
    
    doc.add_heading("CERTIFICATIONS", level=1)
    doc.add_paragraph("AWS Certified Solutions Architect – Associate | Amazon Web Services | 2023")
    
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf.getvalue()

def run_tests():
    print("================================================================================")
    print("FEATURE 3: COMPLETE PIPELINE END-TO-END VALIDATION")
    print("================================================================================")
    
    # 1. DOCX Upload & Parse
    print("\n[Step 1] Upload & Parse Authentic Candidate DOCX Document...")
    docx_bytes = create_sample_docx()
    files = {"file": ("ayush_gupta_resume.docx", io.BytesIO(docx_bytes), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    res = requests.post(f"{BASE_URL}/upload-parse", files=files)
    assert res.status_code == 200, f"Upload parse failed: {res.status_code} {res.text}"
    parsed_data = res.json()
    
    pinfo = parsed_data.get("personalInfo", {})
    structured = parsed_data.get("structuredResume", {})
    skills = structured.get("skills", {})
    experience = structured.get("experience", [])
    internships = structured.get("internships", [])
    education = structured.get("education", [])
    projects = structured.get("projects", [])
    certifications = structured.get("certifications", [])
    
    print(f"  ✓ Full Name: {pinfo.get('fullName')}")
    print(f"  ✓ Professional Title: {pinfo.get('professionalTitle')}")
    print(f"  ✓ Email: {pinfo.get('email')}")
    print(f"  ✓ Phone: {pinfo.get('phone')}")
    print(f"  ✓ Location: {pinfo.get('location')}")
    print(f"  ✓ Education Count: {len(education)} -> {education[0].get('institution') if education else 'N/A'}")
    print(f"  ✓ Programming Languages ({len(skills.get('programmingLanguages', []))}): {skills.get('programmingLanguages', [])}")
    print(f"  ✓ AI/ML Skills ({len(skills.get('aiMlSkills', []))}): {skills.get('aiMlSkills', [])}")
    print(f"  ✓ Experience Roles ({len(experience)}): {[e.get('role') + ' @ ' + e.get('company') for e in experience]}")
    print(f"  ✓ Internships ({len(internships)}): {[i.get('role') + ' @ ' + i.get('organization') for i in internships]}")
    print(f"  ✓ Projects ({len(projects)}): {[p.get('title') for p in projects]}")
    print(f"  ✓ Certifications ({len(certifications)}): {[c.get('name') for c in certifications]}")
    
    assert "AYUSH GUPTA" in pinfo.get("fullName", "").upper(), "Name mismatch"
    assert "ARJUN MEHTA" not in pinfo.get("fullName", "").upper(), "Isolated candidate leaked preset name!"
    assert len(skills.get("programmingLanguages", [])) >= 4, "Languages missing"
    assert len(experience) >= 1, "Experience missing"
    assert len(internships) >= 1, "Internships missing"
    assert len(education) >= 1, "Education missing"
    assert len(projects) >= 1, "Projects missing"
    assert len(certifications) >= 1, "Certifications missing"
    
    # 2. Analyze Job Description
    print("\n[Step 2] Analyze Markdown AI/ML Engineer Job Description...")
    jd_text = """
# Senior AI / Machine Learning Engineer

## Company Overview
Elevate X AI is pioneering next-generation agentic workflows and developer intelligence platforms.

## Key Responsibilities
• Train, fine-tune, and deploy instruction-following language models and multi-agent reasoning graphs.
• Architect low-latency microservices with FastAPI and Docker for real-time model serving.
• Collaborate with product and design teams to build generative interfaces with Next.js.
• Establish rigorous offline and online evaluation benchmarks for semantic search and recommendation.

## Required Skills & Qualifications
• Strong programming proficiency in Python, PyTorch, and Hugging Face Transformers.
• Production experience with Vector Databases (Pinecone, Redis, or Milvus) and RAG architecture.
• Experience building RESTful APIs using FastAPI and modern asynchronous programming.
• Bachelor's or Master's degree in Computer Science, Data Science, or related technical field.
• Hands-on familiarity with Git, Docker, and CI/CD pipelines.

## Preferred Qualifications
• Experience with Apple MLX, ONNX Runtime, or quantization (4-bit/8-bit LoRA).
• Knowledge of TypeScript, React, or modern frontend frameworks.
• Published research in NLP or open-source AI project contributions.
    """
    res_jd = requests.post(f"{BASE_URL}/analyze-jd", json={"jobDescriptionText": jd_text})
    assert res_jd.status_code == 200, f"Analyze JD failed: {res_jd.status_code} {res_jd.text}"
    jd_analysis = res_jd.json()
    
    print(f"  ✓ Inferred Job Title: {jd_analysis.get('jobTitle')}")
    print(f"  ✓ Required Skills ({len(jd_analysis.get('requiredSkills', []))}): {jd_analysis.get('requiredSkills', [])[:4]}...")
    print(f"  ✓ Preferred Skills ({len(jd_analysis.get('preferredSkills', []))}): {jd_analysis.get('preferredSkills', [])[:4]}...")
    print(f"  ✓ Key Responsibilities ({len(jd_analysis.get('keyResponsibilities', []))}): {len(jd_analysis.get('keyResponsibilities', []))} extracted")
    print(f"  ✓ Qualifications ({len(jd_analysis.get('qualifications', []))}): {jd_analysis.get('qualifications', [])}")
    
    assert len(jd_analysis.get("requiredSkills", [])) > 0, "Required skills should NOT be 0!"
    assert len(jd_analysis.get("preferredSkills", [])) > 0, "Preferred skills should NOT be 0!"
    assert len(jd_analysis.get("keyResponsibilities", [])) > 0, "Responsibilities should NOT be 0!"
    assert "Senior AI / Machine Learning Engineer" not in jd_analysis.get("requiredSkills", []), "Job title leaked into skills!"
    
    # 3. ATS Matcher Pipeline
    print("\n[Step 3] Execute ATS Matching & 5-State Evidence Evaluation...")
    match_payload = {
        "resumeData": structured,
        "jobDescription": jd_text,
        "jobTitle": jd_analysis.get("jobTitle")
    }
    res_match = requests.post(f"{BASE_URL}/match-ats", json=match_payload)
    assert res_match.status_code == 200, f"Match ATS failed: {res_match.status_code} {res_match.text}"
    match_result = res_match.json()
    
    overall_score = match_result.get("overallScore")
    breakdown = match_result.get("breakdown", {})
    part_a = breakdown.get("partADetails", {})
    part_b = breakdown.get("partBDetails", {})
    explicit_matches = match_result.get("explicitMatches", [])
    partial_matches = match_result.get("partialMatches", [])
    not_found = match_result.get("notFoundRequirements", [])
    uncertain = match_result.get("uncertainExtractions", [])
    strengths = match_result.get("strengthsSummary", [])
    gaps = match_result.get("criticalGapsSummary", [])
    
    print(f"  ✓ 100-Point Overall ATS Match Score: {overall_score}/100")
    print(f"  ✓ Part A Score (Job Fit): {breakdown.get('partAScore')}/60")
    print(f"    - Required Skills: {part_a.get('requiredSkillsScore')}/25")
    print(f"    - Preferred Skills: {part_a.get('preferredSkillsScore')}/10")
    print(f"    - Responsibilities: {part_a.get('responsibilitiesScore')}/15")
    print(f"    - Qualifications: {part_a.get('qualificationsScore')}/10")
    print(f"  ✓ Part B Score (Resume Quality): {breakdown.get('partBScore')}/40")
    print(f"    - Action Verbs & Impact: {part_b.get('actionVerbsAndImpactScore')}/15")
    print(f"    - Formatting & Parseability: {part_b.get('formattingAndParseabilityScore')}/10")
    print(f"    - Section Completeness: {part_b.get('sectionCompletenessScore')}/15")
    print(f"  ✓ Explicit Matches ({len(explicit_matches)}): {[m.get('requirement') for m in explicit_matches[:3]]}")
    print(f"  ✓ Partial Matches ({len(partial_matches)}): {[m.get('requirement') for m in partial_matches[:3]]}")
    print(f"  ✓ Not Found in Text ({len(not_found)}): {[m.get('requirement') for m in not_found[:3]]}")
    print(f"  ✓ Uncertain Extractions ({len(uncertain)}): {[m.get('requirement') for m in uncertain[:3]]}")
    print(f"  ✓ Strengths Summary ({len(strengths)}): {strengths[:2]}")
    print(f"  ✓ Critical Gaps Summary ({len(gaps)}): {gaps[:2]}")
    
    assert overall_score > 50, f"Expected strong match score, got {overall_score}"
    assert len(explicit_matches) > 0, "No explicit matches found"
    
    # 4. DOCX Export
    print("\n[Step 4] Export Resume to DOCX & Validate OpenXML Binary Document...")
    export_payload = structured
    res_export = requests.post(f"{BASE_URL}/export-docx", json=export_payload)
    assert res_export.status_code == 200, f"DOCX export failed: {res_export.status_code} {res_export.text}"
    docx_stream = res_export.content
    print(f"  ✓ DOCX Export HTTP 200 Received ({len(docx_stream):,} bytes)")
    
    exported_doc = Document(io.BytesIO(docx_stream))
    exported_text = "\n".join(p.text for p in exported_doc.paragraphs if p.text)
    print(f"  ✓ Exported Document Paragraphs: {len(exported_doc.paragraphs)}")
    print(f"  ✓ Candidate Name in Document: {'AYUSH GUPTA' in exported_text.upper()}")
    print(f"  ✓ Technical Skills in Document: {'PyTorch' in exported_text and 'FastAPI' in exported_text}")
    print(f"  ✓ Experience in Document: {'NeuralTech Solutions' in exported_text}")
    print(f"  ✓ Education in Document: {'Delhi Technological University' in exported_text}")
    
    assert "AYUSH GUPTA" in exported_text.upper(), "Candidate name missing from exported DOCX"
    assert "NeuralTech Solutions" in exported_text, "Work experience missing from exported DOCX"
    assert "Delhi Technological University" in exported_text, "Education missing from exported DOCX"
    
    print("\n================================================================================")
    print("ALL FEATURE 3 VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("================================================================================")

if __name__ == "__main__":
    run_tests()
