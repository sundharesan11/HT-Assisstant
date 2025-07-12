from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat
from agno.memory.v2.memory import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.storage.sqlite import SqliteStorage
import sqlite3
from datetime import datetime
from typing import List, Dict

def log_mood_entry(user_id: int, mood: str, db_path: str = "../data/users.db") -> str:
    """
    Inserts a mood entry into the mood_log table with the current timestamp.

    Args:
        user_id (int): The ID of the user.
        mood (str): The mood description (e.g., "happy", "anxious").
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
            INSERT INTO mood_log (user_id, mood, timestamp)
            VALUES (?, ?, ?)
            """,
            (user_id, mood, timestamp)
        )

        conn.commit()
        return f"Mood '{mood}' logged for user {user_id} at {timestamp}."

    except sqlite3.Error as e:
        return f"Failed to insert mood entry: {e}"

    finally:
        conn.close()

def get_mood_history(user_id: int, db_path: str = "../data/users.db") -> List[Dict[str, str]]:
    """
    Retrieves the mood history for a given user from the mood_log table.

    Args:
        user_id (int): The ID of the user.
        db_path (str): Path to the SQLite database.

    Returns:
        List[Dict[str, str]]: A list of mood records with mood and timestamp.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT mood, timestamp
            FROM mood_log
            WHERE user_id = ?
            ORDER BY timestamp DESC
            """,
            (user_id,)
        )

        rows = cursor.fetchall()
        mood_history = [{"mood": mood, "timestamp": timestamp} for mood, timestamp in rows]

        return mood_history

    except sqlite3.Error as e:
        print(f"Failed to retrieve mood history: {e}")
        return []

    finally:
        conn.close()

user_storage = SqliteStorage(
    table_name="users_sessions",
    db_file="../data/users.db"
)

# Create a SQLite database for memory
mood_memory = SqliteMemoryDb(
    table_name="users_moods",  # The table name to use
    db_file="../data/users.db"  # The SQLite database file
)

# Initialize Memory with the storage backend
mood_memory = Memory(db=mood_memory)

mood_tracker_agent = Agent(
    name="mood_tracker_agent",
    role="Mood Tracker Agent",
    tools=[log_mood_entry, get_mood_history],
    model=OpenAIChat(id="gpt-4.1-2025-04-14"),
    storage=user_storage,
    memory=mood_memory,
    enable_agentic_memory=True,
    add_history_to_messages=True,
    instructions="""
    When provided with a mood label (e.g., happy, tired, sad), log the mood in mood_memory and call the log_mood_entry tool to insert the mood with appropriate values.
    and always at end retrieve past mood entries and provide a summary of mood trends.
    If it's the first entry, acknowledge that.
    """,
    markdown=True,
)