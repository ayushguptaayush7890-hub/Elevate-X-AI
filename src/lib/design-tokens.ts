/**
 * ELEVATE X AI - ROYAL GOLD EDITION DESIGN TOKENS
 * Centralized design system colors, typography, gradients, and elevation.
 */

export const colors = {
  // Brand Primary & Navy
  royalNavy: "#17233F",
  deepNavy: "#10192D",
  midnightBlue: "#0B1120",

  // Gold Accents
  champagneGold: "#D6A84B",
  lightGold: "#F0D99B",
  paleGold: "#F9F3E5",
  goldBorder: "#E5CCA0",

  // Intelligence & AI Accent
  electricViolet: "#7355D9",
  electricVioletLight: "#8C71E8",
  electricVioletDark: "#5838BF",
  electricBlue: "#3478F6",
  brightCyan: "#36D6E8",

  // Content Backgrounds (Ivory / Cream)
  warmIvory: "#F5F0E6",
  softCream: "#FBF8F1",
  pureWhite: "#FFFFFF",
  cardBg: "rgba(255, 255, 255, 0.92)",
  navyCardBg: "#17233F",

  // Feedback & Functional Colors
  sageGreen: "#DCEAE6",
  successGreen: "#27856B",
  terracotta: "#C77B54",
  terracottaLight: "#F7EBE5",
  warningAmber: "#D97706",
  infoBlue: "#2563EB",

  // Typography
  mainText: "#20243A",
  secondaryText: "#687187",
  mutedText: "#8E97AB",
  lightText: "#F5F0E6",

  // Borders
  borderLight: "#E6DFD1",
  borderGold: "rgba(214, 168, 75, 0.35)",
  borderNavy: "rgba(23, 35, 63, 0.12)",
  borderDark: "rgba(255, 255, 255, 0.12)",
} as const;

export const gradients = {
  // Hero Gradient (#100B2E, #21105A, #3821A6, #5738D5, #142B68)
  heroRadial: "radial-gradient(ellipse at 50% 30%, #3821A6 0%, #21105A 45%, #100B2E 100%)",
  heroLinear: "linear-gradient(135deg, #100B2E 0%, #21105A 30%, #3821A6 60%, #142B68 100%)",
  
  // Gold Accents
  goldShimmer: "linear-gradient(135deg, #F0D99B 0%, #D6A84B 50%, #B88628 100%)",
  goldText: "linear-gradient(135deg, #F0D99B 0%, #D6A84B 100%)",

  // Electric Blue to Violet (for "Your Skills" highlight)
  skillsGradient: "linear-gradient(135deg, #36D6E8 0%, #3478F6 50%, #7355D9 100%)",
  
  // Royal Navy Surface
  navyCard: "linear-gradient(145deg, #1A2748 0%, #10192D 100%)",
  
  // Buttons
  goldButton: "linear-gradient(135deg, #D6A84B 0%, #C49335 100%)",
  violetButton: "linear-gradient(135deg, #7355D9 0%, #5838BF 100%)",
  navyButton: "linear-gradient(135deg, #17233F 0%, #10192D 100%)",
} as const;

