"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

export type SupportedLanguage = "English" | "Hindi";

interface LanguageContextType {
  language: SupportedLanguage;
  setLanguage: (lang: SupportedLanguage) => void;
  t: (key: string) => string;
}

const translations: Record<SupportedLanguage, Record<string, string>> = {
  English: {
    tagline: "Your Experience. Your Skills. Your Future.",
    getStarted: "Get Started",
    exploreFeatures: "Explore Features",
    dashboard: "Dashboard",
    myProfile: "My Profile",
    experienceRecognition: "Experience Recognition",
    skillAssessment: "Skill Assessment",
    findJobs: "Find Jobs",
    skillGap: "Skill Gap Analyzer",
    resumeBuilder: "AI Resume Builder",
    careerRoadmap: "Career Roadmap",
    careerTransition: "Career Transition",
    interviewLab: "AI Interview Lab",
    aiAssistant: "AI Career Assistant",
    progressTracker: "Progress Tracker",
    applications: "Applications",
    settings: "Settings",
    adminDashboard: "Admin Portal",
    welcomeBack: "Welcome back",
    nextStep: "Let's take the next step in your career journey.",
    verifiedSkills: "Verified Skills",
    matchScore: "Match Score",
    saveJob: "Save Job",
    applyNow: "Apply Now",
    demoDataNotice: "Verified Demonstration Dataset",
  },
  Hindi: {
    tagline: "आपका अनुभव। आपका कौशल। आपका भविष्य।",
    getStarted: "शुरू करें",
    exploreFeatures: "सुविधाएँ देखें",
    dashboard: "डैशबोर्ड",
    myProfile: "मेरी प्रोफ़ाइल",
    experienceRecognition: "अनुभव से कौशल पहचान",
    skillAssessment: "कौशल मूल्यांकन",
    findJobs: "नौकरियां खोजें",
    skillGap: "स्किल गैप विश्लेषण",
    resumeBuilder: "एआई रेज़्यूमे मेकर",
    careerRoadmap: "करियर रोडमैप",
    careerTransition: "करियर बदलाव",
    interviewLab: "इंटरव्यू लैब",
    aiAssistant: "एआई करियर सहायक",
    progressTracker: "प्रगति ट्रैकर",
    applications: "आवेदन सूची",
    settings: "सेटिंग्स",
    adminDashboard: "एडमिन पोर्टल",
    welcomeBack: "वापसी पर स्वागत है",
    nextStep: "आइए आपके करियर की अगली छलांग की तैयारी करें।",
    verifiedSkills: "सत्यापित कौशल",
    matchScore: "मैच स्कोर",
    saveJob: "नौकरी सहेजें",
    applyNow: "आवेदन करें",
    demoDataNotice: "सत्यापित प्रदर्शन डेटा",
  },
};

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguageState] = useState<SupportedLanguage>("English");

  useEffect(() => {
    try {
      const savedLang = localStorage.getItem("elevate_lang") as SupportedLanguage;
      if (savedLang === "English" || savedLang === "Hindi") {
        setLanguageState(savedLang);
      }
    } catch (e) {
      console.warn("Language storage unavailable", e);
    }
  }, []);

  const setLanguage = (lang: SupportedLanguage) => {
    setLanguageState(lang);
    try {
      localStorage.setItem("elevate_lang", lang);
    } catch (e) {
      console.warn("Failed to save language preference", e);
    }
  };

  const t = (key: string): string => {
    return translations[language]?.[key] || translations.English[key] || key;
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error("useLanguage must be used within a LanguageProvider");
  }
  return context;
}
