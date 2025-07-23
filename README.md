# AI-chat: Automated MikroTik Video Tutorial Generator

🧠 About

AI-chat is a smart content automation tool built to generate high-quality MikroTik video tutorials.
It combines artificial intelligence, Q-learning decision making, text-to-speech processing, and video editing tools to create and publish educational content across multiple platforms — all automatically.
It is designed to run fully inside Replit with zero local setup.


---

🖥️ System Information

| Property | Value |
|---|---|
| Version | 1.0.0 |
| Platform | Linux / Python (Replit) |
| Database | SQLite |
| AI Engine | Q-Learning |



---

🚀 Features

✅ Automated Video Generation
✅ AI-Powered Content Planning
✅ Multi-Platform Publishing (e.g., YouTube, Telegram)
✅ Trend & Hashtag Analysis
✅ Resource Optimization (CPU/RAM-aware scheduling)
✅ Telegram Notifications


---

📁 Project Structure

```
AI-chat/
├── main.py                  # Entry point of the application
├── requirements.txt         # Dependencies
├── README.md                # Documentation
├── config/                  # YAML/JSON configuration files
├── modules/
│   ├── chat_engine/         # AI-based content planner and dialogue handler
│   ├── text_to_speech/      # TTS engine (Google, ElevenLabs, etc.)
│   ├── video_generator/     # Combines voice, video templates, subtitles
│   ├── logger/              # Logs, events, and debugging
│   └── utils/               # Helper functions and file handling
├── data/
│   ├── scripts/             # Training scripts or input content
│   ├── audio/               # Generated audio files
│   ├── videos/              # Final exported video files
│   └── subtitles/           # Subtitle files (e.g. SRT)
├── tests/                   # Unit tests
├── scripts/                 # Automation scripts (e.g. deploy, cleanup)
└── docs/                    # Technical documentation and architecture
```

---

▶️ How to Run (on Replit)

1. Open the project in Replit
2. Click the "Run" button
3. Monitor logs and outputs directly from the console

---

📌 Future Plans

- [ ] YouTube integration with scheduling
- [ ] AI-based subtitle translation
- [ ] Voice cloning for custom branding
- [ ] Web dashboard (optional)

---

📜 License
M.khoshbakht
