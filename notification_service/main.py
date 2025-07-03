from fastapi import FastAPI
from prometheus_client import Counter, generate_latest
from fastapi.responses import Response

app = FastAPI()

NOTIFICATION_SENT = Counter("notifications_sent_total", "Total notifications sent")

@app.get("/")
def root():
    NOTIFICATION_SENT.inc()
    return {"message": "Notification Service is running"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
