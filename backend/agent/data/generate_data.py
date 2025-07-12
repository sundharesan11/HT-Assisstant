import sqlite3
import random
from faker import Faker
from datetime import datetime, timedelta
import os

NUM_USERS = 100
CITIES = ['Chennai', 'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad']
DIETARY_PREFERENCES = ['vegetarian', 'non-vegetarian', 'vegan']
MEDICAL_CONDITIONS = ['Type 2 Diabetes', 'Hypertension', 'Celiac Disease', 'High Cholesterol']
PHYSICAL_LIMITATIONS = ['mobility issues', 'swallowing difficulties', 'none']

faker = Faker()

def create_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS cgm_readings")

    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            city TEXT,
            dietary_preference TEXT,
            medical_conditions TEXT,
            physical_limitations TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cgm_readings (
            user_id INTEGER,
            glucose_level INTEGER,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS mood_log (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         user_id INTEGER NOT NULL,
    #         mood TEXT NOT NULL,
    #         timestamp TEXT DEFAULT CURRENT_TIMESTAMP
    #     );
    # """)

    conn.commit()
    return conn

def generate_users():
    users = []
    
    per_group = NUM_USERS // len(DIETARY_PREFERENCES)  # 33
    remainder = NUM_USERS % len(DIETARY_PREFERENCES)   # 1

    dietary_list = DIETARY_PREFERENCES * per_group + random.sample(DIETARY_PREFERENCES, remainder)
    random.shuffle(dietary_list)
    
    for i in range(NUM_USERS):
        first = faker.first_name()
        last = faker.last_name()
        city = random.choice(CITIES)
        dietary = dietary_list[i]

        # 0–2 medical conditions
        med = random.sample(MEDICAL_CONDITIONS, k=random.randint(0, 2))
        # 70% chance of physical limitation
        phys = random.sample(PHYSICAL_LIMITATIONS, k=1 if random.random() < 0.7 else 0)
        if not phys:
            phys = ['none']

        users.append({
            "first": first,
            "last": last,
            "city": city,
            "diet": dietary,
            "medical_conditions": med,
            "physical_limitations": phys
        })
    return users

def insert_users_and_cgm(conn, users):
    cursor = conn.cursor()
    for user in users:
        cursor.execute("""
            INSERT INTO users (first_name, last_name, city, dietary_preference, medical_conditions, physical_limitations)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user["first"],
            user["last"],
            user["city"],
            user["diet"],
            ', '.join(user["medical_conditions"]),
            ', '.join(user["physical_limitations"])
        ))
        user_id = cursor.lastrowid

        # Add CGM readings only if user has Type 2 Diabetes
        if 'Type 2 Diabetes' in user["medical_conditions"]:
            for i in range(7):  # 7 days of readings
                ts = datetime.now() - timedelta(days=i)
                glucose = random.randint(80, 300)
                cursor.execute("""
                    INSERT INTO cgm_readings (user_id, glucose_level, timestamp)
                    VALUES (?, ?, ?)
                """, (user_id, ts.isoformat(), glucose))

    conn.commit()

if __name__ == "__main__":
    conn = create_db()
    users = generate_users()
    insert_users_and_cgm(conn, users)
    print("SQLite DB created with 100 users and CGM readings where applicable.")
