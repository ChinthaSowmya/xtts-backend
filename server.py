import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from tts_service import TTSService

OUTPUT_DIR = Path("outputs")
SPEAKER_DIR = Path("speakers")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(SPEAKER_DIR, exist_ok=True)

app = FastAPI(title="XTTS-v2 Voice Cloning API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tts = TTSService(model_name="coqui/XTTS-v2")

@app.get("/health")
def health():
    return {"status": "running", "model": "coqui/XTTS-v2"}

@app.post("/synthesize")
async def synthesize(
    text: str = Form(...),
    language: str = Form(None),
    speaker: UploadFile = File(None)
):
    uid = uuid.uuid4().hex
    output_path = OUTPUT_DIR / f"{uid}.wav"

    speaker_path = None
    if speaker:
        ext = Path(speaker.filename).suffix
        speaker_path = SPEAKER_DIR / f"{uid}{ext}"
        with speaker_path.open("wb") as f:
            shutil.copyfileobj(speaker.file, f)

    try:
        tts.synthesize_to_file(
            text=text,
            out_path=str(output_path),
            speaker_wav=str(speaker_path) if speaker_path else None,
            language=language
        )
        return FileResponse(str(output_path), media_type="audio/wav", filename="output.wav")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    finally:
        if speaker_path and speaker_path.exists():
            speaker_path.unlink()
