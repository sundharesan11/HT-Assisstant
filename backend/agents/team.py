from agno.agent.agent import Agent
from agno.app.agui.app import AGUIApp
from agno.models.openai import OpenAIChat
from agno.team.team import Team
from agno.tools.reasoning import ReasoningTools
from api_routes import router as api_router 
from greeting import *
from cgm import *
from mood_log import *
from food_log import *
from meal_generate import *


interrupt_agent = Agent(
    name="interrupt_agent",
    role="Interrupt Agent (General Q&A)",
    model=OpenAIChat(id="o4-mini-2025-04-16"),
    memory=mood_memory,
    instructions="""
    You are a general-purpose assistant.
    At any point in the interaction, handle unrelated or general questions using LLM-based responses or FAQs.
    After answering, guide the user back to the main conversation flow without losing context.
    """,
    markdown=True,
)


# TEAM DEFINITION
healthcare_team = Team(
    mode="coordinate",
    members=[
        greeting_agent,
        mood_tracker_agent,
        cgm_agent,
        food_intake_agent,
        meal_planner_agent,
        interrupt_agent,
    ],
    name="healthcare_team",
    tools=[ReasoningTools(add_instructions=True)],
    instructions="""
    You are a multi-agent healthcare assistant system focused on personalized support, wellness tracking, and meal planning.

        Each agent in your team serves a specialized role.
        1. **Greeting Agent**  - for greeeting the user given the user_id
        2. **Mood Tracker Agent**  - to log and analyze user moods.
        3. **CGM Agent (Continuous Glucose Monitor)**  - to log glucose readings and provide health insights.
        4. **Food Intake Agent**  - to log meals and analyze macronutrient content.
        5. **Meal Planner Agent**  - to create adaptive meal plans based on user preferences, medical conditions, and health data.
        6. **Interrupt Agent (General Q&A)**  - to handle general questions and maintain conversation flow.
        - Always active and listening for unrelated or general questions.

        Ensure context-aware coordination:
        - Share relevant data between agents (e.g., use mood and CGM data in meal planning).
        - Always maintain a supportive, conversational tone.
        - Respond gracefully if the user asks for help, repeats instructions, or switches context.

        Your goal is to provide seamless, intelligent assistance that adapts to the user’s health status in real time.

    """,
    show_tool_calls=True,
    add_history_to_messages=True,
    show_members_responses=True,
    enable_agentic_context=True,
    get_member_information_tool=True,
    add_member_tools_to_system_message=True,
    memory=mood_memory,
    enable_user_memories=True,
)

# healthcare_team.print_response("hi, my user id is 100")


# AG-UI Integration
agui_app = AGUIApp(
    team=healthcare_team,
    name="Healthcare Assistant AG-UI",
    app_id="healthcare_agui",
    description="A multi-agent generative AI assistant for greeting, mood tracking, CGM monitoring, food logging, and adaptive meal planning.",
)

app = agui_app.get_app()
app.include_router(api_router)
# Serve the app
if __name__ == "__main__":
    agui_app.serve(app="team:app", port=8000, reload=True)
