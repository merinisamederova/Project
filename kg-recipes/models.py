# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    author = db.Column(db.String(100))
    cook_time = db.Column(db.Integer)
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    rating = db.Column(db.Float)
    favorite = db.Column(db.Boolean, default=False)
    image = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "author": self.author,
            "cook_time": self.cook_time,
            "ingredients": self.ingredients.split("\n") if self.ingredients else [],
            "instructions": self.instructions,
            "rating": self.rating,
            "favorite": self.favorite,
            "image": self.image  
        }

    @staticmethod
    def from_dict(data):
        return Recipe(
            title=data.get("title"),
            category=data.get("category"),
            author=data.get("author"),
            cook_time=data.get("cook_time"),
            ingredients="\n".join(data.get("ingredients", [])),
            instructions=data.get("instructions"),
            rating=data.get("rating", 0),
            favorite=data.get("favorite", False),
            image=data.get("image")
        )

