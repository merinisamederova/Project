# app.py
from flask import Flask, jsonify, request, render_template, send_from_directory
from models import db, Recipe
from flask_cors import CORS
import json
import os

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    CORS(app)
    return app

app = create_app()

# --- helper to save DB to JSON file
def dump_db_to_file(path="recipes_export.json"):
    recipes = Recipe.query.order_by(Recipe.id).all()
    arr = [r.to_dict() for r in recipes]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(arr, f, ensure_ascii=False, indent=2)
    return path

@app.route("/")
def index():
    return render_template("index.html")

# REST API
@app.route("/api/recipes", methods=["GET"])
def list_recipes():
    # supports ?q=searchtext & category=... & favorite=true
    q = request.args.get("q", "").strip()
    category = request.args.get("category")
    favorite = request.args.get("favorite")
    query = Recipe.query
    if q:
        like = f"%{q}%"
        query = query.filter(Recipe.title.ilike(like) | Recipe.ingredients.ilike(like) | Recipe.instructions.ilike(like))
    if category:
        query = query.filter(Recipe.category == category)
    if favorite and favorite.lower() in ("1","true","yes"):
        query = query.filter(Recipe.favorite==True)
    recipes = query.order_by(Recipe.title).all()
    return jsonify([r.to_dict() for r in recipes])

@app.route("/api/recipes/<int:rid>", methods=["GET"])
def get_recipe(rid):
    r = Recipe.query.get_or_404(rid)
    return jsonify(r.to_dict())

@app.route("/api/recipes", methods=["POST"])
def add_recipe():
    data = request.json or {}
    r = Recipe.from_dict(data)
    db.session.add(r)
    db.session.commit()
    return jsonify(r.to_dict()), 201

@app.route("/api/recipes/<int:rid>", methods=["PUT"])
def edit_recipe(rid):
    data = request.json or {}
    r = Recipe.query.get_or_404(rid)
    # update fields
    r.title = data.get("title", r.title)
    r.category = data.get("category", r.category)
    ing = data.get("ingredients")
    if isinstance(ing, list):
        r.ingredients = "\n".join(ing)
    elif isinstance(ing, str):
        r.ingredients = ing
    r.instructions = data.get("instructions", r.instructions)
    r.cook_time = data.get("cook_time", r.cook_time)
    r.rating = data.get("rating", r.rating)
    r.author = data.get("author", r.author)
    if "favorite" in data:
        r.favorite = bool(data.get("favorite"))
    db.session.commit()
    return jsonify(r.to_dict())

@app.route("/api/recipes/<int:rid>", methods=["DELETE"])
def delete_recipe(rid):
    r = Recipe.query.get_or_404(rid)
    db.session.delete(r)
    db.session.commit()
    return jsonify({"status":"ok"})

# upload JSON file -> load into DB (expects JSON array)
@app.route("/api/load_json", methods=["POST"])
def load_json():
    # either file upload or raw JSON body
    if "file" in request.files:
        f = request.files["file"]
        data = json.load(f)
    else:
        data = request.json
    if not isinstance(data, list):
        return jsonify({"error":"expected a JSON array"}), 400
    added = 0
    for item in data:
        if not Recipe.query.filter_by(title=item.get("title")).first():
            r = Recipe.from_dict(item)
            db.session.add(r)
            added += 1
    db.session.commit()
    return jsonify({"added": added})

@app.route("/api/save_json", methods=["GET"])
def save_json():
    path = dump_db_to_file()
    # return contents as response
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify({"path": path, "count": len(data), "data": data})

# static files (if needed)
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    # create DB if missing
    with app.app_context():
        db.create_all()
    app.run(debug=True)
