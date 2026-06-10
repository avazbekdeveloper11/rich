from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.database import get_user, create_user, complete_task, get_user_progress
from services.content import get_task_by_id

CATEGORY_EMOJI = {
    "asoslar": "📋",
    "tejash": "💰",
    "bilim": "📚",
    "daromad": "💵",
    "tarmoq": "🤝",
    "investitsiya": "📈",
    "davom": "🚀"
}

async def task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        user_id = update.callback_query.from_user.id
        username = update.callback_query.from_user.username
        first_name = update.callback_query.from_user.first_name
    else:
        user_id = update.effective_user.id
        username = update.effective_user.username
        first_name = update.effective_user.first_name

    user = await get_user(user_id)
    if not user:
        await create_user(user_id, username, first_name)
        user = await get_user(user_id)

    current_task_id = user["current_task_id"] if user else 1
    task_data = get_task_by_id(current_task_id)

    if not task_data:
        text = "Tabriklaymiz! Barcha asosiy tasklar bajarildi. /menu orqali davom eting."
    else:
        emoji = CATEGORY_EMOJI.get(task_data["category"], "📋")
        text = f"""
*{emoji} BUGUNGI TASK #{task_data['id']}*

*Hafta {task_data['week']}, Kun {task_data['day']}*
*Kategoriya:* {task_data['category'].capitalize()}

*{task_data['title']}*

{task_data['description']}

*Mukofot:* _{task_data['reward']}_

Bajarganingizdan so'ng /done bosing!
"""

    keyboard = [[InlineKeyboardButton("Bajardim!", callback_data="done")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            text, parse_mode="Markdown", reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            text, parse_mode="Markdown", reply_markup=reply_markup
        )

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        user_id = update.callback_query.from_user.id
    else:
        user_id = update.effective_user.id

    user = await get_user(user_id)
    if not user:
        text = "Avval /start bosing!"
        if update.callback_query:
            await update.callback_query.answer(text)
        else:
            await update.message.reply_text(text)
        return

    current_task_id = user["current_task_id"]
    success = await complete_task(user_id, current_task_id)

    if success:
        progress = await get_user_progress(user_id)
        streak = progress["user"]["streak_days"]

        text = f"""
*Tabriklayman!*

Task #{current_task_id} muvaffaqiyatli bajarildi!

*Sizning statistikangiz:*
- Bajarilgan tasklar: {progress['total_completed']}
- Ketma-ket kunlar: {streak}

{get_streak_message(streak)}

Keyingi taskingiz uchun /task bosing!
"""
    else:
        text = "Bu task allaqachon bajarilgan! Keyingi task uchun /task bosing."

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(text, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, parse_mode="Markdown")

async def progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        user_id = update.callback_query.from_user.id
    else:
        user_id = update.effective_user.id

    data = await get_user_progress(user_id)

    if not data["user"]:
        text = "Avval /start bosing!"
    else:
        user = data["user"]
        total = data["total_completed"]
        streak = user["streak_days"]
        current = user["current_task_id"]
        week = (current - 1) // 7 + 1

        progress_bar = get_progress_bar(total, 50)

        text = f"""
*Sizning progressingiz:*

*Bajarilgan tasklar:* {total} / 50
{progress_bar}

*Ketma-ket kunlar:* {streak}
*Hozirgi hafta:* {week}
*Keyingi task:* #{current}

*Daraja:* {get_level(total)}

{get_progress_message(total)}
"""

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(text, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, parse_mode="Markdown")

def get_progress_bar(completed, total):
    filled = int((completed / total) * 10)
    empty = 10 - filled
    return "▓" * filled + "░" * empty + f" {int(completed/total*100)}%"

def get_level(completed):
    if completed < 7:
        return "Yangi boshlovchi"
    elif completed < 14:
        return "O'rganuvchi"
    elif completed < 28:
        return "Harakatchi"
    elif completed < 42:
        return "Izlanuvchi"
    else:
        return "Boylik yo'lida"

def get_streak_message(streak):
    if streak >= 7:
        return "Bir hafta ketma-ket! Ajoyib!"
    elif streak >= 3:
        return "3 kun ketma-ket! Davom eting!"
    else:
        return "Har kuni davom eting!"

def get_progress_message(completed):
    if completed < 7:
        return "Birinchi hafta - eng muhim! Davom eting!"
    elif completed < 14:
        return "Ajoyib! Siz allaqachon o'sishdasiz!"
    elif completed < 28:
        return "Bir oy o'tdi. Siz o'zgarmoqdasiz!"
    else:
        return "Siz haqiqiy harakatchi bo'ldingiz!"
