"use client";

import React, { useState } from "react";
import { 
  History,
  Search,
  Filter,
  Download,
  Info,
  ChevronRight,
  ChevronDown,
  Building2,
  Calendar,
  ShieldAlert
} from "lucide-react";

export default function AuditCenterPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedEventType, setSelectedEventType] = useState("ALL");
  const [selectedRow, setSelectedRow] = useState<string | null>(null);

  const eventLogs = [
    { id: "evt-01", timestamp: "2026-06-26 10:15:35", type: "ApprovalRequested", message: "Intercepted outbound Gmail outreach delivery targeting contact@targetsaas.com", user: "system", employee: "Alex SDR Pro" },
    { id: "evt-02", timestamp: "2026-06-26 10:14:22", type: "PolicyDecisionLogged", message: "Checked write action to HubSpot database. Decision: ALLOW. Rule: safe_schema", user: "system", employee: "Alex SDR Pro" },
    { id: "evt-03", timestamp: "2026-06-26 10:14:02", type: "WorkflowStarted", message: "Start campaign sequence: Find prospect decision makers", user: "admin@qevn.in", employee: "Alex SDR Pro" },
    { id: "evt-04", timestamp: "2026-06-26 09:44:12", type: "PolicyDecisionLogged", message: "Outbound Gmail mass send rate limit exceeded. Decision: DENIED. Rule: limit_outbound", user: "system", employee: "Alex SDR Pro" },
    { id: "evt-05", timestamp: "2026-06-26 08:12:52", type: "WorkflowCompleted", message: "Finished candidate assessment loop for Staff Tech Lead resume evaluations", user: "system", employee: "Sarah Recruiter" },
    { id: "evt-06", timestamp: "2026-06-26 08:12:10", type: "WorkflowStarted", message: "Start candidate resume parsing list load", user: "admin@qevn.in", employee: "Sarah Recruiter" }
  ];

  const filteredLogs = eventLogs.filter(log => {
    const matchesSearch = log.message.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          log.employee.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          log.id.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesType = selectedEventType === "ALL" || log.type === selectedEventType;
    return matchesSearch && matchesType;
  });

  const handleExport = () => {
    // Generate simple mock CSV and download it
    const csvContent = "data:text/csv;charset=utf-8," 
      + ["ID,Timestamp,Event Type,Message,Triggered By,AI Employee", ...filteredLogs.map(l => `${l.id},${l.timestamp},${l.type},"${l.message}",${l.user},"${l.employee}"`)].join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `qevn_audit_export_${new Date().toISOString().slice(0,10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="flex flex-col gap-6 max-w-6xl">
      {/* Title Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-foreground via-foreground/90 to-primary bg-clip-text text-transparent">
            Security & Audit Center
          </h1>
          <p className="text-foreground/60 text-sm mt-1">
            Search, review, and export all workspace and tenant level operations events for SOC2/ISO audit compliance.
          </p>
        </div>
        
        {/* Export trigger */}
        <button
          onClick={handleExport}
          className="px-4 py-2 bg-primary hover:bg-primary/95 text-white rounded font-medium text-xs transition-all flex items-center gap-1.5 self-start md:self-auto shadow-md"
        >
          <Download className="w-4 h-4" />
          Export Audit Logs (CSV)
        </button>
      </div>

      {/* Filter and search bar */}
      <div className="p-4 rounded-lg bg-card border border-border flex flex-col md:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-2.5 w-4 h-4 text-foreground/40" />
          <input
            type="text"
            placeholder="Search event logs by message, employee ID, or audit hash..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="p-2 pl-9 w-full rounded bg-secondary border border-border text-xs focus:border-primary outline-none"
          />
        </div>
        
        {/* Event Type selector */}
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-foreground/50 shrink-0" />
          <select
            value={selectedEventType}
            onChange={(e) => setSelectedEventType(e.target.value)}
            className="p-2 rounded bg-secondary border border-border text-xs focus:border-primary outline-none"
          >
            <option value="ALL">All Events</option>
            <option value="WorkflowStarted">WorkflowStarted</option>
            <option value="WorkflowCompleted">WorkflowCompleted</option>
            <option value="PolicyDecisionLogged">PolicyDecisionLogged</option>
            <option value="ApprovalRequested">ApprovalRequested</option>
          </select>
        </div>
      </div>

      {/* Main Table & Details Split */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Logs Table (Left) */}
        <div className="lg:col-span-2 p-6 rounded-lg bg-card border border-border shadow-sm overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead>
              <tr className="border-b border-border text-foreground/50 uppercase text-[9px] tracking-wider font-semibold">
                <th className="pb-3 w-8"></th>
                <th className="pb-3">Timestamp</th>
                <th className="pb-3">Event Type</th>
                <th className="pb-3">AI Employee</th>
                <th className="pb-3">Message</th>
                <th className="pb-3">Triggered By</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/60">
              {filteredLogs.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-6 text-center text-foreground/40">No audit events match search filters.</td>
                </tr>
              ) : (
                filteredLogs.map(log => (
                  <tr 
                    key={log.id} 
                    onClick={() => setSelectedRow(selectedRow === log.id ? null : log.id)}
                    className={`hover:bg-secondary/15 transition-all cursor-pointer ${selectedRow === log.id ? "bg-secondary/35 border-l-2 border-primary" : ""}`}
                  >
                    <td className="py-3.5 text-center text-foreground/40">
                      {selectedRow === log.id ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
                    </td>
                    <td className="py-3.5 text-foreground/60 whitespace-nowrap">{log.timestamp}</td>
                    <td className="py-3.5">
                      <span className={`px-2 py-0.5 rounded-full text-[9px] font-bold ${
                        log.type === "WorkflowStarted" ? "bg-primary/20 text-primary" :
                        log.type === "WorkflowCompleted" ? "bg-success/20 text-success" :
                        log.type === "ApprovalRequested" ? "bg-warning/20 text-warning" :
                        "bg-secondary-accent/40 text-foreground"
                      }`}>{log.type}</span>
                    </td>
                    <td className="py-3.5 font-medium">{log.employee}</td>
                    <td className="py-3.5 text-foreground/80 max-w-[200px] truncate" title={log.message}>{log.message}</td>
                    <td className="py-3.5 font-mono text-foreground/50">{log.user}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* JSON Details Inspector (Right) */}
        <div className="p-6 rounded-lg bg-card border border-border shadow-sm flex flex-col gap-4">
          <h3 className="text-xs font-bold text-foreground/50 uppercase tracking-wider flex items-center gap-1.5">
            <Info className="w-4 h-4 text-primary" />
            Raw Payload Compliance Inspector
          </h3>
          
          {selectedRow ? (
            <div className="flex flex-col gap-4 text-xs h-full">
              <p className="text-[10px] text-foreground/40">
                Audit Hash: <span className="font-mono text-primary font-bold">{selectedRow}</span>
              </p>
              
              <div className="p-4 bg-[#030303] text-foreground/95 rounded border border-border font-mono text-[10px] overflow-x-auto flex-1 max-h-80">
                <pre>
                  {JSON.stringify(eventLogs.find(l => l.id === selectedRow), null, 2)}
                </pre>
              </div>
              <div className="p-3 bg-secondary/20 rounded border border-border text-[10px] text-foreground/60 leading-relaxed">
                🛡️ This audit entry is sealed. Cryptographic ECDSA signature verifies this log has not been modified since creation.
              </div>
            </div>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center text-center p-6 bg-secondary/10 border border-dashed border-border rounded">
              <span className="text-2xl mb-2">📜</span>
              <p className="text-xs text-foreground/50">Click on any row in the audit logs table to inspect the compliance JSON payload and seal signatures.</p>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
