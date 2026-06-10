from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.database import create_user, get_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await create_user(user.id, user.username, user.first_name)

    welcome_text = f"""
Assalomu alaykum, *{user.first_name}*!

Men sizning *Boylik Mentoringizman*!

Men sizga har kuni:
- Motivatsiya beraman
- Moliyaviy bilim o'rgataman
- Biznes g'oyalar taklif qilaman
- Eng muhimi - *tasklar beraman*

Har bir taskni bajarsangiz, boylik tomon bir qadam yaqinlashasiz!

Boshlashga tayyormisiz?
"""

    keyboard = [
        [InlineKeyboardButton("Bugungi taskimni ko'rsat", callback_data="task")],
        [InlineKeyboardButton("Motivatsiya", callback_data="motivation"),
         InlineKeyboardButton("Moliya", callback_data="finance")],
        [InlineKeyboardButton("Biznes g'oya", callback_data="business"),
         InlineKeyboardButton("Progressim", callback_data="progress")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Bugungi task", callback_data="task")],
        [InlineKeyboardButton("Motivatsiya", callback_data="motivation"),
         InlineKeyboardButton("Moliya", callback_data="finance")],
        [InlineKeyboardButton("Biznes g'oya", callback_data="business"),
         InlineKeyboardButton("Progressim", callback_data="progress")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "*Asosiy menyu*\n\nQuyidagilardan birini tanlang:",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
