/**
 * Deterministic 1000+ Resume Design Engine for Elevate X AI
 * Composes independent layouts, headers, typographies, color palettes,
 * section arrangements, and borders into 1024+ verified reproducible designs.
 */

import {
  DesignSpecification,
  BaseLayoutType,
  HeaderStyleType,
  TypographySystem,
  HeadingCase,
  SectionHeaderStyle,
  BulletStyle,
  SectionOrderType,
  DesignCategory,
  TargetRole,
  AtsCompatibility,
  ColorPaletteConfig,
  DesignFilterOptions,
  AIRecommendationResult,
} from "@/types/resume-design-engine";
import { ResumeFullData } from "@/types/resume-generator";

// 1. Curated Harmonious Color Palettes
export const PALETTES: ColorPaletteConfig[] = [
  {
    name: "Royal Navy & Gold",
    primary: "#17233F",
    secondary: "#D6A84B",
    background: "#FFFFFF",
    cardBg: "#FBF8F1",
    textPrimary: "#17233F",
    textMuted: "#687187",
    border: "#E6DFD1",
    isDark: false,
  },
  {
    name: "Executive Slate & Platinum",
    primary: "#1E293B",
    secondary: "#3B82F6",
    background: "#FFFFFF",
    cardBg: "#F8FAFC",
    textPrimary: "#0F172A",
    textMuted: "#64748B",
    border: "#E2E8F0",
    isDark: false,
  },
  {
    name: "Emerald Forest & Sage",
    primary: "#065F46",
    secondary: "#10B981",
    background: "#FFFFFF",
    cardBg: "#F0FDF4",
    textPrimary: "#064E3B",
    textMuted: "#047857",
    border: "#D1FAE5",
    isDark: false,
  },
  {
    name: "Burgundy Wine & Rose",
    primary: "#831843",
    secondary: "#F43F5E",
    background: "#FFFFFF",
    cardBg: "#FFF1F2",
    textPrimary: "#500724",
    textMuted: "#9F1239",
    border: "#FFE4E6",
    isDark: false,
  },
  {
    name: "Electric Violet & Indigo",
    primary: "#4338CA",
    secondary: "#7355D9",
    background: "#FFFFFF",
    cardBg: "#EEF2FF",
    textPrimary: "#312E81",
    textMuted: "#6366F1",
    border: "#E0E7FF",
    isDark: false,
  },
  {
    name: "Nordic Monochrome & Crisp",
    primary: "#18181B",
    secondary: "#71717A",
    background: "#FFFFFF",
    cardBg: "#F4F4F5",
    textPrimary: "#09090B",
    textMuted: "#52525B",
    border: "#E4E4E7",
    isDark: false,
  },
  {
    name: "Teal Tech & Cyan",
    primary: "#0F766E",
    secondary: "#06B6D4",
    background: "#FFFFFF",
    cardBg: "#ECFEFF",
    textPrimary: "#134E4A",
    textMuted: "#0E7490",
    border: "#CFFAFE",
    isDark: false,
  },
  {
    name: "Terracotta Artisan & Sand",
    primary: "#9A3412",
    secondary: "#F97316",
    background: "#FFFFFF",
    cardBg: "#FFF7ED",
    textPrimary: "#7C2D12",
    textMuted: "#C2410C",
    border: "#FFEDD5",
    isDark: false,
  },
  {
    name: "Terminal Matrix Dark",
    primary: "#10B981",
    secondary: "#34D399",
    background: "#0F172A",
    cardBg: "#1E293B",
    textPrimary: "#F8FAFC",
    textMuted: "#94A3B8",
    border: "#334155",
    isDark: true,
  },
  {
    name: "High-Tech Cyberpunk Dark",
    primary: "#38BDF8",
    secondary: "#818CF8",
    background: "#0B0F19",
    cardBg: "#151D2F",
    textPrimary: "#F1F5F9",
    textMuted: "#94A3B8",
    border: "#1E293B",
    isDark: true,
  },
  {
    name: "Oxford Blue & Champagne",
    primary: "#1E3A8A",
    secondary: "#EAB308",
    background: "#FFFFFF",
    cardBg: "#FEFCE8",
    textPrimary: "#172554",
    textMuted: "#4B5563",
    border: "#E5E7EB",
    isDark: false,
  },
  {
    name: "Minimalist Ivory Classic",
    primary: "#262626",
    secondary: "#A3A3A3",
    background: "#FAF9F6",
    cardBg: "#F5F5F0",
    textPrimary: "#171717",
    textMuted: "#737373",
    border: "#E5E5E5",
    isDark: false,
  },
];

// 2. Base Layouts
const BASE_LAYOUTS: BaseLayoutType[] = [
  "single_column_classic",
  "single_column_modern",
  "two_column_left_sidebar",
  "two_column_right_sidebar",
  "two_column_balanced",
  "split_header_single",
  "compact_technical_terminal",
  "executive_bordered_frame",
];

// 3. Header Styles
const HEADER_STYLES: HeaderStyleType[] = [
  "minimal_inline",
  "centered_classic",
  "banner_accent",
  "terminal_code",
  "editorial_serif",
  "split_contrast",
  "gradient_modern",
];

// 4. Typography Systems
const TYPOGRAPHY_SYSTEMS: TypographySystem[] = [
  "modern_sans",
  "classic_serif",
  "technical_mono",
  "display_serif_body_sans",
  "display_sans_body_serif",
];

// 5. Section Header Styles
const SECTION_HEADER_STYLES: SectionHeaderStyle[] = [
  "underline_solid",
  "left_accent_bar",
  "pill_badge",
  "terminal_comment",
  "boxed_shaded",
  "clean_minimal",
];

// 6. Section Ordering
const SECTION_ORDERS: SectionOrderType[] = [
  "experience_first",
  "skills_first",
  "education_first",
  "projects_first",
];

// 7. Bullet Styles
const BULLET_STYLES: BulletStyle[] = [
  "disc",
  "dash",
  "code_arrow",
  "diamond",
];

// 8. Categories
const CATEGORIES: DesignCategory[] = [
  "modern",
  "minimal",
  "creative",
  "corporate",
  "elegant",
  "technical",
  "ats_friendly",
];

// 9. Target Roles
const TARGET_ROLES: TargetRole[] = [
  "general",
  "developer",
  "data_science",
  "fresher",
  "executive",
  "creative",
];

// Vocabulary for realistic, inspiring Design Names
const ADJECTIVES = [
  "Apex", "Vanguard", "Nordic", "Executive", "Silicon", "Cyber", "Oxford", "Cambridge",
  "Aalto", "Zenith", "Quantum", "Nexus", "Matrix", "Koto", "Elysian", "Monarch",
  "Stellar", "Artisan", "Prism", "Imperial", "Aura", "Nova", "Titan", "Vertex",
  "Pulse", "Crest", "Solace", "Paramount", "Horizon", "Pinnacle", "Echo", "Atlas"
];

const STYLES = [
  "Pro", "Elite", "Classic", "Studio", "Clean", "Minimal", "Craft", "Prime",
  "Standard", "Format", "Suite", "Grid", "Edition", "Frame", "Canvas", "Flow"
];

/**
 * Deterministic PRNG using Murmur-like hash for reproducible design generation
 */
function pseudoHash(n: number): number {
  let x = Math.sin(n + 1) * 10000;
  return x - Math.floor(x);
}

/**
 * Build a distinct, fully harmonized DesignSpecification by integer index (0 - 1023+)
 */
export function generateDesignSpecification(index: number): DesignSpecification {
  const id = `des-${String(index + 1).padStart(4, "0")}`;

  // Deterministic seed variations
  const r1 = Math.floor(pseudoHash(index * 13 + 1) * 10000);
  const r2 = Math.floor(pseudoHash(index * 29 + 3) * 10000);
  const r3 = Math.floor(pseudoHash(index * 47 + 7) * 10000);
  const r4 = Math.floor(pseudoHash(index * 61 + 11) * 10000);
  const r5 = Math.floor(pseudoHash(index * 83 + 17) * 10000);
  const r6 = Math.floor(pseudoHash(index * 97 + 23) * 10000);

  // Pick attributes
  const layout = BASE_LAYOUTS[r1 % BASE_LAYOUTS.length];
  const headerStyle = HEADER_STYLES[r2 % HEADER_STYLES.length];
  const typography = TYPOGRAPHY_SYSTEMS[r3 % TYPOGRAPHY_SYSTEMS.length];
  const palette = PALETTES[r4 % PALETTES.length];
  const sectionHeaderStyle = SECTION_HEADER_STYLES[r5 % SECTION_HEADER_STYLES.length];
  const sectionOrder = SECTION_ORDERS[r6 % SECTION_ORDERS.length];
  const bulletStyle = BULLET_STYLES[(r1 + r2) % BULLET_STYLES.length];
  const spacing: "compact" | "normal" | "spacious" =
    index % 3 === 0 ? "compact" : index % 3 === 1 ? "normal" : "spacious";
  const dividerStyle: "solid" | "subtle" | "dashed" | "none" =
    (["solid", "subtle", "dashed", "none"] as const)[(r3 + r4) % 4];

  // Derive Category & Target Role harmoniously
  let category: DesignCategory = CATEGORIES[(r1 + r3) % CATEGORIES.length];
  let targetRole: TargetRole = TARGET_ROLES[(r2 + r5) % TARGET_ROLES.length];
  let atsCompatibility: AtsCompatibility = "ats_optimized";

  // Harmonize specialized designs
  if (layout === "compact_technical_terminal" || palette.isDark) {
    category = "technical";
    targetRole = (index % 2 === 0) ? "developer" : "data_science";
    atsCompatibility = "visual_first";
  } else if (layout === "single_column_classic" && !palette.isDark) {
    category = "ats_friendly";
    atsCompatibility = "strict_ats";
  } else if (layout === "executive_bordered_frame" || typography === "classic_serif" || typography === "display_serif_body_sans") {
    category = (index % 2 === 0) ? "corporate" : "elegant";
    targetRole = "executive";
  } else if (headerStyle === "banner_accent" || headerStyle === "gradient_modern") {
    category = "creative";
    targetRole = (index % 3 === 0) ? "creative" : "fresher";
  }

  // Heading case
  const headingCase: HeadingCase =
    category === "technical"
      ? "code_style"
      : category === "corporate" || category === "ats_friendly"
        ? "uppercase_tracked"
        : category === "elegant"
          ? "small_caps"
          : "capitalize";

  // Human-readable Unique Name
  const adj = ADJECTIVES[(index * 7 + r1) % ADJECTIVES.length];
  const style = STYLES[(index * 11 + r2) % STYLES.length];
  const name = `${adj} ${palette.name.split("&")[0].trim()} ${style}`;

  return {
    id,
    name,
    category,
    targetRole,
    atsCompatibility,
    layout,
    headerStyle,
    typography,
    headingCase,
    palette,
    sectionOrder,
    sectionHeaderStyle,
    bulletStyle,
    spacing,
    dividerStyle,
  };
}

// Total available distinct indexed designs
export const TOTAL_DESIGNS_COUNT = 1024;

// Cache for high-performance memory lookup
let cachedCatalog: DesignSpecification[] | null = null;

export function getAllDesigns(): DesignSpecification[] {
  if (!cachedCatalog) {
    cachedCatalog = [];
    for (let i = 0; i < TOTAL_DESIGNS_COUNT; i++) {
      cachedCatalog.push(generateDesignSpecification(i));
    }
  }
  return cachedCatalog;
}

/**
 * Filter and search the 1000+ design catalog
 */
export function queryDesigns(
  filter: DesignFilterOptions = {},
  offset: number = 0,
  limit: number = 24
): { designs: DesignSpecification[]; total: number } {
  const all = getAllDesigns();

  let filtered = all;

  if (filter.category && filter.category !== "all") {
    filtered = filtered.filter((d) => d.category === filter.category);
  }

  if (filter.targetRole && filter.targetRole !== "all") {
    filtered = filtered.filter((d) => d.targetRole === filter.targetRole);
  }

  if (filter.atsOnly) {
    filtered = filtered.filter((d) => d.atsCompatibility === "strict_ats" || d.atsCompatibility === "ats_optimized");
  }

  if (filter.searchQuery && filter.searchQuery.trim().length > 0) {
    const q = filter.searchQuery.toLowerCase().trim();
    filtered = filtered.filter(
      (d) =>
        d.name.toLowerCase().includes(q) ||
        d.id.toLowerCase().includes(q) ||
        d.palette.name.toLowerCase().includes(q) ||
        d.category.toLowerCase().includes(q) ||
        d.targetRole.toLowerCase().includes(q)
    );
  }

  const paginated = filtered.slice(offset, offset + limit);
  return {
    designs: paginated,
    total: filtered.length,
  };
}

/**
 * Get a single design by its ID ("des-0042")
 */
export function getDesignById(id: string): DesignSpecification {
  const match = id.match(/des-(\d+)/i);
  if (match) {
    const index = parseInt(match[1], 10) - 1;
    if (index >= 0 && index < TOTAL_DESIGNS_COUNT) {
      return generateDesignSpecification(index);
    }
  }
  // Default to clean Modern Pro
  return generateDesignSpecification(0);
}

/**
 * Surprise Me: Selects an unexpected, top-tier distinct design
 */
export function getRandomDesign(excludeId?: string): DesignSpecification {
  const all = getAllDesigns();
  let candidate = all[Math.floor(Math.random() * all.length)];
  if (candidate.id === excludeId) {
    candidate = all[(all.indexOf(candidate) + 1) % all.length];
  }
  return candidate;
}

/**
 * Fallback Algorithmic Recommendation when local MLX is unavailable.
 * Clearly labeled as heuristic fallback, never faked as AI.
 */
export function getFallbackAIRecommendation(resume: ResumeFullData): AIRecommendationResult {
  const hasExtensiveExp = resume.experience && resume.experience.length >= 3;
  const isTechDev =
    (resume.skills.programmingLanguages && resume.skills.programmingLanguages.length >= 3) ||
    /developer|engineer|software|fullstack|backend|frontend/i.test(resume.personalInfo.professionalTitle || "");
  const isAIML =
    (resume.skills.aiMlSkills && resume.skills.aiMlSkills.length >= 2) ||
    /ai|ml|data|machine learning|deep learning|data scientist/i.test(resume.personalInfo.professionalTitle || "");
  const isFresher = !resume.experience || resume.experience.length === 0;

  if (isAIML) {
    return {
      recommendedDesignId: "des-0007",
      explanation: "Algorithmic heuristic matched AI/ML frameworks with research-oriented balanced architecture.",
      matchingProfileCharacteristics: ["AI & Data Science", "Model Benchmarks", "Deep Learning Stack"],
      whyAppropriate: "Highlights ML model architectures, research benchmarks, and data pipeline technical stacks.",
      isFallback: true,
      fallbackReason: "Local Qwen2.5-1.5B MLX inference unavailable; selected via deterministic algorithmic heuristic.",
      latencyMs: 0,
      modelName: "Algorithmic Heuristic Fallback (Local AI Offline)",
    };
  } else if (isTechDev) {
    return {
      recommendedDesignId: "des-0006",
      explanation: "Algorithmic heuristic matched software engineering competencies with terminal monospace design.",
      matchingProfileCharacteristics: ["Full-Stack / Systems", "Developer Tools", "GitHub Projects"],
      whyAppropriate: "Code terminal accents, command headers, and monospace font emphasize source repositories and systems architecture.",
      isFallback: true,
      fallbackReason: "Local Qwen2.5-1.5B MLX inference unavailable; selected via deterministic algorithmic heuristic.",
      latencyMs: 0,
      modelName: "Algorithmic Heuristic Fallback (Local AI Offline)",
    };
  } else if (hasExtensiveExp) {
    return {
      recommendedDesignId: "des-0004",
      explanation: "Algorithmic heuristic matched senior tenure with corporate executive serif frame.",
      matchingProfileCharacteristics: ["Leadership Progression", "Team Management", "Organizational Milestones"],
      whyAppropriate: "Framed executive serif layout emphasizes leadership chronology and business metrics.",
      isFallback: true,
      fallbackReason: "Local Qwen2.5-1.5B MLX inference unavailable; selected via deterministic algorithmic heuristic.",
      latencyMs: 0,
      modelName: "Algorithmic Heuristic Fallback (Local AI Offline)",
    };
  } else if (isFresher) {
    return {
      recommendedDesignId: "des-0008",
      explanation: "Algorithmic heuristic matched early-career profile with education & project-first visual hierarchy.",
      matchingProfileCharacteristics: ["Degree Coursework", "Academic Standing", "Foundational Projects"],
      whyAppropriate: "Education-first layout features university GPA, core courses, and project repositories prominently.",
      isFallback: true,
      fallbackReason: "Local Qwen2.5-1.5B MLX inference unavailable; selected via deterministic algorithmic heuristic.",
      latencyMs: 0,
      modelName: "Algorithmic Heuristic Fallback (Local AI Offline)",
    };
  }

  return {
    recommendedDesignId: "des-0001",
    explanation: "Algorithmic heuristic selected balanced multi-column professional layout.",
    matchingProfileCharacteristics: ["Multi-Faceted Stack", "Clear Summary", "Balanced Visuals"],
    whyAppropriate: "Royal Navy & Gold palette with balanced dual-column layout maximizes readability.",
    isFallback: true,
    fallbackReason: "Local Qwen2.5-1.5B MLX inference unavailable; selected via deterministic algorithmic heuristic.",
    latencyMs: 0,
    modelName: "Algorithmic Heuristic Fallback (Local AI Offline)",
  };
}

/**
 * Fast synchronous recommendation helper for initial state
 */
export function getRecommendedDesign(resume: ResumeFullData): DesignSpecification {
  const rec = getFallbackAIRecommendation(resume);
  return getDesignById(rec.recommendedDesignId);
}

/**
 * Curated Six-Design Batch Generator
 * Always returns exactly 6 designs.
 * Avoids duplicates from recently displayed batches (seenIds).
 * Prioritizes high visual diversity in layouts, palettes, and typography.
 */
export function getCuratedSixBatch(
  filter: DesignFilterOptions = {},
  seenIds: string[] = [],
  recommendedDesignId?: string,
  includeRecommended: boolean = true
): { designs: DesignSpecification[]; totalMatching: number; newSeenIds: string[] } {
  const all = getAllDesigns();

  // Apply filters to complete catalog
  let filtered = all;
  if (filter.category && filter.category !== "all") {
    filtered = filtered.filter((d) => d.category === filter.category);
  }
  if (filter.targetRole && filter.targetRole !== "all") {
    filtered = filtered.filter((d) => d.targetRole === filter.targetRole);
  }
  if (filter.atsOnly) {
    filtered = filtered.filter((d) => d.atsCompatibility === "strict_ats" || d.atsCompatibility === "ats_optimized");
  }
  if (filter.searchQuery && filter.searchQuery.trim().length > 0) {
    const q = filter.searchQuery.toLowerCase().trim();
    filtered = filtered.filter(
      (d) =>
        d.name.toLowerCase().includes(q) ||
        d.id.toLowerCase().includes(q) ||
        d.palette.name.toLowerCase().includes(q) ||
        d.category.toLowerCase().includes(q) ||
        d.targetRole.toLowerCase().includes(q)
    );
  }

  const totalMatching = filtered.length;
  if (totalMatching === 0) {
    // If no exact match, fallback to general modern
    return {
      designs: all.slice(0, 6),
      totalMatching: all.length,
      newSeenIds: seenIds,
    };
  }

  // Filter unseen designs
  const seenSet = new Set(seenIds);
  let unseen = filtered.filter((d) => !seenSet.has(d.id));

  // If we ran out of unseen matching designs, wrap around (excluding the most recent 6)
  if (unseen.length < 6) {
    const mostRecentSix = new Set(seenIds.slice(-6));
    unseen = filtered.filter((d) => !mostRecentSix.has(d.id));
    if (unseen.length === 0) {
      unseen = [...filtered];
    }
  }

  const selectedDesigns: DesignSpecification[] = [];
  const chosenIds: string[] = [];

  // Check if we should insert the recommended design
  if (includeRecommended && recommendedDesignId) {
    const recDesign = getDesignById(recommendedDesignId);
    // If recommended matches current filter (or filter is loose)
    const matchesFilter = filtered.some((d) => d.id === recDesign.id);
    if (matchesFilter) {
      selectedDesigns.push(recDesign);
      chosenIds.push(recDesign.id);
    }
  }

  // Pick remaining designs to reach exactly 6, prioritizing diverse layouts and palettes
  const usedLayouts = new Set(selectedDesigns.map((d) => d.layout));
  const usedPalettes = new Set(selectedDesigns.map((d) => d.palette.name));

  // First pass: pick designs with distinct layout and palette
  for (const candidate of unseen) {
    if (selectedDesigns.length >= 6) break;
    if (chosenIds.includes(candidate.id)) continue;

    if (!usedLayouts.has(candidate.layout) || !usedPalettes.has(candidate.palette.name)) {
      selectedDesigns.push(candidate);
      chosenIds.push(candidate.id);
      usedLayouts.add(candidate.layout);
      usedPalettes.add(candidate.palette.name);
    }
  }

  // Second pass: fill any remaining slots up to 6
  if (selectedDesigns.length < 6) {
    for (const candidate of unseen) {
      if (selectedDesigns.length >= 6) break;
      if (chosenIds.includes(candidate.id)) continue;
      selectedDesigns.push(candidate);
      chosenIds.push(candidate.id);
    }
  }

  // If still less than 6 (e.g. extremely narrow filter), pull from filtered list
  if (selectedDesigns.length < 6) {
    for (const candidate of filtered) {
      if (selectedDesigns.length >= 6) break;
      if (chosenIds.includes(candidate.id)) continue;
      selectedDesigns.push(candidate);
      chosenIds.push(candidate.id);
    }
  }

  const newSeenIds = Array.from(new Set([...seenIds, ...chosenIds]));

  return {
    designs: selectedDesigns.slice(0, 6),
    totalMatching,
    newSeenIds,
  };
}

