import React from "react";
import Link from "next/link";

interface GradientButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "cyan";
  size?: "sm" | "md" | "lg";
  href?: string;
  icon?: React.ReactNode;
  children: React.ReactNode;
  fullWidth?: boolean;
}

export function GradientButton({
  variant = "primary",
  size = "md",
  href,
  icon,
  children,
  className = "",
  fullWidth = false,
  ...props
}: GradientButtonProps) {
  const sizeClasses = {
    sm: "px-4 py-2 text-xs rounded-xl gap-1.5",
    md: "px-5 py-2.5 text-xs sm:text-sm rounded-xl font-bold gap-2",
    lg: "px-7 py-3.5 text-sm sm:text-base rounded-2xl font-black gap-2.5",
  };

  const variantClasses = {
    primary:
      "bg-gradient-to-r from-[#6938EF] via-[#3478F6] to-[#36D6E8] hover:from-[#5928DF] hover:to-[#26C6D8] text-white shadow-lg shadow-purple-500/25 hover:shadow-purple-500/40 border border-white/20",
    secondary:
      "bg-white hover:bg-purple-50/80 text-[#17152B] hover:text-[#6938EF] border border-purple-200 shadow-sm hover:shadow-md",
    outline:
      "bg-transparent hover:bg-purple-50 text-[#17152B] border border-purple-200 hover:border-[#6938EF]",
    ghost:
      "bg-transparent hover:bg-purple-50 text-slate-700 hover:text-[#6938EF]",
    cyan:
      "bg-gradient-to-r from-[#36D6E8] to-[#3478F6] text-white shadow-md shadow-cyan-500/20 border border-white/20",
  };

  const baseClasses = `inline-flex items-center justify-center font-bold transition-all duration-200 active:scale-[0.98] disabled:opacity-50 disabled:pointer-events-none cursor-pointer ${sizeClasses[size]} ${variantClasses[variant]} ${fullWidth ? "w-full" : ""} ${className}`;

  if (href) {
    return (
      <Link href={href} className={baseClasses}>
        {icon && <span className="shrink-0">{icon}</span>}
        {children}
      </Link>
    );
  }

  return (
    <button className={baseClasses} {...props}>
      {icon && <span className="shrink-0">{icon}</span>}
      {children}
    </button>
  );
}
