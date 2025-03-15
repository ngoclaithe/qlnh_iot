from datetime import datetime
from models import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, manager, waiter, warehouse
    active = db.Column(db.Boolean, default=True)
    
    # Quan hệ với đơn hàng và chấm công, giao dịch kho
    orders = db.relationship("Order", backref="waiter", lazy=True)
    attendances = db.relationship("Attendance", backref="user", lazy=True)
    warehouse_transactions = db.relationship("WarehouseTransaction", backref="operator", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"
