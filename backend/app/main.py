from fastapi import FastAPI, Depends
from app.api.questionnaires import router as questionnaire_router
from app.api.events import router as event_router
from app.api.users import router as user_router
from app.models.questionnaire import User, Questionnaire, Question, Answer, Respondent, Response
from app.core.database import engine
from sqlmodel import Session, SQLModel, create_engine, select
from typing import List

# app = FastAPI(root_path="/api")
app = FastAPI(
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url=None,
)
app.include_router(questionnaire_router)
app.include_router(event_router)
app.include_router(user_router)

# @app.on_event("startup")
# async def on_startup():
#     SQLModel.metadata.create_all(engine)

# Replace this with a function that listens to Redis events and calls the appropriate handler
async def process_events():
    pass
