import json
import random
from pathlib import Path

DATA_DIR = Path("data")

def load_motivations():
    with open(DATA_DIR / "motivations.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["motivations"]

def load_finance_tips():
    with open(DATA_DIR / "finance_tips.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["tips"]

def load_business_ideas():
    with open(DATA_DIR / "business_ideas.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["ideas"]

def load_tasks():
    with open(DATA_DIR / "tasks.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["tasks"]

def get_random_motivation():
    motivations = load_motivations()
    return random.choice(motivations)

def get_random_finance_tip():
    tips = load_finance_tips()
    tip = random.choice(tips)
    return f"*{tip['title']}*\n\n{tip['content']}"

def get_random_business_idea():
    ideas = load_business_ideas()
    idea = random.choice(ideas)
    return (
        f"*{idea['title']}*\n\n"
        f"{idea['description']}\n\n"
        f"Boshlang'ich kapital: {idea['capital']}\n"
        f"Qiyinlik darajasi: {idea['difficulty']}"
    )

def get_task_by_id(task_id: int):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            return task
    if task_id > len(tasks):
        return {
            "id": task_id,
            "week": (task_id - 1) // 7 + 1,
            "day": (task_id - 1) % 7 + 1,
            "category": "davom",
            "title": "O'z maqsadlaringiz ustida ishlang",
            "description": "Asosiy tasklar tugadi. Endi o'z maqsadlaringizni davom ettiring. Har kuni bitta qadam oldinga!",
            "reward": "Siz allaqachon yo'ldasiz!"
        }
    return None
