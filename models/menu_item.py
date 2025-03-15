from models import db

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))  # Ví dụ: appetizer, main course, dessert, drink,...
    active = db.Column(db.Boolean, default=True)
    image = db.Column(db.String(255))  
    
    order_items = db.relationship("OrderItem", backref="menu_item", lazy=True)

    def __repr__(self):
        return f"<MenuItem {self.name}>"
