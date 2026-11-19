import React from "react";

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  glow?: "none" | "gold" | "violet" | "navy" | "sage" | "blue" | "subtle";
  hoverEffect?: boolean;
  padding?: "none" | "sm" | "md" | "lg";
  variant?: "ivory" | "navy" | "gold" | "dark";
  darkVariant?: boolean;
  onClick?: () => void;
}

export function GlassCard({
  children,
  className = "",
  glow = "none",
  hoverEffect = false,
  padding = "md",
  variant = "ivory",
  darkVariant = false,
  onClick,
}: GlassCardProps) {
  const paddingClasses = {
    none: "",
    sm: "p-4",
    md: "p-6",
    lg: "p-8",
  };

  const glowClasses = {
    none: "",
    gold: "border-[#D6A84B] shadow-lg shadow-[#D6A84B]/15",
    violet: "border-[#7355D9] shadow-lg shadow-[#7355D9]/15",
    navy: "border-[#17233F] shadow-lg shadow-[#17233F]/20",
    sage: "border-[#27856B]/40 shadow-lg shadow-[#27856B]/10",
    blue: "border-[#3478F6]/40 shadow-lg shadow-[#3478F6]/10",
    subtle: "border-[#E6DFD1] shadow-sm",
  };

  const activeVariant = darkVariant ? "navy" : variant;

  let baseClass = "";
  if (activeVariant === "navy" || activeVariant === "dark") {
    baseClass = hoverEffect
      ? "glass-card-navy rounded-3xl cursor-pointer hover:border-[#D6A84B]/60 transition-all"
      : "glass-card-navy rounded-3xl";
  } else if (activeVariant === "gold") {
    baseClass = hoverEffect
      ? "glass-card-gold rounded-3xl cursor-pointer hover:scale-[1.01] transition-all"
      : "glass-card-gold rounded-3xl";
  } else {
    // Ivory / Cream default
    baseClass = hoverEffect
      ? "glass-card-ivory-interactive rounded-3xl cursor-pointer"
      : "glass-card-ivory rounded-3xl";
  }

  return (
    <div
      onClick={onClick}
      className={`${baseClass} ${paddingClasses[padding]} ${glowClasses[glow]} ${className}`}
    >
      {children}
    </div>
  );
}
