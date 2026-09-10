import threading
class SpeechService:
    def __init__(self): self._engine = None
    def speak(self, text):
        if not text.strip(): raise ValueError("Text cannot be empty")
        def run():
            import pyttsx3
            self._engine = pyttsx3.init(); self._engine.say(text); self._engine.runAndWait()
        threading.Thread(target=run, daemon=True).start()
    def stop(self):
        if self._engine: self._engine.stop()
