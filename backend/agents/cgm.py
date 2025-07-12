from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat
import sqlite3
from datetime import datetime
from mood_log import *

def log_glucose_reading(user_id: int, glucose_level: int, db_path: str = "../data/users.db") -> str:
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

cgm_agent = Agent(
    name="cgm_agent",
    role="CGM Agent",
    tools=[log_glucose_reading],
    model=OpenAIChat(id="gpt-4.1-2025-04-14"),
    memory=mood_memory,
    storage=user_storage,
    instructions="""
    When given a user_id and a glucose reading (mg/dL), check if the value is within the normal range (80–300 mg/dL).
    Indicate whether the reading is too low, normal, or too high, and suggest action if abnormal.
    call the log_glucose_reading tool with the user_id and glucose reading.
    """,
    markdown=True,
)