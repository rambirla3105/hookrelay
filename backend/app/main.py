from fastapi import FastAPI,HTTPException
from pydantic import BaseModel, Field
from typing import Any


app = FastAPI(
    title="HookRelay API",
    description="Reliable Webhook Delivery Infrastructure",
    version="0.1.0"
)


#define incoming event structure
class EventCreate(BaseModel):
    event_type: str = Field(
        min_length=3,
        max_length=100,
        description="Type of webhook event"
    )
    payload: dict[str, Any] = Field(
        description="Event data"
    )


class EventResponse(BaseModel):
    message: str
    status: str
    event_type: str
    payload: dict[str, Any]

#root endpoint
@app.get("/")
def root():
    return{
        "message": "welcome to HookRelay!",
        "status": "running",
        "version":"0.1.0"
    }

#healt check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "HookRelay API"
    }


@app.get("/events/{event_id}")
def get_event(event_id: int):

    if event_id != 1:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return {
        "event_id": 1,
        "event_type": "order.created"
    }


#publish webhook event
@app.post("/events", response_model=EventResponse)
def publish_event(event: EventCreate):
    return{
        "message" : "Event received successfully",
        "status" : "accepted",
        "event_type" : event.event_type,
        "payload" : event.payload
    }