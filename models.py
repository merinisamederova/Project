from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    __tablename__ = 'recipes' 
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    cook_time = db.Column(db.Integer)
    rating = db.Column(db.Integer, default=0)
    favorite = db.Column(db.Boolean, default=False)
    author = db.Column(db.String(100))
    image = db.Column(db.String(300))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'ingredients': self.ingredients.split('\n') if self.ingredients else [],
            'instructions': self.instructions,
            'cook_time': self.cook_time,
            'rating': self.rating,
            'favorite': self.favorite,
            'author': self.author,
            'image': self.image
        }
    
    @classmethod
    def from_dict(cls, data):
        ingredients = data.get('ingredients', [])
        if isinstance(ingredients, list):
            ingredients = '\n'.join(ingredients)
        
        return cls(
            title=data.get('title', ''),
            category=data.get('category', ''),
            ingredients=ingredients,
            instructions=data.get('instructions', ''),
            cook_time=data.get('cook_time', 0),
            rating=data.get('rating', 0),
            favorite=data.get('favorite', False),
            author=data.get('author', ''),
            image=data.get('image', '')
        )

