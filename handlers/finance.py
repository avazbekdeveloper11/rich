from telegram import Update
from telegram.ext import ContextTypes
from services.content import get_random_finance_tip

async def finance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tip = get_random_finance_tip()

    text = f"""
*Moliyaviy maslahat:*

{tip}

Bilim - bu eng yaxshi investitsiya!
"""

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(text, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, parse_mode="Markdown")
