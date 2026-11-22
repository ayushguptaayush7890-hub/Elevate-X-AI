# Page 9: Repository Information

**Project:** Elevate X AI — AI-Powered Vocational Career & Skills Ecosystem  
**Repository URL:** [https://github.com/ayushguptaayush7890-hub/Elevate-X-AI](https://github.com/ayushguptaayush7890-hub/Elevate-X-AI)  
**Primary Branch:** `main`  
**License / Visibility:** Public Academic & Evaluation Access  
**Repository Commit Reference:** `093da86`  

---

## 1. Official Repository Overview

The official Elevate X AI project repository hosts the complete source code, machine learning evaluation pipelines, occupational taxonomies, and technical verification suites powering the platform. The codebase is organized as a unified full-stack monorepo featuring a FastAPI Python backend service and a Next.js 16 TypeScript web client.

- **Primary Repository:** [https://github.com/ayushguptaayush7890-hub/Elevate-X-AI](https://github.com/ayushguptaayush7890-hub/Elevate-X-AI)
- **Primary Tech Stack:** Python 3.11 (79.5%), TypeScript (19.8%), SQL & Shell (0.7%)
- **Target Deployment:** Local Full-Stack Development & Staging Runtime (`localhost:8000` / `localhost:3002`)

---

## 2. GitHub Repository Homepage & File Structure

Below is the verified screenshot of the active GitHub repository homepage, displaying the root directory structure, branch state, and latest commit history:

![Elevate X AI GitHub Repository Homepage](file:///Users/ayushgupta/.gemini/antigravity/brain/254c5adc-170f-4e89-9dc1-d44fbc4d0a94/github_repo_screenshot.png)

<div style="border: 2px dashed #94a3b8; border-radius: 8px; padding: 16px; margin: 16px 0; background-color: #f8fafc; text-align: center;">
  <p style="margin: 0; font-size: 13px; color: #64748b; font-weight: 500;">
    <strong>Figure 9.1:</strong> Official GitHub Repository Interface (<a href="https://github.com/ayushguptaayush7890-hub/Elevate-X-AI">github.com/ayushguptaayush7890-hub/Elevate-X-AI</a>). <em>[Verified live screenshot captured on branch <code>main</code> at commit <code>093da86</code>]</em>
  </p>
</div>

---

## 3. Verified Repository Directory Structure & Component Inventory

All files and directories listed below have been verified directly against the linked remote GitHub repository (`HEAD: 093da8619fd9142bfc0d6a6385e518393d239741`):

### Core Architecture & Application Directories

- **`backend/`**  
  Houses the complete Python / FastAPI server application:
  - `app/api/v1/`: Versioned REST API routers for authentication, adaptive technical assessments, IRT scoring, skill gap analysis, career transition graph queries, and user profiles.
  - `app/core/`: Application settings, security configurations, database session lifecycle, JWT authorization, and rate limiting.
  - `app/models/` & `app/schemas/`: SQLAlchemy database models and Pydantic validation schemas.
  - `app/services/`: Core algorithmic services, including the Item Response Theory (IRT) engine, AST code execution sandboxes, and vector calibration models.
  - `tests/`: Automated pytest verification suites for API endpoints, sandbox security barriers, and IRT psychometric bounds.

- **`src/`**  
  Contains the Next.js 16 (React 19) App Router frontend:
  - `src/app/`: User-facing interactive routes (`/technical-assessments`, `/skill-gap`, `/career-roadmap`, `/career-transition`, `/resume-builder`, `/profile`, `/auth`).
  - `src/components/`: Modular UI component library built with Tailwind CSS and Radix UI primitives.
  - `src/lib/`: API clients, token persistence managers, and client-side utility functions.

- **`datasets/`**  
  Curated vocational benchmarks and taxonomy alignment resources:
  - International standard datasets: ESCO (European Skills, Competences, Qualifications and Occupations) and O*NET.
  - Indian vocational frameworks: National Classification of Occupations (NCO-2015) and NSQF competency matrices.
  - Assessment banks: Multi-level adaptive question sets across 9 technical vocational disciplines, scenario coding prompts, and isolated SQL testing tables.

- **`scripts/`**  
  Automation and preprocessing utilities:
  - Scripts for data ingestion, occupational taxonomy normalization, vector index generation, and end-to-end integration benchmarking.

- **`public/`**  
  Static assets, platform icons, brand imagery, and styling resources served by Next.js.

---

### Root Configuration & Technical Documentation

- **`README.md` & `README_FEATURE2.md`**  
  Comprehensive project documentation covering system architecture, installation guidelines, environment configuration, database migration steps, and Feature 2 technical assessment operations.
- **`package.json` & `package-lock.json`**  
  Node.js dependency manifest defining Next.js 16, TypeScript, Tailwind CSS, Lucide icons, and React 19 dependencies.
- **`tsconfig.json`, `next.config.ts`, `postcss.config.mjs`, `eslint.config.mjs`**  
  Strict TypeScript compiler configuration, Next.js build configuration, PostCSS Tailwind pipeline, and ESLint rule sets.
- **`.env.example`**  
  Template file declaring required environment variables for database connections, JWT secrets, and API service ports.
- **`.gitignore` & `.ignore`**  
  Clean tracking rules preventing transient cache files, local virtual environments, and build artifacts from contaminating source control.
- **`AGENTS.md`**  
  Guidelines for autonomous agent workflows, codebase rules, and framework boundaries.
- **Root Audit Reports (`FEATURE2_*.md`)**  
  Formal technical verification reports documenting authentication flows, role assessment matrices, sandbox security evaluations, and regression test suites.

---

## 4. Source Code and Resource Availability Summary

| Dimension | Specification | Verification Status |
| :--- | :--- | :---: |
| **Repository URL** | [https://github.com/ayushguptaayush7890-hub/Elevate-X-AI](https://github.com/ayushguptaayush7890-hub/Elevate-X-AI) | Verified Active (HTTP 200) |
| **Active Branch** | `main` | Verified |
| **Commit Integrity** | Synchronized with local workspace (`093da86`) | Verified 1:1 Match |
| **Backend Service** | Python 3.11 / FastAPI / SQLAlchemy / Pytest | Verified Present |
| **Frontend Service** | Next.js 16 / TypeScript / Tailwind CSS | Verified Present |
| **Taxonomies & Data** | ESCO, O*NET, NCO-2015, Technical Question Banks | Verified Present |
| **Unverified Folders** | `prompts/`, `code/`, `test-data/`, `CHANGELOG.md` | Removed (Confirmed Non-Existent) |
