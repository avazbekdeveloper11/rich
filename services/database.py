import aiosqlite
import os
from datetime import datetime

DATABASE_PATH = "database/users.db"

async def init_db():
    os.makedirs("database", exist_ok=True)
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                joined_date TEXT,
                current_task_id INTEGER DEFAULT 1,
                completed_tasks INTEGER DEFAULT 0,
                streak_days INTEGER DEFAULT 0,
                last_active TEXT
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS task_completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                task_id INTEGER,
                completed_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        await db.commit()

async def get_user(user_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        )
        return await cursor.fetchone()

async def create_user(user_id: int, username: str, first_name: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        now = datetime.now().isoformat()
        await db.execute('''
            INSERT OR IGNORE INTO users (user_id, username, first_name, joined_date, last_active)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, now, now))
        await db.commit()

async def update_user_task(user_id: int, task_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE users SET current_task_id = ? WHERE user_id = ?",
            (task_id, user_id)
        )
        await db.commit()

async def complete_task(user_id: int, task_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        now = datetime.now().isoformat()
        today = datetime.now().date().isoformat()

        cursor = await db.execute(
            "SELECT * FROM task_completions WHERE user_id = ? AND task_id = ?",
            (user_id, task_id)
        )
        existing = await cursor.fetchone()
        if existing:
            return False

        await db.execute('''
            INSERT INTO task_completions (user_id, task_id, completed_date)
            VALUES (?, ?, ?)
        ''', (user_id, task_id, today))

        cursor = await db.execute(
            "SELECT last_active, streak_days FROM users WHERE user_id = ?",
            (user_id,)
        )
        user_data = await cursor.fetchone()

        streak = 1
        if user_data and user_data[0]:
            last_active_date = datetime.fromisoformat(user_data[0]).date()
            today_date = datetime.now().date()
            diff = (today_date - last_active_date).days
            if diff == 1:
                streak = (user_data[1] or 0) + 1
            elif diff == 0:
                streak = user_data[1] or 1

        await db.execute('''
            UPDATE users
            SET completed_tasks = completed_tasks + 1,
                current_task_id = current_task_id + 1,
                streak_days = ?,
                last_active = ?
            WHERE user_id = ?
        ''', (streak, now, user_id))

        await db.commit()
        return True

async def get_user_progress(user_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        )
        user = await cursor.fetchone()

        cursor = await db.execute(
            "SELECT COUNT(*) FROM task_completions WHERE user_id = ?",
            (user_id,)
        )
        total_completed = (await cursor.fetchone())[0]

        return {
            "user": dict(user) if user else None,
            "total_completed": total_completed
        }

async def get_all_users():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("SELECT user_id FROM users")
        rows = await cursor.fetchall()
        return [row[0] for row in rows]
