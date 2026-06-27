"use client";

import React, { useState } from "react";
import { 
  Save, 
  HelpCircle, 
  Check, 
  Sliders, 
  Lock, 
  Calendar,
  Users,
  Search,
  BookOpen,
  Activity,
  Shield,
  TrendingUp,
  Clock,
  Coins,
  History,
  FileCode,
  Heart
} from "lucide-react";

export default function EmployeeBuilderPage() {
  const [activeTab, setActiveTab] = useState("inspector"); // 'inspector' | 'builder-general' | 'builder-caps' | 'builder-scopes'
  const [selectedEmployeeId, setSelectedEmployeeId] = useState("emp-sdr-001");
  const [name, setName] = useState("Alex SDR");
  const [prompt, setPrompt] = useState("You qualify incoming sales prospects using CRM details.");
  const [selectedCaps, setSelectedCaps] = useState<string[]>(["research_v1", "email_v1"]);

  const employees = [
    {
      id: "emp-sdr-001",
      name: "Alex SDR Pro",
      department: "Sales & Outbound",
      status: "Active",
      version: "v2.4.1",
      manifest: {
        id: "sdr-outbound-pro",
        type: "employee",
        version: "2.4.1",
        description: "Qualifies prospect accounts and schedules meetings.",
        author: "QEVN Platform Core",
        license: "MIT License"
      },
      stats: {
        successRate: "94.8%",
        avgCost: "$0.14",
        avgLatency: "8.2s",
        runs: 142
      },
      capabilities: [
        { id: "research_v1", name: "SDR Prospecting Research", desc: "Searches open web registers for decision makers." },
        { id: "crm_v1", name: "HubSpot CRM Synchronization", desc: "Performs CRM client updates and deal tracking." },
        { id: "email_v1", name: "Gmail Communication", desc: "Drafts and dispatches personalized outreach campaigns." }
      ],
      skills: ["web_search", "hubspot_deal_create", "gmail_send_message"],
      knowledgeSources: ["SaaS Prospect Directory", "QEVN Standard Q&A Docs"],
      permissions: ["email:send", "crm:write", "contacts:read"],
      policies: [
        { id: "pol-01", name: "Limit Outbound Email Rates", desc: "Max 50 outreach emails sent per active workspace daily." },
        { id: "pol-02", name: "HubSpot Write Check", desc: "Forbid modifications to accounts marked 'Enterprise Account Manager Owned'." }
      ],
      recentExecutions: [
        { id: "run-sdr-101", goal: "Scan leads from London SaaS companies", status: "Completed", date: "10 mins ago" },
        { id: "run-sdr-102", goal: "Follow-up schedule request with Bob CTO", status: "Awaiting Approval", date: "1 hour ago" },
        { id: "run-sdr-103", goal: "HubSpot contact synch: Alice CEO", status: "Completed", date: "4 hours ago" }
      ]
    },
    {
      id: "emp-recruiter-002",
      name: "Sarah Recruiter",
      department: "Human Resources",
      status: "Active",
      version: "v1.1.0",
      manifest: {
        id: "recruiter-resume-analyst",
        type: "employee",
        version: "1.1.0",
        description: "Extracts profiles from uploaded candidate resumes and matches qualifications.",
        author: "QEVN HR Services",
        license: "Proprietary"
      },
      stats: {
        successRate: "98.2%",
        avgCost: "$0.09",
        avgLatency: "5.4s",
        runs: 84
      },
      capabilities: [
        { id: "resume_parse_v1", name: "Resume Parsing & OCR", desc: "Converts resume PDFs into structured candidate profiles." },
        { id: "email_v1", name: "Gmail Communication", desc: "Drafts interview invites and notifications." }
      ],
      skills: ["pdf_ocr", "candidate_scoring", "gmail_send_message"],
      knowledgeSources: ["Company Job Requirements Catalog"],
      permissions: ["documents:read", "email:send"],
      policies: [
        { id: "pol-rec-01", name: "Confidentiality Filter", desc: "Anonymize candidate PII data fields before vector indexing." }
      ],
      recentExecutions: [
        { id: "run-rec-201", goal: "Evaluate resume: Jane Doe Tech Lead", status: "Completed", date: "3 hours ago" },
        { id: "run-rec-202", goal: "Dispatched reject notice for applicant 12", status: "Completed", date: "1 day ago" }
      ]
    }
  ];

  const selectedEmployee = employees.find(e => e.id === selectedEmployeeId) || employees[0];

  const availableCaps = [
    { id: "research_v1", name: "Research Capability", desc: "Allows searching public web records." },
    { id: "crm_v1", name: "CRM Synchronization", desc: "Allows qualifiers to synchronize lead profiles to HubSpot." },
    { id: "email_v1", name: "Email Communication", desc: "Allows drafting and delivering notification emails." }
  ];

  const handleToggleCap = (id: string) => {
    if (selectedCaps.includes(id)) {
      setSelectedCaps(selectedCaps.filter(c => c !== id));
    } else {
      setSelectedCaps([...selectedCaps, id]);
    }
  };

  const handleSave = () => {
    alert(`Configuration saved successfully! Assigned Capabilities: ${JSON.stringify(selectedCaps)}`);
  };

  return (
    <div className="flex flex-col gap-6 max-w-6xl">
      {/* Title Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-foreground via-foreground/90 to-primary bg-clip-text text-transparent">
            AI Employee Hub
          </h1>
          <p className="text-foreground/60 text-sm mt-1">
            Configure prompt parameters or inspect production runtime manifests, permissions, and health status.
          </p>
        </div>
      </div>

      {/* Selector and Main Panel grid */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        
        {/* Left Sidebar: Select Active Employee or Trigger Builder */}
        <div className="flex flex-col gap-4">
          <div className="p-4 rounded-lg bg-card border border-border flex flex-col gap-3">
            <h2 className="text-xs font-semibold uppercase tracking-wider text-foreground/50">Active Employees</h2>
            <div className="flex flex-col gap-2">
              {employees.map((emp) => (
                <button
                  key={emp.id}
                  onClick={() => {
                    setSelectedEmployeeId(emp.id);
                    setActiveTab("inspector");
                  }}
                  className={`w-full text-left p-3 rounded border text-xs flex flex-col gap-1 transition-all ${
                    selectedEmployeeId === emp.id && activeTab === "inspector"
                      ? "border-primary bg-primary/5"
                      : "border-border hover:bg-secondary/40"
                  }`}
                >
                  <span className="font-semibold text-foreground/90">{emp.name}</span>
                  <div className="flex justify-between text-foreground/50 text-[10px]">
                    <span>{emp.department}</span>
                    <span className="text-primary">{emp.version}</span>
                  </div>
                </button>
              ))}
            </div>

            <div className="border-t border-border pt-3 mt-1">
              <button
                onClick={() => {
                  setActiveTab("builder-general");
                }}
                className="w-full py-2 bg-primary hover:bg-primary/90 text-white rounded text-xs font-semibold flex items-center justify-center gap-1.5 transition-all"
              >
                <Sliders className="w-3.5 h-3.5" />
                Configure New Employee
              </button>
            </div>
          </div>
        </div>

        {/* Right Panel: Content Section */}
        <div className="lg:col-span-3 flex flex-col gap-6">
          
          {/* Sub-Navigation Tabs */}
          <div className="flex border-b border-border bg-card/25 p-1 rounded-t">
            <button
              onClick={() => setActiveTab("inspector")}
              className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold transition-all ${
                activeTab === "inspector" 
                  ? "border-b-2 border-primary text-primary" 
                  : "text-foreground/60 hover:text-foreground"
              }`}
            >
              <Users className="w-4 h-4" />
              Runtime Inspector
            </button>
            
            {activeTab.startsWith("builder") && (
              <>
                <button
                  onClick={() => setActiveTab("builder-general")}
                  className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold transition-all ${
                    activeTab === "builder-general" 
                      ? "border-b-2 border-primary text-primary" 
                      : "text-foreground/60 hover:text-foreground"
                  }`}
                >
                  <Sliders className="w-4 h-4" />
                  General Setup
                </button>
                <button
                  onClick={() => setActiveTab("builder-caps")}
                  className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold transition-all ${
                    activeTab === "builder-caps" 
                      ? "border-b-2 border-primary text-primary" 
                      : "text-foreground/60 hover:text-foreground"
                  }`}
                >
                  <Check className="w-4 h-4" />
                  Select Capabilities
                </button>
              </>
            )}
          </div>

          {/* Tab Contents Panels */}
          <div className="p-6 rounded-lg bg-card border border-border shadow-sm">
            
            {/* INSPECTOR TAB */}
            {activeTab === "inspector" && (
              <div className="flex flex-col gap-6">
                
                {/* Header Metrics */}
                <div className="grid grid-cols-4 gap-4 bg-secondary/15 p-4 rounded border border-border">
                  <div className="flex flex-col gap-0.5">
                    <span className="text-[10px] text-foreground/50 uppercase tracking-wider font-semibold">Success Rate</span>
                    <span className="text-xl font-bold text-success flex items-center gap-1">
                      <TrendingUp className="w-4 h-4" />
                      {selectedEmployee.stats.successRate}
                    </span>
                  </div>
                  <div className="flex flex-col gap-0.5">
                    <span className="text-[10px] text-foreground/50 uppercase tracking-wider font-semibold">Avg Run Cost</span>
                    <span className="text-xl font-bold text-foreground/90">{selectedEmployee.stats.avgCost}</span>
                  </div>
                  <div className="flex flex-col gap-0.5">
                    <span className="text-[10px] text-foreground/50 uppercase tracking-wider font-semibold">Avg Latency</span>
                    <span className="text-xl font-bold text-foreground/90 flex items-center gap-1">
                      <Clock className="w-4 h-4 text-primary" />
                      {selectedEmployee.stats.avgLatency}
                    </span>
                  </div>
                  <div className="flex flex-col gap-0.5">
                    <span className="text-[10px] text-foreground/50 uppercase tracking-wider font-semibold">Total Runs</span>
                    <span className="text-xl font-bold text-foreground/90">{selectedEmployee.stats.runs}</span>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  
                  {/* Left Column: Metadata & Manifest */}
                  <div className="md:col-span-2 flex flex-col gap-6">
                    
                    {/* Manifest */}
                    <div className="flex flex-col gap-2">
                      <h3 className="text-xs font-bold text-foreground/80 flex items-center gap-1.5 uppercase tracking-wider">
                        <FileCode className="w-4 h-4 text-primary" />
                        Marketplace Package Manifest
                      </h3>
                      <div className="p-4 rounded border border-border bg-secondary/20 text-xs flex flex-col gap-2">
                        <div className="flex justify-between border-b border-border/50 pb-1.5">
                          <span className="text-foreground/50">Package ID</span>
                          <span className="font-mono text-foreground/90">{selectedEmployee.manifest.id}</span>
                        </div>
                        <div className="flex justify-between border-b border-border/50 pb-1.5">
                          <span className="text-foreground/50">Version</span>
                          <span>{selectedEmployee.manifest.version}</span>
                        </div>
                        <div className="flex justify-between border-b border-border/50 pb-1.5">
                          <span className="text-foreground/50">Author Publisher</span>
                          <span>{selectedEmployee.manifest.author}</span>
                        </div>
                        <div className="flex justify-between border-b border-border/50 pb-1.5">
                          <span className="text-foreground/50">License</span>
                          <span>{selectedEmployee.manifest.license}</span>
                        </div>
                        <p className="text-foreground/60 mt-1 leading-relaxed">{selectedEmployee.manifest.description}</p>
                      </div>
                    </div>

                    {/* Capabilities & Skills */}
                    <div className="flex flex-col gap-2">
                      <h3 className="text-xs font-bold text-foreground/80 flex items-center gap-1.5 uppercase tracking-wider">
                        <Check className="w-4 h-4 text-primary" />
                        Composed Capabilities ({selectedEmployee.capabilities.length})
                      </h3>
                      <div className="flex flex-col gap-2">
                        {selectedEmployee.capabilities.map(cap => (
                          <div key={cap.id} className="p-3 bg-secondary/10 rounded border border-border text-xs">
                            <p className="font-semibold text-foreground/90">{cap.name}</p>
                            <p className="text-foreground/50 mt-0.5 text-[10px]">{cap.desc}</p>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Security & Access Policies */}
                    <div className="flex flex-col gap-2">
                      <h3 className="text-xs font-bold text-foreground/80 flex items-center gap-1.5 uppercase tracking-wider">
                        <Shield className="w-4 h-4 text-warning" />
                        Workspace Governance Policies
                      </h3>
                      <div className="flex flex-col gap-2">
                        {selectedEmployee.policies.map(pol => (
                          <div key={pol.id} className="p-3 bg-secondary/15 rounded border border-border text-xs flex gap-2">
                            <span className="text-warning font-semibold select-none">⚠️</span>
                            <div>
                              <p className="font-semibold text-foreground/95">{pol.name}</p>
                              <p className="text-foreground/50 text-[10px] mt-0.5">{pol.desc}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                  </div>

                  {/* Right Column: Skills, Memory, Executions */}
                  <div className="flex flex-col gap-6">

                    {/* Permissions Scopes */}
                    <div className="flex flex-col gap-2">
                      <h3 className="text-xs font-bold text-foreground/80 flex items-center gap-1.5 uppercase tracking-wider">
                        <Lock className="w-4 h-4 text-primary" />
                        Bound Scopes
                      </h3>
                      <div className="p-3 rounded border border-border bg-secondary/10 flex flex-wrap gap-1.5">
                        {selectedEmployee.permissions.map(perm => (
                          <span key={perm} className="px-2 py-0.5 rounded bg-secondary-accent/20 border border-border text-[9px] font-mono text-primary">{perm}</span>
                        ))}
                      </div>
                    </div>

                    {/* Vector Database Context */}
                    <div className="flex flex-col gap-2">
                      <h3 className="text-xs font-bold text-foreground/80 flex items-center gap-1.5 uppercase tracking-wider">
                        <BookOpen className="w-4 h-4 text-primary" />
                        Knowledge Bases
                      </h3>
                      <div className="p-3 rounded border border-border bg-secondary/10 flex flex-col gap-1.5 text-xs">
                        {selectedEmployee.knowledgeSources.map(source => (
                          <div key={source} className="flex items-center gap-1.5 text-foreground/75 font-medium">
                            <span className="w-1.5 h-1.5 bg-primary rounded-full"></span>
                            {source}
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Recent Runs list */}
                    <div className="flex flex-col gap-2">
                      <h3 className="text-xs font-bold text-foreground/80 flex items-center gap-1.5 uppercase tracking-wider">
                        <History className="w-4 h-4 text-primary" />
                        Recent Runs
                      </h3>
                      <div className="flex flex-col gap-2">
                        {selectedEmployee.recentExecutions.map(run => (
                          <div key={run.id} className="p-2.5 bg-secondary/20 rounded border border-border flex justify-between items-center text-xs">
                            <div className="truncate max-w-[120px]">
                              <p className="font-semibold text-foreground/90 truncate">{run.goal}</p>
                              <p className="text-[9px] text-foreground/40 mt-0.5">{run.date}</p>
                            </div>
                            <span className={`px-2 py-0.5 rounded-full text-[9px] font-bold ${
                              run.status === "Completed" ? "bg-success/20 text-success" : "bg-warning/20 text-warning"
                            }`}>
                              {run.status === "Completed" ? "Done" : "Pending"}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>

                  </div>
                </div>

              </div>
            )}

            {/* BUILDER SETUP TAB */}
            {activeTab === "builder-general" && (
              <div className="flex flex-col gap-6">
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-semibold">Employee Name</label>
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="p-2 rounded bg-secondary border border-border text-sm max-w-md focus:border-primary/70 outline-none"
                  />
                </div>

                <div className="flex flex-col gap-2">
                  <label className="text-sm font-semibold flex items-center gap-1">
                    System Prompt Instructions
                    <HelpCircle className="w-3.5 h-3.5 text-foreground/40" />
                  </label>
                  <textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    rows={5}
                    className="p-2.5 rounded bg-secondary border border-border text-sm focus:border-primary/70 outline-none resize-none font-mono text-xs leading-relaxed"
                  />
                </div>

                <div className="flex justify-end gap-2 border-t border-border pt-4">
                  <button 
                    onClick={() => setActiveTab("builder-caps")}
                    className="px-4 py-2 bg-primary hover:bg-primary/95 text-white rounded font-medium text-xs transition-all flex items-center gap-1"
                  >
                    Next: Capabilities <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            )}

            {/* BUILDER CAPABILITIES TAB */}
            {activeTab === "builder-caps" && (
              <div className="flex flex-col gap-6">
                <p className="text-xs text-foreground/60">
                  Select the capabilities this employee is authorized to trigger at runtime:
                </p>
                <div className="flex flex-col gap-3">
                  {availableCaps.map((cap) => (
                    <div 
                      key={cap.id}
                      onClick={() => handleToggleCap(cap.id)}
                      className={`p-4 rounded border flex items-center justify-between cursor-pointer transition-all ${
                        selectedCaps.includes(cap.id)
                          ? "border-primary bg-primary/5"
                          : "border-border hover:bg-secondary/40"
                      }`}
                    >
                      <div>
                        <h3 className="text-sm font-semibold">{cap.name}</h3>
                        <p className="text-xs text-foreground/60 mt-1">{cap.desc}</p>
                      </div>
                      <div className={`w-5 h-5 rounded border flex items-center justify-center ${
                        selectedCaps.includes(cap.id) ? "bg-primary border-primary" : "border-border"
                      }`}>
                        {selectedCaps.includes(cap.id) && <Check className="w-3 h-3 text-white" />}
                      </div>
                    </div>
                  ))}
                </div>

                <div className="flex justify-between items-center border-t border-border pt-4 mt-2">
                  <button 
                    onClick={() => setActiveTab("builder-general")}
                    className="px-4 py-2 bg-secondary hover:bg-secondary/80 text-foreground border border-border rounded font-medium text-xs transition-all"
                  >
                    Back to General
                  </button>
                  <button 
                    onClick={handleSave}
                    className="px-4 py-2 bg-primary hover:bg-primary/95 text-white rounded font-medium text-xs transition-all flex items-center gap-1.5"
                  >
                    <Save className="w-4 h-4" />
                    Save Configuration
                  </button>
                </div>
              </div>
            )}

          </div>

        </div>

      </div>
    </div>
  );
}

// Subcomponent Helper
function ArrowRight(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      width="24" 
      height="24" 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke="currentColor" 
      strokeWidth="2" 
      strokeLinecap="round" 
      strokeLinejoin="round" 
      {...props}
    >
      <path d="M5 12h14" />
      <path d="m12 5 7 7-7 7" />
    </svg>
  );
}
