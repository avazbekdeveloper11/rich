from telegram import Update
from telegram.ext import ContextTypes
from services.content import get_random_business_idea

async def business(update: Update, context: ContextTypes.DEFAULT_TYPE):
    idea = get_random_business_idea()

    text = f"""
*Biznes g'oya:*

{idea}

G'oya - bu urug'. Harakatga o'ting!
"""

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(text, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, parse_mode="Markdown")
