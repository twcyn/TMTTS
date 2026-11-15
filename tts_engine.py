from pathlib import Path
from typing import Callable
import urllib.request
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro
from kokoro_onnx.config import SAMPLE_RATE

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"

MODEL_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx"
VOICES_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin"

MODEL_PATH = MODELS_DIR / "kokoro-v1.0.int8.onnx"
VOICES_PATH = MODELS_DIR / "voices-v1.0.bin"

# 預設使用自然的美式英文女聲 af_heart
DEFAULT_VOICE = "af_heart"
PAUSE_MARKER = "[PAUSE]"
PAUSE_SECONDS = 1.0


def ensure_models(status_callback: Callable[[str], None] | None = None) -> tuple[Path, Path]:
    """確認 Kokoro 模型檔案存在，若不存在則自動下載。"""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    if not MODEL_PATH.exists():
        if status_callback:
            status_callback("首次執行：正在下載 Kokoro 語音模型 (約 88MB)...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)

    if not VOICES_PATH.exists():
        if status_callback:
            status_callback("首次執行：正在下載英文女聲設定檔 (約 27MB)...")
        urllib.request.urlretrieve(VOICES_URL, VOICES_PATH)

    return MODEL_PATH, VOICES_PATH


class SpeechGenerator:
    def __init__(self, voice: str = DEFAULT_VOICE):
        self.voice = voice
        self._kokoro: Kokoro | None = None

    def _get_engine(self, status_callback: Callable[[str], None] | None = None) -> Kokoro:
        if self._kokoro is None:
            model_path, voices_path = ensure_models(status_callback)
            if status_callback:
                status_callback("正在載入 Kokoro TTS 引擎...")
            self._kokoro = Kokoro(str(model_path), str(voices_path))
        return self._kokoro

    def synthesize_to_mp3(
        self,
        script_text: str,
        output_path: str | Path,
        pause_seconds: float = PAUSE_SECONDS,
        status_callback: Callable[[str], None] | None = None,
    ) -> Path:
        """
        將包含 [PAUSE] 記號的英文講稿轉為 MP3 檔案。
        每個 [PAUSE] 對應插入 pause_seconds 秒的靜音停頓。
        """
        kokoro = self._get_engine(status_callback)

        parts = script_text.split(PAUSE_MARKER)
        audio_chunks: list[np.ndarray] = []
        pause_samples = np.zeros(int(SAMPLE_RATE * pause_seconds), dtype=np.float32)

        total_parts = len(parts)
        for idx, raw_segment in enumerate(parts):
            segment = raw_segment.strip()
            if segment:
                if status_callback:
                    status_callback(f"正在合成語音片段 ({idx + 1}/{total_parts})...")
                samples, _ = kokoro.create(
                    segment,
                    voice=self.voice,
                    speed=1.0,
                    lang="en-us",
                )
                if len(samples) > 0:
                    audio_chunks.append(samples.astype(np.float32))

            # 若不是最後一段，代表中間有一個 [PAUSE] 記號
            if idx < total_parts - 1:
                audio_chunks.append(pause_samples)

        if not audio_chunks:
            raise ValueError("講稿中沒有可發音的英文內容。")

        full_audio = np.concatenate(audio_chunks)
        output_file = Path(output_path).resolve()

        if status_callback:
            status_callback("正在輸出 MP3 檔案...")

        sf.write(str(output_file), full_audio, SAMPLE_RATE, format="MP3")
        return output_file
