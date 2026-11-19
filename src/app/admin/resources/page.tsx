"use client";

import React, { useState } from "react";
import { AdminShell } from "@/components/layout/AdminShell";
import { PageHeader } from "@/components/ui/PageHeader";
import { BrandButton } from "@/components/ui/BrandButton";
import { toast } from "sonner";
import { BookOpen, Plus, ExternalLink, Trash2, CheckCircle2 } from "lucide-react";

export default function AdminResourcesPage() {
  const [resources, setResources] = useState([
    {
      id: "res-1",
      title: "Practical AQL 2.5 Sampling for Export Garment Inspectors",
      type: "Interactive Web Guide",
      duration: "3 hours",
      free: true,
      verifiedDate: "Nov 01, 2026",
    },
    {
      id: "res-2",
      title: "Factory Tablet Defect Logging Simulation Sandbox",
      type: "Hands-on Project",
      duration: "2 hours",
      free: true,
      verifiedDate: "Oct 25, 2026",
    },
    {
      id: "res-3",
      title: "From Paper to Screen: Digital Pattern Drafting in Seamly2D",
      type: "Video Course",
      duration: "4 hours",
      free: true,
      verifiedDate: "Nov 04, 2026",
    },
    {
      id: "res-4",
      title: "5S in Apparel Manufacturing Floor Management",
      type: "Vocational Workshop",
      duration: "1.5 hours",
      free: true,
      verifiedDate: "Nov 08, 2026",
    },
  ]);

  const handleDelete = (id: string) => {
    setResources(resources.filter((r) => r.id !== id));
    toast.info("Resource link removed.");
  };

  return (
    <AdminShell>
      <div className="space-y-6">
        <PageHeader
          badge="Curated Learning Assets"
          title="Learning Resources & Sandboxes"
          description="Audit and verify curated educational modules recommended across candidate vocational skill gap plans."
          variant="navy"
          actions={
            <BrandButton
              variant="gold"
              size="sm"
              onClick={() => toast.info("Resource link addition modal opened.")}
            >
              <Plus className="w-4 h-4 mr-1.5" />
              <span>Add Curated Resource</span>
            </BrandButton>
          }
        />

        <div className="space-y-3">
          {resources.map((res) => (
            <div
              key={res.id}
              className="p-5 rounded-2xl bg-white border border-[#E6DFD1] shadow-xs flex items-center justify-between hover:border-[#D6A84B] transition-all"
            >
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <h3 className="text-sm font-bold text-[#17233F]">{res.title}</h3>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#DCEAE6] text-[#27856B] border border-[#27856B]/30">
                    Verified Link
                  </span>
                </div>
                <p className="text-xs text-[#687187]">
                  Type: {res.type} • Duration: <strong className="text-[#17233F]">{res.duration}</strong> • Access:{" "}
                  <span className="font-semibold text-[#27856B]">{res.free ? "100% Free" : "Sponsored"}</span>
                </p>
                <p className="text-[10px] text-[#687187]">Last Verified: {res.verifiedDate}</p>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => handleDelete(res.id)}
                  className="p-2 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1] text-[#687187] hover:text-[#C77B54] transition-colors"
                  title="Remove Resource"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </AdminShell>
  );
}
