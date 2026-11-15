# TMTTS — 英文演講稿 TTS 語音產生工具 (Kokoro 女聲)

不需在電腦安裝 Python 或 TTS，直接在 GitHub 上貼上講稿即可自動產生英文女聲 `.mp3`！

---

## ☁️ 在任何電腦直接使用（GitHub 雲端版）

### 方法 A：直接編輯 `script.txt`（最快）
1. 👉 **[點我直接編輯 `script.txt` 貼上講稿](https://github.com/twcyn/TMTTS/edit/main/script.txt)**
   - 需要 **1 秒停頓** 的地方，直接打上 `[PAUSE]`（若要 2 秒可打兩個 `[PAUSE] [PAUSE]`）。
   - 貼好後，點擊右上角綠色的 **`Commit changes...`** 儲存。
2. 等待約 **30~45 秒**（可點上方 **[Actions](https://github.com/twcyn/TMTTS/actions)** 查看綠勾勾進度）。
3. 👉 **[點我直接下載最新產生的 `latest_speech.mp3`](https://github.com/twcyn/TMTTS/raw/main/output/latest_speech.mp3)**

### 方法 B：使用線上「插入停頓」按鈕網頁
- 若開啟了 GitHub Pages，可前往 **[https://twcyn.github.io/TMTTS/](https://twcyn.github.io/TMTTS/)**，提供跟本機版一模一樣的 **「插入停頓 (1秒)」** 按鈕，點一下即可複製並跳轉至 `script.txt` 儲存。

---

## 💻 本機視窗版（已安裝環境之電腦）
直接雙擊資料夾內的 **`啟動工具.bat`**（或執行 `python app.py`），即可開啟獨立小視窗產生 MP3。
