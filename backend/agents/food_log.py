from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat


food_intake_agent = Agent(
    name="food_intake_agent",
    role="Food Intake Agent",
    model=OpenAIChat(id="o4-mini-2025-04-16"),
    instructions="""
    When provided with a meal description (and optional timestamp), log the meal and categorize it into macronutrients (carbs, protein, fat) using LLM analysis.
    """,
    markdown=True,
)