import React from "react";
import { GoldBadge } from "./GoldBadge";

interface PageHeaderProps {
  badge?: string;
  badgeVariant?: "gold" | "violet" | "sage" | "terracotta";
  title: string;
  description: string;
  actions?: React.ReactNode;
  variant?: "navy" | "gold" | "ivory";
}

export function PageHeader({
  badge,
  badgeVariant = "gold",
  title,
  description,
  actions,
  variant = "navy",
}: PageHeaderProps) {
  if (variant === "navy") {
    return (
      <div className="relative rounded-3xl p-6 sm:p-8 bg-gradient-to-r from-[#17233F] via-[#10192D] to-[#1F2F54] text-[#F5F0E6] overflow-hidden shadow-xl border border-[#D6A84B]/25">
        <div className="absolute right-0 top-0 bottom-0 w-1/3 bg-gradient-to-l from-[#D6A84B]/10 to-transparent pointer-events-none" />
        <div className="absolute -top-10 -right-10 w-48 h-48 bg-[#7355D9]/20 blur-3xl rounded-full pointer-events-none" />

        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            {badge && (
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#D6A84B]/20 backdrop-blur-md text-[#F0D99B] border border-[#D6A84B]/40 text-xs font-bold">
                {badge}
              </div>
            )}
            <h1 className="text-2xl sm:text-3xl font-black tracking-tight text-white">
              {title}
            </h1>
            <p className="text-xs sm:text-sm text-[#E6DFD1]/85 leading-relaxed">
              {description}
            </p>
          </div>

          {actions && <div className="flex flex-wrap items-center gap-3 shrink-0">{actions}</div>}
        </div>
      </div>
    );
  }

  // Ivory / Light Page Header
  return (
    <div className="rounded-3xl p-6 sm:p-8 bg-white border border-[#E6DFD1] shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div className="space-y-1.5 max-w-2xl">
        {badge && <GoldBadge variant={badgeVariant}>{badge}</GoldBadge>}
        <h1 className="text-2xl sm:text-3xl font-black text-[#17233F] tracking-tight">
          {title}
        </h1>
        <p className="text-xs sm:text-sm text-[#687187] leading-relaxed">
          {description}
        </p>
      </div>

      {actions && <div className="flex flex-wrap items-center gap-3 shrink-0">{actions}</div>}
    </div>
  );
}

