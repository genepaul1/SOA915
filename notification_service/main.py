from fastapi import FastAPI
from prometheus_client import Counter, generate_latest
from fastapi.responses import Response

app = FastAPI()

NOTIFICATION_SENT = Counter("notifications_sent_total", "Total notifications sent")

@app.get("/")
def root():
    NOTIFICATION_SENT.inc()
    return {"message": "Notification Service is running"}

@app.post("/notify")
async def notify(request: Request):
    data = await request.json()
    username = data.get("username", "Unknown")
    NOTIFICATION_REQUESTS.inc()
    return {"message": f"User '{username}' notified successfully"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
