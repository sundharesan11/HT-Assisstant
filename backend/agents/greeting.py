from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools import tool
import sqlite3

@tool(
    name="fetch_user_details",                # Custom name for the tool (otherwise the function name is used)
    description="Fetch user details from the users table by user_id",
    # show_result=True,                               # Show result after function call
    # stop_after_tool_call=True,                      # Return the result immediately after the tool call and stop the agent                     # Hook to run before and after execution
    # requires_user_input=True,
    # user_input_fields=['user_id']
)
def get_user_by_id(user_id: int, db_path: str = "../data/users.db") -> dict | None:
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