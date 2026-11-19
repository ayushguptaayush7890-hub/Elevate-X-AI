"use client";

import React from "react";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "@/lib/query-client";
import { AuthProvider } from "@/context/AuthContext";
import { LanguageProvider } from "@/context/LanguageContext";
import { Toaster } from "sonner";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <LanguageProvider>
          {children}
          <Toaster 
            position="top-right" 
            theme="dark"
            toastOptions={{
              style: {
                background: "#141D33",
                border: "1px solid rgba(255, 255, 255, 0.1)",
                color: "#F8FAFC",
              },
            }}
          />
        </LanguageProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
}
