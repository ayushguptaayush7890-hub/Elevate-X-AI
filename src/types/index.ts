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

export interface RoadmapMilestone {
  id: string;
  stageNumber: number;
  title: string;
  timeEstimate: string;
  status: 'completed' | 'in_progress' | 'upcoming';
  description: string;
  skillsToAcquire: string[];
  practicalTasks: string[];
  resources: {
    name: string;
    type: string;
    duration: string;
    free: boolean;
  }[];
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
  language?: 'English' | 'Hindi';
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
