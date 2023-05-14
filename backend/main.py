from fastapi import FastAPI, Depends
from backend.api.routes import router as api_router
from backend.api.events import router as event_router
from backend.api.users import router as user_router
from backend.models.questionnaire import User, Questionnaire, Question, Answer, Respondent, Response
# from core.database import engine, get_session


# ... startup, shutdown events, and process_events function ...
from sqlmodel import Session, SQLModel, create_engine, select
from typing import List

app = FastAPI()
app.include_router(api_router)
app.include_router(event_router)
app.include_router(user_router)

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)

@app.on_event("startup")
async def on_startup():
    SQLModel.metadata.create_all(engine)

# Replace this with a function that listens to Redis events and calls the appropriate handler
async def process_events():
    pass
