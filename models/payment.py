from datetime import datetime
from models import db

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_time = db.Column(db.DateTime, default=datetime.utcnow)
    payment_type = db.Column(db.String(50), nullable=False)  
    customer_name = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    
    order = db.relationship("Order", backref="payment", uselist=False)

    def __repr__(self):
        return f"<Payment {self.id} for Order {self.order_id}>"
