from TTS.api import TTS
import torch

class TTSService:
    def __init__(self, model_name="coqui/XTTS-v2"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading XTTS model on {self.device} ...")

        self.tts = TTS(
            model_name=model_name,
            progress_bar=False,
            gpu=(self.device == "cuda")
        )

        if self.device == "cuda":
            try:
                self.tts.to("cuda")
            except Exception as e:
                print("CUDA move failed:", e)

    def synthesize_to_file(self, text, out_path, speaker_wav=None, language=None):
        extra = {}
        if language:
            extra["language"] = language

        if speaker_wav:
            self.tts.tts_with_vc_to_file(
                text=text,
                speaker_wav=speaker_wav,
                file_path=out_path,
                **extra
            )
        else:
            self.tts.tts_to_file(
                text=text,
                file_path=out_path,
                **extra
            )
