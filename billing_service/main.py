from fastapi import FastAPI
from prometheus_client import Counter, generate_latest
from fastapi.responses import Response

app = FastAPI()

BILLING_REQUESTS = Counter("billing_requests_total", "Total number of billing requests")

@app.get("/")
def root():
    BILLING_REQUESTS.inc()
    return {"message": "Billing Service is running"}

@app.post("/charge")
async def charge(request: Request):
    data = await request.json()
    username = data.get("username", "Unknown")
    BILLING_REQUESTS.inc()
    return {"message": f"User '{username}' charged successfully"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
