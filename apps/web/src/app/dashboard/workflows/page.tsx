"use client";

import React, { useState } from "react";
import { 
  GitBranch, 
  Play, 
  Pause, 
  RotateCcw, 
  Clock, 
  Coins, 
  HelpCircle,
  Database,
  Shield,
  CheckCircle,
  AlertTriangle,
  ChevronRight,
  ChevronDown,
  ArrowRight,
  Code
} from "lucide-react";

export default function WorkflowsPage() {
  const [activeTab, setActiveTab] = useState("explorer"); // 'explorer' | 'replay'
  const [selectedRunId, setSelectedRunId] = useState("run-sdr-101");
  const [replayStep, setReplayStep] = useState(0);

  const workflowRuns = [
    {
      id: "run-sdr-101",
      employee: "Alex SDR Pro",
      goal: "Find prospect decision makers in London SaaS and qualify CRM leads",
      status: "Running",
      startTime: "10 mins ago",
      duration: "1m 45s",
      cost: "$0.18",
      steps: [
        {
          id: "step-1",
          type: "planner",
          title: "Supervisor Planner Decision",
          desc: "Plan formulated: Query web records for SaaS companies in London with 20-100 employee count, filter prospects, score via lead qualifier capability, and synchronize HubSpot records.",
          timestamp: "10:14:02 AM"
        },
        {
          id: "step-2",
          type: "capability",
          title: "Invoke: SDR Prospecting Research (sdr_research_v1)",
          desc: "Dispatched search request parameters to capability worker.",
          timestamp: "10:14:05 AM"
        },
        {
          id: "step-3",
          type: "skill",
          title: "Execute: web_search skill",
          desc: "Triggered search engine scrape for 'London SaaS companies 20-100 employees'.",
          timestamp: "10:14:08 AM"
        },
        {
          id: "step-4",
          type: "tool",
          title: "Tool Call: Google Search API",
          desc: "Query: 'site:linkedin.com/company London SaaS 20-100'. Response: 12 potential leads found.",
          timestamp: "10:14:12 AM"
        },
        {
          id: "step-5",
          type: "memory",
          title: "Memory OS Write: Save prospects profile list",
          desc: "Stored 4 qualified prospect matches in conversation short-term context cache.",
          timestamp: "10:14:18 AM"
        },
        {
          id: "step-6",
          type: "policy",
          title: "Policy Engine: Outbound Check",
          desc: "Decision: ALLOW. Reason: Verified outbound domains are not on the tenant blocklist.",
          timestamp: "10:15:20 AM"
        },
        {
          id: "step-7",
          type: "approval",
          title: "⚠️ Awaiting Approval Checkpoint",
          desc: "Supervisor intercepted: Requires manual human approval before initiating Gmail send_message to contact@targetsaas.com.",
          timestamp: "10:15:35 AM",
          pending: true
        }
      ],
      checkpoints: [
        { step: 0, node: "Planner init", state: { goal: "SaaS London", loop_count: 0 } },
        { step: 1, node: "sdr_research_v1", state: { leads_scraped: 4, scored: [] } },
        { step: 2, node: "HubSpot sync", state: { leads_scraped: 4, synced: 4, deal_stage: "Lead Created" } },
        { step: 3, node: "Gmail approval", state: { awaiting_manual: true, emails_drafted: 1 } }
      ]
    },
    {
      id: "run-rec-202",
      employee: "Sarah Recruiter",
      goal: "Analyze resumes and rank candidates for Staff TS role",
      status: "Completed",
      startTime: "2 hours ago",
      duration: "42s",
      cost: "$0.08",
      steps: [
        {
          id: "step-r1",
          type: "planner",
          title: "Supervisor Planner Decision",
          desc: "Plan: OCR input resume PDF documents, score against Staff TS prompt bounds, cache candidate context.",
          timestamp: "08:12:10 AM"
        },
        {
          id: "step-r2",
          type: "capability",
          title: "Invoke: Resume OCR parsing",
          desc: "Parsed document payload successfully.",
          timestamp: "08:12:15 AM"
        },
        {
          id: "step-r3",
          type: "memory",
          title: "Memory OS Read: Load Job Specs Catalog",
          desc: "Loaded 12 job specifications from organization vector database.",
          timestamp: "08:12:20 AM"
        },
        {
          id: "step-r4",
          type: "policy",
          title: "Policy Engine: PII Masking Filter",
          desc: "Decision: ALLOW. Reason: Candidate emails and phones masked before saving embedding vectors.",
          timestamp: "08:12:28 AM"
        },
        {
          id: "step-r5",
          type: "success",
          title: "Workflow Completed",
          desc: "Candidate qualified with rating 94% and synchronized to workspace applicant pool.",
          timestamp: "08:12:52 AM"
        }
      ],
      checkpoints: [
        { step: 0, node: "Planner OCR init", state: { file: "jane_resume.pdf" } },
        { step: 1, node: "OCR read", state: { parsed_text_size: 4200 } },
        { step: 2, node: "Evaluation", state: { match_percentage: 94, skills_matched: ["React", "Rust"] } }
      ]
    }
  ];

  const selectedRun = workflowRuns.find(r => r.id === selectedRunId) || workflowRuns[0];

  const handleApprove = () => {
    alert("Manual approval granted. Resuming workflow engine...");
  };

  const handleReject = () => {
    alert("Outbound outreach rejected. Suspending workflow execution.");
  };

  return (
    <div className="flex flex-col gap-6 max-w-6xl">
      {/* Title Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-foreground via-foreground/90 to-primary bg-clip-text text-transparent">
          Workflows & Orchestrations
        </h1>
        <p className="text-foreground/60 text-sm mt-1">
          Explore step-by-step orchestrator execution timelines, verify planner actions, or replay checkpoints in sandbox mode.
        </p>
      </div>

      {/* Tabs Row Bar */}
      <div className="flex border-b border-border bg-card/25 p-1 rounded-t">
        <button
          onClick={() => setActiveTab("explorer")}
          className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold transition-all ${
            activeTab === "explorer" 
              ? "border-b-2 border-primary text-primary" 
              : "text-foreground/60 hover:text-foreground"
          }`}
        >
          <GitBranch className="w-4 h-4" />
          Workflow Explorer
        </button>
        <button
          onClick={() => {
            setActiveTab("replay");
            setReplayStep(0);
          }}
          className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold transition-all ${
            activeTab === "replay" 
              ? "border-b-2 border-primary text-primary" 
              : "text-foreground/60 hover:text-foreground"
          }`}
        >
          <RotateCcw className="w-4 h-4" />
          Replay Debugger (Checkpoint Sandboxing)
        </button>
      </div>

      {/* Selector and Main Panel Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        
        {/* Left Sidebar: Select active running / completed executions */}
        <div className="flex flex-col gap-4">
          <div className="p-4 rounded-lg bg-card border border-border flex flex-col gap-3">
            <h2 className="text-xs font-semibold uppercase tracking-wider text-foreground/50">Execution List</h2>
            <div className="flex flex-col gap-2">
              {workflowRuns.map((run) => (
                <button
                  key={run.id}
                  onClick={() => setSelectedRunId(run.id)}
                  className={`w-full text-left p-3 rounded border text-xs flex flex-col gap-1 transition-all ${
                    selectedRunId === run.id
                      ? "border-primary bg-primary/5"
                      : "border-border hover:bg-secondary/40"
                  }`}
                >
                  <span className="font-semibold text-foreground/90">{run.employee}</span>
                  <p className="text-[10px] text-foreground/50 truncate max-w-full">{run.goal}</p>
                  <div className="flex justify-between items-center text-[10px] mt-1.5">
                    <span className={`px-1.5 py-0.5 rounded-full font-bold text-[8px] uppercase ${
                      run.status === "Completed" ? "bg-success/20 text-success" : "bg-primary/20 text-primary animate-pulse"
                    }`}>{run.status}</span>
                    <span className="text-foreground/40">{run.startTime}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Right Main Panel */}
        <div className="lg:col-span-3">

          {/* EXPLORER VIEW */}
          {activeTab === "explorer" && (
            <div className="flex flex-col gap-6">
              
              {/* Header summary metadata */}
              <div className="p-5 rounded-lg bg-card border border-border grid grid-cols-4 gap-4 text-xs">
                <div className="flex flex-col gap-0.5">
                  <span className="text-foreground/50">Status</span>
                  <span className="font-semibold text-primary">{selectedRun.status}</span>
                </div>
                <div className="flex flex-col gap-0.5">
                  <span className="text-foreground/50">Execution Time</span>
                  <span className="font-semibold">{selectedRun.duration}</span>
                </div>
                <div className="flex flex-col gap-0.5">
                  <span className="text-foreground/50">Accumulated Cost</span>
                  <span className="font-semibold">{selectedRun.cost}</span>
                </div>
                <div className="flex flex-col gap-0.5">
                  <span className="text-foreground/50">Checkpoints Logged</span>
                  <span className="font-semibold">{selectedRun.checkpoints.length} Saved</span>
                </div>
              </div>

              {/* Timeline nodes wrapper */}
              <div className="p-6 rounded-lg bg-card border border-border flex flex-col gap-6 relative shadow-sm">
                <h3 className="text-sm font-semibold flex items-center gap-2">
                  <GitBranch className="w-4 h-4 text-primary" />
                  Visual Execution Timeline logs
                </h3>

                {/* Timeline vertical bar */}
                <div className="absolute left-9 top-16 bottom-8 w-0.5 bg-secondary-accent/20" />

                <div className="flex flex-col gap-6">
                  {selectedRun.steps.map((step, idx) => {
                    const iconColor = 
                      step.type === "planner" ? "bg-purple-500/20 text-purple-400 border-purple-500/50" :
                      step.type === "capability" ? "bg-primary/20 text-primary border-primary/50" :
                      step.type === "skill" ? "bg-indigo-500/20 text-indigo-400 border-indigo-500/50" :
                      step.type === "tool" ? "bg-teal-500/20 text-teal-400 border-teal-500/50" :
                      step.type === "memory" ? "bg-blue-500/20 text-blue-400 border-blue-500/50" :
                      step.type === "policy" ? "bg-amber-500/20 text-amber-400 border-amber-500/50" :
                      step.type === "success" ? "bg-success/20 text-success border-success/50" :
                      "bg-warning/20 text-warning border-warning/50";

                    return (
                      <div key={step.id} className="flex gap-4 relative z-10">
                        {/* Bullet Circle */}
                        <div className={`w-8 h-8 rounded-full border flex items-center justify-center font-mono text-[10px] font-bold shrink-0 ${iconColor}`}>
                          {idx + 1}
                        </div>

                        {/* Content text */}
                        <div className="p-4 rounded border border-border bg-secondary/15 flex-1 flex flex-col gap-1.5 hover:border-primary/30 transition-all text-xs">
                          <div className="flex justify-between items-center">
                            <span className="font-semibold text-foreground/90 uppercase tracking-wide text-[10px]">{step.title}</span>
                            <span className="text-[9px] text-foreground/40">{step.timestamp}</span>
                          </div>
                          <p className="text-foreground/75 leading-relaxed">{step.desc}</p>
                          
                          {/* Approval gates trigger actions inline */}
                          {(step as any).pending && (
                            <div className="flex gap-2 mt-2 pt-2 border-t border-border/50">
                              <button 
                                onClick={handleApprove}
                                className="px-3 py-1 bg-success hover:bg-success/90 text-white rounded text-[10px] font-semibold transition-all"
                              >
                                Approve Outreach
                              </button>
                              <button 
                                onClick={handleReject}
                                className="px-3 py-1 bg-danger hover:bg-danger/90 text-white rounded text-[10px] font-semibold transition-all"
                              >
                                Deny / Suspend
                              </button>
                            </div>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>

              </div>

            </div>
          )}

          {/* REPLAY MODE VIEW */}
          {activeTab === "replay" && (
            <div className="flex flex-col gap-6">
              
              {/* Checkpoint Stepper Controller */}
              <div className="p-6 rounded-lg bg-card border border-border flex flex-col gap-4 shadow-sm">
                <div className="flex justify-between items-center">
                  <h3 className="text-sm font-semibold flex items-center gap-2">
                    <RotateCcw className="w-4 h-4 text-primary" />
                    State Checkpoint Sandbox Stepper
                  </h3>
                  <span className="text-xs text-warning font-semibold bg-warning/15 px-2 py-0.5 rounded">
                    Replay Mode Active (Sandbox)
                  </span>
                </div>
                
                <p className="text-xs text-foreground/60">
                  Select a past logged checkpoint snapshot from PostgreSQL database and replay the state transitions locally in-memory without initiating actual tool side-effects.
                </p>

                {/* Control bar */}
                <div className="flex gap-3 items-center bg-secondary/25 p-4 rounded border border-border mt-2">
                  <button 
                    disabled={replayStep === 0}
                    onClick={() => setReplayStep(Math.max(0, replayStep - 1))}
                    className="p-2 bg-secondary border border-border rounded text-xs hover:bg-secondary-accent/20 disabled:opacity-40 disabled:hover:bg-secondary transition-all"
                  >
                    ⏮️ Prev Step
                  </button>
                  
                  <div className="flex-1 flex justify-center gap-2 text-xs font-semibold">
                    <span>Checkpoint {replayStep + 1} of {selectedRun.checkpoints.length}</span>
                    <span className="text-primary font-mono font-bold">[{selectedRun.checkpoints[replayStep].node}]</span>
                  </div>

                  <button 
                    disabled={replayStep === selectedRun.checkpoints.length - 1}
                    onClick={() => setReplayStep(Math.min(selectedRun.checkpoints.length - 1, replayStep + 1))}
                    className="p-2 bg-secondary border border-border rounded text-xs hover:bg-secondary-accent/20 disabled:opacity-40 disabled:hover:bg-secondary transition-all"
                  >
                    Next Step ⏭️
                  </button>
                </div>
              </div>

              {/* State inspector panel */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                
                {/* Checkpoint Metadata */}
                <div className="p-6 rounded-lg bg-card border border-border flex flex-col gap-3">
                  <h4 className="text-xs font-bold text-foreground/80 flex items-center gap-1.5 uppercase tracking-wider">
                    <Database className="w-4.5 h-4.5 text-primary" />
                    Checkpoint Variables State
                  </h4>
                  <div className="p-4 bg-secondary/15 rounded border border-border font-mono text-xs overflow-x-auto flex-1 max-h-80">
                    <pre className="text-foreground/80">
                      {JSON.stringify(selectedRun.checkpoints[replayStep].state, null, 2)}
                    </pre>
                  </div>
                </div>

                {/* Replay Console output */}
                <div className="p-6 rounded-lg bg-[#030303] text-foreground font-mono border border-border flex flex-col gap-3 shadow-md">
                  <h4 className="text-xs font-bold text-foreground/50 flex items-center gap-1.5 uppercase tracking-wider">
                    <Code className="w-4.5 h-4.5 text-success" />
                    Sandbox Execution Console
                  </h4>
                  <div className="flex-1 p-3 bg-black rounded text-[11px] leading-relaxed text-success flex flex-col gap-1.5 min-h-[220px]">
                    <p className="text-foreground/40">[{new Date().toLocaleTimeString()}] Initializing sandbox frame...</p>
                    <p className="text-foreground/40">[{new Date().toLocaleTimeString()}] Restoring database checkpoint for step {replayStep}...</p>
                    <p className="text-success font-semibold">
                      [Replay Simulation] Step {replayStep} successfully loaded. Currently executing Node: {selectedRun.checkpoints[replayStep].node}
                    </p>
                    <p className="text-success">
                      [Verification Sandbox] Intercepting all write side-effects. HubSpot and Gmail calls will bypass real endpoints and match stored payloads.
                    </p>
                    <p className="text-success font-bold mt-2">✅ Dry-run evaluation: Ready.</p>
                  </div>
                </div>

              </div>

            </div>
          )}

        </div>

      </div>
    </div>
  );
}
