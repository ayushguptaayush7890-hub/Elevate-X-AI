export interface PersonalInfo {
  fullName: string;
  professionalTitle: string;
  email: string;
  phone: string;
  location: string;
  linkedIn?: string;
  gitHub?: string;
  portfolio?: string;
  summary: string;
}

export interface EducationEntry {
  id: string;
  institution: string;
  degree: string;
  fieldOfStudy?: string;
  startDate: string;
  endDate: string;
  grade?: string;
  coursework: string[];
}

export interface SkillCategories {
  programmingLanguages: string[];
  frameworks: string[];
  databases: string[];
  developerTools: string[];
  aiMlSkills: string[];
  otherSkills: string[];
}

export interface ExperienceEntry {
  id: string;
  company: string;
  role: string;
  employmentType: string;
  location?: string;
  startDate: string;
  endDate: string;
  current: boolean;
  responsibilities: string[];
}

export interface InternshipEntry {
  id: string;
  organization: string;
  role: string;
  duration: string;
  workPerformed: string[];
  achievements: string[];
}

export interface ProjectEntry {
  id: string;
  title: string;
  description: string;
  technologies: string[];
  contributions: string[];
  projectUrl?: string;
  githubUrl?: string;
}

export interface CertificationEntry {
  id: string;
  name: string;
  issuingOrganization: string;
  issueDate: string;
  credentialUrl?: string;
}

export interface AdditionalSections {
  achievements: string[];
  awards: string[];
  publications: string[];
  volunteerExperience: string[];
  extracurricular: string[];
  languages: string[];
  interests: string[];
}

export type TemplateId =
  | "modern"
  | "minimal"
  | "ats_friendly"
  | "corporate_executive"
  | "creative_portfolio"
  | "technical"
  | "data_science"
  | "fresher"
  | "experienced"
  | "elegant";

export interface ResumeFullData {
  personalInfo: PersonalInfo;
  education: EducationEntry[];
  skills: SkillCategories;
  experience: ExperienceEntry[];
  internships: InternshipEntry[];
  projects: ProjectEntry[];
  certifications: CertificationEntry[];
  additional: AdditionalSections;
  templateId: TemplateId;
  accentColor: string;
  typography: "sans" | "serif" | "mono";
  spacing: "compact" | "normal" | "relaxed";
}
