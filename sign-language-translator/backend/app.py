import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database.database import init_db
from backend.app_state import classifier, detector
from backend.routes import auth, prediction, speech
@asynccontextmanager
async def lifespan(app): init_db(); yield
app=FastAPI(title="Sign Language Translator", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=os.getenv("CORS_ORIGINS","http://localhost:8000").split(","),allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(auth.router); app.include_router(prediction.router); app.include_router(speech.router)
@app.get("/api/health")
def health(): return {"status":"ok","model_available":classifier.available,"hand_tracking_available":detector is not None,"model_message":classifier.error}
app.mount("/",StaticFiles(directory="frontend",html=True),name="frontend")
