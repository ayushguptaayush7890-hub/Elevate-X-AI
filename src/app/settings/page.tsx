"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { BrandButton } from "@/components/ui/BrandButton";
import { PageHeader } from "@/components/ui/PageHeader";
import { useAuth } from "@/context/AuthContext";
import { useLanguage } from "@/context/LanguageContext";
import { toast } from "sonner";
import {
  Settings,
  Globe,
  Bell,
  Key,
  LogOut,
  Sparkles,
  ShieldCheck
} from "lucide-react";

export default function SettingsPage() {
  const { logout } = useAuth();
  const { language, setLanguage } = useLanguage();

  const [emailAlerts, setEmailAlerts] = useState(true);
  const [smsAlerts, setSmsAlerts] = useState(false);
  const [recruiterVisibility, setRecruiterVisibility] = useState(true);

  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");

  const handlePasswordUpdate = (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentPassword || !newPassword) {
      toast.error("Please fill in current and new password.");
      return;
    }
    toast.success("Security credentials updated successfully.");
    setCurrentPassword("");
    setNewPassword("");
  };

  const handleSavePreferences = () => {
    toast.success("Preferences updated successfully.");
  };

  return (
    <AppShell>
      <div className="space-y-6">
        <PageHeader
          badge="User Configuration"
          title="Account & Platform Settings"
          description="Manage your localization, verification privacy, alert channels, and security credentials."
          variant="navy"
          actions={
            <div className="flex items-center gap-2 text-xs text-[#F0D99B] bg-[#10192D] px-3.5 py-2 rounded-xl border border-[#D6A84B]/40">
              <ShieldCheck className="w-4 h-4 text-[#D6A84B]" />
              <span>Data Privacy Encrypted</span>
            </div>
          }
        />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Language & Interface */}
          <div className="p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-4">
            <h2 className="text-xs font-bold text-[#17233F] uppercase tracking-wider flex items-center gap-2">
              <Globe className="w-4 h-4 text-[#7355D9]" /> Language & Localization
            </h2>
            <p className="text-xs text-[#687187]">
              Select your primary language for dashboard navigation, AI assessments, and career assistant dialogues.
            </p>

            <div className="grid grid-cols-2 gap-3 pt-1 text-xs">
              <button
                type="button"
                onClick={() => {
                  setLanguage("English");
                  toast.success("Language set to English");
                }}
                className={`p-3.5 rounded-xl border text-center transition-all ${
                  language === "English"
                    ? "bg-[#17233F] text-[#F0D99B] border-[#D6A84B] font-bold shadow-sm"
                    : "bg-[#FBF8F1] border-[#E6DFD1] text-[#687187] hover:text-[#17233F]"
                }`}
              >
                English
              </button>
              <button
                type="button"
                onClick={() => {
                  setLanguage("Hindi");
                  toast.success("भाषा बदलकर हिन्दी कर दी गई है");
                }}
                className={`p-3.5 rounded-xl border text-center transition-all ${
                  language === "Hindi"
                    ? "bg-[#17233F] text-[#F0D99B] border-[#D6A84B] font-bold shadow-sm"
                    : "bg-[#FBF8F1] border-[#E6DFD1] text-[#687187] hover:text-[#17233F]"
                }`}
              >
                हिन्दी (Hindi)
              </button>
            </div>
          </div>

          {/* Theme Settings */}
          <div className="p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-4">
            <h2 className="text-xs font-bold text-[#17233F] uppercase tracking-wider flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-[#D6A84B]" /> Brand Design System
            </h2>
            <p className="text-xs text-[#687187]">
              Elevate X AI runs on the Royal Gold Edition: rich Royal Navy, Champagne Gold, Electric Violet, and Warm Ivory for maximal accessibility and clarity.
            </p>

            <div className="p-3.5 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1] flex items-center justify-between text-xs text-[#20243A]">
              <span>Active Design Theme:</span>
              <span className="font-bold text-[#17233F] px-2.5 py-1 rounded-full bg-[#F0D99B]/40 border border-[#D6A84B]">
                Royal Gold Edition
              </span>
            </div>
          </div>

          {/* Notifications & Recruiter Privacy */}
          <div className="p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-4">
            <h2 className="text-xs font-bold text-[#17233F] uppercase tracking-wider flex items-center gap-2">
              <Bell className="w-4 h-4 text-[#27856B]" /> Notification & Visibility Controls
            </h2>

            <div className="space-y-3 text-xs text-[#20243A]">
              <label className="flex items-center justify-between p-3.5 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1] cursor-pointer hover:border-[#D6A84B]/60 transition-colors">
                <span className="font-medium">Email notifications for matching formal job offers</span>
                <input
                  type="checkbox"
                  checked={emailAlerts}
                  onChange={(e) => setEmailAlerts(e.target.checked)}
                  className="rounded border-[#E6DFD1] text-[#17233F] focus:ring-[#D6A84B]"
                />
              </label>

              <label className="flex items-center justify-between p-3.5 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1] cursor-pointer hover:border-[#D6A84B]/60 transition-colors">
                <span className="font-medium">SMS alerts for interview round appointments</span>
                <input
                  type="checkbox"
                  checked={smsAlerts}
                  onChange={(e) => setSmsAlerts(e.target.checked)}
                  className="rounded border-[#E6DFD1] text-[#17233F] focus:ring-[#D6A84B]"
                />
              </label>

              <label className="flex items-center justify-between p-3.5 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1] cursor-pointer hover:border-[#D6A84B]/60 transition-colors">
                <span className="font-medium">Allow vetted employers to view my verified credentials</span>
                <input
                  type="checkbox"
                  checked={recruiterVisibility}
                  onChange={(e) => setRecruiterVisibility(e.target.checked)}
                  className="rounded border-[#E6DFD1] text-[#17233F] focus:ring-[#D6A84B]"
                />
              </label>
            </div>

            <div className="pt-2">
              <BrandButton variant="navy" onClick={handleSavePreferences} size="sm">
                Save Preferences
              </BrandButton>
            </div>
          </div>

          {/* Security / Password Update */}
          <div className="p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-4">
            <h2 className="text-xs font-bold text-[#17233F] uppercase tracking-wider flex items-center gap-2">
              <Key className="w-4 h-4 text-[#D6A84B]" /> Security & Credentials
            </h2>

            <form onSubmit={handlePasswordUpdate} className="space-y-3 text-xs">
              <div className="space-y-1">
                <label className="text-[#687187] font-semibold">Current Password</label>
                <input
                  type="password"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3 py-2 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
                />
              </div>

              <div className="space-y-1">
                <label className="text-[#687187] font-semibold">New Password</label>
                <input
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  placeholder="Min 8 characters"
                  className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3 py-2 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
                />
              </div>

              <div className="pt-2 flex items-center justify-between">
                <BrandButton variant="gold" type="submit" size="sm">
                  Update Password
                </BrandButton>

                <button
                  type="button"
                  onClick={logout}
                  className="text-xs font-bold text-[#C77B54] hover:text-[#C77B54]/80 flex items-center gap-1.5 transition-colors"
                >
                  <LogOut className="w-3.5 h-3.5" /> Sign Out
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
