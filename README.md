# XTTS-v2 Multilingual Voice Cloning Backend

FastAPI backend for multilingual text-to-speech and voice cloning using XTTS-v2.

## Run locally
```
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8000
```

## API
POST /synthesize
Fields:
- text
- language (optional)
- speaker (optional WAV)

Returns: WAV audio file.
