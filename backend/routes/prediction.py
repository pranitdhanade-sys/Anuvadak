from fastapi import APIRouter, File, HTTPException, UploadFile
from backend.app_state import classifier, detector
from backend.services.feature_extractor import extract_features
router=APIRouter(prefix="/api", tags=["prediction"])
@router.get("/gestures")
def gestures(): return {"model_available":classifier.available,"labels":[] if not classifier.available else classifier.model.classes_.tolist(),"message":classifier.error}
@router.post("/predict")
async def predict(image: UploadFile=File(...)):
    if image.content_type not in {"image/jpeg","image/png","image/webp"}: raise HTTPException(415,"Upload a JPEG, PNG, or WebP frame")
    if not classifier.available: raise HTTPException(503,classifier.error)
    if detector is None: raise HTTPException(503, "Hand tracking is unavailable; install MediaPipe correctly")
    try:
        hands=detector.detect(await image.read())
        if not hands: return {"detected":False,"message":"No hand detected"}
        label, confidence=classifier.predict(extract_features(hands))
        return {"detected":True,"gesture":label,"confidence":confidence,"hand_count":len(hands)}
    except ValueError as exc: raise HTTPException(422,str(exc))
