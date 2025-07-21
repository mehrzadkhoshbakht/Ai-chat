# 💎 HyperPrompt Platinum — Zero‑Touch MikroTik AI Content Factory

## 🎯 Mission
Create a *fully autonomous* Persian content production system for MikroTik tutorials using AI, minimal resources, and smart orchestration.

---

## 🧱 System Goals & Capabilities

1. **Resource-aware scheduling**: Auto-detect 4GB RAM, 2 CPU cores, 1 Gbps bandwidth. Run only when idle.
2. **Trend-driven planning**: Scrape Google Trends, Reddit, X to identify hot MikroTik topics.
3. **Persian script generation**: Write tutorial scripts from basic to advanced.
4. **Text-to-Speech (TTS)**: Use Coqui (offline) or fallback to cloud TTS.
5. **Visual creation**: Generate slides/images with StableDiffusion, DALL·E, Runway.
6. **Video production**: Combine with moviepy/ffmpeg, normalize sound, add watermark.
7. **Subtitles & Translations**: Create Farsi SRTs + translate to EN/AR using Whisper.
8. **Publishing**: Upload to YouTube (full), Twitter (teaser), Instagram Reels (≤ 90s).
9. **SEO + Hashtag AI**: Use past feedback to optimize title, description, hashtags.
10. **Feedback learning**: Analyze daily CTR, engagement, adapt with Q-learning.
11. **Orchestration**: Self-healing Celery worker (Redis Streams), Airflow fallback.
12. **Storage mgmt**: Backup finished media, clean up local storage.

---

## ⚙️ Project Structure

```
zero_touch_mikrotik/
├─ bootstrap.py               # Interactive installer (env + Docker setup)
├─ orchestrator.py            # Celery-based job runner + scheduler
├─ services/
│  ├─ resource_watcher.py     # Monitor CPU, RAM, bandwidth
│  ├─ trend_scanner.py        # Fetch trending topics
│  ├─ content_planner.py      # Pick right MikroTik lessons
│  ├─ script_generator.py     # Create Persian scripts
│  ├─ voice_generator.py      # TTS using Coqui/cloud
│  ├─ visual_generator.py     # Generate visuals from scripts
│  ├─ video_assembler.py      # Merge content into final video
│  ├─ subtitle_translator.py  # Create SRT + translate
│  ├─ publisher.py            # Post to YouTube, X, IG
│  ├─ feedback_analytics.py   # Analyze reactions, update planner
│  └─ storage_manager.py      # Backup & cleanup
├─ data/
│  ├─ scripts/      ├─ audio/      ├─ videos/     ├─ subtitles/   └─ logs/
├─ config/
│  ├─ scheduler_config.yaml   └─ hashtags.json
└─ README.md
```

---

## 🔐 Security & Deployment

- Dockerized architecture (services are containerized)
- Encrypted API keys / .env configs
- Offline-first (Coqui, Whisper) with fallback cloud options
- Tokenized publishing
- Localhost-only access for admin dashboard
- Object storage backup with media versioning

---

## 🧠 Intelligence Engine

- Q-learning task scheduler (topic, time, length, hashtag optimizer)
- Feedback loop with analytics: CTR, comments, watch-time
- Self-healing job queue: retries + dynamic rescheduling
- Trend comparison across regions and languages

---

## 🚀 Getting Started with Docker

This project is designed to run with Docker and Docker Compose for easy setup and deployment.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Configuration

1.  **API Keys:** Before running the application, you need to provide your API keys. Create a file named `.env` in the `zero_touch_mikrotik` directory with the following content:

    ```env
    OPENAI_API_KEY=your_openai_api_key

    # Twitter API Credentials
    TWITTER_CONSUMER_KEY=your_twitter_consumer_key
    TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret
    TWITTER_ACCESS_TOKEN=your_twitter_access_token
    TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

    # Instagram Credentials
    INSTAGRAM_USERNAME=your_instagram_username
    INSTAGRAM_PASSWORD=your_instagram_password

    # Email Notification Credentials (for error reporting)
    # Note: For Gmail, you may need to use an "App Password"
    EMAIL_USER=your_email@gmail.com
    EMAIL_PASSWORD=your_email_app_password
    EMAIL_TO=recipient_email@example.com
    ```

2.  **YouTube Authentication:** The first time you run the application, you will need to authorize it to access your YouTube account. Follow the on-screen instructions in the terminal where you run `docker-compose`. This will generate a `youtube_credentials.json` file.

### Running the Application

1.  **Build and Run the Containers:**
    Open a terminal in the `zero_touch_mikrotik` directory and run:
    ```bash
    docker-compose up --build
    ```
    This will build the Docker image, download the Redis image, and start all the services.

2.  **Triggering a Task Manually (Optional):**
    If you want to trigger the content creation pipeline manually for testing, you can open another terminal and run:
    ```bash
    docker-compose exec app celery -A orchestrator call orchestrator.main_task
    ```

---

## 📦 Output

You will receive:
- Daily YouTube-ready Persian MikroTik video
- SEO-optimized title, description, and hashtags
- Reels/Shorts automatically sliced and scheduled
- Subtitle files in `.srt` (FA/EN/AR)
- Clean local state with object storage backup

---

## ✅ Goals

🚀 Zero human babysitting after setup
🎯 Publish like clockwork
🧠 Learn & improve from performance
📊 Align with trending market demand
