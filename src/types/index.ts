export type SkillVerificationStatus = 
  | 'self_reported' 
  | 'ai_inferred' 
  | 'assessed' 
  | 'certified';

export type SkillProficiency = 'Beginner' | 'Intermediate' | 'Advanced' | 'Expert' | 'Not assessed';

export interface RecognizedSkill {
  id: string;
  name: string;
  normalizedSkill?: string;
  evidenceText?: string;
  category: 'Technical' | 'Transferable' | 'Domain' | 'Tools & Machinery';
  confidence: number; // 0 - 100
  status: SkillVerificationStatus;
  proficiency: SkillProficiency;
  evidence: string;
  assessedScore?: number;
  yearsOfPractice?: number;
  spanId?: string;
  startOffset?: number;
  endOffset?: number;
  canonicalSkill?: string | null;
  canonicalSkillId?: string | null;
  isUnmapped?: boolean;
  humanReviewRequired?: boolean;
  mappingConfidence?: number;
  isDemoData?: boolean;
}

export interface ExtractedSkillCrosswalks {
  esco_uri?: string | null;
  onet_soc_code?: string | null;
  nsqf_reference?: string | null;
}

export interface ExtractedSkillSpan {
  span_id: string;
  extracted_skill: string;
  normalized_skill?: string;
  evidence_text?: string;
  start_offset: number;
  end_offset: number;
  skill_category: string;
  category_confidence: number;
  canonical_skill: string | null;
  canonical_skill_id: string | null;
  mapping_status: string;
  is_unmapped_skill: boolean;
  mapping_confidence: number;
  human_review_required: boolean;
  crosswalks: ExtractedSkillCrosswalks;
}

export interface DetectedOccupation {
  occupation_id: string;
  occupation_title: string;
  confidence: number;
}

export interface SkillExtractionMetadata {
  model_version: string;
  inference_device: string;
  latency_ms: number;
  training_safety_gate_status: string;
  model_provenance?: string;
  benchmark_type?: string;
}

export interface SkillExtractionResponse {
  input_text: string;
  detected_occupation: DetectedOccupation;
  extracted_skills_count: number;
  extracted_skills: ExtractedSkillSpan[];
  metadata: SkillExtractionMetadata;
}

export interface UserProfile {
  id: string;
  fullName: string;
  email: string;
  phone: string;
  avatarUrl?: string;
  role: 'user' | 'admin';
  location: string;
  preferredLanguage: 'English' | 'Hindi';
  ageRange: string;
  educationLevel: string;
  qualifications: string[];
  currentOccupation: string;
  yearsOfExperience: number;
  workDescription: string;
  desiredSalaryMin: number;
  desiredSalaryMax: number;
  preferredLocations: string[];
  employmentType: 'Full-time' | 'Part-time' | 'Contract' | 'Self-employed';
  profileCompleteness: number; // percentage
  skills: RecognizedSkill[];
}

export interface JobListing {
  id: string;
  title: string;
  company: string;
  logoUrl?: string;
  location: string;
  salaryRange: string;
  employmentType: 'Full-time' | 'Part-time' | 'Contract' | 'Apprenticeship';
  experienceLevel: string;
  requiredSkills: string[];
  source: string;
  postedDate: string;
  matchScore: number; // 0 - 100
  matchingSkills: string[];
  missingSkills: string[];
  matchExplanation: string;
  description: string;
  responsibilities: string[];
  qualifications: string[];
  benefits: string[];
  employerInfo: {
    name: string;
    about: string;
    size: string;
    industry: string;
  };
}

export interface AggregatedJobListing {
  id: string;
  employer_id?: string;
  employer?: {
    id?: string;
    name: string;
    website?: string | null;
    location?: string | null;
    logo_url?: string | null;
  } | null;
  title: string;
  location: string;
  country?: string;
  description: string;
  salary_min?: number | null;
  salary_max?: number | null;
  salary_currency?: string;
  employment_type?: string;
  experience_required_years?: number;
  experience_min_years?: number | null;
  experience_max_years?: number | null;
  education_required?: string | null;
  source_type?: string;
  source_provider?: string;
  source_url?: string | null;
  application_url?: string | null;
  provider_job_id?: string | null;
  work_mode?: string;
  required_skills_list?: string[];
  last_verified_at?: string | null;
  listing_status?: string;
  match_details?: {
    match_score: number;
    match_tier: string;
    matching_verified_skills: string[];
    missing_required_skills: string[];
    relevant_experience_years: number;
    experience_fit: string;
    academic_alignment?: string | null;
    matching_methodology: string;
  } | null;
  is_saved?: boolean;
  posted_date?: string | null;
  expiry_date?: string | null;
  is_verified?: boolean;
  is_active?: boolean;
  created_at?: string;
}

export interface JobProviderStatus {
  provider_id: string;
  name: string;
  official_website: string;
  api_docs_url?: string | null;
  status: "active" | "ready_for_key" | "pending_partner_approval";
  public_api_available: boolean;
  auth_requirements: string;
  commercial_usage_permission: string;
  data_fields_available: string[];
  original_listing_url_available: boolean;
  direct_application_url_available: boolean;
  refresh_restrictions: string;
  jobs_imported_count: number;
  last_sync_timestamp?: string | null;
}

export interface AssessmentQuestion {
  id: string;
  questionNumber: number;
  type: 'multiple_choice' | 'scenario' | 'practical';
  questionText: string;
  scenarioContext?: string;
  options: {
    id: string;
    text: string;
  }[];
  correctOptionId: string;
  explanation: string;
  skillEvaluated: string;
}

export interface AssessmentResult {
  id: string;
  skillName: string;
  dateCompleted: string;
  score: number; // percentage
  totalQuestions: number;
  correctAnswers: number;
  timeSpentMinutes: number;
  strengths: string[];
  areasToImprove: string[];
  nextSteps: string[];
  status: 'passed' | 'needs_practice';
  indicativeLevel: SkillProficiency;
}

export interface SkillGapItem {
  id: string;
  skillName: string;
  category: string;
  currentLevel: SkillProficiency | 'None';
  requiredLevel: SkillProficiency;
  importance: 'High' | 'Medium' | 'Low';
  gapScore: number; // 0 - 100
  learningRecommendation: string;
  recommendedResource: {
    title: string;
    type: 'Video' | 'Hands-on Project' | 'Vocational Workshop' | 'Interactive Guide';
    duration: string;
    isFree: boolean;
  };
}

export interface ResumeData {
  fullName: string;
  email: string;
  phone: string;
  location: string;
  headline: string;
  summary: string;
  experience: {
    id: string;
    role: string;
    organization: string;
    period: string;
    highlights: string[];
  }[];
  education: {
    id: string;
    degree: string;
    institution: string;
    year: string;
  }[];
  skills: {
    technical: string[];
    transferable: string[];
    tools: string[];
  };
  certifications: string[];
  projects: {
    id: string;
    name: string;
    description: string;
  }[];
  template: 'modern' | 'minimal' | 'skills_focused';
}

export interface RoadmapTaskItem {
  id: string;
  milestone_id?: string;
  title: string;
  description?: string;
  task_type?: string;
  estimated_hours?: number;
  is_completed: boolean;
  resource_url?: string;
}

export interface RoadmapMilestone {
  id: string;
  stageNumber?: number;
  stage_number?: number;
  order_index?: number;
  title: string;
  timeEstimate?: string;
  time_estimate?: string;
  status: 'completed' | 'in_progress' | 'upcoming' | 'blocked';
  is_completed?: boolean;
  description: string;
  rationale?: string;
  skillsToAcquire?: string[];
  skills_to_acquire?: string[];
  practicalTasks?: string[];
  practical_tasks?: string[];
  competencyEvidence?: Record<string, string>;
  competency_evidence?: Record<string, string>;
  tasks?: RoadmapTaskItem[];
  resources: {
    name: string;
    title?: string;
    type: string;
    duration: string;
    free: boolean;
    url?: string;
    source_domain?: string;
  }[];
}

export interface CareerRoadmapData {
  id: string;
  user_id?: string;
  title: string;
  target_role: string;
  target_occupation_id?: string;
  estimated_duration_weeks: number;
  progress_percentage: number;
  status: string;
  total_milestones: number;
  completed_milestones: number;
  total_tasks: number;
  completed_tasks: number;
  estimated_total_hours: number;
  milestones: RoadmapMilestone[];
  created_at?: string;
  updated_at?: string;
}

export interface CareerTransitionPath {
  id: string;
  targetRole: string;
  industry: string;
  suitabilityScore: number; // 0 - 100
  transitionDifficulty: 'Low' | 'Moderate' | 'High';
  averageSalaryIncrease: string;
  transferableSkills: string[];
  skillsToAcquire: string[];
  bridgeSteps: string[];
  demandLevel: 'High' | 'Very High' | 'Growing';
}

export interface InterviewQuestion {
  id: string;
  role: string;
  category: 'Experience' | 'Situational' | 'Technical' | 'Customer Communication';
  question: string;
  sampleAnswer: string;
  evaluationCriteria: string[];
}

export interface MockInterviewSession {
  id: string;
  targetJob: string;
  date: string;
  overallScore: number;
  relevanceScore: number;
  communicationScore: number;
  strengths: string[];
  growthAreas: string[];
  feedbackNotes: string;
}

export interface AssistantMessage {
  id: string;
  sender: 'user' | 'assistant';
  content: string;
  timestamp: string;
  suggestions?: string[];
  language?: 'English' | 'Hindi' | string;
  model_used?: string;
  tokens_used?: number;
}

export interface ConsultationItem {
  id: string;
  title: string;
  language: string;
  date: string;
  last_message_preview?: string;
  message_count: number;
  updated_at: string;
}

export interface ConsultationDetail {
  id: string;
  title: string;
  language: string;
  created_at: string;
  updated_at: string;
  messages: AssistantMessage[];
}

export interface JobApplication {
  id: string;
  jobId: string;
  jobTitle: string;
  company: string;
  location: string;
  salary: string;
  status: 'saved' | 'applied' | 'interview' | 'shortlisted' | 'rejected' | 'offer';
  appliedDate: string;
  lastUpdated: string;
  matchScore: number;
  notes: string;
}

export type PromptTechnique = 
  | 'Zero-Shot'
  | 'Few-Shot'
  | 'Role-Based'
  | 'Structured JSON'
  | 'Multi-Step'
  | 'Context-Aware'
  | 'RAG-Grounded'
  | 'Guardrail'
  | 'Adaptive';

export interface PromptEvaluationItem {
  id: string;
  name: string;
  category: 'Skill Extraction' | 'Job Matching' | 'Resume Enhancement' | 'Roadmap Generation' | 'Skill Gap Analysis';
  technique: PromptTechnique;
  version: string;
  status: 'Production' | 'Experimental' | 'Deprecated';
  systemPrompt: string;
  userPromptTemplate: string;
  testInput: string;
  baselineOutput: string;
  improvedOutput: string;
  metrics: {
    extractionAccuracy: number;
    evidenceValidation: number;
    jobRelevance: number;
    factuality: number;
    jsonValidity: number;
    latencyMs: number;
  };
  baselineMetrics: {
    extractionAccuracy: number;
    evidenceValidation: number;
    jobRelevance: number;
    factuality: number;
    jsonValidity: number;
    latencyMs: number;
  };
}
