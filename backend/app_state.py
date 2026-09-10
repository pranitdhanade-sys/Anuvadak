from backend.services.gesture_classifier import GestureClassifier
from backend.services.hand_detector import HandDetector
from backend.services.speech_service import SpeechService
classifier=GestureClassifier()
try: detector=HandDetector()
except RuntimeError: detector=None
speech=SpeechService()
