from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, generate_latest
from fastapi.responses import Response

app = FastAPI()
users_db = {}

# Prometheus counter
REGISTRATION_COUNTER = Counter("user_registrations_total", "Total user registrations")

class User(BaseModel):
    username: str

@app.get("/")
def health_check():
    return {"message": "User Service is running"}

@app.post("/register")
def register_user(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.username] = user.dict()
    REGISTRATION_COUNTER.inc()
    return {"message": f"User '{user.username}' registered successfully"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
