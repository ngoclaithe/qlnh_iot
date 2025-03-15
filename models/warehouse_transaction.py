from datetime import datetime
from models import db

class WarehouseTransaction(db.Model):
    __tablename__ = 'warehouse_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)  
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)  
    total_amount = db.Column(db.Float, nullable=False)  
    transaction_date = db.Column(db.DateTime, default=datetime.now)
    performed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    note = db.Column(db.Text)

    def __repr__(self):
        return (f"<WarehouseTransaction {self.transaction_type} {self.quantity} of "
                f"Ingredient:{self.ingredient_id} at {self.price} each, Total: {self.total_amount}>")
