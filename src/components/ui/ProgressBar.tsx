import React from "react";

interface ProgressBarProps {
  value: number; // 0 to 100
  label?: string;
  showValue?: boolean;
  size?: "sm" | "md" | "lg";
  variant?: "purple" | "gradient" | "emerald" | "amber" | "gold" | "violet" | "sage" | "navy";
  color?: "purple" | "gradient" | "emerald" | "amber" | "gold" | "violet" | "sage" | "navy";
  className?: string;
}

export function ProgressBar({
  value,
  label,
  showValue = true,
  size = "md",
  variant = "gold",
  color,
  className = "",
}: ProgressBarProps) {
  const clampedValue = Math.min(100, Math.max(0, value));

  const effectiveVariant = color || variant;

  const sizeClasses = {
    sm: "h-2",
    md: "h-2.5",
    lg: "h-4",
  };

  const variantClasses = {
    gold: "bg-gradient-to-r from-[#D6A84B] to-[#F0D99B]",
    violet: "bg-gradient-to-r from-[#7355D9] to-[#9171F8]",
    sage: "bg-gradient-to-r from-[#27856B] to-[#3AB091]",
    navy: "bg-[#17233F]",
    purple: "bg-[#7355D9]",
    gradient: "bg-gradient-to-r from-[#17233F] via-[#7355D9] to-[#D6A84B]",
    emerald: "bg-gradient-to-r from-[#27856B] to-[#3AB091]",
    amber: "bg-gradient-to-r from-[#D6A84B] to-[#C77B54]",
  };

  return (
    <div className={`w-full ${className}`}>
      {(label || showValue) && (
        <div className="flex justify-between items-center text-xs mb-1.5 font-bold">
          {label && <span className="text-[#20243A]">{label}</span>}
          {showValue && <span className="text-[#17233F] font-mono">{clampedValue}%</span>}
        </div>
      )}
      <div className={`w-full bg-[#E6DFD1]/60 rounded-full overflow-hidden border border-[#E6DFD1] ${sizeClasses[size]}`}>
        <div
          className={`h-full rounded-full transition-all duration-500 ease-out shadow-xs ${variantClasses[effectiveVariant]}`}
          style={{ width: `${clampedValue}%` }}
        />
      </div>
    </div>
  );
}

export function CircularProgress({
  value,
  size = 80,
  strokeWidth = 7,
  label,
  subtitle,
}: {
  value: number;
  size?: number;
  strokeWidth?: number;
  label?: string;
  subtitle?: string;
}) {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const clampedValue = Math.min(100, Math.max(0, value));
  const strokeDashoffset = circumference - (clampedValue / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="-rotate-90">
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#E6DFD1"
            strokeWidth={strokeWidth}
            fill="none"
          />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#D6A84B"
            strokeWidth={strokeWidth}
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-700 ease-out"
          />
        </svg>
        <span className="absolute font-extrabold text-sm text-[#17233F] font-mono">
          {clampedValue}%
        </span>
      </div>
      {label && <span className="text-xs font-bold text-[#17233F] mt-2">{label}</span>}
      {subtitle && <span className="text-[10px] text-[#687187]">{subtitle}</span>}
    </div>
  );
}
