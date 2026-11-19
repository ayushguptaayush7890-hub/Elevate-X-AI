"use client";

import React, { useState } from "react";
import { AdminShell } from "@/components/layout/AdminShell";
import { PageHeader } from "@/components/ui/PageHeader";
import { toast } from "sonner";
import { Users, Search, Shield, Award, CheckCircle2, MoreVertical, Ban, RefreshCw } from "lucide-react";

export default function AdminUsersPage() {
  const [search, setSearch] = useState("");
  const [usersList, setUsersList] = useState([
    {
      id: "u-1",
      name: "Ramesh Sharma",
      email: "ramesh.sharma@example.com",
      trade: "Master Tailor & Artisan",
      verifiedSkills: 4,
      role: "Candidate",
      status: "Active",
      joined: "Nov 02, 2026",
    },
    {
      id: "u-2",
      name: "Sunita Verma",
      email: "sunita.bakery@example.com",
      trade: "Commercial Bakery Artisan",
      verifiedSkills: 5,
      role: "Candidate",
      status: "Active",
      joined: "Nov 05, 2026",
    },
    {
      id: "u-3",
      name: "Mohd. Arif",
      email: "arif.electric@example.com",
      trade: "Solar Field Service Tech",
      verifiedSkills: 6,
      role: "Candidate",
      status: "Active",
      joined: "Oct 28, 2026",
    },
    {
      id: "u-4",
      name: "Deepak Patel",
      email: "deepak.admin@elevatex-ai.org",
      trade: "Vocational Auditor",
      verifiedSkills: 8,
      role: "Admin",
      status: "Active",
      joined: "Sep 15, 2026",
    },
  ]);

  const handleToggleStatus = (id: string) => {
    setUsersList((prev) =>
      prev.map((u) =>
        u.id === id ? { ...u, status: u.status === "Active" ? "Suspended" : "Active" } : u
      )
    );
    toast.success("User account status updated.");
  };

  const filtered = usersList.filter(
    (u) =>
      u.name.toLowerCase().includes(search.toLowerCase()) ||
      u.trade.toLowerCase().includes(search.toLowerCase()) ||
      u.email.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <AdminShell>
      <div className="space-y-6">
        <PageHeader
          badge="Candidate & Auditor Directory"
          title="Worker & Recruiter Directory"
          description="Manage candidates, verify trade portfolios, and audit account privileges across the vocational ecosystem."
          variant="navy"
          actions={
            <div className="flex items-center gap-2 text-xs text-[#F0D99B] bg-[#10192D] px-3.5 py-2 rounded-xl border border-[#D6A84B]/40">
              <Users className="w-4 h-4 text-[#D6A84B]" />
              <span>{usersList.length} Active Records</span>
            </div>
          }
        />

        <div className="p-4 rounded-2xl bg-white border border-[#E6DFD1] shadow-xs">
          <div className="relative">
            <Search className="w-4 h-4 text-[#687187] absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search candidates by name, trade, or email..."
              className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl pl-10 pr-4 py-2.5 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
            />
          </div>
        </div>

        <div className="rounded-2xl bg-white border border-[#E6DFD1] shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-[#17233F] text-[#F0D99B] border-b border-[#D6A84B]/30">
                <tr>
                  <th className="p-4 font-semibold uppercase tracking-wider text-[10px]">Worker Name</th>
                  <th className="p-4 font-semibold uppercase tracking-wider text-[10px]">Trade Background</th>
                  <th className="p-4 font-semibold uppercase tracking-wider text-[10px]">Verified Skills</th>
                  <th className="p-4 font-semibold uppercase tracking-wider text-[10px]">Platform Role</th>
                  <th className="p-4 font-semibold uppercase tracking-wider text-[10px]">Status</th>
                  <th className="p-4 font-semibold uppercase tracking-wider text-[10px] text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E6DFD1] text-[#20243A]">
                {filtered.map((u) => (
                  <tr key={u.id} className="hover:bg-[#FBF8F1] transition-colors">
                    <td className="p-4">
                      <p className="font-bold text-[#17233F]">{u.name}</p>
                      <p className="text-[10px] text-[#687187]">{u.email}</p>
                    </td>
                    <td className="p-4 font-semibold text-[#17233F]">{u.trade}</td>
                    <td className="p-4 font-bold text-[#27856B]">
                      {u.verifiedSkills} Badges
                    </td>
                    <td className="p-4">
                      <span className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full ${
                        u.role === "Admin" ? "bg-[#17233F] text-[#F0D99B] border border-[#D6A84B]" : "bg-[#F5F0E6] text-[#17233F] border border-[#E6DFD1]"
                      }`}>
                        {u.role}
                      </span>
                    </td>
                    <td className="p-4">
                      <span className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full ${
                        u.status === "Active" ? "bg-[#DCEAE6] text-[#27856B] border border-[#27856B]/30" : "bg-[#C77B54]/15 text-[#C77B54] border border-[#C77B54]/30"
                      }`}>
                        {u.status}
                      </span>
                    </td>
                    <td className="p-4 text-right">
                      <button
                        onClick={() => handleToggleStatus(u.id)}
                        className="px-3 py-1 rounded-lg border border-[#E6DFD1] bg-[#FBF8F1] hover:bg-[#F5F0E6] text-[11px] font-semibold text-[#17233F] transition-colors"
                      >
                        {u.status === "Active" ? "Suspend" : "Activate"}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </AdminShell>
  );
}
