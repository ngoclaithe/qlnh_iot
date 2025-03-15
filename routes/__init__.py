from routes.auth import auth_bp
from routes.orders import orders_bp
from routes.menu import menu_bp
from routes.warehouse import warehouse_bp
from routes.ingredient import ingredient_bp
from routes.attendance import attendance_bp
from routes.main import main_bp
from routes.statistical import statistical_bp
from routes.manage_user import manage_user_bp
from routes.payment import payment_bp
def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(warehouse_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(ingredient_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(statistical_bp)
    app.register_blueprint(manage_user_bp)
    app.register_blueprint(payment_bp)
