"use client";

import React, { useState, useEffect, useRef } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { BrandButton } from "@/components/ui/BrandButton";
import { AssistantMessage, ConsultationItem } from "@/types";
import { apiService } from "@/services/api-service";
import { toast } from "sonner";
import ReactMarkdown from "react-markdown";
import {
  Send,
  Bot,
  User,
  Copy,
  Plus,
  Globe,
  ShieldCheck,
  Loader2,
  Trash2,
  MessageSquare,
} from "lucide-react";

export default function AssistantPage() {
  const [consultations, setConsultations] = useState<ConsultationItem[]>([]);
  const [activeConsultationId, setActiveConsultationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<AssistantMessage[]>([]);
  const [inputText, setInputText] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [isLoadingConsultations, setIsLoadingConsultations] = useState(true);
  const [isLoadingMessages, setIsLoadingMessages] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState<"English" | "Hindi">("English");

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  // Load consultations on initial mount
  useEffect(() => {
    async function loadInitialData() {
      setIsLoadingConsultations(true);
      try {
        const list = await apiService.getAssistantConsultations();
        if (list && list.length > 0) {
          setConsultations(list);
          const firstId = list[0].id;
          setActiveConsultationId(firstId);
          await loadConsultationDetail(firstId);
        } else {
          // If no consultations exist, create one
          const created = await apiService.createAssistantConsultation(
            "Career & Skills Consultation",
            selectedLanguage
          );
          if (created) {
            setConsultations([
              {
                id: created.id,
                title: created.title,
                language: created.language,
                date: "Today",
                message_count: created.messages.length,
                updated_at: created.updated_at,
              },
            ]);
            setActiveConsultationId(created.id);
            setMessages(created.messages);
          }
        }
      } catch (err: any) {
        console.error("Failed to load consultations:", err);
        toast.error("Could not load consultation history.");
      } finally {
        setIsLoadingConsultations(false);
      }
    }

    loadInitialData();
  }, []);

  // Fetch full messages for a specific consultation
  const loadConsultationDetail = async (id: string) => {
    setIsLoadingMessages(true);
    try {
      const detail = await apiService.getAssistantConsultation(id);
      if (detail) {
        setMessages(detail.messages || []);
        if (detail.language === "Hindi") {
          setSelectedLanguage("Hindi");
        } else {
          setSelectedLanguage("English");
        }
      }
    } catch (err: any) {
      console.error("Failed to load consultation detail:", err);
      toast.error("Failed to load conversation messages.");
    } finally {
      setIsLoadingMessages(false);
    }
  };

  const handleSelectConsultation = (id: string) => {
    if (id === activeConsultationId) return;
    setActiveConsultationId(id);
    loadConsultationDetail(id);
  };

  const handleNewConsultation = async () => {
    try {
      setIsTyping(false);
      const newConsultation = await apiService.createAssistantConsultation(
        "New Career Consultation",
        selectedLanguage
      );
      if (newConsultation) {
        const newItem: ConsultationItem = {
          id: newConsultation.id,
          title: newConsultation.title,
          language: newConsultation.language,
          date: "Today",
          message_count: newConsultation.messages.length,
          updated_at: newConsultation.updated_at,
        };
        setConsultations((prev) => [newItem, ...prev.filter((c) => c.id !== newItem.id)]);
        setActiveConsultationId(newConsultation.id);
        setMessages(newConsultation.messages || []);
        toast.info("Started new career consultation.");
      }
    } catch (err: any) {
      console.error("Failed to create new consultation:", err);
      toast.error("Failed to start new consultation.");
    }
  };

  const handleLanguageChange = async (lang: "English" | "Hindi") => {
    setSelectedLanguage(lang);
    if (activeConsultationId) {
      try {
        await apiService.updateAssistantConsultation(activeConsultationId, {
          language: lang,
        });
      } catch (err) {
        console.warn("Failed to persist language preference:", err);
      }
    }
  };

  const handleSendMessage = async (textToSend?: string) => {
    const text = (textToSend || inputText).trim();
    if (!text || isTyping) return;

    if (!activeConsultationId) {
      toast.error("No active consultation session found.");
      return;
    }

    const tempUserMsg: AssistantMessage = {
      id: `temp-${Date.now()}`,
      sender: "user",
      content: text,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      language: selectedLanguage,
    };

    setMessages((prev) => [...prev, tempUserMsg]);
    setInputText("");
    setIsTyping(true);

    try {
      const reply = await apiService.sendAssistantMessage(
        activeConsultationId,
        text,
        selectedLanguage
      );

      setMessages((prev) => [...prev, reply]);

      // Refresh consultations list to update sidebar preview and title
      const updatedList = await apiService.getAssistantConsultations();
      if (updatedList) {
        setConsultations(updatedList);
      }
    } catch (err: any) {
      console.error("Error from AI Career Mentor:", err);
      toast.error(
        err?.message || "Failed to receive response from Elevate X AI Career Mentor."
      );
    } finally {
      setIsTyping(false);
    }
  };

  const handleDeleteConsultation = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    try {
      await apiService.deleteAssistantConsultation(id);
      const remaining = consultations.filter((c) => c.id !== id);
      setConsultations(remaining);
      toast.success("Consultation removed.");

      if (activeConsultationId === id) {
        if (remaining.length > 0) {
          setActiveConsultationId(remaining[0].id);
          loadConsultationDetail(remaining[0].id);
        } else {
          handleNewConsultation();
        }
      }
    } catch (err: any) {
      console.error("Failed to delete consultation:", err);
      toast.error("Failed to delete consultation.");
    }
  };

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    toast.success("Response copied to clipboard.");
  };

  return (
    <AppShell>
      {/* Workspace Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 h-[calc(100vh-140px)] min-h-[620px]">
        {/* Left Sidebar: Conversations (3 cols) */}
        <div className="hidden lg:flex lg:col-span-3 flex-col bg-white rounded-2xl border border-[#E6DFD1] shadow-sm p-4 space-y-4">
          <button
            onClick={handleNewConsultation}
            className="flex items-center justify-center gap-2 w-full py-2.5 px-3 rounded-xl bg-[#17233F] hover:bg-[#10192D] text-[#F0D99B] border border-[#D6A84B]/40 text-xs font-bold transition-all shadow-xs cursor-pointer"
          >
            <Plus className="w-4 h-4 text-[#D6A84B]" /> New Career Consultation
          </button>

          <div className="flex-1 overflow-y-auto space-y-1.5 pr-1">
            <span className="text-[10px] font-bold text-[#687187] uppercase tracking-wider block px-2 mb-2">
              Recent Consultations
            </span>

            {isLoadingConsultations ? (
              <div className="p-4 flex items-center justify-center text-xs text-[#687187] gap-2">
                <Loader2 className="w-4 h-4 animate-spin text-[#7355D9]" />
                <span>Loading sessions...</span>
              </div>
            ) : consultations.length === 0 ? (
              <div className="p-4 text-center text-xs text-[#687187]">
                No recent consultations.
              </div>
            ) : (
              consultations.map((conv) => {
                const isActive = conv.id === activeConsultationId;
                return (
                  <div
                    key={conv.id}
                    onClick={() => handleSelectConsultation(conv.id)}
                    className={`group relative p-3 rounded-xl border text-xs cursor-pointer transition-all ${
                      isActive
                        ? "bg-[#F5F0E6] border-[#D6A84B] shadow-2xs font-semibold"
                        : "bg-[#FBF8F1] hover:bg-[#F5F0E6] border-[#E6DFD1] text-[#20243A]"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-1">
                      <p className="font-bold text-[#17233F] truncate flex-1">
                        {conv.title}
                      </p>
                      <button
                        onClick={(e) => handleDeleteConsultation(e, conv.id)}
                        className="opacity-0 group-hover:opacity-100 hover:text-red-600 p-0.5 transition-opacity"
                        title="Delete consultation"
                      >
                        <Trash2 className="w-3 h-3 text-[#687187] hover:text-red-600" />
                      </button>
                    </div>
                    <div className="flex items-center justify-between text-[10px] text-[#687187] mt-1">
                      <span>{conv.date}</span>
                      <span className="bg-white/80 px-1.5 py-0.5 rounded border border-[#E6DFD1]/60 text-[9px]">
                        {conv.language}
                      </span>
                    </div>
                  </div>
                );
              })
            )}
          </div>

          {/* Language Toggle */}
          <div className="pt-3 border-t border-[#E6DFD1]">
            <div className="flex items-center justify-between text-xs text-[#687187] mb-2">
              <span className="flex items-center gap-1 font-semibold">
                <Globe className="w-3.5 h-3.5 text-[#7355D9]" /> Language:
              </span>
              <span className="font-bold text-[#17233F]">{selectedLanguage}</span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <button
                type="button"
                onClick={() => handleLanguageChange("English")}
                className={`py-2 rounded-xl border text-center transition-all cursor-pointer ${
                  selectedLanguage === "English"
                    ? "bg-[#17233F] text-[#F0D99B] border-[#D6A84B] font-bold shadow-sm"
                    : "bg-[#FBF8F1] border-[#E6DFD1] text-[#687187] hover:text-[#17233F]"
                }`}
              >
                English
              </button>
              <button
                type="button"
                onClick={() => handleLanguageChange("Hindi")}
                className={`py-2 rounded-xl border text-center transition-all cursor-pointer ${
                  selectedLanguage === "Hindi"
                    ? "bg-[#17233F] text-[#F0D99B] border-[#D6A84B] font-bold shadow-sm"
                    : "bg-[#FBF8F1] border-[#E6DFD1] text-[#687187] hover:text-[#17233F]"
                }`}
              >
                हिन्दी
              </button>
            </div>
          </div>
        </div>

        {/* Main Panel: Chat Window (9 cols) */}
        <div className="lg:col-span-9 flex flex-col bg-white rounded-2xl border border-[#E6DFD1] shadow-sm overflow-hidden">
          {/* Top Bar */}
          <div className="p-4 border-b border-[#E6DFD1] flex items-center justify-between bg-[#FBF8F1]">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-[#17233F] text-[#F0D99B] border border-[#D6A84B]/40 flex items-center justify-center shadow-sm">
                <Bot className="w-5 h-5 text-[#D6A84B]" />
              </div>
              <div>
                <h2 className="text-sm font-bold text-[#17233F]">Elevate X AI Career Mentor</h2>
                <p className="text-xs text-[#27856B] font-semibold flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-[#27856B] animate-pulse" /> Official Gemini API Active ({selectedLanguage})
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              {/* Mobile language switch */}
              <div className="lg:hidden flex items-center gap-1">
                <button
                  type="button"
                  onClick={() => handleLanguageChange(selectedLanguage === "English" ? "Hindi" : "English")}
                  className="px-2 py-1 text-xs rounded-lg border border-[#E6DFD1] bg-white font-semibold text-[#17233F]"
                >
                  {selectedLanguage === "English" ? "हिन्दी" : "English"}
                </button>
              </div>

              <div className="hidden sm:flex items-center gap-2 text-xs text-[#687187] bg-white px-3 py-1.5 rounded-xl border border-[#E6DFD1]">
                <ShieldCheck className="w-3.5 h-3.5 text-[#27856B]" />
                <span>Vocational Career Coach</span>
              </div>
            </div>
          </div>

          {/* Messages Stream */}
          <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 bg-[#FBF8F1]/40">
            {isLoadingMessages ? (
              <div className="h-full flex flex-col items-center justify-center text-xs text-[#687187] gap-3">
                <Loader2 className="w-6 h-6 animate-spin text-[#D6A84B]" />
                <span>Loading consultation messages...</span>
              </div>
            ) : messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-8 space-y-3">
                <div className="w-12 h-12 rounded-2xl bg-[#F5F0E6] border border-[#D6A84B]/40 flex items-center justify-center text-[#17233F]">
                  <MessageSquare className="w-6 h-6 text-[#D6A84B]" />
                </div>
                <h3 className="font-bold text-sm text-[#17233F]">Start Your Career Consultation</h3>
                <p className="text-xs text-[#687187] max-w-md">
                  Ask any question about vocational transitions, interview preparation, trade certifications, or resume improvements.
                </p>
              </div>
            ) : (
              messages.map((msg) => {
                const isUser = msg.sender === "user";
                return (
                  <div
                    key={msg.id}
                    className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}
                  >
                    {!isUser && (
                      <div className="w-8 h-8 rounded-xl bg-[#17233F] text-[#D6A84B] flex items-center justify-center shrink-0 mt-0.5 border border-[#D6A84B]/30">
                        <Bot className="w-4 h-4 text-[#D6A84B]" />
                      </div>
                    )}

                    <div className={`max-w-2xl space-y-2 ${isUser ? "items-end" : "items-start"}`}>
                      <div
                        className={`p-4 rounded-2xl text-xs sm:text-sm leading-relaxed ${
                          isUser
                            ? "bg-[#17233F] text-white rounded-tr-none shadow-md border border-[#D6A84B]/30"
                            : "bg-white border border-[#E6DFD1] text-[#20243A] rounded-tl-none shadow-sm"
                        }`}
                      >
                        <div className={isUser ? "prose prose-invert prose-xs sm:prose-sm max-w-none text-white whitespace-pre-wrap" : "prose prose-slate prose-xs sm:prose-sm max-w-none text-[#20243A]"}>
                          <ReactMarkdown>{msg.content}</ReactMarkdown>
                        </div>
                      </div>

                      <div className="flex items-center gap-2 px-1 text-[11px] text-[#687187]">
                        <span>{msg.timestamp}</span>
                        {msg.model_used && (
                          <span className="text-[9px] bg-[#F5F0E6] text-[#7355D9] px-1.5 py-0.2 rounded border border-[#E6DFD1]">
                            {msg.model_used}
                          </span>
                        )}
                        {!isUser && (
                          <button
                            onClick={() => handleCopy(msg.content)}
                            className="hover:text-[#17233F] transition-colors cursor-pointer"
                            title="Copy response"
                          >
                            <Copy className="w-3 h-3" />
                          </button>
                        )}
                      </div>

                      {/* Suggested Chips */}
                      {!isUser && msg.suggestions && msg.suggestions.length > 0 && (
                        <div className="flex flex-wrap gap-1.5 pt-1">
                          {msg.suggestions.map((sug, i) => (
                            <button
                              key={i}
                              onClick={() => handleSendMessage(sug)}
                              className="text-xs px-3 py-1 rounded-full bg-white border border-[#D6A84B]/60 text-[#17233F] hover:bg-[#F0D99B]/30 transition-colors font-medium shadow-2xs cursor-pointer text-left"
                            >
                              {sug}
                            </button>
                          ))}
                        </div>
                      )}
                    </div>

                    {isUser && (
                      <div className="w-8 h-8 rounded-xl bg-[#F5F0E6] text-[#17233F] flex items-center justify-center shrink-0 mt-0.5 border border-[#E6DFD1]">
                        <User className="w-4 h-4" />
                      </div>
                    )}
                  </div>
                );
              })
            )}

            {isTyping && (
              <div className="flex items-center gap-2.5 text-xs font-semibold text-[#7355D9] p-2 bg-white/70 rounded-xl border border-[#E6DFD1] w-fit shadow-2xs">
                <Loader2 className="w-3.5 h-3.5 animate-spin text-[#D6A84B]" />
                <span>Elevate X AI Career Mentor is drafting personalized guidance via Gemini...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Box */}
          <div className="p-4 border-t border-[#E6DFD1] bg-white">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSendMessage();
              }}
              className="flex items-center gap-2"
            >
              <input
                type="text"
                value={inputText}
                disabled={isTyping}
                onChange={(e) => setInputText(e.target.value)}
                placeholder={
                  selectedLanguage === "Hindi"
                    ? "अपने काम या करियर से जुड़ा कोई भी सवाल पूछें (जैसे: इंटरव्यू की तैयारी, रेज़्यूमे सुधार)..."
                    : "Ask any career, skill assessment, or interview question..."
                }
                className="flex-1 bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-4 py-2.5 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B] disabled:opacity-60"
              />

              <BrandButton type="submit" variant="gold" size="sm" disabled={isTyping || !inputText.trim()}>
                {isTyping ? (
                  <Loader2 className="w-3.5 h-3.5 mr-1 animate-spin" />
                ) : (
                  <Send className="w-3.5 h-3.5 mr-1" />
                )}
                <span>Send</span>
              </BrandButton>
            </form>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
