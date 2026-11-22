/**
 * Complete Design Engine Type Definitions for Elevate X AI
 * Supports 1000+ distinct, reproducible, composition-based resume designs.
 */

import { ResumeFullData } from "./resume-generator";

export type BaseLayoutType =
  | "single_column_classic"
  | "single_column_modern"
  | "two_column_left_sidebar"
  | "two_column_right_sidebar"
  | "two_column_balanced"
  | "split_header_single"
  | "compact_technical_terminal"
  | "executive_bordered_frame";

export type HeaderStyleType =
  | "minimal_inline"
  | "centered_classic"
  | "banner_accent"
  | "terminal_code"
  | "editorial_serif"
  | "split_contrast"
  | "gradient_modern";

export type TypographySystem =
  | "modern_sans"
  | "classic_serif"
  | "technical_mono"
  | "display_serif_body_sans"
  | "display_sans_body_serif";

export type HeadingCase =
  | "uppercase_tracked"
  | "capitalize"
  | "code_style"
  | "small_caps";

export type SectionHeaderStyle =
  | "underline_solid"
  | "left_accent_bar"
  | "pill_badge"
  | "terminal_comment"
  | "boxed_shaded"
  | "clean_minimal";

export type BulletStyle =
  | "disc"
  | "dash"
  | "code_arrow"
  | "diamond";

export type SectionOrderType =
  | "experience_first"
  | "skills_first"
  | "education_first"
  | "projects_first";

export type DesignCategory =
  | "modern"
  | "minimal"
  | "creative"
  | "corporate"
  | "elegant"
  | "technical"
  | "ats_friendly";

export type TargetRole =
  | "fresher"
  | "developer"
  | "data_science"
  | "executive"
  | "creative"
  | "general";

export type AtsCompatibility =
  | "strict_ats"
  | "ats_optimized"
  | "visual_first";

export interface ColorPaletteConfig {
  name: string;
  primary: string;
  secondary: string;
  background: string;
  cardBg: string;
  textPrimary: string;
  textMuted: string;
  border: string;
  isDark: boolean;
}

export interface DesignSpecification {
  id: string; // e.g. "des-0001", "des-0412"
  name: string; // e.g. "Apex Minimalist Ivory", "Cyberpunk Terminal Pro"
  category: DesignCategory;
  targetRole: TargetRole;
  atsCompatibility: AtsCompatibility;
  layout: BaseLayoutType;
  headerStyle: HeaderStyleType;
  typography: TypographySystem;
  headingCase: HeadingCase;
  palette: ColorPaletteConfig;
  sectionOrder: SectionOrderType;
  sectionHeaderStyle: SectionHeaderStyle;
  bulletStyle: BulletStyle;
  spacing: "compact" | "normal" | "spacious";
  dividerStyle: "solid" | "subtle" | "dashed" | "none";
}

export interface DesignFilterOptions {
  category?: DesignCategory | "all";
  targetRole?: TargetRole | "all";
  atsOnly?: boolean;
  searchQuery?: string;
}

export interface AIRecommendationResult {
  recommendedDesignId: string;
  explanation: string;
  matchingProfileCharacteristics: string[];
  whyAppropriate: string;
  isFallback: boolean;
  fallbackReason?: string;
  latencyMs?: number;
  modelName?: string;
}
