"use client";

import React, { useState } from "react";
import AgentTerminal from "../../components/AgentTerminal";

import { 
  Users, 
  Play, 
  Activity, 
  Coins, 
  AlertCircle,
  TrendingUp,
  Cpu,
  Clock,
  Database,
  ArrowRight,
  RefreshCw,
  Gauge,
  CheckCircle,
  AlertTriangle
} from "lucide-react";

export default function DashboardPage() {
  const [retryQueue, setRetryQueue] = useState([
    { id: "retry-01", employee: "Alex SDR", goal: "CRM syncing leads to HubSpot", attempt: "2/5", backoff: "45s remaining", reason: "HubSpot API Rate Limit" },
    { id: "retry-02", employee: "Sarah Recruiter", goal: "Gmail deliver resume review summary", attempt: "1/5", backoff: "12s remaining", reason: "SMTP Handshake Timeout" }
  ]);

  const stats = [
    { name: "Active Employees", value: "6 Online", change: "99.9% Up-time", icon: Users, desc: "SDR, Recruiter, Calendar EA active" },
    { name: "Running Workflows", value: "3 Running", change: "1 Queued, 0 Failed", icon: Play, desc: "Real-time state orchestration" },
    { name: "Average Latency & Cost", value: "11.2s / $0.18", change: "18% optimization savings", icon: Clock, desc: "Cache-optimized routing" },
    { name: "Tokens & Memory", value: "164,800 Tx", change: "82% Cache Hit Rate", icon: Cpu, desc: "Memory OS Provider Active" }
  ];

  const recentRuns = [
    { id: "run-01", employee: "Alex (SDR)", goal: "Qualify prospect leads from London SaaS campaigns", status: "Running", time: "Just now", progress: 75 },
    { id: "run-02", employee: "Sarah (Recruiter)", goal: "Extract candidates matching Staff TS architect role", status: "Completed", time: "12 min ago", progress: 100 },
    { id: "run-03", employee: "Executive Assistant", goal: "Reschedule calendar conflicts on HubSpot meeting links", status: "Awaiting Approval", time: "1 hour ago", progress: 40 },
    { id: "run-04", employee: "Operations Manager", goal: "Compile weekly slack delivery reports", status: "Failed", time: "3 hours ago", progress: 90 }
  ];

  const toolHealth = [
    { name: "Gmail Connector", status: "Healthy", latency: "142ms", rate: "12/100 min" },
    { name: "HubSpot CRM Integration", status: "Degraded", latency: "1840ms", rate: "85/100 min" },
    { name: "Slack Event Gateway", status: "Healthy", latency: "89ms", rate: "4/60 min" },
    { name: "Calendar API", status: "Healthy", latency: "115ms", rate: "20/120 min" }
  ];

  const handleTriggerRetry = (id: string) => {
    setRetryQueue(retryQueue.filter((item) => item.id !== id));
  };

  return (
    <div className="flex flex-col gap-8 max-w-6xl">
      {/* Title Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-foreground via-foreground/90 to-primary bg-clip-text text-transparent">
          Operations Dashboard
        </h1>
        <p className="text-foreground/60 text-sm mt-1">
          Monitor running workflows, view active retry queues, observe token costs, and check external integration health.
        </p>
      </div>

      {/* Stats Cards Panel */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <div 
            key={stat.name}
            className="p-6 rounded-lg bg-card border border-border flex flex-col justify-between hover:border-primary/50 transition-all cursor-default shadow-md"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs text-foreground/60 font-semibold uppercase tracking-wider">{stat.name}</span>
              <stat.icon className="w-5 h-5 text-primary" />
            </div>
            <div className="mt-4">
              <span className="text-2xl font-bold tracking-tight">{stat.value}</span>
              <p className="text-[11px] text-primary/90 mt-1 flex items-center gap-1 font-medium">
                <TrendingUp className="w-3 h-3 text-primary" />
                {stat.change}
              </p>
              <p className="text-[10px] text-foreground/40 mt-1">{stat.desc}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Main Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Column: Workflows Stream & Retry Queue */}
        <div className="lg:col-span-2 flex flex-col gap-6">
          
          {/* Active Workflows Panel */}
          <div className="p-6 rounded-lg bg-card border border-border flex flex-col gap-4 shadow-sm">
            <div className="flex justify-between items-center">
              <h2 className="text-base font-semibold flex items-center gap-2">
                <Activity className="w-4 h-4 text-primary" />
                Active Workflow Executions
              </h2>
              <span className="text-xs text-primary font-medium hover:underline cursor-pointer flex items-center gap-1">
                View all explorer logs <ArrowRight className="w-3 h-3" />
              </span>
            </div>

            <div className="flex flex-col gap-3">
              {recentRuns.map((run) => (
                <div 
                  key={run.id}
                  className="p-4 rounded border border-border bg-secondary/20 flex flex-col gap-3 hover:bg-secondary/40 transition-all text-sm"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-semibold text-foreground/95">{run.employee}</p>
                      <p className="text-xs text-foreground/60 mt-1">{run.goal}</p>
                    </div>
                    <div className="text-right">
                      <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                        run.status === "Completed" ? "bg-success/20 text-success" :
                        run.status === "Running" ? "bg-primary/20 text-primary animate-pulse" :
                        run.status === "Failed" ? "bg-danger/20 text-danger" :
                        "bg-warning/20 text-warning"
                      }`}>
                        {run.status}
                      </span>
                      <p className="text-[10px] text-foreground/40 mt-1">{run.time}</p>
                    </div>
                  </div>
                  {/* Progress bar */}
                  <div className="w-full bg-secondary-accent/25 rounded-full h-1.5 overflow-hidden">
                    <div 
                      className={`h-1.5 rounded-full transition-all duration-500 ${
                        run.status === "Completed" ? "bg-success" :
                        run.status === "Failed" ? "bg-danger" : "bg-primary"
                      }`}
                      style={{ width: `${run.progress}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Retry Queue Backoff Manager */}
          <div className="p-6 rounded-lg bg-card border border-border flex flex-col gap-4 shadow-sm">
            <h2 className="text-base font-semibold flex items-center gap-2">
              <RefreshCw className="w-4 h-4 text-warning" />
              Retry Queue & Backoff Manager
            </h2>
            {retryQueue.length === 0 ? (
              <p className="text-xs text-foreground/40 py-2">No workflows currently backing off in retry loops.</p>
            ) : (
              <div className="flex flex-col gap-3">
                {retryQueue.map((item) => (
                  <div 
                    key={item.id} 
                    className="p-4 rounded border border-border bg-secondary/35 flex items-center justify-between text-xs hover:border-warning/50 transition-all"
                  >
                    <div className="flex flex-col gap-1">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-foreground/90">{item.employee}</span>
                        <span className="px-1.5 py-0.5 rounded bg-warning/25 text-warning font-bold text-[9px] uppercase">Attempt {item.attempt}</span>
                      </div>
                      <p className="text-foreground/60">{item.goal}</p>
                      <p className="text-danger font-medium mt-0.5">Error: {item.reason}</p>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="text-[10px] text-foreground/50 font-medium">{item.backoff}</span>
                      <button 
                        onClick={() => handleTriggerRetry(item.id)}
                        className="px-2.5 py-1 bg-secondary text-foreground hover:bg-secondary-accent/40 border border-border rounded text-[10px] font-semibold flex items-center gap-1 transition-all"
                      >
                        <RefreshCw className="w-3 h-3 text-primary" />
                        Force Retry
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>

        {/* Right Column: Health Status Desk */}
        <div className="flex flex-col gap-6">

          {/* Tool Connector Health Monitor */}
          <div className="p-6 rounded-lg bg-card border border-border flex flex-col gap-4 shadow-sm">
            <h2 className="text-base font-semibold flex items-center gap-2">
              <Gauge className="w-4 h-4 text-primary" />
              Integration Health Desk
            </h2>
            <div className="flex flex-col gap-3">
              {toolHealth.map((tool) => (
                <div 
                  key={tool.name}
                  className="p-3.5 rounded border border-border bg-secondary/15 flex items-center justify-between text-xs"
                >
                  <div className="flex flex-col gap-0.5">
                    <span className="font-medium text-foreground/90">{tool.name}</span>
                    <span className="text-[10px] text-foreground/40">Quota: {tool.rate}</span>
                  </div>
                  <div className="text-right">
                    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full font-bold text-[9px] ${
                      tool.status === "Healthy" ? "bg-success/20 text-success" : "bg-warning/20 text-warning"
                    }`}>
                      {tool.status === "Healthy" ? (
                        <CheckCircle className="w-2.5 h-2.5" />
                      ) : (
                        <AlertTriangle className="w-2.5 h-2.5" />
                      )}
                      {tool.status}
                    </span>
                    <p className="text-[9px] text-foreground/50 mt-1">Latency: {tool.latency}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Memory OS Utilizations */}
          <div className="p-6 rounded-lg bg-card border border-border flex flex-col gap-4 shadow-sm">
            <h2 className="text-base font-semibold flex items-center gap-2">
              <Database className="w-4 h-4 text-primary" />
              Memory OS Diagnostics
            </h2>
            <div className="flex flex-col gap-3 text-xs">
              <div className="p-3 bg-secondary/20 rounded border border-border">
                <div className="flex justify-between font-semibold">
                  <span>Conversation Store</span>
                  <span className="text-success">Active</span>
                </div>
                <p className="text-foreground/50 text-[10px] mt-1">Redis Cache: 2.4 MB | DB Sync: Verified</p>
              </div>

              <div className="p-3 bg-secondary/20 rounded border border-border">
                <div className="flex justify-between font-semibold">
                  <span>Task & Context Store</span>
                  <span className="text-success">Active</span>
                </div>
                <p className="text-foreground/50 text-[10px] mt-1">Gzip compression ratio: 4.2x savings</p>
              </div>

              <div className="p-3 bg-secondary/20 rounded border border-border">
                <div className="flex justify-between font-semibold">
                  <span>Knowledge Retrieval DB</span>
                  <span className="text-success">Active</span>
                </div>
                <p className="text-foreground/50 text-[10px] mt-1">Qdrant Vector DB: 12,400 embeddings active</p>
              </div>
            </div>
          </div>

        </div>

      </div>

      {/* Full-Width Agent Terminal Console */}
      <div className="mt-6 border-t border-border pt-6">
        <AgentTerminal conversationId="default-session" />
      </div>
    </div>
  );
}

