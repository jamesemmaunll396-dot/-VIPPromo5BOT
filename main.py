
import asyncio
import logging
import os
import sys

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BotCommand,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ==========================================
# CONFIGURATION
# ==========================================

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ==========================================
# WELCOME MESSAGE
# ==========================================

WELCOME_TEXT = (
    "Welcome to Forex Market Education! 📊\n\n"
    "Explore general currency market information, "
    "financial news and educational resources.\n\n"
    "Select a category below to get started."
)


# ==========================================
# MAIN MENU
# ==========================================

MAIN_MENU = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            "📰 Major Forex News",
            callback_data="news"
        ),
        InlineKeyboardButton(
            "📊 Technical Analysis",
            callback_data="technical"
        ),
    ],
    [
        InlineKeyboardButton(
            "🏦 Central Banks",
            callback_data="central_banks"
        ),
        InlineKeyboardButton(
            "📚 Forex Learning",
            callback_data="learning"
        ),
    ],
    [
        InlineKeyboardButton(
            "⚠️ Risk Management",
            callback_data="risk"
        ),
        InlineKeyboardButton(
            "ℹ️ About & Disclaimer",
            callback_data="about"
        ),
    ],
])


BACK_MENU = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            "⬅️ Back to Menu",
            callback_data="menu"
        )
    ]
])


# ==========================================
# FOREX NEWS LINKS
# ==========================================

NEWS_MENU = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            "Reuters Markets",
            url="https://www.reuters.com/markets/"
        )
    ],
    [
        InlineKeyboardButton(
            "CNBC Finance",
            url="https://www.cnbc.com/finance/"
        )
    ],
    [
        InlineKeyboardButton(
            "MarketWatch",
            url="https://www.marketwatch.com/"
        )
    ],
    [
        InlineKeyboardButton(
            "⬅️ Back to Menu",
            callback_data="menu"
        )
    ],
])


# ==========================================
# CENTRAL BANK LINKS
# ==========================================

CENTRAL_BANKS_MENU = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            "US Federal Reserve",
            url="https://www.federalreserve.gov/"
        )
    ],
    [
        InlineKeyboardButton(
            "European Central Bank",
            url="https://www.ecb.europa.eu/"
        )
    ],
    [
        InlineKeyboardButton(
            "Bank of England",
            url="https://www.bankofengland.co.uk/"
        )
    ],
    [
        InlineKeyboardButton(
            "Bank of Japan",
            url="https://www.boj.or.jp/en/"
        )
    ],
    [
        InlineKeyboardButton(
            "⬅️ Back to Menu",
            callback_data="menu"
        )
    ],
])


# ==========================================
# EDUCATIONAL CONTENT
# ==========================================

PAGES = {

    "technical": (
        "📊 TECHNICAL ANALYSIS\n\n"
        "Technical analysis is the study of historical "
        "price charts and market data.\n\n"
        "Topics to learn:\n\n"
        "1. Candlestick charts\n"
        "2. Market trends\n"
        "3. Support and resistance\n"
        "4. Moving averages\n"
        "5. Technical indicators\n\n"
        "These tools help explain market behaviour. "
        "They cannot predict prices with certainty.\n\n"
        "This content is for educational purposes only."
    ),

    "learning": (
        "📚 FOREX LEARNING\n\n"
        "Welcome to the Forex learning section.\n\n"
        "Begin with these basic concepts:\n\n"
        "1. Currency pairs\n"
        "2. Pips and spreads\n"
        "3. Leverage and margin\n"
        "4. Forex market sessions\n"
        "5. Economic calendars\n"
        "6. Currency market fundamentals\n\n"
        "Learn the basics before considering "
        "real-money trading."
    ),

    "risk": (
        "⚠️ RISK MANAGEMENT\n\n"
        "Forex and leveraged trading involve "
        "substantial financial risks.\n\n"
        "Important educational principles:\n\n"
        "• Understand leverage before using it.\n"
        "• Consider potential losses.\n"
        "• Avoid borrowing money to trade.\n"
        "• Never risk money you cannot afford to lose.\n"
        "• Be cautious of guaranteed-profit promises.\n\n"
        "This section does not provide personalised "
        "financial advice."
    ),

    "about": (
        "ℹ️ ABOUT FOREX MARKET EDUCATION\n\n"
        "This is an independent educational bot "
        "providing general information about:\n\n"
        "• Currency markets\n"
        "• Financial news resources\n"
        "• Central bank announcements\n"
        "• Forex learning materials\n"
        "• Market education\n\n"
        "DISCLAIMER:\n"
        "All information is general and educational. "
        "It is not investment advice or a recommendation "
        "to buy or sell any financial instrument.\n\n"
        "External articles and materials belong to "
        "their respective owners."
    ),

}


# ==========================================
# START COMMAND
# ==========================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.message is None:
        return

    await update.message.reply_text(
        text=WELCOME_TEXT,
        reply_markup=MAIN_MENU
    )

    logger.info(
        "User %s started the bot",
        update.effective_user.id
    )


# ==========================================
# HELP COMMAND
# ==========================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.message is None:
        return

    await update.message.reply_text(
        "Welcome to Forex Market Education!\n\n"
        "Use /start to open the main menu.\n"
        "Choose any category to explore the resources.",
        reply_markup=MAIN_MENU
    )


# ==========================================
# BUTTON HANDLER
# ==========================================

async def menu_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    choice = query.data

    # Return to main menu

    if choice == "menu":

        await query.edit_message_text(
            text=WELCOME_TEXT,
            reply_markup=MAIN_MENU
        )

    # Major Forex News

    elif choice == "news":

        await query.edit_message_text(
            text=(
                "📰 MAJOR FOREX NEWS\n\n"
                "Explore financial news and currency "
                "market coverage from external publishers.\n\n"
                "Select a source below to read its latest "
                "published updates."
            ),
            reply_markup=NEWS_MENU
        )

    # Technical Analysis

    elif choice == "technical":

        await query.edit_message_text(
            text=PAGES["technical"],
            reply_markup=BACK_MENU
        )

    # Central Banks

    elif choice == "central_banks":

        await query.edit_message_text(
            text=(
                "🏦 CENTRAL BANK UPDATES\n\n"
                "Explore official central bank websites "
                "for monetary policy announcements, "
                "interest rate decisions and financial updates.\n\n"
                "Select an institution below."
            ),
            reply_markup=CENTRAL_BANKS_MENU
        )

    # Forex Learning

    elif choice == "learning":

        await query.edit_message_text(
            text=PAGES["learning"],
            reply_markup=BACK_MENU
        )

    # Risk Management

    elif choice == "risk":

        await query.edit_message_text(
            text=PAGES["risk"],
            reply_markup=BACK_MENU
        )

    # About and Disclaimer

    elif choice == "about":

        await query.edit_message_text(
            text=PAGES["about"],
            reply_markup=BACK_MENU
        )

    else:

        await query.edit_message_text(
            text=WELCOME_TEXT,
            reply_markup=MAIN_MENU
        )


# ==========================================
# BOT STARTUP CHECK
# ==========================================

async def post_init(
    application: Application
):

    # Confirm Telegram connection

    bot_info = await application.bot.get_me()

    logger.info(
        "Connected to Telegram successfully: @%s",
        bot_info.username
    )

    # Register Telegram commands

    await application.bot.set_my_commands([
        BotCommand("start", "Open the main menu"),
        BotCommand("help", "Get help"),
    ])


# ==========================================
# ERROR HANDLER
# ==========================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    error = context.error

    if error:

        logger.error(
            "An error occurred while processing an update",
            exc_info=(
                type(error),
                error,
                error.__traceback__
            )
        )


# ==========================================
# MAIN APPLICATION
# ==========================================

def main():

    if not BOT_TOKEN:

        raise RuntimeError(
            "BOT_TOKEN is missing. "
            "Add BOT_TOKEN in Render Environment."
        )

    # Explicitly create an event loop.
    # This addresses the event-loop error in your
    # previous Render deployment logs.

    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    logger.info(
        "Python version: %s",
        sys.version.split()[0]
    )

    # Build Telegram application

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # Register commands

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    # Register inline button handler

    application.add_handler(
        CallbackQueryHandler(menu_callback)
    )

    # Register errors

    application.add_error_handler(
        error_handler
    )

    logger.info(
        "Forex Market Education bot is starting."
    )

    try:

        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=False,
            close_loop=False
        )

    finally:

        if not loop.is_closed():

            loop.close()

        asyncio.set_event_loop(None)


# ==========================================
# RUN BOT
# ==========================================

if __name__ == "__main__":

    main()
