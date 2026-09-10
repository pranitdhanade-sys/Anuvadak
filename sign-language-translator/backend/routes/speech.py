from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.app_state import speech
router=APIRouter(prefix="/api/speech", tags=["speech"])
class SpeechRequest(BaseModel): text: str = Field(min_length=1,max_length=1000)
@router.post("")
def speak(body: SpeechRequest):
    try: speech.speak(body.text); return {"status":"speaking"}
    except ValueError as exc: raise HTTPException(422,str(exc))
@router.post("/stop")
def stop(): speech.stop(); return {"status":"stopped"}
