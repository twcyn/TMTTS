import os
from pathlib import Path
from tts_engine import SpeechGenerator

BASE_DIR = Path(__file__).resolve().parent
SCRIPT_FILE = BASE_DIR / "script.txt"
OUTPUT_DIR = BASE_DIR / "output"
LATEST_MP3 = OUTPUT_DIR / "latest_speech.mp3"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 支援從環境變數 INPUT_SCRIPT 讀取，或直接讀取 script.txt
    script_text = os.environ.get("INPUT_SCRIPT", "").strip()
    if not script_text:
        if not SCRIPT_FILE.exists():
            raise FileNotFoundError(f"找不到講稿檔案：{SCRIPT_FILE}")
        script_text = SCRIPT_FILE.read_text(encoding="utf-8").strip()
    else:
        # 若從 Action 輸入框提供文字，同步更新回 script.txt
        SCRIPT_FILE.write_text(script_text + "\n", encoding="utf-8")

    if not script_text:
        raise ValueError("script.txt 內容為空，請先貼上英文講稿。")

    generator = SpeechGenerator()
    saved = generator.synthesize_to_mp3(
        script_text=script_text,
        output_path=LATEST_MP3,
        status_callback=print,
    )
    print(f"成功產生 MP3：{saved}")


if __name__ == "__main__":
    main()
