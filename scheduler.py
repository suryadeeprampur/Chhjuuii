# scheduler helpers for auto-posting
import os
import config
from apscheduler.triggers.cron import CronTrigger
import random

SAMPLE_MOVIES = [
    "The Matrix", "Inception", "Interstellar", "Titanic", "Avengers: Endgame"
]

def setup(scheduler, app_client):
    cron_expr = os.getenv("SCHEDULE_CRON", "")
    target = os.getenv("TARGET_CHANNEL", "")
    if not cron_expr or not target:
        return

    # basic cron parser expecting "min hour day month dow" or a string accepted by CronTrigger
    try:
        trigger = CronTrigger.from_crontab(cron_expr)
    except Exception:
        return

    def job():
        # pick a random sample movie and send using app_client
        title = random.choice(SAMPLE_MOVIES)
        # we can't call async send here directly; use app_client.loop.create_task
        app_client.loop.create_task(_send_movie(title, app_client, target))

    scheduler.add_job(job, trigger=trigger, id="daily_poster_job")

async def _send_movie(title, app_client, target):
    # reuse movie search handler logic by calling TMDB directly
    import requests
    TMDB_BASE = "https://api.themoviedb.org/3"
    IMG_BASE = "https://image.tmdb.org/t/p/w500"
    params = {"api_key": config.TMDB_API_KEY, "query": title, "page": 1}
    r = requests.get(f"{TMDB_BASE}/search/movie", params=params, timeout=15)
    if r.status_code != 200:
        return
    data = r.json()
    results = data.get("results") or []
    if not results:
        return
    movie = results[0]
    caption = f"🎬 *{movie.get('title')}* ({(movie.get('release_date') or 'N/A')[:4]})\n⭐ TMDB: {movie.get('vote_average')}\n\n{(movie.get('overview') or '')[:800]}"
    poster_path = movie.get('poster_path')
    buttons = [
        [dict(text='▶️ Watch (Netflix)', url='https://www.netflix.com/')],
        [dict(text='▶️ Watch (Prime)', url='https://www.primevideo.com/')],
    ]
    if poster_path:
        poster_url = IMG_BASE + poster_path
        await app_client.send_photo(chat_id=target, photo=poster_url, caption=caption, reply_markup={'inline_keyboard': buttons})
    else:
        await app_client.send_message(chat_id=target, text=caption, reply_markup={'inline_keyboard': buttons})