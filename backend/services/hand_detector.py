import cv2, numpy as np
from .feature_extractor import LANDMARKS_PER_HAND
class HandDetector:
    def __init__(self):
        try:
            import mediapipe as mp
            self.hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, model_complexity=0, min_detection_confidence=.55, min_tracking_confidence=.55)
        except ImportError as exc: raise RuntimeError("MediaPipe is not installed") from exc
    def detect(self, image_bytes: bytes):
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        if image is None: raise ValueError("Invalid image data")
        result = self.hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        return [] if not result.multi_hand_landmarks else [[[p.x,p.y,p.z] for p in hand.landmark] for hand in result.multi_hand_landmarks]
