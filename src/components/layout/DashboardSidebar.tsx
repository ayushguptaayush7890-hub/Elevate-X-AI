"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Logo } from "@/components/ui/Logo";
import { useAuth } from "@/context/AuthContext";
import {
  LayoutDashboard,
  User,
  Sparkles,
  Award,
  Briefcase,
  GitCompare,
  FileText,
  MapPin,
  TrendingUp,
  Mic,
  MessageSquare,
  BarChart3,
  Kanban,
  Settings,
  Shield,
  LogOut,
  ChevronRight
} from "lucide-react";

interface NavItem {
  label: string;
  href: string;
  icon: React.ReactNode;
  badge?: string;
  isAi?: boolean;
}

export function DashboardSidebar({
  mobileOpen = false,
  setMobileOpen,
  isLocked = false,
  onLockedNavigation,
}: {
  mobileOpen?: boolean;
  setMobileOpen?: (open: boolean) => void;
  isLocked?: boolean;
  onLockedNavigation?: () => void;
}) {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  // Group 1: Core Navigation
  const coreNav: NavItem[] = [
    {
      label: "Overview",
      href: "/dashboard",
      icon: <LayoutDashboard className="w-4 h-4" />,
    },
    {
      label: "My Profile",
      href: "/profile",
      icon: <User className="w-4 h-4" />,
    },
  ];

  // Group 2: AI Intelligence & Recognition
  const aiModules: NavItem[] = [
    {
      label: "Experience Recognition",
      href: "/experience",
      icon: <Sparkles className="w-4 h-4 text-[#7355D9]" />,
      badge: "AI Core",
      isAi: true,
    },
    {
      label: "Skill Assessment",
      href: "/assessment",
      icon: <Award className="w-4 h-4 text-[#3478F6]" />,
      badge: "Adaptive",
    },
    {
      label: "Find Jobs",
      href: "/jobs",
      icon: <Briefcase className="w-4 h-4 text-[#D6A84B]" />,
    },
    {
      label: "Skill Gap Analyzer",
      href: "/skill-gap",
      icon: <GitCompare className="w-4 h-4 text-[#C77B54]" />,
    },
    {
      label: "AI Resume Builder",
      href: "/resume",
      icon: <FileText className="w-4 h-4 text-[#7355D9]" />,
      badge: "ATS Studio",
      isAi: true,
    },
  ];

  // Group 3: Career Pathways & Coaching
  const careerTools: NavItem[] = [
    {
      label: "Career Roadmap",
      href: "/roadmap",
      icon: <MapPin className="w-4 h-4 text-[#D6A84B]" />,
    },
    {
      label: "Career Transition",
      href: "/career-transition",
      icon: <TrendingUp className="w-4 h-4 text-[#27856B]" />,
    },
    {
      label: "AI Interview Lab",
      href: "/interview",
      icon: <Mic className="w-4 h-4 text-[#7355D9]" />,
      badge: "Voice",
      isAi: true,
    },
    {
      label: "AI Assistant",
      href: "/assistant",
      icon: <MessageSquare className="w-4 h-4 text-[#36D6E8]" />,
      badge: "Bilingual",
      isAi: true,
    },
  ];

  // Group 4: Tracking & Workspace
  const trackingNav: NavItem[] = [
    {
      label: "Progress Tracker",
      href: "/progress",
      icon: <BarChart3 className="w-4 h-4" />,
    },
    {
      label: "Applications",
      href: "/applications",
      icon: <Kanban className="w-4 h-4" />,
    },
    {
      label: "Settings",
      href: "/settings",
      icon: <Settings className="w-4 h-4" />,
    },
  ];

  const renderNavGroup = (title: string, items: NavItem[]) => (
    <div className="space-y-1">
      <div className="px-3 py-1.5 text-[10px] font-black uppercase tracking-widest text-[#D6A84B]/70">
        {title}
      </div>
      {items.map((item) => {
        const isActive = pathname === item.href;
        return (
          <Link
            key={item.href}
            href={item.href}
            onClick={(e) => {
              if (isLocked) {
                e.preventDefault();
                onLockedNavigation?.();
                return;
              }
              if (setMobileOpen) setMobileOpen(false);
            }}
            className={`group flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold transition-all duration-200 ${
              isActive
                ? "bg-gradient-to-r from-[#D6A84B] to-[#F0D99B] text-[#10192D] font-bold shadow-md shadow-[#D6A84B]/20"
                : isLocked 
                ? "text-white/40 cursor-not-allowed hover:text-white/60"
                : "text-white/80 hover:text-white hover:bg-white/10"
            }`}
          >
            <div className="flex items-center gap-2.5">
              <span
                className={`transition-transform duration-200 group-hover:scale-110 ${
                  isActive ? "text-[#10192D]" : ""
                }`}
              >
                {item.icon}
              </span>
              <span className="truncate">{item.label}</span>
            </div>

            {item.badge && (
              <span
                className={`text-[9px] font-extrabold uppercase px-1.5 py-0.5 rounded tracking-wider ${
                  isActive
                    ? "bg-[#10192D]/20 text-[#10192D]"
                    : item.isAi
                    ? "bg-[#7355D9]/25 text-[#D6A84B] border border-[#7355D9]/40"
                    : "bg-white/10 text-[#E6DFD1]"
                }`}
              >
                {item.badge}
              </span>
            )}
          </Link>
        );
      })}
    </div>
  );

  return (
    <>
      {mobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-[#10192D]/70 backdrop-blur-sm lg:hidden"
          onClick={() => setMobileOpen && setMobileOpen(false)}
        />
      )}

      <aside
        className={`fixed top-0 bottom-0 left-0 z-50 w-64 bg-[#17233F] border-r border-[#D6A84B]/20 flex flex-col transition-transform duration-300 lg:translate-x-0 shadow-2xl ${
          mobileOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        {/* Brand Header */}
        <div className="h-16 px-5 border-b border-[#D6A84B]/20 flex items-center justify-between shrink-0 bg-[#10192D]">
          <div 
            onClick={(e) => {
              if (isLocked) {
                e.preventDefault();
                e.stopPropagation();
                onLockedNavigation?.();
              }
            }}
          >
            <Logo size="sm" lightText={true} />
          </div>
          {isLocked && (
            <span className="text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded bg-amber-500/20 text-[#F0D99B] border border-amber-500/30">
              🔒 Locked
            </span>
          )}
        </div>

        {/* Scrollable Navigation Groups */}
        <div className="flex-1 overflow-y-auto px-3 py-4 space-y-5">
          {renderNavGroup("Core", coreNav)}
          {renderNavGroup("AI Modules", aiModules)}
          {renderNavGroup("Career Development", careerTools)}
          {renderNavGroup("Management", trackingNav)}

          {/* Admin Switcher Shortcut */}
          <div className="pt-2">
            <Link
              href="/admin"
              className="flex items-center justify-between p-2.5 rounded-xl bg-[#10192D] border border-[#D6A84B]/25 hover:border-[#D6A84B] text-xs font-bold text-[#F0D99B] transition-all group"
            >
              <div className="flex items-center gap-2">
                <Shield className="w-3.5 h-3.5 text-[#D6A84B]" />
                <span>Admin & Prompt Lab</span>
              </div>
              <ChevronRight className="w-3.5 h-3.5 text-[#D6A84B] group-hover:translate-x-0.5 transition-transform" />
            </Link>
          </div>
        </div>

        {/* User Profile Footer */}
        <div className="p-3 border-t border-[#D6A84B]/20 bg-[#10192D] shrink-0">
          <div className="flex items-center justify-between p-2 rounded-xl bg-[#17233F] border border-[#D6A84B]/15">
            <Link href="/profile" className="flex items-center gap-2.5 min-w-0">
              <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-[#D6A84B] to-[#7355D9] flex items-center justify-center text-xs font-black text-[#10192D] shrink-0 shadow-xs">
                {user.fullName.charAt(0)}
              </div>
              <div className="min-w-0 text-left">
                <p className="text-xs font-bold text-white truncate">{user.fullName}</p>
                <p className="text-[10px] text-[#D6A84B] truncate font-medium">{user.currentOccupation}</p>
              </div>
            </Link>
            <button
              onClick={logout}
              className="p-1.5 hover:bg-white/10 rounded-lg text-slate-400 hover:text-rose-400 transition-colors"
              title="Sign Out"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </aside>
    </>
  );
}
