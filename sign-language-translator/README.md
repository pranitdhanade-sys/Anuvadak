# Sign Language Translator

A modular SIH social-impact prototype that translates trained Indian Sign Language (ISL) hand gestures to text and speech. The browser owns webcam access; it samples compressed frames twice a second and sends them over REST only while translation is active. FastAPI uses MediaPipe to find one or two hands, converts 21 landmarks per hand into translation- and scale-invariant 126-value features, and runs a persisted scikit-learn Random Forest.

> **Responsible deployment:** ISL is a complete language and signs vary by signer and region. This project deliberately returns no invented recognition when the model has not been trained. Collect diverse, consented data with ISL users and validate each deployed vocabulary.

## Architecture

`Browser webcam → /api/predict → MediaPipe landmarks → normalized features → Random Forest → sentence builder / browser speech`.

FastAPI serves the static frontend and provides authentication plus speech endpoints. Docker production uses PostgreSQL; local development/tests default to SQLite. Passwords use bcrypt hashes. The persisted PostgreSQL data lives in the `postgres_data` Docker volume.

## Run with Docker (production infrastructure)

```bash
cp .env.example .env                 # change POSTGRES_PASSWORD and SECRET_KEY
docker compose up --build
# open http://localhost:8000
docker compose down                  # stop services
docker compose down -v               # also remove PostgreSQL data
```

The backend waits for PostgreSQL's healthcheck. Camera access stays in the browser, so it works on the host without passing a webcam device into a container. Train the model on the host and it is mounted into the backend container at `ml/models/`.

## Local setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Optional local database fallback (default): do not set DATABASE_URL
uvicorn backend.app:app --reload
# open http://localhost:8000
pytest -q
```

For local PostgreSQL, set `DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/DB`. Configure CORS and model location in `.env` (copy `.env.example`); no secrets are hardcoded.

## Real dataset and training workflow

Collect **many samples per label**, across people, lighting, distance, handedness, and background. Labels can be alphabet signs and words such as `HELLO`, `THANK_YOU`, `YES`, `NO`, `HELP`, `PLEASE`, `GOOD_MORNING`, plus controls `SPACE`, `DELETE`, `CLEAR`.

```bash
python ml/collect_data.py HELLO       # SPACE saves a real landmark sample; Q exits
python ml/collect_data.py YES
# repeat for every desired label
python ml/preprocess.py
python ml/train.py                    # writes ml/models/gesture_classifier.joblib
python ml/evaluate.py
```

`ml/collect_data.py` accesses a host webcam. `ml/preprocess.py` validates/normalizes samples, `train.py` fits a CPU-friendly Random Forest, `evaluate.py` reports accuracy, and `predict.py sample.json` runs a saved model against a landmark JSON sample. The API reports a clear 503 training message until the model exists.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Backend/model/hand-tracker status |
| GET | `/api/gestures` | Available trained labels |
| POST | `/api/predict` | Multipart `image` JPEG/PNG/WebP frame |
| POST | `/api/speech` | `{ "text": "..." }` backend speech fallback |
| POST | `/api/speech/stop` | Stop backend speech |
| POST | `/api/auth/signup` | Email/password registration |
| POST | `/api/auth/login` | Password-verified login |

## Troubleshooting

- **Model needs training:** follow the collection/training workflow; predictions are intentionally unavailable without a genuine model.
- **Camera unavailable:** grant browser camera permission, close competing camera apps, and use localhost/HTTPS.
- **Low confidence/repeated text:** improve training diversity; the UI requires 70% confidence and a 1.2-second gesture debounce (both configurable in source/env).
- **Container cannot speak:** browser speech is preferred; host audio is not normally available to containers.
