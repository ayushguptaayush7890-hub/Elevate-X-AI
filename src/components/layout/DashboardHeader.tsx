"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { useLanguage } from "@/context/LanguageContext";
import {
  Menu,
  Search,
  Bell,
  Globe,
  User,
  Settings,
  Shield,
  LogOut,
  Sparkles,
  CheckCircle2,
  X
} from "lucide-react";

export function DashboardHeader({
  onMenuToggle,
  isLocked = false,
  onLockedNavigation,
}: {
  onMenuToggle?: () => void;
  isLocked?: boolean;
  onLockedNavigation?: () => void;
}) {
  const { user, role, switchRole, logout } = useAuth();
  const { language, setLanguage } = useLanguage();
  const router = useRouter();

  const [searchQuery, setSearchQuery] = useState("");
  const [showNotifications, setShowNotifications] = useState(false);
  const [showProfileMenu, setShowProfileMenu] = useState(false);

  const notifications = [
    {
      id: "n-1",
      title: "New Vocational Opportunity Match",
      desc: "Your hands-on skills match candidate criteria for 2 verified openings.",
      time: "25m ago",
      read: false,
    },
    {
      id: "n-2",
      title: "Assessment Diagnostic Completed",
      desc: "Tactile machine operation assessment recorded on your profile.",
      time: "2h ago",
      read: false,
    },
    {
      id: "n-3",
      title: "Roadmap Milestone Ready",
      desc: "Stage 2 quality sampling simulation exercise is ready to review.",
      time: "Yesterday",
      read: true,
    },
  ];

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    router.push(`/jobs?q=${encodeURIComponent(searchQuery)}`);
  };

  return (
    <header className="h-16 bg-[#FBF8F1]/90 backdrop-blur-xl border-b border-[#E6DFD1] px-4 sm:px-6 flex items-center justify-between sticky top-0 z-30 shadow-xs">
      {/* Left: Mobile Toggle & Global Search */}
      <div className="flex items-center gap-3 flex-1 max-w-lg">
        <button
          onClick={onMenuToggle}
          className="p-2 rounded-xl bg-white border border-[#E6DFD1] text-[#17233F] lg:hidden hover:text-[#D6A84B] shadow-xs"
          aria-label="Toggle Navigation Drawer"
        >
          <Menu className="w-5 h-5" />
        </button>

        <form onSubmit={handleSearchSubmit} className="relative w-full hidden sm:block">
          <Search className="w-4 h-4 text-[#8E97AB] absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search verified skills, jobs, roadmaps, or interview topics..."
            className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl pl-10 pr-4 py-2 text-xs text-[#20243A] placeholder:text-[#8E97AB] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all shadow-inner"
          />
        </form>
      </div>

      {/* Right: Actions, Language, Notifications, Profile */}
      <div className="flex items-center gap-2.5 sm:gap-4">
        {/* Language Switcher */}
        <button
          onClick={() => setLanguage(language === "English" ? "Hindi" : "English")}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white hover:bg-[#F5F0E6] border border-[#E6DFD1] text-xs font-bold text-[#17233F] hover:text-[#D6A84B] transition-colors shadow-xs"
          title="Switch Language (English / Hindi)"
        >
          <Globe className="w-3.5 h-3.5 text-[#3478F6]" />
          <span className="hidden sm:inline">{language === "English" ? "हिन्दी" : "EN"}</span>
        </button>

        {/* Notifications Popover */}
        <div className="relative">
          <button
            onClick={() => {
              setShowNotifications(!showNotifications);
              setShowProfileMenu(false);
            }}
            className="p-2 rounded-xl bg-white hover:bg-[#F5F0E6] border border-[#E6DFD1] text-[#17233F] hover:text-[#D6A84B] transition-colors relative shadow-xs"
            title="Notifications"
          >
            <Bell className="w-4 h-4" />
            <span className="w-2 h-2 rounded-full bg-[#D6A84B] absolute top-1.5 right-1.5" />
          </button>

          {showNotifications && (
            <div className="absolute right-0 mt-2 w-80 sm:w-96 bg-white rounded-2xl shadow-2xl border border-[#E6DFD1] py-3 z-50">
              <div className="px-4 pb-2 border-b border-[#E6DFD1] flex items-center justify-between">
                <span className="text-xs font-black text-[#17233F]">Notifications</span>
                <span className="text-[10px] font-bold text-[#D6A84B] bg-[#D6A84B]/15 px-2 py-0.5 rounded-full">
                  2 New
                </span>
              </div>
              <div className="divide-y divide-[#E6DFD1] max-h-72 overflow-y-auto">
                {notifications.map((n) => (
                  <div
                    key={n.id}
                    className={`p-3 text-xs space-y-1 hover:bg-[#FBF8F1] transition-colors ${
                      !n.read ? "bg-[#F5F0E6]/50" : ""
                    }`}
                  >
                    <p className="font-bold text-[#20243A]">{n.title}</p>
                    <p className="text-[11px] text-[#687187] leading-relaxed">{n.desc}</p>
                    <p className="text-[9px] text-[#8E97AB] font-mono">{n.time}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* User Profile Menu */}
        <div className="relative">
          <button
            onClick={() => {
              setShowProfileMenu(!showProfileMenu);
              setShowNotifications(false);
            }}
            className="flex items-center gap-2 p-1.5 rounded-xl bg-white hover:bg-[#F5F0E6] border border-[#E6DFD1] transition-colors shadow-xs"
          >
            <div className="w-7 h-7 rounded-lg bg-gradient-to-tr from-[#D6A84B] to-[#7355D9] flex items-center justify-center text-xs font-black text-[#10192D]">
              {user.fullName.charAt(0)}
            </div>
            <span className="text-xs font-bold text-[#17233F] hidden md:inline max-w-[100px] truncate">
              {user.fullName}
            </span>
          </button>

          {showProfileMenu && (
            <div className="absolute right-0 mt-2 w-56 bg-white rounded-2xl shadow-2xl border border-[#E6DFD1] py-2 z-50 text-xs">
              <div className="px-4 py-2 border-b border-[#E6DFD1]">
                <p className="font-bold text-[#17233F] truncate">{user.fullName}</p>
                <p className="text-[10px] text-[#687187] truncate">{user.email}</p>
              </div>

              <div className="p-1.5 space-y-0.5">
                <Link
                  href="/profile"
                  onClick={() => setShowProfileMenu(false)}
                  className="flex items-center gap-2 px-3 py-2 rounded-xl text-[#20243A] hover:bg-[#F5F0E6] hover:text-[#D6A84B] font-semibold transition-colors"
                >
                  <User className="w-3.5 h-3.5 text-[#D6A84B]" />
                  <span>My Profile</span>
                </Link>

                <Link
                  href="/settings"
                  onClick={() => setShowProfileMenu(false)}
                  className="flex items-center gap-2 px-3 py-2 rounded-xl text-[#20243A] hover:bg-[#F5F0E6] hover:text-[#D6A84B] font-semibold transition-colors"
                >
                  <Settings className="w-3.5 h-3.5" />
                  <span>Account Settings</span>
                </Link>

                <Link
                  href="/admin"
                  onClick={() => setShowProfileMenu(false)}
                  className="flex items-center gap-2 px-3 py-2 rounded-xl text-[#7355D9] hover:bg-[#7355D9]/10 font-bold transition-colors"
                >
                  <Shield className="w-3.5 h-3.5" />
                  <span>Admin Gateway</span>
                </Link>
              </div>

              <div className="pt-1.5 border-t border-[#E6DFD1] px-1.5">
                <button
                  onClick={() => {
                    setShowProfileMenu(false);
                    logout();
                  }}
                  className="w-full flex items-center gap-2 px-3 py-2 rounded-xl text-rose-600 hover:bg-rose-50 font-bold transition-colors"
                >
                  <LogOut className="w-3.5 h-3.5" />
                  <span>Sign Out</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
