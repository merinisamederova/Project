# import_json.py
from app import app
from models import db, Recipe
import json

with app.app_context():
    db.session.query(Recipe).delete()

    with open("recipes.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        r = Recipe.from_dict(item)
        db.session.add(r)

    db.session.commit()
    print(f"✅ Импортировано {len(data)} рецептов!")
