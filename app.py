import logging
from flask import Flask, request
from waitress import serve
from models import init_db
from routes import register_routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
app.config['SECRET_KEY'] = 'my_secret_key'

init_db(app)
register_routes(app)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),                    
    ]
)

@app.before_request
def log_request_info():
    logging.info(f"Request: {request.method} {request.path}")
    logging.info(f"Headers: {request.headers}")
    logging.info(f"Body: {request.get_data()}")

@app.after_request
def log_response_info(response):
    logging.info(f"Response status: {response.status}")
    return response

if __name__ == "__main__":
    logging.info("Server đang chạy trên 0.0.0.0:5000")
    serve(app, host="0.0.0.0", port=5000)
