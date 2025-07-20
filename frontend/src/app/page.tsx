"use client";

import Image from "next/image";
import ReactMarkdown from "react-markdown";
import { useCopilotReadable } from "@copilotkit/react-core";
import { useCopilotAction } from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";
import { CopilotChat } from "@copilotkit/react-ui";
import { useCopilotContext } from "@copilotkit/react-core";
import { useEffect, useState } from "react";
import { 
  Bot, 
  Code, 
  FileText, 
  BarChart3, 
  Users, 
  MessageSquare,
  Settings,
  Home,
  Brain,
  Zap,
  Shield,
  ChevronLeft,
  ChevronRight
} from "lucide-react";
import { Dashboard } from "../components/dashboard";


// Dashboard component

export default function Chat() {
  const [currentView, setCurrentView] = useState("dashboard"); // "dashboard" or "chat"
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const handleChatStart = () => {
    setCurrentView("chat");
  };

  useCopilotReadable({
    description: "User ID for the current health dashboard session",
    value: `Current user ID is 7`,
  });

  useCopilotReadable({
    description: "Current time",
    value: new Date().toLocaleTimeString(),
  })

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className={`${sidebarCollapsed ? 'w-16' : 'w-64'} bg-white border-r border-gray-200 transition-all duration-300 flex flex-col`}>
        {/* Header */}
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            {!sidebarCollapsed && (
              <h1 className="text-xl font-bold text-gray-900">Health Care AI</h1>
            )}
            <button
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              className="p-1 rounded-lg hover:bg-gray-100"
            >
              {sidebarCollapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
            </button>
          </div>
        </div>

        {/* Navigation */}
        <div className="p-4 space-y-2">
          <button
            onClick={() => setCurrentView("dashboard")}
            className={`w-full flex items-center space-x-3 p-3 rounded-lg transition-colors ${
              currentView === "dashboard"
                ? "bg-blue-50 text-blue-600"
                : "text-gray-700 hover:bg-gray-50"
            }`}
          >
            <Home size={20} />
            {!sidebarCollapsed && <span>Dashboard</span>}
          </button>
          
          <button
            onClick={handleChatStart}
            className={`w-full flex items-center space-x-3 p-3 rounded-lg transition-colors ${
              currentView === "chat"
                ? "bg-blue-50 text-blue-600"
                : "text-gray-700 hover:bg-gray-50"
            }`}
          >
            <MessageSquare size={20} />
            {!sidebarCollapsed && <span>Start Chat</span>}
          </button>
        </div>


        {/* Settings */}
        <div className="p-4 border-t border-gray-200">
          <button className="w-full flex items-center space-x-3 p-3 rounded-lg text-gray-700 hover:bg-gray-50">
            <Settings size={20} />
            {!sidebarCollapsed && <span>Settings</span>}
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {currentView === "dashboard" ? (
          <Dashboard />
        ) : (
          <CopilotChat
          />
        )}
        <CopilotSidebar />
      </div>
    </div>
  );
}