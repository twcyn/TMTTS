from datetime import datetime
from pathlib import Path
import threading
import tkinter as tk
from tkinter import scrolledtext

from tts_engine import PAUSE_MARKER, SpeechGenerator

BASE_DIR = Path(__file__).resolve().parent
PAUSE_INSERT_TEXT = f" {PAUSE_MARKER} "


class SpeechTTSApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("英文演講稿 TTS 工具")
        self.root.geometry("640x480")
        self.root.configure(bg="#f5f5f5")

        self.generator = SpeechGenerator()
        self.is_generating = False

        # 頂部工具列
        toolbar = tk.Frame(root, bg="#f5f5f5", padx=12, pady=10)
        toolbar.pack(fill=tk.X)

        self.pause_btn = tk.Button(
            toolbar,
            text="插入停頓 (1秒)",
            command=self.insert_pause,
            font=("Microsoft JhengHei UI", 10),
            bg="#ffffff",
            fg="#222222",
            relief=tk.SOLID,
            bd=1,
            padx=12,
            pady=4,
            cursor="hand2",
        )
        self.pause_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.generate_btn = tk.Button(
            toolbar,
            text="產生 MP3",
            command=self.start_generate_mp3,
            font=("Microsoft JhengHei UI", 10, "bold"),
            bg="#333333",
            fg="#ffffff",
            activebackground="#555555",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=16,
            pady=5,
            cursor="hand2",
        )
        self.generate_btn.pack(side=tk.LEFT)

        # 中間純文字講稿編輯區
        editor_frame = tk.Frame(root, bg="#f5f5f5", padx=12, pady=0)
        editor_frame.pack(fill=tk.BOTH, expand=True)

        self.text_area = scrolledtext.ScrolledText(
            editor_frame,
            wrap=tk.WORD,
            font=("Consolas", 12),
            bg="#ffffff",
            fg="#111111",
            insertbackground="#111111",
            relief=tk.SOLID,
            bd=1,
            padx=10,
            pady=10,
            undo=True,
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        sample_text = (
            "Good morning everyone. [PAUSE]\n\n"
            "Today, I would like to share a story about perseverance. [PAUSE] "
            "When we face challenges, the most important thing is to keep moving forward."
        )
        self.text_area.insert("1.0", sample_text)

        # 底部極簡狀態列
        self.status_var = tk.StringVar(
            value="就緒 — 貼上英文講稿後，點擊「產生 MP3」即可輸出至本資料夾"
        )
        status_label = tk.Label(
            root,
            textvariable=self.status_var,
            anchor="w",
            font=("Microsoft JhengHei UI", 9),
            bg="#f5f5f5",
            fg="#666666",
            padx=12,
            pady=8,
        )
        status_label.pack(fill=tk.X)

    def set_status(self, message: str):
        self.root.after(0, lambda: self.status_var.set(message))

    def insert_pause(self):
        self.text_area.insert(tk.INSERT, PAUSE_INSERT_TEXT)
        self.text_area.focus_set()
        self.status_var.set(f"已在游標處插入 1 秒停頓記號 {PAUSE_MARKER}")

    def start_generate_mp3(self):
        if self.is_generating:
            return

        content = self.text_area.get("1.0", tk.END).strip()
        if not content:
            self.status_var.set("請先輸入或貼上英文講稿文字！")
            return

        self.is_generating = True
        self.generate_btn.config(state=tk.DISABLED, text="產生中...")
        threading.Thread(
            target=self._generate_worker, args=(content,), daemon=True
        ).start()

    def _generate_worker(self, content: str):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = BASE_DIR / f"speech_{timestamp}.mp3"
            saved_file = self.generator.synthesize_to_mp3(
                script_text=content,
                output_path=output_path,
                status_callback=self.set_status,
            )
            self.set_status(f"完成！已儲存 MP3：{saved_file.name}")
        except Exception as exc:
            self.set_status(f"發生錯誤：{exc}")
        finally:
            self.root.after(0, self._reset_button)

    def _reset_button(self):
        self.is_generating = False
        self.generate_btn.config(state=tk.NORMAL, text="產生 MP3")


if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechTTSApp(root)
    root.mainloop()
