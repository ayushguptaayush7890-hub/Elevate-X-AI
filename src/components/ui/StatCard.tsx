import React from "react";
import { GlassCard } from "./GlassCard";

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: React.ReactNode;
  trend?: {
    value: string;
    isPositive?: boolean;
  };
  glow?: "gold" | "violet" | "navy" | "sage" | "blue" | "subtle" | "none";
  className?: string;
}

export function StatCard({
  title,
  value,
  subtitle,
  icon,
  trend,
  glow = "subtle",
  className = "",
}: StatCardProps) {
  return (
    <GlassCard glow={glow} padding="md" className={`relative overflow-hidden ${className}`}>
      <div className="flex items-start justify-between">
        <div className="space-y-1">
          <p className="text-[11px] font-extrabold text-[#687187] tracking-wider uppercase">{title}</p>
          <div className="text-2xl sm:text-3xl font-black text-[#17233F] tracking-tight">{value}</div>
          {subtitle && <p className="text-xs text-[#687187] mt-0.5">{subtitle}</p>}
        </div>

        {icon && (
          <div className="p-3 rounded-2xl bg-[#D6A84B]/10 border border-[#D6A84B]/25 text-[#D6A84B] shadow-xs">
            {icon}
          </div>
        )}
      </div>

      {trend && (
        <div className="mt-3 pt-3 border-t border-[#E6DFD1] flex items-center gap-1.5 text-xs">
          <span
            className={`font-bold flex items-center gap-0.5 ${
              trend.isPositive ? "text-[#27856B]" : "text-[#C77B54]"
            }`}
          >
            {trend.isPositive ? "↑" : "↓"} {trend.value}
          </span>
          <span className="text-[#8E97AB]">vs benchmark</span>
        </div>
      )}
    </GlassCard>
  );
}
