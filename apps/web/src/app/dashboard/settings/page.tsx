"use client";

import React, { useState } from "react";
import { 
  Settings,
  Sliders,
  Shield,
  HelpCircle,
  ToggleLeft,
  Building2,
  Lock,
  Cpu,
  Save,
  Check
} from "lucide-react";

export default function SettingsFlagsPage() {
  const [activeTab, setActiveTab] = useState("flags"); // 'flags' | 'workspace' | 'keys'
  const [organization, setOrganization] = useState("QEVN Technology");
  
  // Feature Flags States
  const [flags, setFlags] = useState({
    empSdrPro: true,
    empRecruiter: true,
    capResearchV2: false,
    capEmailV2: true,
    skillGoogleSearchApi: true,
    skillOcrDocumentScan: false,
    routingLangGraphSupervisor: true,
    reflectionMemoryOS: false,
    automaticBackoffRetries: true
  });

  const handleToggle = (key: keyof typeof flags) => {
    setFlags({
      ...flags,
      [key]: !flags[key]
    });
  };

  const handleSaveWorkspace = () => {
    alert("Workspace general settings saved successfully.");
  };

  return (
    <div className="flex flex-col gap-6 max-w-4xl">
      {/* Title Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-foreground via-foreground/90 to-primary bg-clip-text text-transparent">
            Settings & Feature Flags
          </h1>
          <p className="text-foreground/60 text-sm mt-1">
            Manage experimental feature rollouts, toggle active employees and skills, and update organization API keys.
          </p>
        </div>
      </div>

      {/* Tabs Row Bar */}
      <div className="flex border-b border-border bg-card/25 p-1 rounded-t">
        <button
          onClick={() => setActiveTab("flags")}
          className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold transition-all ${
            activeTab === "flags" 
              ? "border-b-2 border-primary text-primary" 
              : "text-foreground/60 hover:text-foreground"
          }`}
        >
          <Sliders className="w-4 h-4" />
          Feature Flags
        </button>
        <button
          onClick={() => setActiveTab("workspace")}
          className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold transition-all ${
            activeTab === "workspace" 
              ? "border-b-2 border-primary text-primary" 
              : "text-foreground/60 hover:text-foreground"
          }`}
        >
          <Building2 className="w-4 h-4" />
          Workspace Settings
        </button>
        <button
          onClick={() => setActiveTab("keys")}
          className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold transition-all ${
            activeTab === "keys" 
              ? "border-b-2 border-primary text-primary" 
              : "text-foreground/60 hover:text-foreground"
          }`}
        >
          <Lock className="w-4 h-4" />
          LLM & API Credentials
        </button>
      </div>

      {/* Main Content Area */}
      <div className="p-6 rounded-lg bg-card border border-border shadow-sm">
        
        {/* FEATURE FLAGS */}
        {activeTab === "flags" && (
          <div className="flex flex-col gap-6">
            
            {/* AI Employees Rollout */}
            <div className="flex flex-col gap-4">
              <h3 className="text-xs font-bold text-foreground/50 uppercase tracking-wider">AI Employee Access Control</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded border border-border bg-secondary/15 flex justify-between items-center text-xs">
                  <div>
                    <p className="font-semibold text-foreground/90">Alex SDR Pro Rollout</p>
                    <p className="text-[10px] text-foreground/45 mt-0.5">Authorizes outbound email & CRM tools.</p>
                  </div>
                  <button 
                    onClick={() => handleToggle("empSdrPro")}
                    className={`w-11 h-6 rounded-full transition-all relative ${flags.empSdrPro ? "bg-primary" : "bg-secondary-accent/40"}`}
                  >
                    <span className={`absolute top-1 left-1 bg-white w-4 h-4 rounded-full transition-all ${flags.empSdrPro ? "translate-x-5" : ""}`} />
                  </button>
                </div>

                <div className="p-4 rounded border border-border bg-secondary/15 flex justify-between items-center text-xs">
                  <div>
                    <p className="font-semibold text-foreground/90">Sarah Recruiter Rollout</p>
                    <p className="text-[10px] text-foreground/45 mt-0.5">Authorizes document parsing & scoring.</p>
                  </div>
                  <button 
                    onClick={() => handleToggle("empRecruiter")}
                    className={`w-11 h-6 rounded-full transition-all relative ${flags.empRecruiter ? "bg-primary" : "bg-secondary-accent/40"}`}
                  >
                    <span className={`absolute top-1 left-1 bg-white w-4 h-4 rounded-full transition-all ${flags.empRecruiter ? "translate-x-5" : ""}`} />
                  </button>
                </div>
              </div>
            </div>

            {/* Experimental Platform Features */}
            <div className="flex flex-col gap-4 border-t border-border pt-6 mt-2">
              <h3 className="text-xs font-bold text-foreground/50 uppercase tracking-wider">Orchestrator Experimental Rollouts</h3>
              <div className="flex flex-col gap-3">
                
                <div className="p-4 rounded border border-border bg-secondary/10 flex justify-between items-center text-xs">
                  <div>
                    <p className="font-semibold text-foreground/95 flex items-center gap-1.5">
                      Dynamic LangGraph Supervisor Routing
                      <span className="px-1.5 py-0.5 rounded bg-primary/20 text-primary text-[8px] font-bold uppercase">Stable</span>
                    </p>
                    <p className="text-[10px] text-foreground/50 mt-0.5">Utilizes supervisor LLM planning steps instead of static routing chains.</p>
                  </div>
                  <button 
                    onClick={() => handleToggle("routingLangGraphSupervisor")}
                    className={`w-11 h-6 rounded-full transition-all relative ${flags.routingLangGraphSupervisor ? "bg-primary" : "bg-secondary-accent/40"}`}
                  >
                    <span className={`absolute top-1 left-1 bg-white w-4 h-4 rounded-full transition-all ${flags.routingLangGraphSupervisor ? "translate-x-5" : ""}`} />
                  </button>
                </div>

                <div className="p-4 rounded border border-border bg-secondary/10 flex justify-between items-center text-xs">
                  <div>
                    <p className="font-semibold text-foreground/95 flex items-center gap-1.5">
                      Reflection Memory OS Engine
                      <span className="px-1.5 py-0.5 rounded bg-warning/20 text-warning text-[8px] font-bold uppercase">Experimental</span>
                    </p>
                    <p className="text-[10px] text-foreground/50 mt-0.5">Runs offline LLM reflection steps over conversation memory pools to extract behavioral rules.</p>
                  </div>
                  <button 
                    onClick={() => handleToggle("reflectionMemoryOS")}
                    className={`w-11 h-6 rounded-full transition-all relative ${flags.reflectionMemoryOS ? "bg-primary" : "bg-secondary-accent/40"}`}
                  >
                    <span className={`absolute top-1 left-1 bg-white w-4 h-4 rounded-full transition-all ${flags.reflectionMemoryOS ? "translate-x-5" : ""}`} />
                  </button>
                </div>

                <div className="p-4 rounded border border-border bg-secondary/10 flex justify-between items-center text-xs">
                  <div>
                    <p className="font-semibold text-foreground/95 flex items-center gap-1.5">
                      Automatic Tool Fallback Backoff Retries
                      <span className="px-1.5 py-0.5 rounded bg-primary/20 text-primary text-[8px] font-bold uppercase">Stable</span>
                    </p>
                    <p className="text-[10px] text-foreground/50 mt-0.5">Applies exponential backoff jitter on 429 and connection rate limit failures.</p>
                  </div>
                  <button 
                    onClick={() => handleToggle("automaticBackoffRetries")}
                    className={`w-11 h-6 rounded-full transition-all relative ${flags.automaticBackoffRetries ? "bg-primary" : "bg-secondary-accent/40"}`}
                  >
                    <span className={`absolute top-1 left-1 bg-white w-4 h-4 rounded-full transition-all ${flags.automaticBackoffRetries ? "translate-x-5" : ""}`} />
                  </button>
                </div>

              </div>
            </div>

          </div>
        )}

        {/* WORKSPACE SETTINGS */}
        {activeTab === "workspace" && (
          <div className="flex flex-col gap-6 text-xs">
            <div className="flex flex-col gap-2">
              <label className="text-sm font-semibold">Workspace / Organization Name</label>
              <input
                type="text"
                value={organization}
                onChange={(e) => setOrganization(e.target.value)}
                className="p-2 rounded bg-secondary border border-border text-sm max-w-md focus:border-primary outline-none"
              />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-sm font-semibold">Active Tenant ID</label>
              <input
                type="text"
                readOnly
                value="uuid-org-999888-aaabbb-ccc123"
                className="p-2 rounded bg-secondary-accent/25 border border-border text-sm max-w-md font-mono text-foreground/50 outline-none"
              />
            </div>

            <div className="flex justify-end gap-2 border-t border-border pt-4">
              <button 
                onClick={handleSaveWorkspace}
                className="px-4 py-2 bg-primary hover:bg-primary/95 text-white rounded font-medium text-xs transition-all flex items-center gap-1.5"
              >
                <Save className="w-4 h-4" />
                Save Changes
              </button>
            </div>
          </div>
        )}

        {/* CREDENTIALS */}
        {activeTab === "keys" && (
          <div className="flex flex-col gap-6 text-xs">
            <p className="text-[10px] text-foreground/50 leading-relaxed bg-secondary/30 p-3 rounded border border-border">
              🔑 Decrypted API credentials are saved inside HashiCorp Vault. The gateway references vaults using organization IAM bindings. Secret keys are never logged or stored in plain-text databases.
            </p>
            
            <div className="flex flex-col gap-2">
              <label className="text-sm font-semibold">Anthropic API Key</label>
              <input
                type="password"
                placeholder="sk-ant-••••••••••••••••"
                className="p-2 rounded bg-secondary border border-border text-sm max-w-md focus:border-primary outline-none"
              />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-sm font-semibold">OpenAI API Key</label>
              <input
                type="password"
                placeholder="sk-proj-••••••••••••••••"
                className="p-2 rounded bg-secondary border border-border text-sm max-w-md focus:border-primary outline-none"
              />
            </div>

            <div className="flex justify-end gap-2 border-t border-border pt-4">
              <button 
                onClick={() => alert("Credentials saved successfully.")}
                className="px-4 py-2 bg-primary hover:bg-primary/95 text-white rounded font-medium text-xs transition-all flex items-center gap-1.5"
              >
                <Save className="w-4 h-4" />
                Save API Keys
              </button>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
