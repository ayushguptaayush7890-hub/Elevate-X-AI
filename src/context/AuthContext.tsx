"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { UserProfile } from "@/types";
import { defaultUserProfile } from "@/data/mock-data";

interface AuthContextType {
  user: UserProfile;
  isAuthenticated: boolean;
  role: "user" | "admin";
  login: (email: string, role?: "user" | "admin", token?: string) => void;
  logout: () => void;
  switchRole: (role: "user" | "admin") => void;
  updateUser: (updates: Partial<UserProfile>) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<UserProfile>(defaultUserProfile);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

  useEffect(() => {
    try {
      const savedUser = localStorage.getItem("elevate_user_profile");
      const savedToken = localStorage.getItem("elevate_auth_token");
      if (savedUser) {
        setUser(JSON.parse(savedUser));
      }
      setIsAuthenticated(Boolean(savedToken));
    } catch (e) {
      console.warn("Failed to read user from localStorage", e);
    }
  }, []);

  const login = (email: string, role: "user" | "admin" = "user", token?: string) => {
    const updatedUser: UserProfile = {
      ...user,
      email,
      role,
    };
    setUser(updatedUser);
    setIsAuthenticated(true);
    try {
      localStorage.setItem("elevate_user_profile", JSON.stringify(updatedUser));
      if (token) {
        localStorage.setItem("elevate_auth_token", token);
      }
    } catch (e) {
      console.warn("Failed to save user session", e);
    }
  };

  const logout = () => {
    setIsAuthenticated(false);
    try {
      localStorage.removeItem("elevate_auth_token");
    } catch (e) {
      console.warn("Failed to remove token", e);
    }
  };

  const switchRole = (newRole: "user" | "admin") => {
    const updated = { ...user, role: newRole };
    setUser(updated);
    try {
      localStorage.setItem("elevate_user_profile", JSON.stringify(updated));
    } catch (e) {
      console.warn("Failed to persist role", e);
    }
  };

  const updateUser = (updates: Partial<UserProfile>) => {
    const updated = { ...user, ...updates };
    setUser(updated);
    try {
      localStorage.setItem("elevate_user_profile", JSON.stringify(updated));
    } catch (e) {
      console.warn("Failed to persist user updates", e);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated,
        role: user.role,
        login,
        logout,
        switchRole,
        updateUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
