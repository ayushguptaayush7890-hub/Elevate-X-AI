import { apiClient } from "@/lib/api";
import { 
  UserProfile, 
  RecognizedSkill, 
  SkillExtractionResponse,
  JobListing, 
  SkillGapItem, 
  RoadmapMilestone, 
  CareerTransitionPath, 
  AssessmentResult, 
  JobApplication, 
  PromptEvaluationItem, 
  ResumeData 
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

  async getJobDetails(id: string) {
    const job = mockJobListings.find((j) => j.id === id) || mockJobListings[0];
    return apiClient<JobListing>(
      `/jobs/${id}`,
      { method: "GET" },
      job
    );
  },

  // Skill Gap
  async analyzeSkillGap() {
    return apiClient<SkillGapItem[]>(
      "/skill-gap",
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

  // Roadmap
  async generateRoadmap() {
    return apiClient<RoadmapMilestone[]>(
      "/roadmap",
      { method: "GET" },
      mockRoadmapMilestones
    );
  },

  // Career Transitions
  async getCareerTransitions() {
    return apiClient<CareerTransitionPath[]>(
      "/career/transitions",
      { method: "GET" },
      mockCareerTransitions
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
};

