from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config, os

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    text = "👋 Hi! I'm Movie OTT Poster Bot.\n\nSend /movie <movie name> to get poster and info."
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔎 Search Movie", switch_inline_query_current_chat="")],
        [InlineKeyboardButton("🌐 Source (TMDB)", url="https://www.themoviedb.org/")]
    ])
    await message.reply(text, reply_markup=buttons)