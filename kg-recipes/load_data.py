from app import app, db, Recipe
import json

with app.app_context():
    db.create_all()
    print("База данных создана!")
    
    try:
        with open('recipes.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        existing_count = Recipe.query.count()
        print(f"Сейчас в базе: {existing_count} рецептов")

        added_count = 0
        for recipe_data in data:
            if not Recipe.query.filter_by(title=recipe_data['title']).first():
                recipe = Recipe.from_dict(recipe_data)
                db.session.add(recipe)
                added_count += 1
        
        db.session.commit()
        print(f"Добавлено новых рецептов: {added_count}")
        print(f"Всего в базе: {Recipe.query.count()} рецептов")
        
    except FileNotFoundError:
        print("Ошибка: Файл recipes.json не найден!")
    except Exception as e:
        print(f"Ошибка загрузки: {e}")