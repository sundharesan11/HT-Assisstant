from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List, Dict, Optional
import sqlite3
from datetime import datetime
from meal_generate import *
from food_log import *
router = APIRouter()
db_path = "data/users.db"

# Utility...
def connect_db():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/api/cgm-history")
def get_cgm_history(user_id: int):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT timestamp, glucose_level 
            FROM cgm_readings 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 30
        """, (user_id,))
        rows = cursor.fetchall()
        return [{"timestamp": row["timestamp"], "glucose_level": row["glucose_level"]} for row in rows]
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()


# @router.get("/api/mood-summary")
# def get_mood_summary(user_id: int):
#     # your code ...

# class LogFoodRequest(BaseModel):
#     user_id: int
#     description: str

@router.post("/api/log-food")
def log_food(description: str):
    response: RunResponse = food_intake_agent.run(f"{description}")    
    return {"food_log": response.content}


@router.post("/api/meal_generate")
def generate_meal(user_id: str):
    response: RunResponse = meal_planner_agent.run(f"my user id is {user_id}")
    return {"meal_plan": response.content}
