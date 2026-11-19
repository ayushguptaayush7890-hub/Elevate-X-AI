import React from "react";
import Link from "next/link";

interface BrandButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "gold" | "violet" | "navy" | "ivory";
  size?: "sm" | "md" | "lg";
  href?: string;
  icon?: React.ReactNode;
  iconPosition?: "left" | "right";
  fullWidth?: boolean;
  children: React.ReactNode;
  className?: string;
}

export function BrandButton({
  variant = "gold",
  size = "md",
  href,
  icon,
  iconPosition = "left",
  fullWidth = false,
  children,
  className = "",
  disabled,
  ...props
}: BrandButtonProps) {
  const sizeClasses = {
    sm: "px-3.5 py-1.5 text-xs rounded-xl gap-1.5",
    md: "px-5 py-2.5 text-xs sm:text-sm rounded-xl gap-2",
    lg: "px-7 py-3.5 text-sm sm:text-base rounded-2xl gap-2.5",
  };

  const variantClasses = {
    gold: "btn-gold",
    violet: "btn-violet",
    navy: "btn-navy",
    ivory: "btn-ivory",
  };

  const baseStyle = `inline-flex items-center justify-center font-bold tracking-wide transition-all duration-200 select-none cursor-pointer ${
    sizeClasses[size]
  } ${variantClasses[variant]} ${fullWidth ? "w-full" : ""} ${
    disabled ? "opacity-50 cursor-not-allowed pointer-events-none" : ""
  } ${className}`;

  if (href) {
    return (
      <Link href={href} className={baseStyle}>
        {icon && iconPosition === "left" && <span>{icon}</span>}
        <span>{children}</span>
        {icon && iconPosition === "right" && <span>{icon}</span>}
      </Link>
    );
  }

  return (
    <button className={baseStyle} disabled={disabled} {...props}>
      {icon && iconPosition === "left" && <span>{icon}</span>}
      <span>{children}</span>
      {icon && iconPosition === "right" && <span>{icon}</span>}
    </button>
  );
}
