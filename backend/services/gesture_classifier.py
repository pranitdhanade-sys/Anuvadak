import os, joblib, numpy as np
class GestureClassifier:
    def __init__(self, model_path=None):
        self.model_path = model_path or os.getenv("MODEL_PATH", "ml/models/gesture_classifier.joblib")
        self.model = None; self.error = None
        self.load()
    def load(self):
        try: self.model, self.error = joblib.load(self.model_path), None
        except FileNotFoundError: self.error = f"Model missing at {self.model_path}. Collect data and run: python ml/train.py"; self.model = None
    @property
    def available(self): return self.model is not None
    def predict(self, features):
        if not self.model: raise RuntimeError(self.error)
        probabilities = self.model.predict_proba(np.asarray(features).reshape(1,-1))[0]
        index = int(np.argmax(probabilities)); return str(self.model.classes_[index]), float(probabilities[index])
