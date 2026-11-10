import os
import logging
import asyncio
import feedparser
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Trusted Forex News RSS Feeds (FXStreet & Investing.com)
FEEDS = {
    "major": "https://www.fxstreet.com/rss/news",               # General/Major Forex News
    "analysis": "https://www.fxstreet.com/rss/analysis",         # Technical Analysis
    "central_banks": "https://www.fxstreet.com/rss/central-banks", # Central Banks (Fed, ECB, etc.)
}

def build_menu_keyboard():
    """Builds inline keyboard options for the user."""
    keyboard = [
        [
            InlineKeyboardButton("💱 Major Forex News", callback_data="news_major"),
            InlineKeyboardButton("📊 Technical Analysis", callback_data="news_analysis"),
        ],
        [
            InlineKeyboardButton("🏛️ Central Banks", callback_data="news_central_banks"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def fetch_latest_news(feed_key: str, limit: int = 4) -> str:
    """Fetches and formats top currency headlines from an RSS feed."""
    url = FEEDS.get(feed_key)
    if not url:
        return "Category not found."

    feed = feedparser.parse(url)
    if not feed.entries:
        return "Failed to retrieve Forex news at the moment."

    msg = f"📈 **Latest {feed_key.upper().replace('_', ' ')} News**\n\n"
    for entry in feed.entries[:limit]:
        title = entry.get("title", "No Title")
        link = entry.get("link", "#")
        msg += f"• [{title}]({link})\n\n"

    return msg

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends start message with interactive buttons."""
    welcome_text = (
        "Welcome to the **Forex News Bot**! 💱📊\n\n"
        "Select a category below to get the latest currency market updates:"
    )
    await update.message.reply_text(
        text=welcome_text,
        reply_markup=build_menu_keyboard(),
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles button presses from inline keyboards."""
    query = update.callback_query
    await query.answer()

    if query.data.startswith("news_"):
        category = query.data.replace("news_", "")
        news_content = fetch_latest_news(category)

        await query.edit_message_text(
            text=news_content,
            reply_markup=build_menu_keyboard(),
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is missing.")

    # Event loop management for compatibility on Render
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

if __name__ == "__main__":
    main()
