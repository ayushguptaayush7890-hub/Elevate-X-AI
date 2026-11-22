import { apiClient } from "@/lib/api";
import { 
  UserProfile, 
  RecognizedSkill, 
  SkillExtractionResponse,
  JobListing, 
  SkillGapItem, 
  RoadmapMilestone, 
  CareerRoadmapData, 
  CareerTransitionPath, 
  AssessmentResult, 
  JobApplication, 
  PromptEvaluationItem, 
  ResumeData,
  AssistantMessage,
  AggregatedJobListing,
  JobProviderStatus,
} from "@/types";
import { 
  defaultUserProfile, 
  mockJobListings, 
  mockSkillGaps, 
  mockRoadmapMilestones, 
  mockCareerTransitions, 
  mockAssessmentResults, 
  mockApplications, 
  mockPromptEvaluations, 
  defaultResumeData 
} from "@/data/mock-data";

export const apiService = {
  // Authentication
  async login(email: string, password: string = "Password@123") {
    return apiClient<{ token: { access_token: string; refresh_token: string }; user: any }>(
      "/auth/login",
      {
        method: "POST",
        body: JSON.stringify({ email, password }),
      }
      // No fallback: auth failure must throw so the UI shows the real error
    );
  },

  async register(userData: Partial<UserProfile> & { password?: string; trade_category?: string }) {
    return apiClient<{ token: { access_token: string; refresh_token: string }; user: any }>(
      "/auth/register",
      {
        method: "POST",
        body: JSON.stringify({
          email: userData.email,
          password: userData.password || "Password@123",
          full_name: userData.fullName,
          trade_category: userData.trade_category || userData.currentOccupation,
        }),
      }
      // No fallback: auth failure must throw so the UI shows the real error
    );
  },

  async getCurrentUser() {
    return apiClient<any>(
      "/auth/me",
      { method: "GET" },
      defaultUserProfile
    );
  },

  // Profile
  async getProfile() {
    return apiClient<any>(
      "/profiles/me",
      { method: "GET" },
      defaultUserProfile
    );
  },

  async updateProfile(updates: Partial<UserProfile>) {
    return apiClient<any>(
      "/profiles/me",
      {
        method: "PUT",
        body: JSON.stringify(updates),
      },
      { ...defaultUserProfile, ...updates }
    );
  },

  // Education
  async getEducation() {
    return apiClient<any[]>(
      "/profiles/education",
      { method: "GET" },
      []
    );
  },

  async addEducation(eduData: any) {
    return apiClient<any>(
      "/profiles/education",
      {
        method: "POST",
        body: JSON.stringify(eduData),
      },
      eduData
    );
  },

  // Work Experience
  async getExperiences() {
    return apiClient<any[]>(
      "/profiles/experience",
      { method: "GET" },
      []
    );
  },

  async addExperience(expData: any) {
    return apiClient<any>(
      "/profiles/experience",
      {
        method: "POST",
        body: JSON.stringify(expData),
      },
      expData
    );
  },

  // Skills
  async getMySkills() {
    return apiClient<any[]>(
      "/profiles/me/skills",
      { method: "GET" },
      defaultUserProfile.skills || []
    );
  },

  async addMySkill(skillData: any) {
    return apiClient<any>(
      "/profiles/me/skills",
      {
        method: "POST",
        body: JSON.stringify(skillData),
      },
      skillData
    );
  },

  async getCatalogSkills(search?: string) {
    const q = search ? `?search=${encodeURIComponent(search)}` : "";
    return apiClient<any[]>(
      `/skills${q}`,
      { method: "GET" },
      []
    );
  },

  // Experience Recognition (Feature 1 AI Skill Extraction)
  async analyzeExperience(narrative: string, occupationHint?: string) {
    return apiClient<SkillExtractionResponse>(
      "/skills/extract",
      {
        method: "POST",
        body: JSON.stringify({
          text: narrative,
          occupation_hint: occupationHint || null,
        }),
      }
      // Strictly no fallbackData: Live predictions must reflect the submitted narrative
    );
  },

  async extractSkills(text: string, occupationHint?: string) {
    return this.analyzeExperience(text, occupationHint);
  },

  async saveSkills(skills: RecognizedSkill[]) {
    return apiClient<RecognizedSkill[]>(
      "/experience/skills",
      {
        method: "POST",
        body: JSON.stringify({ skills }),
      },
      skills
    );
  },

  // Jobs
  async getJobs() {
    return apiClient<JobListing[]>(
      "/jobs",
      { method: "GET" },
      mockJobListings
    );
  },

  async getAggregatedJobs(params?: {
    search?: string;
    location?: string;
    country?: string;
    role_category?: string;
    source?: string;
    work_mode?: string;
    employment_type?: string;
    max_experience?: number;
    min_salary?: number;
    min_compatibility?: number;
    freshness_days?: number;
    saved_only?: boolean;
    limit?: number;
    offset?: number;
  }) {
    const query = new URLSearchParams();
    if (params) {
      if (params.search) query.set("search", params.search);
      if (params.location && params.location !== "All") query.set("location", params.location);
      if (params.country) query.set("country", params.country);
      if (params.role_category && params.role_category !== "All" && params.role_category !== "All Roles") {
        query.set("role_category", params.role_category);
      }
      if (params.source && params.source !== "All") query.set("source", params.source);
      if (params.work_mode && params.work_mode !== "All") query.set("work_mode", params.work_mode);
      if (params.employment_type && params.employment_type !== "All") query.set("employment_type", params.employment_type);
      if (params.max_experience !== undefined) query.set("max_experience", params.max_experience.toString());
      if (params.min_salary !== undefined) query.set("min_salary", params.min_salary.toString());
      if (params.min_compatibility !== undefined) query.set("min_compatibility", params.min_compatibility.toString());
      if (params.freshness_days !== undefined) query.set("freshness_days", params.freshness_days.toString());
      if (params.saved_only) query.set("saved_only", "true");
      if (params.limit) query.set("limit", params.limit.toString());
      if (params.offset) query.set("offset", params.offset.toString());
    }
    const qStr = query.toString();
    const endpoint = qStr ? `/jobs?${qStr}` : "/jobs";
    return apiClient<AggregatedJobListing[]>(endpoint, { method: "GET" });
  },

  async getJobProviders() {
    return apiClient<JobProviderStatus[]>("/jobs/providers", { method: "GET" });
  },

  async syncJobProviders(limit_per_source: number = 35) {
    return apiClient<{ total_fetched: number; total_imported: number; total_updated: number; providers: any }>(
      `/jobs/sync?limit_per_source=${limit_per_source}`,
      { method: "POST" }
    );
  },

  async toggleSaveJob(jobId: string) {
    return apiClient<{ saved: boolean; message: string; job_id: string }>(
      `/jobs/${jobId}/save`,
      { method: "POST" }
    );
  },

  async getMySavedJobs() {
    return apiClient<AggregatedJobListing[]>("/jobs/saved/my", { method: "GET" });
  },

  async getJobDetails(id: string) {
    return apiClient<AggregatedJobListing>(
      `/jobs/${id}`,
      { method: "GET" }
    );
  },

  // Legacy Skill Gap
  async getLegacySkillGaps() {
    return apiClient<SkillGapItem[]>(
      "/skill-gaps",
      { method: "GET" },
      mockSkillGaps
    );
  },

  // Resume
  async generateResume() {
    return apiClient<ResumeData>(
      "/resume/generate",
      { method: "POST" },
      defaultResumeData
    );
  },

  // Career Roadmap
  async getCurrentRoadmap() {
    return apiClient<CareerRoadmapData>(
      "/career-roadmaps/current",
      { method: "GET" }
    );
  },

  async generateRoadmap(targetRole?: string, candidateSkills?: string[]) {
    return apiClient<CareerRoadmapData>(
      "/career-roadmaps/generate",
      {
        method: "POST",
        body: JSON.stringify({
          target_role: targetRole || "AI Engineer",
          candidate_skills: candidateSkills,
        }),
      }
    );
  },

  async updateCareerGoal(targetRole: string) {
    return apiClient<CareerRoadmapData>(
      "/career-roadmaps/goal",
      {
        method: "PATCH",
        body: JSON.stringify({ target_role: targetRole }),
      }
    );
  },

  async recalibrateRoadmap(targetRole?: string, candidateSkills?: string[]) {
    return apiClient<CareerRoadmapData>(
      "/career-roadmaps/recalibrate",
      {
        method: "POST",
        body: JSON.stringify({
          target_role: targetRole,
          candidate_skills: candidateSkills,
        }),
      }
    );
  },

  async toggleMilestone(milestoneId: string) {
    return apiClient<CareerRoadmapData>(
      `/career-roadmaps/milestones/${milestoneId}/toggle`,
      { method: "PATCH" }
    );
  },

  async toggleTask(taskId: string) {
    return apiClient<CareerRoadmapData>(
      `/career-roadmaps/tasks/${taskId}/toggle`,
      { method: "PATCH" }
    );
  },

  // Career Transitions
  async getAcademicProfile() {
    return apiClient<any>(
      "/career-transitions/academic-profile",
      { method: "GET" }
    );
  },

  async getCareerTransitions() {
    return apiClient<CareerTransitionPath[]>(
      "/career/transitions",
      { method: "GET" },
      mockCareerTransitions
    );
  },

  async searchOccupations(query: string, limit: number = 10, taxonomy?: string) {
    const taxParam = taxonomy ? `&taxonomy=${encodeURIComponent(taxonomy)}` : "";
    return apiClient<any[]>(
      `/career-transitions/occupations?q=${encodeURIComponent(query)}&limit=${limit}${taxParam}`,
      { method: "GET" }
    );
  },

  async getCareerTransitionRecommendations(currentOccupation: string, candidateSkills?: string[], limit: number = 6) {
    return apiClient<any[]>(
      "/career-transitions/recommendations",
      {
        method: "POST",
        body: JSON.stringify({
          current_occupation: currentOccupation,
          candidate_skills: candidateSkills,
          limit,
        }),
      }
    );
  },

  async analyzeCareerTransition(fromOccupation: string, toOccupation: string, candidateSkills?: string[]) {
    return apiClient<any>(
      "/career-transitions/analyze",
      {
        method: "POST",
        body: JSON.stringify({
          from_occupation: fromOccupation,
          to_occupation: toOccupation,
          candidate_skills: candidateSkills,
        }),
      }
    );
  },

  async generateTransitionBlueprint(fromOccupation: string, toOccupation: string, candidateSkills?: string[], recalibrate?: boolean) {
    return apiClient<any>(
      "/career-transitions/blueprint",
      {
        method: "POST",
        body: JSON.stringify({
          from_occupation: fromOccupation,
          to_occupation: toOccupation,
          candidate_skills: candidateSkills,
          recalibrate: recalibrate || false,
        }),
      }
    );
  },

  async adoptTransitionGoal(payload: {
    from_occupation_title: string;
    target_occupation_id: string;
    target_occupation_title: string;
    fit_percentage: number;
    transition_delta: number;
    difficulty_category: string;
    blueprint?: any;
  }) {
    return apiClient<{ success: boolean; goal_id: string; message: string; roadmap_id?: string }>(
      "/career-transitions/adopt-goal",
      {
        method: "POST",
        body: JSON.stringify(payload),
      }
    );
  },

  async getUserTransitionProgress() {
    return apiClient<any[]>(
      "/career-transitions/progress",
      { method: "GET" }
    );
  },

  // Assessment Results
  async getAssessmentResults() {
    return apiClient<AssessmentResult[]>(
      "/assessment/results",
      { method: "GET" },
      mockAssessmentResults
    );
  },

  // Applications
  async getApplications() {
    return apiClient<JobApplication[]>(
      "/applications",
      { method: "GET" },
      mockApplications
    );
  },

  // Prompts (Admin Evaluation)
  async getPrompts() {
    return apiClient<PromptEvaluationItem[]>(
      "/admin/prompts",
      { method: "GET" },
      mockPromptEvaluations
    );
  },

  // Feature 2: Technical Assessments
  async getTechnicalRoles() {
    return apiClient<Array<{ role_id: string; title: string; category: string; description: string; skill_count: number }>>(
      "/assessments/technical/roles",
      { method: "GET" }
    );
  },

  async getTechnicalRoleDetails(roleId: string) {
    return apiClient<{
      role_id: string;
      title: string;
      category: string;
      description: string;
      skills: Array<{ skill_id: string; name: string; subtopics: string[] }>;
    }>(
      `/assessments/technical/roles/${roleId}`,
      { method: "GET" }
    );
  },

  async startTechnicalAssessment(params: {
    role_id: string;
    skill_id?: string;
    assessment_type?: string;
    difficulty?: string;
    question_count?: number;
  }) {
    return apiClient<{
      session_id: string;
      role_id: string;
      role_title: string;
      difficulty_mode: string;
      duration_minutes: number;
      total_questions: number;
      questions: any[];
    }>(
      "/assessments/technical/start",
      {
        method: "POST",
        body: JSON.stringify(params),
      }
    );
  },

  async runCodeSandbox(params: {
    question_id?: string;
    language?: string;
    code: string;
    visible_test_cases?: any[];
  }) {
    return apiClient<{
      passed: boolean;
      score: number;
      total_tests: number;
      passed_tests: number;
      test_results: any[];
      error?: string;
      execution_time_ms: number;
    }>(
      "/assessments/technical/sandbox/run-code",
      {
        method: "POST",
        body: JSON.stringify(params),
      }
    );
  },

  async runSQLSandbox(params: {
    question_id?: string;
    candidate_query: string;
    schema_sql?: string;
    sample_db_sql?: string;
  }) {
    return apiClient<{
      passed: boolean;
      score: number;
      actual_rows: any[];
      error?: string;
      execution_time_ms: number;
    }>(
      "/assessments/technical/sandbox/run-sql",
      {
        method: "POST",
        body: JSON.stringify(params),
      }
    );
  },

  async submitTechnicalAssessment(params: {
    session_id: string;
    role_id: string;
    answers: Array<{
      question_id: string;
      answer: any;
      language?: string;
      time_taken_seconds?: number;
    }>;
  }) {
    return apiClient<any>(
      "/assessments/technical/submit",
      {
        method: "POST",
        body: JSON.stringify(params),
      }
    );
  },

  async getTechnicalAssessmentHistory() {
    return apiClient<any[]>(
      "/assessments/technical/history",
      { method: "GET" }
    );
  },

  async getTechnicalAssessmentResult(resultId: string) {
    return apiClient<any>(
      `/assessments/technical/results/${resultId}`,
      { method: "GET" }
    );
  },

  async getAssessmentSession(sessionId: string) {
    return apiClient<{
      session_id: string;
      role_id: string;
      role_title: string;
      difficulty_mode: string;
      questions: any[];
      current_index: number;
      answers: Record<string, any>;
      time_left_seconds: number;
      is_expired: boolean;
      total_questions: number;
    }>(
      `/assessments/technical/sessions/${sessionId}`,
      { method: "GET" }
    );
  },

  async saveAssessmentSessionProgress(sessionId: string, currentIndex: number, answers: Record<string, any>) {
    return apiClient<{ success: boolean; saved_answers_count: number }>(
      `/assessments/technical/sessions/${sessionId}/progress`,
      {
        method: "POST",
        body: JSON.stringify({ current_index: currentIndex, answers }),
      }
    );
  },

  async cancelAssessmentSession(sessionId: string) {
    return apiClient<{ success: boolean; message: string }>(
      `/assessments/technical/sessions/${sessionId}/cancel`,
      { method: "POST" }
    );
  },

  // Feature 3: AI Resume Generator & Exports
  async aiGenerateResume(payload: { rawResumeData: any; targetRole?: string; instruction?: string }) {
    return apiClient<{
      enhancedResumeData: any;
      recommendedTemplate: string;
      recommendationReason: string;
      generationLatencyMs: number;
      modelName: string;
      modificationsSummary: string[];
    }>("/resumes/ai-generate", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  async aiEnhanceText(payload: { text: string; sectionType: string; contextRole?: string }) {
    return apiClient<{
      originalText: string;
      enhancedText: string;
      suggestedBullets: string[];
      latencyMs: number;
    }>("/resumes/enhance-text", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  async recommendResumeDesign(payload: {
    resumeData: any;
    targetRole?: string;
    candidateDesignCatalog?: any[];
  }) {
    return apiClient<{
      recommendedDesignId: string;
      explanation: string;
      matchingProfileCharacteristics: string[];
      whyAppropriate: string;
      isFallback: boolean;
      fallbackReason?: string;
      latencyMs: number;
      modelName: string;
    }>("/resumes/recommend-design", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  async saveResume(payload: {
    resumeData?: any;
    resume_data?: any;
    title?: string;
    resumeId?: string;
    isPrimary?: boolean;
    is_primary?: boolean;
    template_id?: string;
  }) {
    return apiClient<{
      success: boolean;
      resumeId: string;
      versionId: string;
      title: string;
      updatedAt: string;
      message: string;
    }>("/resumes/save", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  async listSavedResumes() {
    return apiClient<any[]>("/resumes", { method: "GET" });
  },

  async getResumeJson(resumeId: string) {
    return apiClient<any>(`/resumes/${resumeId}/json`, { method: "GET" });
  },

  async exportResumeDocx(resumeData: any): Promise<Blob> {
    const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
    const token = typeof window !== "undefined" ? localStorage.getItem("auth_token") : null;
    const response = await fetch(`${API_BASE_URL}/resumes/export-docx`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(resumeData),
    });
    if (!response.ok) {
      throw new Error(`DOCX export failed with status: ${response.status}`);
    }
    return response.blob();
  },

  async uploadResumeFile(file: File): Promise<any> {
    const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
    const token = typeof window !== "undefined" ? localStorage.getItem("auth_token") : null;
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/resumes/upload-parse`, {
      method: "POST",
      headers: {
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: formData,
    });

    if (!response.ok) {
      const errJson = await response.json().catch(() => null);
      throw new Error(errJson?.detail || `Upload parse failed with status ${response.status}`);
    }
    return response.json();
  },

  async analyzeJobDescription(jobDescriptionText: string, jobTitle?: string) {
    const res = await apiClient<{
      jobTitle: string;
      seniorityLevel: string;
      requiredSkills: string[];
      preferredSkills: string[];
      qualifications: string[];
      keyResponsibilities: string[];
      sourceEvidence: Record<string, string[]>;
      analysisLatencyMs: number;
    }>("/resumes/analyze-jd", {
      method: "POST",
      body: JSON.stringify({ jobDescriptionText, jobTitle }),
    });
    return res.data;
  },

  async matchResumeAts(payload: {
    resumeData?: any;
    parsedResume?: any;
    jobDescription: string;
    jobTitle?: string;
  }) {
    const res = await apiClient<{
      overallScore: number;
      breakdown: {
        partAScore: number;
        partBScore: number;
        totalScore: number;
        partADetails: {
          requiredSkillsScore: number;
          preferredSkillsScore: number;
          responsibilitiesScore: number;
          qualificationsScore: number;
        };
        partBDetails: {
          actionVerbsAndImpactScore: number;
          formattingAndParseabilityScore: number;
          sectionCompletenessScore: number;
        };
        explanation: string;
      };
      strongMatches: Array<{
        requirement: string;
        category: string;
        status: string;
        similarityScore: number;
        resumeEvidence?: string;
        jdEvidence?: string;
      }>;
      partialMatches: Array<{
        requirement: string;
        category: string;
        status: string;
        similarityScore: number;
        resumeEvidence?: string;
        jdEvidence?: string;
      }>;
      missingRequirements: Array<{
        requirement: string;
        category: string;
        status: string;
        similarityScore: number;
        resumeEvidence?: string;
        jdEvidence?: string;
      }>;
      strengthsSummary: string[];
      criticalGapsSummary: string[];
      evaluatedAt: string;
    }>("/resumes/match-ats", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    return res.data;
  },

  async improveResumeAts(payload: {
    resumeData: any;
    jobDescription: string;
    gapRequirements?: string[];
  }) {
    const res = await apiClient<{
      suggestions: Array<{
        id: string;
        targetSection: string;
        originalText: string;
        suggestedText: string;
        starMethodologyNotes: string;
        missingEvidenceQuestion?: string;
        rationale: string;
        status: string;
      }>;
      targetedQuestions: string[];
      groundingDisclaimer: string;
    }>("/resumes/ai-improve", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    return res.data;
  },

  // ==========================================
  // Skill Gap Analyzer Endpoints (Feature 4)
  // ==========================================

  async analyzeSkillGap(payload: {
    candidateSkills: string[];
    targetOccupationTitle: string;
    targetOccupationSource?: string;
    customJobDescription?: string;
    includeAiStrategy?: boolean;
  }) {
    const res = await apiClient<{
      targetOccupation: string;
      sourceTaxonomy: string;
      overallMatchScore: number;
      totalCompetenciesRequired: number;
      verifiedSkillsCount: number;
      partialSkillsCount: number;
      gapSkillsCount: number;
      competencies: Array<{
        skillName: string;
        canonicalName: string;
        category: string;
        status: "verified_match" | "partially_supported" | "skill_gap" | "not_assessed";
        importance: "essential" | "optional" | "in_demand";
        candidateLevel: string;
        expectedLevel: string;
        similarityScore: number;
        evidence?: string;
        priorityRank: number;
        recommendedResources: Array<{
          id: string;
          title: string;
          provider: string;
          url: string;
          difficulty: string;
          type: string;
          verified: boolean;
        }>;
      }>;
      learningResources: Array<{
        id: string;
        title: string;
        provider: string;
        url: string;
        difficulty: string;
        type: string;
        verified: boolean;
      }>;
      aiStrategy?: {
        targetRole: string;
        overallMatchScore: number;
        executiveSummary: string;
        weeklyMilestones: Array<{
          week: number;
          title: string;
          focusSkills: string[];
          actionItems: string[];
          suggestedResourceUrl?: string;
        }>;
        practicalProjects: string[];
        assessmentMilestones: string[];
        groundingDisclaimer: string;
      };
      evaluatedAt: string;
    }>("/skill-gaps/analyze", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    return res.data;
  },

  async getSkillGapOccupations(query: string = "", source: string = "esco") {
    const res = await apiClient<Array<{
      title: string;
      source: string;
      totalCompetencies: number;
      description?: string;
    }>>(`/skill-gaps/occupations?query=${encodeURIComponent(query)}&source=${encodeURIComponent(source)}`);
    return res.data;
  },

  async getSkillGapResources(skills: string[]) {
    const res = await apiClient<Array<{
      id: string;
      title: string;
      provider: string;
      url: string;
      difficulty: string;
      type: string;
      verified: boolean;
    }>>("/skill-gaps/learning-resources", {
      method: "POST",
      body: JSON.stringify(skills),
    });
    return res.data;
  },

  // AI Assistant / Career Mentor (Google Gemini API)
  async getAssistantConsultations() {
    const res = await apiClient<Array<{
      id: string;
      title: string;
      language: string;
      date: string;
      last_message_preview?: string;
      message_count: number;
      updated_at: string;
    }>>("/assistant/consultations");
    return res.data;
  },

  async createAssistantConsultation(title?: string, language?: string) {
    const res = await apiClient<{
      id: string;
      title: string;
      language: string;
      created_at: string;
      updated_at: string;
      messages: AssistantMessage[];
    }>("/assistant/consultations", {
      method: "POST",
      body: JSON.stringify({ title, language }),
    });
    return res.data;
  },

  async getAssistantConsultation(consultationId: string) {
    const res = await apiClient<{
      id: string;
      title: string;
      language: string;
      created_at: string;
      updated_at: string;
      messages: AssistantMessage[];
    }>(`/assistant/consultations/${consultationId}`);
    return res.data;
  },

  async sendAssistantMessage(consultationId: string, content: string, language?: string) {
    const res = await apiClient<AssistantMessage>(`/assistant/consultations/${consultationId}/messages`, {
      method: "POST",
      body: JSON.stringify({ content, language }),
    });
    return res.data;
  },

  async deleteAssistantConsultation(consultationId: string) {
    const res = await apiClient<{ message: string; id: string }>(`/assistant/consultations/${consultationId}`, {
      method: "DELETE",
    });
    return res.data;
  },

  async updateAssistantConsultation(consultationId: string, data: { title?: string; language?: string }) {
    const res = await apiClient<{
      id: string;
      title: string;
      language: string;
      created_at: string;
      updated_at: string;
      messages: AssistantMessage[];
    }>(`/assistant/consultations/${consultationId}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    });
    return res.data;
  },
};



