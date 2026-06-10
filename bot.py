import asyncio
import logging
from datetime import time
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from telegram.request import HTTPXRequest
from config import BOT_TOKEN, DAILY_MOTIVATION_HOUR, DAILY_MOTIVATION_MINUTE
from services.database import init_db, get_all_users
from services.content import get_random_motivation
from handlers.start import start, menu
from handlers.motivation import motivation
from handlers.finance import finance
from handlers.business import business
from handlers.tasks import task, done, progress

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def send_daily_motivation(context: ContextTypes.DEFAULT_TYPE):
    users = await get_all_users()
    quote = get_random_motivation()

    text = f"""
*Xayrli tong!*

*Bugungi motivatsiya:*
_{quote}_

Bugungi taskingizsz uchun /task bosing!
"""

    for user_id in users:
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=text,
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Xabar yuborishda xatolik {user_id}: {e}")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == "task":
        await task(update, context)
    elif data == "motivation":
        await motivation(update, context)
    elif data == "finance":
        await finance(update, context)
    elif data == "business":
        await business(update, context)
    elif data == "progress":
        await progress(update, context)
    elif data == "done":
        await done(update, context)

async def post_init(application: Application):
    await init_db()
    logger.info("Database initialized")

def main():
    request = HTTPXRequest(
        connect_timeout=30.0,
        read_timeout=30.0,
        write_timeout=30.0,
        pool_timeout=30.0
    )
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .request(request)
        .post_init(post_init)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("motivation", motivation))
    application.add_handler(CommandHandler("finance", finance))
    application.add_handler(CommandHandler("business", business))
    application.add_handler(CommandHandler("task", task))
    application.add_handler(CommandHandler("done", done))
    application.add_handler(CommandHandler("progress", progress))

    application.add_handler(CallbackQueryHandler(button_handler))

    job_queue = application.job_queue
    job_queue.run_daily(
        send_daily_motivation,
        time=time(hour=DAILY_MOTIVATION_HOUR, minute=DAILY_MOTIVATION_MINUTE),
        name="daily_motivation"
    )

    logger.info("Bot ishga tushdi!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
