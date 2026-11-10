import asyncio
def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is missing. Add it in Render Environment."
        )

    # Create an event loop for the Telegram bot
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(menu_callback))
    application.add_error_handler(error_handler)

    logger.info("Forex Market Education bot is starting.")

    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
