from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from prometheus_client import Counter, generate_latest
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

app = FastAPI()

DB_FILE = "users.db"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users_db = {}

# Prometheus counter
REGISTRATION_COUNTER = Counter("user_registrations_total", "Total user registrations")

class User(BaseModel):
    username: str
    email: str = None

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.get("/")
def health_check():
    return {"message": "User Service is running"}

@app.post("/register")
def register_user(user: User):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (user.username, user.email))
        conn.commit()
        REGISTRATION_COUNTER.inc()
        return {"message": f"User '{user.username}' registered successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")
    finally:
        conn.close()

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

@app.get("/users")
def list_users():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    conn.close()
    return {"users": [{"id": u[0], "username": u[1], "email": u[2]} for u in users]}

