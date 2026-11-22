/**
 * Elevate X AI — Skill Normalization & Deduplication Utilities
 * Preserves distinct skills (e.g. Java vs JavaScript, C vs C++) while canonicalizing
 * verified aliases (e.g. py -> Python, k8s -> Kubernetes, reactjs -> React.js).
 */

export const CANONICAL_SKILL_SYNONYMS: Record<string, string> = {
  "py": "Python",
  "python3": "Python",
  "python programming": "Python",
  "cpp": "C++",
  "c plus plus": "C++",
  "cplusplus": "C++",
  "c#": "C#",
  "csharp": "C#",
  "c sharp": "C#",
  "js": "JavaScript",
  "javascript": "JavaScript",
  "ts": "TypeScript",
  "typescript": "TypeScript",
  "react": "React.js",
  "reactjs": "React.js",
  "react.js": "React.js",
  "node": "Node.js",
  "nodejs": "Node.js",
  "node.js": "Node.js",
  "postgres": "PostgreSQL",
  "postgresql": "PostgreSQL",
  "k8s": "Kubernetes",
  "kubernetes": "Kubernetes",
  "docker": "Docker",
  "docker container": "Docker",
  "ml": "Machine Learning",
  "dl": "Deep Learning",
  "ai": "Artificial Intelligence",
  "nlp": "Natural Language Processing",
  "cv": "Computer Vision",
  "llm": "Large Language Models",
  "llms": "Large Language Models",
  "rag": "Retrieval-Augmented Generation",
  "dsa": "Data Structures and Algorithms",
  "oop": "Object-Oriented Programming",
  "dbms": "Database Management Systems",
  "html": "HTML",
  "html5": "HTML",
  "css": "CSS",
  "css3": "CSS",
  "aws": "Amazon Web Services (AWS)",
  "aws cloud": "Amazon Web Services (AWS)",
  "gcp": "Google Cloud Platform (GCP)",
  "azure": "Microsoft Azure",
  "git": "Git",
  "github": "GitHub",
  "fastapi": "FastAPI",
  "flask": "Flask",
  "pytorch": "PyTorch",
  "tensorflow": "TensorFlow",
  "pandas": "Pandas",
  "numpy": "NumPy",
  "scikit-learn": "Scikit-learn",
  "sklearn": "Scikit-learn",
};

/**
 * Normalizes skill key for case-insensitive and canonical comparison.
 * Preserves distinct skills like Java vs JavaScript, C vs C++.
 */
export function normalizeSkillKey(raw: string): string {
  if (!raw || typeof raw !== "string") return "";
  const trimmed = raw.trim().toLowerCase();
  if (CANONICAL_SKILL_SYNONYMS[trimmed]) {
    return CANONICAL_SKILL_SYNONYMS[trimmed].toLowerCase();
  }
  const clean = trimmed
    .replace(/\s+/g, " ")
    .replace(/[^\w\s\+\#\.\-]/g, "")
    .trim();
  if (CANONICAL_SKILL_SYNONYMS[clean]) {
    return CANONICAL_SKILL_SYNONYMS[clean].toLowerCase();
  }
  return clean || trimmed;
}

/**
 * Generates a stable unique ID suitable for React keys and data records.
 */
export function createSkillId(raw: string): string {
  const normKey = normalizeSkillKey(raw);
  const slug = normKey
    .replace(/\+/g, "plus")
    .replace(/#/g, "sharp")
    .replace(/\./g, "dot")
    .replace(/[^a-z0-9]/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
  return `skill-${slug || "item"}`;
}

/**
 * Generates a deterministic, namespaced, unique candidate skill ID.
 * Preserves source attribution and competency identity without ID collisions.
 */
export function generateCandidateSkillId(name: string, source: string = "profile", sourceId?: string): string {
  const normKey = normalizeSkillKey(name);
  const slug = normKey
    .replace(/\+/g, "plus")
    .replace(/#/g, "sharp")
    .replace(/\./g, "dot")
    .replace(/[^a-z0-9]/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
  const baseSlug = slug || "item";
  const sourcePrefix = source.replace(/[^a-z0-9]/gi, "-").toLowerCase();
  return `cand-${sourcePrefix}-${baseSlug}`;
}

/**
 * Deduplicates and normalizes candidate skills, preventing duplicate competencies
 * while preserving source attribution, confidence, and taxonomy references.
 */
export function deduplicateCandidateSkills<T extends { name: string; id?: string; source?: string; sourceId?: string; confidence?: number; evidence?: string }>(
  skills: T[]
): (T & { id: string })[] {
  if (!Array.isArray(skills)) return [];
  const seenKeys = new Map<string, T & { id: string }>();

  for (const item of skills) {
    if (!item || !item.name || typeof item.name !== "string") continue;
    const trimmed = item.name.trim();
    if (!trimmed) continue;

    const normKey = normalizeSkillKey(trimmed);
    if (!normKey) continue;

    const preferredName = CANONICAL_SKILL_SYNONYMS[trimmed.toLowerCase()] || trimmed;
    const source = item.source || "profile_verified";
    const originalSourceId = item.sourceId || (item.id && !item.id.startsWith("cand-") ? item.id : undefined);
    const stableId = generateCandidateSkillId(preferredName, source, originalSourceId);

    if (!seenKeys.has(normKey)) {
      seenKeys.set(normKey, {
        ...item,
        name: preferredName,
        id: stableId,
        sourceId: originalSourceId,
      });
    } else {
      // Merge enrichment metadata: preserve highest confidence and richest evidence
      const existing = seenKeys.get(normKey)!;
      const existingConf = existing.confidence ?? 0;
      const itemConf = item.confidence ?? 0;
      if (itemConf > existingConf) {
        existing.confidence = itemConf;
      }
      if (!existing.evidence && item.evidence) {
        existing.evidence = item.evidence;
      }
      if (!existing.sourceId && originalSourceId) {
        existing.sourceId = originalSourceId;
      }
    }
  }

  return Array.from(seenKeys.values());
}

/**
 * Deduplicates skill list case-insensitively, preserving preferred casing.
 */
export function deduplicateSkills(skills: string[]): string[] {
  if (!Array.isArray(skills)) return [];
  const seenKeys = new Set<string>();
  const deduplicated: string[] = [];

  for (const item of skills) {
    if (!item || typeof item !== "string") continue;
    const trimmed = item.trim();
    if (!trimmed) continue;
    
    const key = normalizeSkillKey(trimmed);
    if (!key) continue;
    
    if (!seenKeys.has(key)) {
      seenKeys.add(key);
      const canonicalName = CANONICAL_SKILL_SYNONYMS[trimmed.toLowerCase()] || trimmed;
      deduplicated.push(canonicalName);
    }
  }

  return deduplicated;
}
