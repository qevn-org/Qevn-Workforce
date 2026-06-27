"use client";

import React, { useState } from "react";
import Link from "next/link";
import { 
  LayoutDashboard, 
  Users, 
  GitBranch, 
  BookOpen, 
  Settings, 
  Building2, 
  ShoppingBag,
  Bell,
  ChevronDown,
  Database,
  Shield,
  LineChart,
  History
} from "lucide-react";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const [currentOrg, setCurrentOrg] = useState("QEVN Technology");
  const [showOrgDropdown, setShowOrgDropdown] = useState(false);

  const navigation = [
    { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    { name: "AI Employees", href: "/dashboard/employees", icon: Users },
    { name: "Workflows", href: "/dashboard/workflows", icon: GitBranch },
    { name: "Registries", href: "/dashboard/registries", icon: Database },
    { name: "Governance", href: "/dashboard/governance", icon: Shield },
    { name: "Cost Analytics", href: "/dashboard/analytics", icon: LineChart },
    { name: "Audit Center", href: "/dashboard/audit", icon: History },
    { name: "Marketplace", href: "/dashboard/marketplace", icon: ShoppingBag },
    { name: "Knowledge Center", href: "/dashboard/knowledge", icon: BookOpen },
    { name: "Settings", href: "/dashboard/settings", icon: Settings }
  ];

  return (
    <div className="flex h-screen bg-background text-foreground font-sans overflow-hidden">
      {/* Sidebar Panel */}
      <aside className="w-64 bg-card border-r border-border flex flex-col justify-between">
        <div>
          {/* Brand Header & Org Switcher */}
          <div className="p-4 border-b border-border relative">
            <button 
              onClick={() => setShowOrgDropdown(!showOrgDropdown)}
              className="w-full flex items-center justify-between p-2 rounded bg-secondary hover:bg-secondary/80 border border-border"
            >
              <div className="flex items-center gap-2">
                <Building2 className="w-5 h-5 text-primary" />
                <span className="font-semibold text-sm truncate">{currentOrg}</span>
              </div>
              <ChevronDown className="w-4 h-4 text-secondary-accent" />
            </button>

            {showOrgDropdown && (
              <div className="absolute left-4 right-4 mt-2 bg-card border border-border rounded shadow-lg z-50">
                {["QEVN Technology", "Partner Inc", "Acme Enterprise"].map((org) => (
                  <button
                    key={org}
                    onClick={() => {
                      setCurrentOrg(org);
                      setShowOrgDropdown(false);
                    }}
                    className="w-full text-left px-4 py-2 hover:bg-secondary text-sm"
                  >
                    {org}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Navigation Links */}
          <nav className="p-4 flex flex-col gap-1">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className="flex items-center gap-3 px-3 py-2 rounded text-sm text-foreground/80 hover:text-foreground hover:bg-secondary transition-all"
              >
                <item.icon className="w-4 h-4 text-primary" />
                {item.name}
              </Link>
            ))}
          </nav>
        </div>

        {/* Profile Card footer */}
        <div className="p-4 border-t border-border flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center font-bold text-sm">
            Q
          </div>
          <div>
            <p className="text-xs font-semibold">QEVN Developer</p>
            <p className="text-[10px] text-foreground/60">admin@qevn.in</p>
          </div>
        </div>
      </aside>

      {/* Main Panel Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Header bar */}
        <header className="h-14 border-b border-border bg-card/50 backdrop-blur-md px-6 flex items-center justify-between z-10">
          <div className="flex items-center gap-2 text-sm text-foreground/60">
            <span>Workspaces</span>
            <span>/</span>
            <span className="text-foreground font-medium">Default Workspace</span>
          </div>
          <div className="flex items-center gap-4">
            <button className="relative p-2 hover:bg-secondary rounded">
              <Bell className="w-4 h-4" />
              <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-primary"></span>
            </button>
          </div>
        </header>

        {/* Dynamic page contents */}
        <main className="flex-1 overflow-y-auto p-8">
          {children}
        </main>
      </div>
    </div>
  );
}
