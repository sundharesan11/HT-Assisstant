"use client";

import Image from "next/image";
import ReactMarkdown from "react-markdown";
import { useCopilotReadable } from "@copilotkit/react-core";
import { useCopilotAction } from "@copilotkit/react-core";
import { useCopilotContext } from "@copilotkit/react-core";
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

export function Dashboard() {

  const userId = 7;
  type CGMEntry = {
    timestamp: string;
    glucose_level: number | string;
  };
  type MoodLogEntry = {
    timestamp: string;
    mood: string;
  };

  type MoodCountEntry = {
    mood: string;
    count: number;
  };

  const [moodData, setMoodData] = useState<MoodCountEntry[]>([]);
  const [cgmData, setCgmData] = useState<CGMEntry[]>([]);
  const [foodText, setFoodText] = useState("");
  const [foodLog, setFoodLog] = useState<{ food_log: string } | null>(null);
  const [mealPlan, setMealPlan] = useState<{ meal_plan: string } | null>(null);
  const [userName, setUserName] = useState<string>("");
  // const [isDataLoaded, setIsDataLoaded] = useState(false);


  useEffect(() => {
    fetch(`http://localhost:8000/api/user-greeting?user_id=${userId}`, {
      method: "POST",
    })
      .then(res => res.json())
      .then(data => {
        if (data.first_name) {
          setUserName(data.first_name);
          console.log("Fetched first name:", data.first_name);
        } else {
          console.error("No first_name found in response:", data);
        }
      })
      .catch(err => console.error("Error fetching user name:", err));
  }, []);
    

  useEffect(() => {
    fetch(`http://localhost:8000/api/cgm-history?user_id=${userId}`).then(res => res.json()).then(setCgmData);
  }, []);

  const formattedData = cgmData
    .filter(entry => entry.timestamp && entry.glucose_level)
    .map(entry => ({
      timestamp: new Date(entry.timestamp).toLocaleDateString('en-GB', {
        day: '2-digit',
        month: 'short'
      }),
      glucose_level: Number(entry.glucose_level)
    }));
    

  useEffect(() => {
  fetch(`http://localhost:8000/api/mood-summary?user_id=${userId}`)
      .then(res => res.json())
      .then((data: { timestamp: string; mood: string }[]) => {
        const moodCounts: Record<string, number> = {};

        data.forEach(entry => {
          const mood = entry.mood.trim().toLowerCase();
          moodCounts[mood] = (moodCounts[mood] || 0) + 1;
        });

        const formattedMoodData = Object.entries(moodCounts).map(([mood, count]) => ({
          mood,
          count,
        }));

        console.log("Formatted Mood Data:", formattedMoodData);
        setMoodData(formattedMoodData);
      })
      .catch(err => console.error("Error fetching mood logs:", err));
  }, [userId]);


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

  const userContextId = useCopilotReadable({
    description: "User ID for the current health dashboard session",
    value: userId
  });

  useCopilotReadable({
    description: "User name",
    value: userName,
    parentId: userContextId
  });
 
  useCopilotReadable({
    description: "CGM data Glucose readings",
    value: cgmData,
    parentId: userContextId
  });

  useCopilotReadable({
    description: "Mood data",
    value: moodData,
    parentId: userContextId
  });

  useCopilotContext();
  useCopilotReadable({
    description: "Current time",
    value: new Date().toLocaleTimeString(),
  })

  return (
    <div className="p-6 space-y-6">
      {/* Welcome Message Below */}
        {userName && (
          <div className="mt-4 bg-white p-4 rounded-lg shadow-sm border border-gray-200">
            <h2 className="text-lg font-semibold text-gray-800">
              Welcome, {userName} 👋
            </h2>
          </div>
        )}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600">Overview of your Health Care Assistant activities</p>
      </div>
      
      {/* 1. CGM Line Chart */}
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <h2 className="text-lg font-semibold mb-2">Glucose Readings (Last 7 Days)</h2>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={formattedData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="timestamp" />
            <YAxis domain={[60, 320]} /> {/* Adjust based on expected glucose range */}
            <Tooltip />
            <Line
              type="monotone"
              dataKey="glucose_level"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={{ r: 4 }}
              activeDot={{ r: 6 }}
            />
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
