from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat
from agno.memory.v2.memory import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.storage.sqlite import SqliteStorage

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