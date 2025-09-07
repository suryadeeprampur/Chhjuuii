# Movie OTT Poster Bot (Full)
An enhanced Telegram Poster Bot that fetches movie posters and basic info from TMDB, supports scheduled auto-posting, Docker, Render/Heroku deploy, and CI workflow.

## Features
- `/movie <title>` — search TMDB and send poster + info
- Inline buttons: Watch (placeholders), Download (placeholder)
- Scheduled auto-post to a target channel (via APScheduler cron)
- Dockerfile, Procfile, and GitHub Actions workflow included
- Easy to expand: JustWatch integration, OTT mapping, admin panel

## Quickstart (local)
1. Copy `.env.example` to `.env` and fill credentials.
2. Install dependencies and run:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python app.py
   ```

## Deploy
- **Heroku**: push to Git, set environment variables, scale worker: `heroku ps:scale worker=1`
- **Render**: Create a Background Worker service using Dockerfile or `python app.py` command.
- **Docker**:
   ```bash
   docker build -t movie-ott-bot .
   docker run --env-file .env movie-ott-bot
   ```

## Notes
- For accurate OTT availability, integrate JustWatch or another OTT availability source.
- Scheduler uses APScheduler and supports a CRON expression via environment variable (example provided).