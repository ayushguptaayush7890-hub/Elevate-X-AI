"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Logo } from "@/components/ui/Logo";
import { useAuth } from "@/context/AuthContext";
import {
  LayoutDashboard,
  Users,
  Briefcase,
  Layers,
  BookOpen,
  Terminal,
  Activity,
  ArrowLeft,
  ShieldCheck,
} from "lucide-react";

export function AdminSidebar({
  mobileOpen = false,
  setMobileOpen,
}: {
  mobileOpen?: boolean;
  setMobileOpen?: (open: boolean) => void;
}) {
  const pathname = usePathname();
  const { switchRole } = useAuth();

  const adminNav = [
    { label: "Admin Overview", href: "/admin", icon: <LayoutDashboard className="w-4 h-4" /> },
    { label: "User Management", href: "/admin/users", icon: <Users className="w-4 h-4" /> },
    { label: "Job Directory", href: "/admin/jobs", icon: <Briefcase className="w-4 h-4" /> },
    { label: "Skill Taxonomy", href: "/admin/skills", icon: <Layers className="w-4 h-4" /> },
    { label: "Learning Resources", href: "/admin/resources", icon: <BookOpen className="w-4 h-4" /> },
    {
      label: "Prompt Engineering Lab",
      href: "/admin/prompts",
      icon: <Terminal className="w-4 h-4 text-[#7355D9]" />,
      badge: "AI Lab",
    },
    { label: "Telemetry & Analytics", href: "/admin/analytics", icon: <Activity className="w-4 h-4" /> },
  ];

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
        <div className="h-16 px-5 border-b border-[#D6A84B]/20 flex items-center justify-between shrink-0 bg-[#10192D]">
          <Logo size="sm" lightText={true} />
        </div>

        <div className="px-4 py-3 bg-[#10192D] border-b border-[#D6A84B]/15 flex items-center gap-2 text-xs text-[#D6A84B] font-bold">
          <ShieldCheck className="w-4 h-4 text-[#D6A84B] shrink-0" />
          <span>Superadmin Security Layer</span>
        </div>

        <div className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
          {adminNav.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setMobileOpen && setMobileOpen(false)}
                className={`flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                  isActive
                    ? "bg-gradient-to-r from-[#D6A84B] to-[#F0D99B] text-[#10192D] font-bold shadow-md shadow-[#D6A84B]/20"
                    : "text-white/80 hover:text-white hover:bg-white/10"
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <span className={isActive ? "text-[#10192D]" : "text-[#D6A84B]"}>
                    {item.icon}
                  </span>
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className="text-[9px] font-black uppercase px-1.5 py-0.5 rounded bg-[#7355D9]/30 text-[#F0D99B] border border-[#7355D9]/40">
                    {item.badge}
                  </span>
                )}
              </Link>
            );
          })}
        </div>

        {/* Back to User Dashboard */}
        <div className="p-3 border-t border-[#D6A84B]/20 bg-[#10192D] shrink-0">
          <Link
            href="/dashboard"
            onClick={() => switchRole("user")}
            className="w-full flex items-center justify-center gap-2 p-2.5 rounded-xl bg-[#17233F] hover:bg-[#1f2f54] text-xs font-bold text-[#E6DFD1] hover:text-[#F0D99B] border border-[#D6A84B]/20 transition-all shadow-xs"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Return to User Dashboard</span>
          </Link>
        </div>
      </aside>
    </>
  );
}
