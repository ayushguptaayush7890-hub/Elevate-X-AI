"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Logo } from "@/components/ui/Logo";
import { useLanguage } from "@/context/LanguageContext";
import { useAuth } from "@/context/AuthContext";
import { Menu, X, Globe, Sparkles, LayoutDashboard, ArrowRight } from "lucide-react";

export function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { language, setLanguage, t } = useLanguage();
  const { isAuthenticated, user } = useAuth();
  const pathname = usePathname();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const navLinks = [
    { label: "Home", href: "/" },
    { label: "How It Works", href: "/#how-it-works" },
    { label: "Features", href: "/#features" },
    { label: "Career Opportunities", href: "/jobs" },
    { label: "About Us", href: "/about" },
  ];

  const toggleLanguage = () => {
    setLanguage(language === "English" ? "Hindi" : "English");
  };

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled
          ? "bg-[#10192D]/92 backdrop-blur-2xl border-b border-[#D6A84B]/20 shadow-2xl py-3"
          : "bg-transparent py-4 sm:py-5"
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between">
        {/* Left: Brand Logo */}
        <Logo size="md" lightText={true} />

        {/* Center: Desktop Navigation Bar with pill design */}
        <nav className="hidden md:flex items-center gap-1 px-4 py-1.5 rounded-full bg-[#17233F]/80 backdrop-blur-xl border border-[#D6A84B]/25 shadow-lg">
          {navLinks.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.label}
                href={link.href}
                className={`px-4 py-1.5 text-xs font-semibold rounded-full transition-all duration-200 ${
                  isActive
                    ? "bg-gradient-to-r from-[#D6A84B] to-[#F0D99B] text-[#10192D] font-bold shadow-sm"
                    : "text-[#E6DFD1] hover:text-[#F0D99B] hover:bg-white/5"
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>

        {/* Right: Actions */}
        <div className="hidden md:flex items-center gap-3">
          {/* Language Switcher */}
          <button
            onClick={toggleLanguage}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold text-[#E6DFD1] hover:text-[#F0D99B] bg-[#17233F]/60 hover:bg-[#17233F] border border-[#D6A84B]/25 transition-all shadow-sm"
            title="Switch Language (English / Hindi)"
          >
            <Globe className="w-3.5 h-3.5 text-[#36D6E8]" />
            <span>{language === "English" ? "हिन्दी" : "EN"}</span>
          </button>

          {isAuthenticated ? (
            <Link
              href="/dashboard"
              className="btn-gold inline-flex items-center gap-2 px-5 py-2 rounded-xl text-xs font-bold shadow-lg"
            >
              <LayoutDashboard className="w-3.5 h-3.5" />
              <span>{user?.role === "admin" ? "Admin Portal" : "My Dashboard"}</span>
            </Link>
          ) : (
            <>
              <Link
                href="/login"
                className="px-4 py-2 text-xs font-bold text-[#E6DFD1] hover:text-[#F0D99B] transition-colors"
              >
                Sign In
              </Link>
              <Link
                href="/onboarding"
                className="btn-gold inline-flex items-center gap-2 px-5 py-2 rounded-xl text-xs font-bold shadow-lg"
              >
                <Sparkles className="w-3.5 h-3.5" />
                <span>Get Started</span>
              </Link>
            </>
          )}
        </div>

        {/* Mobile Hamburger Button */}
        <div className="flex md:hidden items-center gap-2">
          <button
            onClick={toggleLanguage}
            className="p-2 rounded-xl bg-[#17233F] border border-[#D6A84B]/25 text-[#E6DFD1]"
          >
            <Globe className="w-4 h-4 text-[#36D6E8]" />
          </button>
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 rounded-xl bg-[#17233F] border border-[#D6A84B]/25 text-white"
            aria-label="Toggle Menu"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Dropdown Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-[#10192D] border-b border-[#D6A84B]/25 px-4 pt-4 pb-6 space-y-3">
          <nav className="flex flex-col space-y-2">
            {navLinks.map((link) => (
              <Link
                key={link.label}
                href={link.href}
                onClick={() => setMobileMenuOpen(false)}
                className="px-3 py-2 text-sm font-semibold text-[#E6DFD1] hover:text-[#F0D99B] hover:bg-white/5 rounded-xl"
              >
                {link.label}
              </Link>
            ))}
          </nav>

          <div className="pt-3 border-t border-white/10 flex flex-col gap-2">
            {isAuthenticated ? (
              <Link
                href="/dashboard"
                onClick={() => setMobileMenuOpen(false)}
                className="btn-gold text-center py-2.5 rounded-xl text-xs font-bold"
              >
                My Dashboard
              </Link>
            ) : (
              <>
                <Link
                  href="/login"
                  onClick={() => setMobileMenuOpen(false)}
                  className="px-4 py-2 text-center text-xs font-bold text-[#E6DFD1] bg-[#17233F] rounded-xl"
                >
                  Sign In
                </Link>
                <Link
                  href="/onboarding"
                  onClick={() => setMobileMenuOpen(false)}
                  className="btn-gold text-center py-2.5 rounded-xl text-xs font-bold"
                >
                  Get Started
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  );
}
