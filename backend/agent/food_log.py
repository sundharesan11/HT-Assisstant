from agno.agent.agent import Agent
from agno.app.agui.app import AGUIApp
from agno.models.openai import OpenAIChat
from agno.team.team import Team
from agno.memory.v2.memory import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.storage.sqlite import SqliteStorage
from agno.tools import tool
from agno.tools.reasoning import ReasoningTools
import sqlite3
from datetime import datetime
import sqlite3
from typing import Optional, Dict
from agno.agent import Agent, RunResponse
from agno.utils.pprint import pprint_run_response


food_intake_agent = Agent(
    name="food_intake_agent",
    role="Food Intake Agent",
    model=OpenAIChat(id="o4-mini-2025-04-16"),
    instructions="""
    When provided with a meal description (and optional timestamp), log the meal and categorize it into macronutrients (carbs, protein, fat) using LLM analysis.
    """,
    markdown=True,
)