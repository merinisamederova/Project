# db_init.py
import json
from app import create_app
from models import db, Recipe
import os

app = create_app()
app.app_context().push()

DB_PATH = os.path.join(os.path.dirname(__file__), "recipes_sample.json")

def init_db(load_sample=True):
    print("Создаю таблицы...")
    db.create_all()
    if load_sample and os.path.exists(DB_PATH):
        print("Загружаю sample JSON...")
        with open(DB_PATH, "r", encoding="utf-8") as f:
            arr = json.load(f)
            for item in arr:
                if not Recipe.query.filter_by(title=item.get("title")).first():
                    r = Recipe.from_dict(item)
                    db.session.add(r)
            db.session.commit()
    print("Готово.")

if __name__ == "__main__":
    init_db(load_sample=True)
