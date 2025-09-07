from pyrogram import Client
import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from plugins import movie, scheduler as sched_plugin

app = Client(
    "movie_poster_bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="plugins")
)

scheduler = AsyncIOScheduler()

if __name__ == "__main__":
    # start scheduler for auto posts if configured
    sched_plugin.setup(scheduler, app)
    scheduler.start()
    print("🚀 Movie OTT Poster Bot starting...")
    app.run()