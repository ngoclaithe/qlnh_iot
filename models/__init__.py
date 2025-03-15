from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        from models.user import User
        from models.menu_item import MenuItem
        from models.order import Order
        from models.order_item import OrderItem
        from models.ingredient import Ingredient
        from models.warehouse_transaction import WarehouseTransaction
        from models.attendance import Attendance
        from models.payment import Payment
        db.create_all()
        print("Database tables created successfully!")
