
import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# Railway environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

WELCOME_TEXT = (
    "Welcome to Forex Market Education!\n\n"
    "Explore general currency-market information, educational resources, "
    "and links to financial news and official central-bank updates.\n\n"
    "Choose a section below to get started."
)

MENU = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📰 Major Forex News", callback_data="news"),
        InlineKeyboardButton("📊 Technical Analysis", callback_data="technical"),
    ],
    [
        InlineKeyboardButton("🏦 Central Banks", callback_data="central_banks"),
        InlineKeyboardButton("📚 Forex Learning", callback_data="learning"),
    ],
    [
        InlineKeyboardButton("⚠️ Risk Management", callback_data="risk"),
        InlineKeyboardButton("ℹ️ About & Disclaimer", callback_data="about"),
    ],
])

BACK_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("⬅️ Back to menu", callback_data="menu")]
])

NEWS_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("Reuters Markets", url="https://www.reuters.com/markets/")],
    [InlineKeyboardButton("CNBC Finance", url="https://www.cnbc.com/finance/")],
    [InlineKeyboardButton("MarketWatch", url="https://www.marketwatch.com/")],
    [InlineKeyboardButton("⬅️ Back to menu", callback_data="menu")],
])

CENTRAL_BANKS_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("US Federal Reserve", url="https://www.federalreserve.gov/")],
    [InlineKeyboardButton("European Central Bank", url="https://www.ecb.europa.eu/")],
    [InlineKeyboardButton("Bank of England", url="https://www.bankofengland.co.uk/")],
    [InlineKeyboardButton("Bank of Japan", url="https://www.boj.or.jp/en/")],
    [InlineKeyboardButton("⬅️ Back to menu", callback_data="menu")],
])

PAGES = {
    "technical": (
        "📊 Technical Analysis – Learning Guide\n\n"
        "Technical analysis is the study of historical price charts and market "
        "data. It cannot predict prices with certainty.\n\n"
        "Topics to study:\n"
        "• Candlesticks and price charts\n"
        "• Market trends\n"
        "• Support and resistance\n"
        "• Moving averages\n"
        "• Technical indicators\n\n"
        "This section is educational, not a trade recommendation."
    ),

    "learning": (
        "📚 Forex Learning Resources\n\n"
        "Start with these basic concepts:\n\n"
        "1. Currency pairs: base and quote currencies.\n"
        "2. Pips and spreads: price movements and transaction costs.\n"
        "3. Leverage and margin: understand how leverage magnifies "
        "both gains and losses.\n"
        "4. Market sessions: learn when major currency markets are active.\n"
        "5. Economic calendars: understand scheduled financial events.\n\n"
        "Learn each topic before considering real-money trading."
    ),

    "risk": (
        "⚠️ Risk Management Basics\n\n"
        "Forex and leveraged trading involve substantial risk. "
        "You can lose some or all of the money you deposit.\n\n"
        "Educational risk principles:\n"
        "• Never trade with money you cannot afford to lose.\n"
        "• Understand leverage and margin.\n"
        "• Consider possible losses before entering a trade.\n"
        "• Avoid borrowing money to trade.\n"
        "• Be cautious of guaranteed-profit promises.\n\n"
        "This bot does not provide personalised financial advice."
    ),

    "about": (
        "ℹ️ About Forex Market Education\n\n"
        "This independent bot shares general Forex education "
        "and directs users to external financial-news publishers "
        "and official central-bank websites.\n\n"
        "Third-party articles, logos and materials remain the "
        "property of their respective owners.\n\n"
        "Disclaimer: Information is general and educational only. "
        "It is not investment advice or a recommendation to buy or sell. "
        "Always verify information with the original source."
    ),
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            WELCOME_TEXT,
            reply_markup=MENU
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "Use /start to open the menu.\n"
            "Choose a topic to view educational information and source links.",
            reply_markup=MENU
        )


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if not query:
        return

    await query.answer()
    choice = query.data

    if choice == "menu":
        await query.edit_message_text(
            WELCOME_TEXT,
            reply_markup=MENU
        )

    elif choice == "news":
        await query.edit_message_text(
            "📰 Major Forex News\n\n"
            "Use the links below to read current market coverage "
            "from the original publishers. This bot does not copy "
            "or republish their articles.",
            reply_markup=NEWS_KEYBOARD,
            disable_web_page_preview=True
        )

    elif choice == "central_banks":
        await query.edit_message_text(
            "🏦 Official Central Bank Updates\n\n"
            "Select an official institution website to check "
            "its statements, policy decisions and announcements.",
            reply_markup=CENTRAL_BANKS_KEYBOARD,
            disable_web_page_preview=True
        )

    elif choice in PAGES:
        await query.edit_message_text(
            PAGES[choice],
            reply_markup=BACK_BUTTON
        )

    else:
        await query.edit_message_text(
            WELCOME_TEXT,
            reply_markup=MENU
        )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.exception(
        "An error occurred while processing an update:",
        exc_info=context.error
    )


def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is missing. Add your Telegram bot token "
            "in Railway under Service > Variables."
        )

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(menu_callback))
    application.add_error_handler(error_handler)

    logger.info("Forex Market Education bot is starting.")

    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
