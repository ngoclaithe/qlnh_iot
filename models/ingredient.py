from models import db

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    unit = db.Column(db.String(20))  
    image = db.Column(db.Text)  
    name_supplier = db.Column(db.Text)  
    current_stock = db.Column(db.Float, default=0.0)
    min_stock = db.Column(db.Float, default=0.0)
    
    # Quan hệ với các giao dịch kho
    transactions = db.relationship("WarehouseTransaction", backref="ingredient", lazy=True)

    def __repr__(self):
        return f"<Ingredient {self.name}>"
