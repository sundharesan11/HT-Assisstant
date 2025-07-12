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


@tool(
    name="fetch_user_details",                # Custom name for the tool (otherwise the function name is used)
    description="Fetch user details from the users table by user_id",
    # show_result=True,                               # Show result after function call
    # stop_after_tool_call=True,                      # Return the result immediately after the tool call and stop the agent                     # Hook to run before and after execution
    # requires_user_input=True,
    # user_input_fields=['user_id']
)
def get_user_by_id(user_id: int, db_path: str = "data/users.db") -> dict | None:
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


def get_cgm_context(user_id: int, db_path: str = "data/users.db") -> Optional[Dict]:
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
    db_file="data/users.db"
)

# Create a SQLite database for memory
mood_memory = SqliteMemoryDb(
    table_name="users_moods",  # The table name to use
    db_file="data/users.db"  # The SQLite database file
)

# Initialize Memory with the storage backend
mood_memory = Memory(db=mood_memory)

meal_planner_agent = Agent(
    name="meal_planner_agent",
    role="Meal Planner Agent",
    tools = [get_user_by_id, get_cgm_context],
    memory=mood_memory,
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="""
    When given a user_id, fetch the user’s dietary preferences, medical conditions, recent mood, and latest glucose reading with the tools provided.
    Generate a 3-meal adaptive plan that aligns with these constraints and promotes health stability.
    """,
    markdown=True,
)


