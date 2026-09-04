from fastapi import FastAPI
from dotenv import load_dotenv
from google import genai
from fastapi.middleware.cors import CORSMiddleware

from models.User import User
from models.StudyDeck import StudyDeck
from models.DeckShare import ShareDeck

from routes.ai_routes import router as ai_router
from routes.user_routes import router as user_router
from routes.study_deck_routes import router as study_deck_router
from routes.share_deck_routes import router as share_deck_router
from routes.upload_routes import router as upload_router
from routes.auth_routes import router as auth_router
from routes.dashboard_routes import router as dashboard_router

import os

load_dotenv()

app = FastAPI()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
frontend_url = os.getenv("FRONTEND_URL")

print(f"Frontend URL: {frontend_url}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        frontend_url,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "AI Reviewer API is running!"}


app.include_router(auth_router)

app.include_router(ai_router)

app.include_router(study_deck_router)

app.include_router(share_deck_router)

app.include_router(user_router)

app.include_router(upload_router)

app.include_router(dashboard_router)