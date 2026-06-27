"use client";

import React, { useState } from "react";
import { 
  LineChart,
  TrendingDown,
  Coins,
  Cpu,
  Compass,
  ArrowRight,
  TrendingUp,
  Lightbulb,
  Building2,
  Calendar
} from "lucide-react";

export default function AnalyticsPage() {
  const [timePeriod, setTimePeriod] = useState("month");

  const summary = {
    totalCost: "$142.50",
    savings: "$32.10",
    avgCostPerRun: "$0.14",
    totalTokens: "1,284,000"
  };

  const employeeCosts = [
    { name: "Alex SDR Pro", cost: "$94.50", percentage: 66, runs: 675 },
    { name: "Sarah Recruiter", cost: "$38.20", percentage: 27, runs: 424 },
    { name: "Executive Assistant", cost: "$9.80", percentage: 7, runs: 112 }
  ];

  const capabilityCosts = [
    { name: "SDR Prospecting Research (sdr_research_v1)", cost: "$42.00", percentage: 44 },
    { name: "HubSpot CRM Synchronization (crm_v1)", cost: "$20.25", percentage: 21 },
    { name: "Gmail Communication (email_v1)", cost: "$32.55", percentage: 35 }
  ];

  const toolCosts = [
    { name: "HubSpot CRM API Gateway", cost: "$18.40", percentage: 53 },
    { name: "Google Search API Scraper", cost: "$12.00", percentage: 34 },
    { name: "Gmail SMTP Relay Service", cost: "$2.30", percentage: 7 },
    { name: "Stripe Subscriptions Webhook", cost: "$2.10", percentage: 6 }
  ];

  const modelCosts = [
    { name: "Claude 3.5 Sonnet (Anthropic)", cost: "$88.40", percentage: 62 },
    { name: "GPT-4o (OpenAI)", cost: "$54.10", percentage: 38 }
  ];

  const recommendations = [
    { title: "Enable Prompt Caching on Alex SDR Pro", desc: "SDR web prospecting system prompts are recurring. Caching system directives on Claude 3.5 can save up to $22.40 (15.7%) monthly.", severity: "High Savings" },
    { title: "Downgrade Resume Parsing Model", desc: "Basic OCR and parsing within Sarah Recruiter can be resolved via Claude 3 Haiku / GPT-4o-mini instead of Claude 3.5 Sonnet, saving 42% cost per candidate evaluation.", severity: "Medium Savings" },
    { title: "Eliminate Redundant HubSpot GET Loops", desc: "HubSpot CRM sync currently makes duplicate polling requests inside the sdr_research_v1 capability. Restructuring DB lookups reduces HubSpot rate-limit charges.", severity: "Low Overhead" }
  ];

  return (
    <div className="flex flex-col gap-6 max-w-6xl">
      {/* Title Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-foreground via-foreground/90 to-primary bg-clip-text text-transparent">
            Cost & Usage Analytics
          </h1>
          <p className="text-foreground/60 text-sm mt-1">
            Analyze execution tokens, LLM model costs, third-party API tool costs, and access AI-generated budget recommendations.
          </p>
        </div>
        
        {/* Time selector */}
        <div className="flex gap-1.5 bg-secondary/35 p-1 rounded border border-border text-xs">
          {["week", "month", "year"].map((period) => (
            <button
              key={period}
              onClick={() => setTimePeriod(period)}
              className={`px-3 py-1.5 rounded font-semibold capitalize transition-all ${
                timePeriod === period 
                  ? "bg-primary text-white" 
                  : "text-foreground/60 hover:text-foreground"
              }`}
            >
              {period}
            </button>
          ))}
        </div>
      </div>

      {/* Summary Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-5 rounded-lg bg-card border border-border shadow-sm flex flex-col justify-between">
          <span className="text-[10px] text-foreground/50 font-bold uppercase tracking-wider">Total Monthly Billing</span>
          <div className="mt-3">
            <span className="text-2xl font-bold text-foreground/95">{summary.totalCost}</span>
            <p className="text-[10px] text-foreground/40 mt-1">Due July 01, 2026</p>
          </div>
        </div>
        
        <div className="p-5 rounded-lg bg-card border border-border shadow-sm flex flex-col justify-between">
          <span className="text-[10px] text-foreground/50 font-bold uppercase tracking-wider">Total Savings</span>
          <div className="mt-3">
            <span className="text-2xl font-bold text-success flex items-center gap-1">
              <TrendingDown className="w-5 h-5 text-success" />
              {summary.savings}
            </span>
            <p className="text-[10px] text-success/80 mt-1 font-semibold">18.4% optimization rate</p>
          </div>
        </div>

        <div className="p-5 rounded-lg bg-card border border-border shadow-sm flex flex-col justify-between">
          <span className="text-[10px] text-foreground/50 font-bold uppercase tracking-wider">Avg Cost / Run</span>
          <div className="mt-3">
            <span className="text-2xl font-bold text-foreground/95">{summary.avgCostPerRun}</span>
            <p className="text-[10px] text-foreground/40 mt-1">Based on 1,211 executions</p>
          </div>
        </div>

        <div className="p-5 rounded-lg bg-card border border-border shadow-sm flex flex-col justify-between">
          <span className="text-[10px] text-foreground/50 font-bold uppercase tracking-wider">Tokens Transacted</span>
          <div className="mt-3">
            <span className="text-2xl font-bold text-foreground/95">{summary.totalTokens}</span>
            <p className="text-[10px] text-primary/80 mt-1 font-semibold flex items-center gap-1">
              <Coins className="w-3.5 h-3.5" />
              82% Prompt cache hits
            </p>
          </div>
        </div>
      </div>

      {/* Main Analysis Panels */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Side: Cost Breakdowns */}
        <div className="lg:col-span-2 flex flex-col gap-6">
          
          {/* Employee & Capability cost split */}
          <div className="p-6 rounded-lg bg-card border border-border flex flex-col gap-6 shadow-sm">
            <h2 className="text-sm font-semibold flex items-center gap-2">
              <LineChart className="w-4.5 h-4.5 text-primary" />
              Resource Billing Breakdown
            </h2>

            {/* Employee Billing Grid */}
            <div className="flex flex-col gap-4">
              <h3 className="text-xs font-bold text-foreground/50 uppercase tracking-wider">Cost by AI Employee</h3>
              <div className="flex flex-col gap-3">
                {employeeCosts.map(emp => (
                  <div key={emp.name} className="flex flex-col gap-1.5 text-xs">
                    <div className="flex justify-between font-medium">
                      <span className="text-foreground/90">{emp.name} ({emp.runs} runs)</span>
                      <span className="font-semibold">{emp.cost}</span>
                    </div>
                    <div className="w-full bg-secondary-accent/25 rounded-full h-2 overflow-hidden">
                      <div className="bg-primary h-2 rounded-full" style={{ width: `${emp.percentage}%` }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Capability Billing Grid */}
            <div className="flex flex-col gap-4 border-t border-border pt-6 mt-2">
              <h3 className="text-xs font-bold text-foreground/50 uppercase tracking-wider">Cost by Capability</h3>
              <div className="flex flex-col gap-3">
                {capabilityCosts.map(cap => (
                  <div key={cap.name} className="flex flex-col gap-1.5 text-xs">
                    <div className="flex justify-between font-medium">
                      <span className="text-foreground/80 truncate max-w-sm">{cap.name}</span>
                      <span className="font-semibold">{cap.cost}</span>
                    </div>
                    <div className="w-full bg-secondary-accent/25 rounded-full h-2 overflow-hidden">
                      <div className="bg-indigo-500 h-2 rounded-full" style={{ width: `${cap.percentage}%` }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>

          </div>

        </div>

        {/* Right Side: Tools, Models & Recommendations */}
        <div className="flex flex-col gap-6">
          
          {/* Optimization Suggestions */}
          <div className="p-6 rounded-lg bg-card border border-border flex flex-col gap-4 shadow-sm">
            <h2 className="text-sm font-semibold flex items-center gap-1.5">
              <Lightbulb className="w-4.5 h-4.5 text-warning" />
              Budget Recommendations
            </h2>
            <div className="flex flex-col gap-3">
              {recommendations.map((rec, idx) => (
                <div key={idx} className="p-3 bg-secondary/15 rounded border border-border text-xs flex flex-col gap-1 hover:border-warning/45 transition-all">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-foreground/95">{rec.title}</span>
                    <span className="px-1.5 py-0.5 rounded bg-warning/20 text-warning text-[8px] font-bold uppercase">{rec.severity}</span>
                  </div>
                  <p className="text-foreground/60 text-[10px] leading-relaxed mt-1">{rec.desc}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Model and Tool Billing Shares */}
          <div className="p-6 rounded-lg bg-card border border-border flex flex-col gap-4 shadow-sm text-xs">
            <h2 className="text-sm font-semibold">Integrations & LLM Shares</h2>
            
            {/* LLM Model Split */}
            <div className="flex flex-col gap-2">
              <span className="font-bold text-[10px] text-foreground/50 uppercase tracking-wider">LLM Model API Split</span>
              <div className="flex flex-col gap-2.5">
                {modelCosts.map(m => (
                  <div key={m.name} className="flex items-center justify-between p-2 rounded bg-secondary/10 border border-border/50">
                    <span className="text-foreground/75">{m.name}</span>
                    <span className="font-semibold text-primary">{m.cost} ({m.percentage}%)</span>
                  </div>
                ))}
              </div>
            </div>

            {/* External Tool API Costs */}
            <div className="flex flex-col gap-2 mt-2">
              <span className="font-bold text-[10px] text-foreground/50 uppercase tracking-wider">Tool Connector API Overhead</span>
              <div className="flex flex-col gap-2.5">
                {toolCosts.map(t => (
                  <div key={t.name} className="flex items-center justify-between p-2 rounded bg-secondary/10 border border-border/50">
                    <span className="text-foreground/75 truncate max-w-[120px]">{t.name}</span>
                    <span className="font-semibold">{t.cost} ({t.percentage}%)</span>
                  </div>
                ))}
              </div>
            </div>

          </div>

        </div>

      </div>
    </div>
  );
}
