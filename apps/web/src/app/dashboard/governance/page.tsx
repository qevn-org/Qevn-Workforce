"use client";

import React, { useState } from "react";
import { 
  Shield,
  CheckCircle,
  XCircle,
  AlertOctagon,
  Clock,
  UserCheck,
  Search,
  Building2,
  Trash2,
  AlertTriangle,
  History
} from "lucide-react";

export default function GovernancePage() {
  const [activeTab, setActiveTab] = useState("approvals"); // 'approvals' | 'policies' | 'incidents'
  
  const [approvals, setApprovals] = useState([
    { id: "appr-01", employee: "Alex SDR Pro", workflow: "Find prospect decision makers", action: "Gmail outbound outreach email delivery", target: "contact@targetsaas.com", timestamp: "5 mins ago", status: "Pending" },
    { id: "appr-02", employee: "Alex SDR Pro", workflow: "CRM syncing leads to HubSpot", action: "Modify lead status: 'Enterprise Match'", target: "hs-deal-888999", timestamp: "20 mins ago", status: "Pending" }
  ]);

  const [approvalHistory, setApprovalHistory] = useState([
    { id: "appr-03", employee: "Sarah Recruiter", workflow: "Evaluate resume", action: "Gmail send candidate interview invite", target: "dev-candidate-jane@gmail.com", timestamp: "2 hours ago", status: "Approved", authorizedBy: "admin@qevn.in" },
    { id: "appr-04", employee: "Alex SDR Pro", workflow: "SDR Campaign London", action: "Gmail mass campaign blast (50+ recipients)", target: "Broad list", timestamp: "1 day ago", status: "Rejected", authorizedBy: "admin@qevn.in" }
  ]);

  const policyDecisions = [
    { id: "dec-01", action: "gmail:send_message", decision: "Approval Required", reason: "Action involves communication with external domains.", timestamp: "10:15:35 AM", employee: "Alex SDR Pro", workflow: "Find prospect decision makers" },
    { id: "dec-02", action: "crm:write_deal", decision: "Allowed", reason: "Payload size is within safe schema guidelines.", timestamp: "10:14:22 AM", employee: "Alex SDR Pro", workflow: "Find prospect decision makers" },
    { id: "dec-03", action: "gmail:mass_send", decision: "Denied", reason: "Workspace rate limits exceeded. Max 50 outbound emails limit triggered.", timestamp: "09:44:12 AM", employee: "Alex SDR Pro", workflow: "SDR Campaign London" },
    { id: "dec-04", action: "db:write_pii", decision: "Escalated", reason: "PII masking filter detected raw social security text field.", timestamp: "08:12:28 AM", employee: "Sarah Recruiter", workflow: "Evaluate resume" }
  ];

  const incidents = [
    { id: "inc-01", severity: "Critical", component: "HubSpot API Connector", issue: "HTTP 429 Rate Limit Exceeded - HubSpot Gateway offline", timestamp: "12 mins ago", status: "Open" },
    { id: "inc-02", severity: "High", component: "Model Endpoint (Anthropic Claude-3)", issue: "Token generation timeouts (latency > 25s)", timestamp: "45 mins ago", status: "Resolved" },
    { id: "inc-03", severity: "Warning", component: "Policy Interceptor", issue: "Blocked suspicious script injection request", timestamp: "2 hours ago", status: "Resolved" },
    { id: "inc-04", severity: "Warning", component: "Gmail SMTP Deliverer", issue: "Gmail connection timeout. Automatically retrying attempt 2/5", timestamp: "3 hours ago", status: "Open" }
  ];

  const handleApprove = (id: string) => {
    const item = approvals.find(a => a.id === id);
    if (!item) return;
    setApprovals(approvals.filter(a => a.id !== id));
    setApprovalHistory([
      { ...item, status: "Approved", authorizedBy: "admin@qevn.in" },
      ...approvalHistory
    ]);
  };

  const handleReject = (id: string) => {
    const item = approvals.find(a => a.id === id);
    if (!item) return;
    setApprovals(approvals.filter(a => a.id !== id));
    setApprovalHistory([
      { ...item, status: "Rejected", authorizedBy: "admin@qevn.in" },
      ...approvalHistory
    ]);
  };

  return (
    <div className="flex flex-col gap-6 max-w-6xl">
      {/* Title Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-foreground via-foreground/90 to-primary bg-clip-text text-transparent">
          Governance & Safety Desk
        </h1>
        <p className="text-foreground/60 text-sm mt-1">
          Review manual action approvals, inspect real-time policy rules execution, and track system incident alerts.
        </p>
      </div>

      {/* Tabs Row Bar */}
      <div className="flex border-b border-border bg-card/25 p-1 rounded-t">
        <button
          onClick={() => setActiveTab("approvals")}
          className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold transition-all ${
            activeTab === "approvals" 
              ? "border-b-2 border-primary text-primary" 
              : "text-foreground/60 hover:text-foreground"
          }`}
        >
          <UserCheck className="w-4 h-4" />
          Approval Center
        </button>
        <button
          onClick={() => setActiveTab("policies")}
          className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold transition-all ${
            activeTab === "policies" 
              ? "border-b-2 border-primary text-primary" 
              : "text-foreground/60 hover:text-foreground"
          }`}
        >
          <Shield className="w-4 h-4" />
          Policy Explorer
        </button>
        <button
          onClick={() => setActiveTab("incidents")}
          className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold transition-all ${
            activeTab === "incidents" 
              ? "border-b-2 border-primary text-primary" 
              : "text-foreground/60 hover:text-foreground"
          }`}
        >
          <AlertOctagon className="w-4 h-4" />
          Incident Center
        </button>
      </div>

      {/* Main Content Area */}
      <div className="p-6 rounded-lg bg-card border border-border shadow-sm">
        
        {/* APPROVAL CENTER */}
        {activeTab === "approvals" && (
          <div className="flex flex-col gap-6">
            
            {/* Pending Approvals */}
            <div className="flex flex-col gap-3">
              <h3 className="text-xs font-bold text-foreground/50 uppercase tracking-wider">Pending Approvals Queue</h3>
              {approvals.length === 0 ? (
                <p className="text-xs text-foreground/40 py-4 bg-secondary/10 border border-border rounded text-center">No pending approval requests. Systems operating autonomously.</p>
              ) : (
                <div className="flex flex-col gap-3">
                  {approvals.map(item => (
                    <div key={item.id} className="p-4 bg-secondary/20 rounded border border-border flex flex-col md:flex-row justify-between items-start md:items-center gap-4 text-xs">
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="font-semibold text-foreground/90">{item.employee}</span>
                          <span className="text-foreground/40 font-mono">({item.id})</span>
                          <span className="px-1.5 py-0.5 rounded bg-warning/20 text-warning text-[9px] font-bold uppercase animate-pulse">Needs human eye</span>
                        </div>
                        <p className="text-foreground/70 mt-1 font-semibold">Action: {item.action}</p>
                        <p className="text-foreground/50 text-[10px] mt-0.5">Target: {item.target} | Workflow: {item.workflow}</p>
                      </div>
                      <div className="flex gap-2 shrink-0">
                        <button 
                          onClick={() => handleApprove(item.id)}
                          className="px-3 py-1.5 bg-success hover:bg-success/90 text-white rounded text-[10px] font-semibold transition-all"
                        >
                          Approve Action
                        </button>
                        <button 
                          onClick={() => handleReject(item.id)}
                          className="px-3 py-1.5 bg-danger hover:bg-danger/90 text-white rounded text-[10px] font-semibold transition-all"
                        >
                          Reject / Block
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Approval History */}
            <div className="flex flex-col gap-3 border-t border-border pt-6 mt-2">
              <h3 className="text-xs font-bold text-foreground/50 uppercase tracking-wider flex items-center gap-1.5">
                <History className="w-3.5 h-3.5" />
                Audit Logs History
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full text-xs text-left">
                  <thead>
                    <tr className="border-b border-border text-foreground/40 uppercase text-[9px] tracking-wider font-semibold">
                      <th className="pb-2">Employee</th>
                      <th className="pb-2">Action Type</th>
                      <th className="pb-2">Target Address</th>
                      <th className="pb-2">Time Decision</th>
                      <th className="pb-2">Authorized By</th>
                      <th className="pb-2">Decision Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border/60">
                    {approvalHistory.map(hist => (
                      <tr key={hist.id} className="hover:bg-secondary/10 transition-all text-foreground/80">
                        <td className="py-3 font-medium">{hist.employee}</td>
                        <td className="py-3">{hist.action}</td>
                        <td className="py-3 font-mono text-[10px] text-foreground/60">{hist.target}</td>
                        <td className="py-3 text-foreground/50">{hist.timestamp}</td>
                        <td className="py-3 font-mono">{hist.authorizedBy}</td>
                        <td className="py-3">
                          <span className={`px-2 py-0.5 rounded text-[9px] font-bold ${
                            hist.status === "Approved" ? "bg-success/20 text-success" : "bg-danger/20 text-danger"
                          }`}>{hist.status}</span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

          </div>
        )}

        {/* POLICY EXPLORER */}
        {activeTab === "policies" && (
          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead>
                <tr className="border-b border-border text-foreground/50 uppercase text-[10px] tracking-wider font-semibold">
                  <th className="pb-3">Action Intercepted</th>
                  <th className="pb-3">Policy Decision</th>
                  <th className="pb-3">Policy Engine Reason</th>
                  <th className="pb-3">Employee</th>
                  <th className="pb-3">Workflow Run</th>
                  <th className="pb-3">Timestamp</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/60">
                {policyDecisions.map(dec => (
                  <tr key={dec.id} className="hover:bg-secondary/15 transition-all text-foreground/80">
                    <td className="py-4 font-mono text-[11px] text-foreground/95">{dec.action}</td>
                    <td className="py-4">
                      <span className={`px-2 py-0.5 rounded text-[9px] font-bold ${
                        dec.decision === "Allowed" ? "bg-success/20 text-success" :
                        dec.decision === "Denied" ? "bg-danger/20 text-danger" :
                        dec.decision === "Escalated" ? "bg-secondary-accent/40 text-foreground" :
                        "bg-warning/20 text-warning"
                      }`}>{dec.decision}</span>
                    </td>
                    <td className="py-4 text-foreground/60">{dec.reason}</td>
                    <td className="py-4">{dec.employee}</td>
                    <td className="py-4 truncate max-w-[150px]">{dec.workflow}</td>
                    <td className="py-4 text-foreground/50">{dec.timestamp}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* INCIDENT CENTER */}
        {activeTab === "incidents" && (
          <div className="flex flex-col gap-6">
            
            {/* Health Alert bar */}
            <div className="p-4 bg-danger/10 border border-danger/30 rounded flex items-center gap-3 text-xs">
              <AlertTriangle className="w-5 h-5 text-danger shrink-0 animate-bounce" />
              <div>
                <p className="font-semibold text-danger">Ongoing Alert: HubSpot API Outage</p>
                <p className="text-foreground/60 mt-0.5">Platform is receiving HTTP 429 Rate Limit responses. Automatic backoff engine is queueing tasks.</p>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead>
                  <tr className="border-b border-border text-foreground/50 uppercase text-[10px] tracking-wider font-semibold">
                    <th className="pb-3">Severity</th>
                    <th className="pb-3">Affected Component</th>
                    <th className="pb-3">Incident Description</th>
                    <th className="pb-3">Occurrence Time</th>
                    <th className="pb-3">Resolution Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border/60">
                  {incidents.map(inc => (
                    <tr key={inc.id} className="hover:bg-secondary/15 transition-all text-foreground/80">
                      <td className="py-4">
                        <span className={`px-2 py-0.5 rounded text-[9px] font-bold ${
                          inc.severity === "Critical" ? "bg-danger/25 text-danger font-extrabold" :
                          inc.severity === "High" ? "bg-orange-500/20 text-orange-400" :
                          "bg-warning/20 text-warning"
                        }`}>{inc.severity}</span>
                      </td>
                      <td className="py-4 font-semibold text-foreground/90">{inc.component}</td>
                      <td className="py-4 text-foreground/60">{inc.issue}</td>
                      <td className="py-4 text-foreground/50">{inc.timestamp}</td>
                      <td className="py-4">
                        <span className={`inline-flex items-center gap-1 text-[10px] font-bold ${
                          inc.status === "Resolved" ? "text-success" : "text-danger animate-pulse"
                        }`}>
                          <span className={`w-1.5 h-1.5 rounded-full ${inc.status === "Resolved" ? "bg-success" : "bg-danger"}`}></span>
                          {inc.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

          </div>
        )}

      </div>
    </div>
  );
}
