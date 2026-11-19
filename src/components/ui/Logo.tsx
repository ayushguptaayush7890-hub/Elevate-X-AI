import React from "react";
import Link from "next/link";

interface LogoProps {
  className?: string;
  size?: "sm" | "md" | "lg";
  showText?: boolean;
  lightText?: boolean;
}

export function Logo({
  className = "",
  size = "md",
  showText = true,
  lightText = false,
}: LogoProps) {
  const iconDimensions = {
    sm: "w-7 h-7",
    md: "w-9 h-9",
    lg: "w-12 h-12",
  };

  const textSizes = {
    sm: "text-base",
    md: "text-lg",
    lg: "text-2xl",
  };

  return (
    <Link href="/" className={`inline-flex items-center gap-2.5 group cursor-pointer ${className}`}>
      {/* Royal Gold 3D Gradient Icon Badge */}
      <div
        className={`relative flex items-center justify-center rounded-2xl bg-gradient-to-br from-[#17233F] via-[#7355D9] to-[#D6A84B] p-0.5 shadow-md shadow-[#D6A84B]/20 group-hover:shadow-[#D6A84B]/40 transition-all duration-300 ${iconDimensions[size]}`}
      >
        <div className="w-full h-full bg-[#10192D] rounded-[14px] flex items-center justify-center overflow-hidden">
          <svg
            viewBox="0 0 32 32"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className="w-5/6 h-5/6 transform group-hover:scale-105 transition-transform duration-300"
          >
            <defs>
              <linearGradient id="elevateRoyalGrad" x1="0%" y1="100%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#D6A84B" />
                <stop offset="50%" stopColor="#7355D9" />
                <stop offset="100%" stopColor="#36D6E8" />
              </linearGradient>
            </defs>
            {/* Neural network nodes & connections */}
            <circle cx="8" cy="24" r="2.5" fill="#D6A84B" />
            <circle cx="24" cy="24" r="2.5" fill="#7355D9" />
            <circle cx="16" cy="15" r="2.5" fill="#36D6E8" />
            <circle cx="16" cy="5" r="2" fill="#D6A84B" />

            <line x1="8" y1="24" x2="16" y2="15" stroke="rgba(214, 168, 75, 0.5)" strokeWidth="1.5" />
            <line x1="24" y1="24" x2="16" y2="15" stroke="rgba(115, 85, 217, 0.5)" strokeWidth="1.5" />
            <line x1="16" y1="15" x2="16" y2="7" stroke="rgba(54, 214, 232, 0.8)" strokeWidth="1.5" strokeDasharray="2 2" />

            {/* Upward Chevron / Career Arrow */}
            <path
              d="M10 16L16 9L22 16"
              stroke="url(#elevateRoyalGrad)"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M16 9V27"
              stroke="url(#elevateRoyalGrad)"
              strokeWidth="2.5"
              strokeLinecap="round"
            />
          </svg>
        </div>
      </div>

      {showText && (
        <div className="flex flex-col">
          <div className="flex items-center tracking-wider font-black">
            <span
              className={`font-black tracking-tight ${textSizes[size]} ${
                lightText ? "text-white" : "text-[#17233F]"
              }`}
            >
              ELEVATE
            </span>
            <span
              className={`bg-gradient-to-r from-[#D6A84B] to-[#F0D99B] bg-clip-text text-transparent ml-1 font-black ${textSizes[size]}`}
            >
              X
            </span>
            <span className="text-[10px] font-black px-1.5 py-0.5 rounded ml-1.5 bg-[#D6A84B]/15 text-[#D6A84B] border border-[#D6A84B]/35">
              AI
            </span>
          </div>
          <span
            className={`text-[9px] uppercase tracking-widest font-bold -mt-0.5 ${
              lightText ? "text-slate-400" : "text-[#687187]"
            }`}
          >
            Career Ecosystem
          </span>
        </div>
      )}
    </Link>
  );
}
