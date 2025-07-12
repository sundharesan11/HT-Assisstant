"use client";

import Image from "next/image";
import ReactMarkdown from "react-markdown";
import { CopilotSidebar } from "@copilotkit/react-ui"; 
import { CopilotChat } from "@copilotkit/react-ui";
import { useEffect, useState } from "react";
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
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

import { HttpAgent } from "@ag-ui/client"

const mealagent = new HttpAgent({
  url: "https://your-agent-endpoint.com/agent",
  headers: {
    Authorization: "Bearer your-api-key",
  },
})



// Single agent configuration
const agent = {
  id: "healthcare_agent",
  name: "Health Care Agent",
  icon: Bot,
  description: "Health Care Assistant",
  instructions: "A multi-agent health-care generative AI assistant for greeting, mood tracking, CGM monitoring, food logging, and adaptive meal planning.",
  color: "bg-blue-500"
};

// Dashboard component
function Dashboard() {
  const [cgmData, setCgmData] = useState([]);
  const [moodData, setMoodData] = useState([]);
  const [foodText, setFoodText] = useState("");
  const [foodLog, setFoodLog] = useState<{ food_log: string } | null>(null);
  const [mealPlan, setMealPlan] = useState<{ meal_plan: string } | null>(null);


  const userId = 100;

  useEffect(() => {
    fetch(`http://localhost:8000/api/cgm-history?user_id=${userId}`).then(res => res.json()).then(setCgmData);
    // fetch(`/api/mood-summary?user_id=${userId}`).then(res => res.json()).then(setMoodData);
  }, []);




  const handleLogFood = async () => {
    const res = await fetch(`http://localhost:8000/api/log-food?description=${foodText}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      // body: JSON.stringify({ user_id: userId, description: foodText })
    });
    // alert("Food logged!");
    // setFoodText("");
    const food = await res.json();
    setFoodLog(food);
  };

  const handleMealPlan = async () => {
    const res = await fetch(`http://localhost:8000/api/meal_generate?user_id=${userId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
      // body: JSON.stringify({ user_id: userId })
    });
    const plan = await res.json();
    setMealPlan(plan);
  };
  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600">Overview of your Health Care Assistant activities</p>
      </div>

      {/* 1. CGM Line Chart */}
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <h2 className="text-lg font-semibold mb-2">Glucose Readings (Last 7 Days)</h2>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={cgmData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="timestamp" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="glucose_level" stroke="#3b82f6" />
          </LineChart>
        </ResponsiveContainer>
      </div>
      {/* 2. Mood Bar Chart */}
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <h2 className="text-lg font-semibold mb-2">Mood Summary</h2>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={moodData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="mood" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#34d399" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* 3. Food Logging Form */}
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <h2 className="text-lg font-semibold mb-2">Log Your Meal</h2>
        <div className="flex items-center space-x-4">
          <input
            type="text"
            className="border p-2 rounded flex-1"
            placeholder="e.g., 2 chapatis, dal, salad"
            value={foodText}
            onChange={(e) => setFoodText(e.target.value)}
          />
          <button
            className="bg-blue-600 text-white px-4 py-2 rounded"
            onClick={handleLogFood}
          >
            Submit
          </button>
        </div>
        {foodLog && (
          <div className="mt-4 text-sm text-gray-700 whitespace-pre-line">
            <h3 className="font-semibold mb-2">Nutrients Breakdown:</h3>
                <ReactMarkdown>{foodLog.food_log}</ReactMarkdown>
          </div>
        )}
      </div>

      {/* 4. Generate Meal Plan */}
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <h2 className="text-lg font-semibold mb-2">Adaptive Meal Planner</h2>
        <button
          className="bg-green-600 text-white px-4 py-2 rounded"
          onClick={handleMealPlan}
        >Generate Meal Plan
        </button>

        {mealPlan && (
          <div className="mt-4 text-sm text-gray-700 whitespace-pre-line">
            <h3 className="font-semibold mb-2">Suggested Meals:</h3>
                <ReactMarkdown>{mealPlan.meal_plan}</ReactMarkdown>
          </div>
        )}
        </div>
    </div>
  );
}

export default function Chat() {
  const [currentView, setCurrentView] = useState("dashboard"); // "dashboard" or "chat"
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const handleChatStart = () => {
    setCurrentView("chat");
  };

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
          <div className="flex-1 flex flex-col">
            {/* Chat Header */}
            <div className="bg-white border-b border-gray-200 p-4">
              <div className="flex items-center space-x-3">
                <div className={`w-10 h-10 rounded-lg ${agent.color} flex items-center justify-center`}>
                  <agent.icon size={20} className="text-white" />
                </div>
                <div>
                  <h2 className="text-lg font-semibold text-gray-900">{agent.name}</h2>
                  <p className="text-sm text-gray-600">{agent.description}</p>
                </div>
              </div>
            </div>

            {/* Chat Interface */}
            <div className="flex-1">
              <CopilotChat
                instructions={agent.instructions}
                labels={{
                  title: agent.name,
                  initial: `Hi! 👋 I'm your ${agent.name}. I can help you with mood tracking, CGM monitoring, food logging, and meal planning. How can I assist you today?`,
                }}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}