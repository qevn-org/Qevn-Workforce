"use client";

import React, { useState } from "react";
import { 
  Database,
  CheckCircle,
  AlertTriangle,
  Clock,
  Coins,
  Cpu,
  Layers,
  Settings,
  Shield,
  HelpCircle,
  RefreshCw,
  Search,
  BookOpen
} from "lucide-react";

export default function RegistriesPage() {
  const [activeTab, setActiveTab] = useState("capabilities"); // 'capabilities' | 'skills' | 'tools'
  const [searchQuery, setSearchQuery] = useState("");

  const capabilities = [
    { id: "research_v1", name: "SDR Prospecting Research", version: "1.0.0", tools: ["Google Search API", "LinkedIn Scraper"], dependencies: ["web_search"], runtime: "4.2s", cost: "$0.04", health: "100%", consumers: ["Alex SDR Pro"], errorRate: "0.0%" },
    { id: "crm_v1", name: "HubSpot CRM Synchronization", version: "1.2.0", tools: ["HubSpot API"], dependencies: ["hubspot_deal_create", "contacts_read"], runtime: "8.5s", cost: "$0.06", health: "98.4%", consumers: ["Alex SDR Pro"], errorRate: "1.6%" },
    { id: "email_v1", name: "Gmail Communication", version: "2.1.0", tools: ["Gmail API"], dependencies: ["gmail_send_message"], runtime: "2.8s", cost: "$0.02", health: "100%", consumers: ["Alex SDR Pro", "Sarah Recruiter"], errorRate: "0.0%" },
    { id: "resume_parse_v1", name: "Resume Parsing & OCR", version: "1.0.2", tools: ["Document OCR Tool"], dependencies: ["pdf_ocr", "candidate_scoring"], runtime: "5.4s", cost: "$0.05", health: "99.1%", consumers: ["Sarah Recruiter"], errorRate: "0.9%" }
  ];

  const skills = [
    { id: "web_search", name: "Web Search Scraper", version: "1.0.0", inputs: "{ query: string, pages: number }", outputs: "{ results: Array<{title, link, snippet}> }", latency: "1400ms", tools: ["Google Search API"], failureRate: "0.0%" },
    { id: "hubspot_deal_create", name: "HubSpot Deal Create", version: "1.1.0", inputs: "{ company: string, deal_value: number, stage: string }", outputs: "{ deal_id: string, success: boolean }", latency: "2100ms", tools: ["HubSpot API"], failureRate: "2.4%" },
    { id: "gmail_send_message", name: "Gmail Send Message", version: "2.0.0", inputs: "{ to: string, subject: string, body: string }", outputs: "{ message_id: string, success: boolean }", latency: "950ms", tools: ["Gmail API"], failureRate: "0.0%" },
    { id: "pdf_ocr", name: "PDF OCR Scraper", version: "1.0.1", inputs: "{ file_path: string }", outputs: "{ extracted_text: string }", latency: "3800ms", tools: ["Document OCR Tool"], failureRate: "1.1%" },
    { id: "candidate_scoring", name: "Candidate Scoring Parser", version: "1.0.0", inputs: "{ candidate_text: string, job_spec: string }", outputs: "{ score: number, matched_skills: string[] }", latency: "1100ms", tools: ["LLM Matcher"], failureRate: "0.0%" }
  ];

  const tools = [
    { id: "gmail", name: "Gmail SMTP API", provider: "Google Cloud Console", health: "Healthy", rateLimit: "12 / 100 per min", failures: 0, retries: 0, quota: "12% daily quota used" },
    { id: "hubspot", name: "HubSpot Developer Portal CRM", provider: "HubSpot OAuth", health: "Degraded", rateLimit: "85 / 100 per min", failures: 4, retries: 12, quota: "45% daily quota used" },
    { id: "slack", name: "Slack Event Gateway", provider: "Slack App Bot", health: "Healthy", rateLimit: "4 / 60 per min", failures: 0, retries: 0, quota: "1% daily quota used" },
    { id: "calendar", name: "Google Calendar API", provider: "Google Cloud Console", health: "Healthy", rateLimit: "20 / 120 per min", failures: 0, retries: 0, quota: "8% daily quota used" }
  ];

  const filteredCaps = capabilities.filter(c => c.name.toLowerCase().includes(searchQuery.toLowerCase()) || c.id.toLowerCase().includes(searchQuery.toLowerCase()));
  const filteredSkills = skills.filter(s => s.name.toLowerCase().includes(searchQuery.toLowerCase()) || s.id.toLowerCase().includes(searchQuery.toLowerCase()));
  const filteredTools = tools.filter(t => t.name.toLowerCase().includes(searchQuery.toLowerCase()));

  return (
    <div className="flex flex-col gap-6 max-w-6xl">
      {/* Title Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-foreground via-foreground/90 to-primary bg-clip-text text-transparent">
            Capability & Tool Registries
          </h1>
          <p className="text-foreground/60 text-sm mt-1">
            Browse and inspect reusable capabilities, atomic system skills, and third-party connector API configurations.
          </p>
        </div>
        
        {/* Search bar */}
        <div className="relative max-w-xs w-full">
          <Search className="absolute left-3 top-2.5 w-4 h-4 text-foreground/40" />
          <input
            type="text"
            placeholder="Search registry catalogs..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="p-2 pl-9 w-full rounded bg-secondary border border-border text-xs focus:border-primary outline-none"
          />
        </div>
      </div>

      {/* Tabs Row Bar */}
      <div className="flex border-b border-border bg-card/25 p-1 rounded-t">
        <button
          onClick={() => setActiveTab("capabilities")}
          className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold transition-all ${
            activeTab === "capabilities" 
              ? "border-b-2 border-primary text-primary" 
              : "text-foreground/60 hover:text-foreground"
          }`}
        >
          <Layers className="w-4 h-4" />
          Capability Explorer
        </button>
        <button
          onClick={() => setActiveTab("skills")}
          className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold transition-all ${
            activeTab === "skills" 
              ? "border-b-2 border-primary text-primary" 
              : "text-foreground/60 hover:text-foreground"
          }`}
        >
          <Cpu className="w-4 h-4" />
          Skill Explorer
        </button>
        <button
          onClick={() => setActiveTab("tools")}
          className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold transition-all ${
            activeTab === "tools" 
              ? "border-b-2 border-primary text-primary" 
              : "text-foreground/60 hover:text-foreground"
          }`}
        >
          <Settings className="w-4 h-4" />
          Tool Explorer
        </button>
      </div>

      {/* Main Table Content */}
      <div className="p-6 rounded-lg bg-card border border-border shadow-sm">
        
        {/* CAPABILITIES EXPLORER */}
        {activeTab === "capabilities" && (
          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead>
                <tr className="border-b border-border text-foreground/50 uppercase text-[10px] tracking-wider font-semibold">
                  <th className="pb-3">Capability ID & Name</th>
                  <th className="pb-3">Version</th>
                  <th className="pb-3">Bound Tools</th>
                  <th className="pb-3">Avg Latency</th>
                  <th className="pb-3">Cost / Run</th>
                  <th className="pb-3">Consumers</th>
                  <th className="pb-3">Health Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/60">
                {filteredCaps.map(cap => (
                  <tr key={cap.id} className="hover:bg-secondary/15 transition-all">
                    <td className="py-4">
                      <p className="font-semibold text-foreground/90">{cap.name}</p>
                      <p className="text-[10px] text-foreground/40 font-mono mt-0.5">{cap.id}</p>
                    </td>
                    <td className="py-4">{cap.version}</td>
                    <td className="py-4">
                      <div className="flex flex-wrap gap-1">
                        {cap.tools.map(t => (
                          <span key={t} className="px-1.5 py-0.5 rounded bg-secondary-accent/20 border border-border text-[9px] font-medium text-foreground/80">{t}</span>
                        ))}
                      </div>
                    </td>
                    <td className="py-4 font-mono">{cap.runtime}</td>
                    <td className="py-4 font-mono">{cap.cost}</td>
                    <td className="py-4 font-mono">{cap.consumers.join(", ")}</td>
                    <td className="py-4">
                      <span className={`px-2 py-0.5 rounded-full text-[9px] font-bold ${
                        cap.health === "100%" ? "bg-success/20 text-success" : "bg-warning/20 text-warning"
                      }`}>{cap.health} Active</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* SKILLS EXPLORER */}
        {activeTab === "skills" && (
          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead>
                <tr className="border-b border-border text-foreground/50 uppercase text-[10px] tracking-wider font-semibold">
                  <th className="pb-3">Skill ID & Name</th>
                  <th className="pb-3">Inputs Schema</th>
                  <th className="pb-3">Outputs Schema</th>
                  <th className="pb-3">Latency</th>
                  <th className="pb-3">Failure Rate</th>
                  <th className="pb-3">Bound Tools</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/60">
                {filteredSkills.map(skill => (
                  <tr key={skill.id} className="hover:bg-secondary/15 transition-all">
                    <td className="py-4">
                      <p className="font-semibold text-foreground/90">{skill.name}</p>
                      <p className="text-[10px] text-foreground/40 font-mono mt-0.5">{skill.id} (v{skill.version})</p>
                    </td>
                    <td className="py-4 font-mono text-[10px] text-foreground/60 max-w-[200px] truncate" title={skill.inputs}>{skill.inputs}</td>
                    <td className="py-4 font-mono text-[10px] text-foreground/60 max-w-[200px] truncate" title={skill.outputs}>{skill.outputs}</td>
                    <td className="py-4 font-mono">{skill.latency}</td>
                    <td className="py-4 text-danger font-mono font-semibold">{skill.failureRate}</td>
                    <td className="py-4">
                      <div className="flex flex-wrap gap-1">
                        {skill.tools.map(t => (
                          <span key={t} className="px-1.5 py-0.5 bg-secondary-accent/20 border border-border text-[9px] font-medium text-foreground/80 rounded">{t}</span>
                        ))}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* TOOL EXPLORER */}
        {activeTab === "tools" && (
          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead>
                <tr className="border-b border-border text-foreground/50 uppercase text-[10px] tracking-wider font-semibold">
                  <th className="pb-3">Tool Name & Credentials</th>
                  <th className="pb-3">Provider</th>
                  <th className="pb-3">Rate Limit Remaining</th>
                  <th className="pb-3">Failures</th>
                  <th className="pb-3">Automatic Retries</th>
                  <th className="pb-3">Quota Usage</th>
                  <th className="pb-3">Connection Health</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/60">
                {filteredTools.map(tool => (
                  <tr key={tool.id} className="hover:bg-secondary/15 transition-all">
                    <td className="py-4">
                      <p className="font-semibold text-foreground/90">{tool.name}</p>
                      <p className="text-[10px] text-foreground/40 font-mono mt-0.5">{tool.id}</p>
                    </td>
                    <td className="py-4 text-foreground/70">{tool.provider}</td>
                    <td className="py-4 font-mono">{tool.rateLimit}</td>
                    <td className="py-4 font-mono font-semibold text-danger">{tool.failures}</td>
                    <td className="py-4 font-mono">{tool.retries}</td>
                    <td className="py-4 font-semibold text-primary">{tool.quota}</td>
                    <td className="py-4">
                      <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full font-bold text-[9px] ${
                        tool.health === "Healthy" ? "bg-success/20 text-success" : "bg-warning/20 text-warning"
                      }`}>
                        <span className={`w-1.5 h-1.5 rounded-full ${tool.health === "Healthy" ? "bg-success" : "bg-warning"}`}></span>
                        {tool.health}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

      </div>
    </div>
  );
}
