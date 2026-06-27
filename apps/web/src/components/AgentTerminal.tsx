"use client";

import React, { useEffect, useState, useRef } from "react";
import { Terminal, Shield, CheckCircle, AlertOctagon } from "lucide-react";

interface LogMessage {
  timestamp: string;
  event: string;
  message: string;
  type: "info" | "success" | "warning" | "error";
}

export default function AgentTerminal({ conversationId }: { conversationId: string }) {
  const [logs, setLogs] = useState<LogMessage[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const terminalEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Connect to versioned WebSocket stream
    const socket = new WebSocket("wss://api.qevn.workforce/v1/stream");
    let heartbeat: NodeJS.Timeout;

    socket.onopen = () => {
      setIsConnected(true);
      
      // 1. Subscribe to conversation logs channel using JWT
      socket.send(JSON.stringify({
        token: "mock_jwt",
        conversation_id: conversationId
      }));

      // 2. Schedule client-side heartbeat pings every 10 seconds
      heartbeat = setInterval(() => {
        if (socket.readyState === WebSocket.OPEN) {
          socket.send(JSON.stringify({ action: "ping" }));
        }
      }, 10000);

      appendLog("System", "WebSocket Stream Connection Established.", "success");
    };

    socket.onmessage = (event) => {
      const data = jsonParse(event.data);
      if (!data || data.event === "ping" || data.status === "subscribed") return;
      
      // Parse custom domain events
      const time = new Date().toLocaleTimeString();
      let logType: "info" | "success" | "warning" | "error" = "info";
      let msg = "";

      if (data.event === "CapabilityStarted") {
        msg = `Capability Started: ${data.data.capability_id} | Action: ${data.data.action}`;
      } else if (data.event === "CapabilityCompleted") {
        msg = `Capability Complete: ${data.data.capability_id} (Success: ${data.data.success})`;
        logType = data.data.success ? "success" : "error";
      } else if (data.event === "ApprovalRequested") {
        msg = `⚠️ ACTION INTERRUPTED: Approval requested for ${data.data.action_type}.`;
        logType = "warning";
      } else if (data.event === "PolicyDecisionLogged") {
        msg = `Policy Engine: Checked '${data.data.action}' -> Decision: ${data.data.decision.toUpperCase()}`;
        logType = data.data.decision === "allow" ? "info" : "error";
      } else {
        msg = JSON.stringify(data.data);
      }

      appendLog(data.event, msg, logType);
    };

    socket.onclose = () => {
      setIsConnected(false);
      clearInterval(heartbeat);
      appendLog("System", "WebSocket Stream Closed.", "error");
    };

    return () => {
      socket.close();
      clearInterval(heartbeat);
    };
  }, [conversationId]);

  useEffect(() => {
    terminalEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  const appendLog = (event: string, message: string, type: "info" | "success" | "warning" | "error") => {
    setLogs((prev) => [
      ...prev,
      {
        timestamp: new Date().toLocaleTimeString(),
        event,
        message,
        type
      }
    ]);
  };

  const jsonParse = (str: string) => {
    try {
      return JSON.parse(str);
    } catch {
      return null;
    }
  };

  return (
    <div className="w-full rounded-lg border border-border bg-[#030303] text-foreground font-mono shadow-2xl flex flex-col h-80 overflow-hidden">
      {/* Console Header bar */}
      <div className="bg-[#09090b] px-4 py-2 border-b border-border flex items-center justify-between text-xs text-foreground/60 select-none">
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-primary" />
          <span>Agent Terminal Console (WSS)</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className={`w-2 h-2 rounded-full ${isConnected ? "bg-success" : "bg-danger"}`}></span>
          <span>{isConnected ? "Connected" : "Disconnected"}</span>
        </div>
      </div>

      {/* Terminal Log Console */}
      <div className="flex-1 p-4 overflow-y-auto flex flex-col gap-2 text-xs leading-relaxed select-text">
        {logs.map((log, idx) => (
          <div key={idx} className="flex gap-2 items-start">
            <span className="text-foreground/40">{log.timestamp}</span>
            <span className="text-primary font-semibold shrink-0">[{log.event}]</span>
            <span className={`flex items-center gap-1 ${
              log.type === "success" ? "text-success" :
              log.type === "warning" ? "text-warning font-semibold" :
              log.type === "error" ? "text-danger" : "text-foreground/80"
            }`}>
              {log.type === "warning" && <Shield className="w-3.5 h-3.5" />}
              {log.type === "success" && <CheckCircle className="w-3.5 h-3.5" />}
              {log.type === "error" && <AlertOctagon className="w-3.5 h-3.5" />}
              {log.message}
            </span>
          </div>
        ))}
        <div ref={terminalEndRef} />
      </div>
    </div>
  );
}
