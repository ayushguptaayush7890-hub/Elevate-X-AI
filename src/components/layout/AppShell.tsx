"use client";

import React, { useState, Suspense } from "react";
import { DashboardSidebar } from "./DashboardSidebar";
import { DashboardHeader } from "./DashboardHeader";

function AppShellInner({ 
  children,
  isLocked = false,
  onLockedNavigation,
}: { 
  children: React.ReactNode;
  isLocked?: boolean;
  onLockedNavigation?: () => void;
}) {
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#FBF8F1] text-[#20243A] flex">
      {/* Sidebar Navigation */}
      <DashboardSidebar
        mobileOpen={mobileSidebarOpen}
        setMobileOpen={setMobileSidebarOpen}
        isLocked={isLocked}
        onLockedNavigation={onLockedNavigation}
      />

      {/* Main Workspace Area */}
      <div className="flex-1 flex flex-col min-w-0 lg:pl-64">
        {/* Sticky Header */}
        <DashboardHeader
          onMenuToggle={() => setMobileSidebarOpen(!mobileSidebarOpen)}
          isLocked={isLocked}
          onLockedNavigation={onLockedNavigation}
        />

        {/* Dynamic Page Content */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto space-y-6">
          {children}
        </main>
      </div>
    </div>
  );
}

export function AppShell({ 
  children,
  isLocked = false,
  onLockedNavigation,
}: { 
  children: React.ReactNode;
  isLocked?: boolean;
  onLockedNavigation?: () => void;
}) {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-[#FBF8F1] flex items-center justify-center text-xs text-[#687187] font-bold">
          Loading Elevate X...
        </div>
      }
    >
      <AppShellInner isLocked={isLocked} onLockedNavigation={onLockedNavigation}>
        {children}
      </AppShellInner>
    </Suspense>
  );
}
