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
from api_routes import router as api_router 




@tool(
    name="fetch_user_details",                # Custom name for the tool (otherwise the function name is used)
    description="Fetch user details from the users table by user_id",
    # show_result=True,                               # Show result after function call
    # stop_after_tool_call=True,                      # Return the result immediately after the tool call and stop the agent                     # Hook to run before and after execution
    # requires_user_input=True,
    # user_input_fields=['user_id']
)
def get_user_by_id(user_id: int, db_path: str = "./data/users.db") -> dict | None:
    """
    Fetch user details from the users table by user_id.

    Args:
        user_id (int): The ID of the user to fetch.
        db_path (str): Path to the SQLite database file.

    Returns:
        dict | None: Dictionary with user details if found, else None.
    """
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enables dictionary-style access
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        print(row)
        if row:
            return dict(row)
        else:
            return None

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

    finally:
        conn.close()



def log_glucose_reading(user_id: int, glucose_level: int, db_path: str = "./data/users.db") -> str:
    """
    Inserts a glucose reading into the cgm_readings table with current timestamp.

    Args:
        user_id (int): The ID of the user.
        glucose_level (int): The glucose level in mg/dL.
        db_path (str): Path to the SQLite database.

    Returns:
        str: Confirmation message or error.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        timestamp = datetime.now().isoformat()
        cursor.execute(
            """
            INSERT INTO cgm_readings (user_id, glucose_level, timestamp)
            VALUES (?, ?, ?)
            """,
            (user_id, glucose_level, timestamp)
        )

        conn.commit()
        return f"Glucose reading of {glucose_level} mg/dL logged for user {user_id} at {timestamp}."

    except sqlite3.Error as e:
        return f"Failed to insert glucose reading: {e}"

    finally:
        conn.close()

import sqlite3
from typing import Optional, Dict

def get_cgm_context(user_id: int, db_path: str = "./data/users.db") -> Optional[Dict]:
    """
    Fetches dietary preference, medical conditions, and the latest glucose reading for a given user.

    Args:
        user_id (int): The user's ID
        db_path (str): Path to the SQLite database

    Returns:
        dict | None: A dictionary containing the user's health context or None if user not found.
    """
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Get latest CGM reading
        cursor.execute(
            """
            SELECT glucose_level, timestamp 
            FROM cgm_readings 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
            """,
            (user_id,)
        )
        cgm_row = cursor.fetchone()

        latest_glucose_level = cgm_row["glucose_level"] if cgm_row else None
        glucose_timestamp = cgm_row["timestamp"] if cgm_row else None

        return {
            "user_id": user_id,
            "latest_glucose_level": latest_glucose_level,
            "glucose_timestamp": glucose_timestamp
        }

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

    finally:
        conn.close()


user_storage = SqliteStorage(
    table_name="users_sessions",
    db_file="./data/users.db"
)

# Create a SQLite database for memory
mood_memory = SqliteMemoryDb(
    table_name="users_moods",  # The table name to use
    db_file="./data/users.db"  # The SQLite database file
)

# Initialize Memory with the storage backend
mood_memory = Memory(db=mood_memory)

# AGENTS
greeting_agent = Agent(
    name="greeting_agent",
    tools=[get_user_by_id],
    role="Greeting Agent",
    model=OpenAIChat(id="o4-mini-2025-04-16"),
    instructions="""
    When provided with a user_id, call the tool and fetch information about the user and greet them by name and city.
    If the ID is invalid, ask for a valid one before continuing.
    """,
    markdown=True,
)

mood_tracker_agent = Agent(
    name="mood_tracker_agent",
    role="Mood Tracker Agent",
    model=OpenAIChat(id="o4-mini-2025-04-16"),
    storage=user_storage,
    memory=mood_memory,
    enable_agentic_memory=True,
    add_history_to_messages=True,
    instructions="""
    When provided with a mood label (e.g., happy, tired, sad), log the mood in mood_memory.
    Then retrieve past mood entries and provide a summary of mood trends.
    If it's the first entry, acknowledge that.
    """,
    markdown=True,
)

cgm_agent = Agent(
    name="cgm_agent",
    role="CGM Agent",
    tools=[log_glucose_reading],
    model=OpenAIChat(id="o4-mini-2025-04-16"),
    instructions="""
    When given a user_id and a glucose reading (mg/dL), check if the value is within the normal range (80–300 mg/dL).
    Indicate whether the reading is too low, normal, or too high, and suggest action if abnormal.
    call the log_glucose_reading tool with the user_id and glucose reading.
    """,
    markdown=True,
)

food_intake_agent = Agent(
    name="food_intake_agent",
    role="Food Intake Agent",
    model=OpenAIChat(id="o4-mini-2025-04-16"),
    instructions="""
    When provided with a meal description (and optional timestamp), log the meal and categorize it into macronutrients (carbs, protein, fat) using LLM analysis.
    """,
    markdown=True,
)

meal_planner_agent = Agent(
    name="meal_planner_agent",
    role="Meal Planner Agent",
    tools = [get_user_by_id, get_cgm_context],
    memory=mood_memory,
    model=OpenAIChat(id="o4-mini-2025-04-16"),
    instructions="""
    When given a user_id, fetch the user’s dietary preferences, medical conditions, recent mood, and latest glucose reading with the tools provided.
    Generate a 3-meal adaptive plan that aligns with these constraints and promotes health stability.
    """,
    markdown=True,
)

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
    agui_app.serve(app="main:app", port=8000, reload=True)
