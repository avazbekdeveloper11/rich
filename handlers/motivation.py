from telegram import Update
from telegram.ext import ContextTypes
from services.content import get_random_motivation

async def motivation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quote = get_random_motivation()

    text = f"""
*Bugungi motivatsiya:*

_{quote}_

Boylik tomon oldinga!
"""

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(text, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, parse_mode="Markdown")
