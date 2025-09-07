from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests, config, os

TMDB_BASE = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p/w500"

@Client.on_message(filters.command("movie"))
async def movie_search(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: /movie The Matrix")

    query = message.text.split(" ", 1)[1].strip()
    await message.chat.do("typing")
    params = {"api_key": config.TMDB_API_KEY, "query": query, "page": 1}
    r = requests.get(f"{TMDB_BASE}/search/movie", params=params, timeout=15)
    if r.status_code != 200:
        return await message.reply("❌ TMDB API error. Check your TMDB_API_KEY and network.")

    data = r.json()
    results = data.get("results") or []
    if not results:
        return await message.reply("❌ Movie not found on TMDB.")

    movie = results[0]
    title = movie.get("title") or movie.get("name") or "Unknown"
    year = (movie.get("release_date") or "N/A")[:4]
    overview = movie.get("overview") or "No description available."
    rating = movie.get("vote_average", "N/A")
    poster_path = movie.get("poster_path")

    caption = f"🎬 *{title}* ({year})\n⭐ TMDB: {rating}\n\n{overview[:800]}"

    buttons = [
        [InlineKeyboardButton("▶️ Watch (Netflix)", url="https://www.netflix.com/")],
        [InlineKeyboardButton("▶️ Watch (Prime)", url="https://www.primevideo.com/")],
        [InlineKeyboardButton("📥 Download", url="https://example.com/download")],
    ]

    if poster_path:
        poster_url = IMG_BASE + poster_path
        await client.send_photo(
            chat_id=message.chat.id,
            photo=poster_url,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        await message.reply(caption, reply_markup=InlineKeyboardMarkup(buttons))