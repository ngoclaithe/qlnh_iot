from models import db

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Text)  # Ghi chú đặc biệt (nếu có)

    def __repr__(self):
        return f"<OrderItem Order:{self.order_id} MenuItem:{self.menu_item_id}>"
