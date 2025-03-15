from datetime import datetime
from models import db

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_time = db.Column(db.DateTime, default=datetime.now)
    waiter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # pending, in_progress, completed, canceled
    total_amount = db.Column(db.Float, default=0.0)
    
    # Quan hệ với order items
    order_items = db.relationship("OrderItem", backref="order", lazy=True)

    def __repr__(self):
        return f"<Order {self.id} - Status: {self.status}>"
