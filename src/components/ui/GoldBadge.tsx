import React from "react";

interface BadgeProps {
  children: React.ReactNode;
  variant?: "gold" | "violet" | "navy" | "sage" | "terracotta";
  size?: "sm" | "md";
  className?: string;
  icon?: React.ReactNode;
}

export function GoldBadge({
  children,
  variant = "gold",
  size = "md",
  className = "",
  icon,
}: BadgeProps) {
  const sizeClasses = {
    sm: "px-2 py-0.5 text-[10px]",
    md: "px-3 py-1 text-xs",
  };

  const variantClasses = {
    gold: "bg-[#D6A84B]/15 text-[#9A7320] border border-[#D6A84B]/40",
    violet: "bg-[#7355D9]/15 text-[#5838BF] border border-[#7355D9]/35",
    navy: "bg-[#17233F]/10 text-[#17233F] border border-[#17233F]/20",
    sage: "bg-[#27856B]/15 text-[#1D634F] border border-[#27856B]/30",
    terracotta: "bg-[#C77B54]/15 text-[#9E5632] border border-[#C77B54]/30",
  };

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full font-bold uppercase tracking-wider ${
        sizeClasses[size]
      } ${variantClasses[variant]} ${className}`}
    >
      {icon && <span className="shrink-0">{icon}</span>}
      <span>{children}</span>
    </span>
  );
}

export function SkillBadge({
  name,
  category,
  confidence,
}: {
  name: string;
  category?: string;
  confidence?: number;
}) {
  return (
    <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white border border-[#E6DFD1] shadow-xs text-xs">
      <span className="font-bold text-[#17233F]">{name}</span>
      {category && (
        <span className="text-[10px] text-[#687187] bg-[#F5F0E6] px-2 py-0.5 rounded-md font-medium">
          {category}
        </span>
      )}
      {typeof confidence === "number" && (
        <span className="text-[10px] font-black text-[#27856B] bg-[#27856B]/10 px-1.5 py-0.5 rounded-md">
          {confidence}%
        </span>
      )}
    </div>
  );
}

