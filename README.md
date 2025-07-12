
# 🏥 Multi-Agent Healthcare Assistant

A full-stack AI-powered system that helps users **track health data**, **log meals**, **monitor glucose levels**, and **generate adaptive meal plans**. Built using **FastAPI**, **CopilotKit**, **AGNO**, and **Next.js**, this assistant combines multiple agents to offer an intelligent, personalized wellness experience.

---

## 🌟 Features

### 🎯 Core Capabilities
- 🧠 AI-powered **multi-agent system** (mood, glucose, food, greeting, planner)
- 📊 Visual **dashboard** with health insights (mood & CGM charts)
- 💬 Natural language **chat interface**
- 🍱 Meal logging with **nutritional breakdown**
- 🥗 Adaptive **meal planning** based on user health and mood
- 🧾 SQLite database with pre-seeded test data
- 🔄 Dockerized deployment with `docker-compose`

---

## 🧠 Agents Overview

| Agent              | Description |
|-------------------|-------------|
| **Greeting Agent** | Greets user by name and city after fetching from DB |
| **Mood Tracker**   | Logs and summarizes mood trends |
| **CGM Agent**      | Logs glucose levels and provides normal/abnormal flags |
| **Food Log Agent** | Analyzes meals into macronutrients using LLM |
| **Meal Planner**   | Generates 3-meal adaptive plans using CGM + mood data |
| **Interrupt Agent**| Handles unrelated/general queries during conversation |

All agents work in a **coordinated team**, sharing memory and reasoning capabilities.

---

## 🖥️ Frontend (Next.js + AG-UI)

### Dashboard
- 👋 **Welcome message** personalized by user ID
- 📈 **CGM line chart** for last 7 days
- 📊 **Mood bar chart** with trend summary
- 🍽️ **Meal logger** with nutrient analysis
- 🥗 **Meal planner** based on health context

### Chat Interface
- 💬 Chat with the assistant using natural language
- 🧠 Powered by CopilotKit + OpenAI LLM + multi-agent backend

---

## 🔧 Tech Stack

| Layer | Technologies |
|-------|--------------|
| Backend | FastAPI, AGNO, SQLite, SQLAlchemy |
| Frontend | Next.js, React, TailwindCSS, AG-UI, Recharts |
| LLM | OpenAI via `OpenAIAdapter` |
| Orchestration | Docker, Docker Compose |
| Dev Tools | Faker, dotenv, CopilotKit Runtime |

---

## 🧾 Database (SQLite)

Generated via `generate_data.py`:

- 100 fake users
- Glucose readings (if diabetic)
- Mood logs
- Stored in `data/users.db`

---

## 🚀 Quick Start (Docker)

### 1. Clone the project

```bash
git clone https://github.com/sundharesan11/HT-Assisstant.git
cd ht-assistant
```

---

### 2. Set your `.env`

Create a file at `deploy/.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-xxxxx
```

---

### 3. Run with Docker Compose

From the project root or `deploy/` folder, run:

```bash
docker-compose -f deploy/docker-compose.yml up --build
```
