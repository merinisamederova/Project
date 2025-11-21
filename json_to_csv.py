import json
import csv

with open('recipes.json', 'r', encoding='utf-8') as f:
    recipes = json.load(f)

with open('recipes.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    
    writer.writerow(['title', 'category', 'ingredients', 'instructions', 'cook_time', 'rating', 'favorite', 'author'])
    
    for recipe in recipes:
        ingredients = recipe.get('ingredients', [])
        if isinstance(ingredients, list):
            ingredients = '\n'.join(ingredients)
        
        writer.writerow([
            recipe.get('title', ''),
            recipe.get('category', ''),
            ingredients,
            recipe.get('instructions', ''),
            recipe.get('cook_time', 0),
            recipe.get('rating', 0),
            int(recipe.get('favorite', False)),
            recipe.get('author', '')
        ])

print("Конвертировано в recipes.csv")