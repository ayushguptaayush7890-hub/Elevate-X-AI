"use client";

import React, { useState, Suspense } from "react";
import { AdminSidebar } from "./AdminSidebar";
import { Menu, ShieldAlert, Sparkles } from "lucide-react";

function AdminShellInner({ children }: { children: React.ReactNode }) {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#FBF8F1] text-[#20243A] flex">
      <AdminSidebar mobileOpen={mobileOpen} setMobileOpen={setMobileOpen} />

      <div className="flex-1 flex flex-col min-w-0 lg:pl-64">
        {/* Top Header */}
        <header className="h-16 bg-[#FBF8F1]/90 backdrop-blur-xl border-b border-[#E6DFD1] px-4 sm:px-6 flex items-center justify-between sticky top-0 z-30 shadow-xs">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="p-2 rounded-xl bg-white border border-[#E6DFD1] text-[#17233F] lg:hidden"
            >
              <Menu className="w-5 h-5" />
            </button>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-[#27856B] animate-pulse" />
              <span className="text-xs font-bold text-[#17233F]">
                AI Orchestration Gateway: Active (v3.2)
              </span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span className="px-3 py-1 rounded-full text-xs font-bold bg-[#D6A84B]/15 text-[#9A7320] border border-[#D6A84B]/40 flex items-center gap-1.5 shadow-xs">
              <Sparkles className="w-3.5 h-3.5 text-[#7355D9]" /> Admin Benchmark Mode
            </span>
          </div>
        </header>

        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto space-y-6">
          {children}
        </main>
      </div>
    </div>
  );
}

export function AdminShell({ children }: { children: React.ReactNode }) {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-[#FBF8F1] flex items-center justify-center text-xs text-[#687187] font-bold">
          Loading Admin Gateway...
        </div>
      }
    >
      <AdminShellInner>{children}</AdminShellInner>
    </Suspense>
  );
}
