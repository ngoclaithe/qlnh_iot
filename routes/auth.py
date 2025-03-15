import datetime
import jwt
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from models import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Dữ liệu không hợp lệ"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username và password là bắt buộc"}), 400

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role

        payload = {
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({
            "message": "Đăng nhập thành công",
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role
            }
        }), 200
    else:
        return jsonify({"error": "Tên đăng nhập hoặc mật khẩu không đúng"}), 401

@auth_bp.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Dữ liệu không hợp lệ"}), 400

    username = data.get('username')
    password = data.get('password')
    full_name = data.get('full_name')
    role = data.get('role', 'waiter')  

    if not username or not password or not full_name:
        return jsonify({"error": "Username, password và full_name là bắt buộc"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username đã tồn tại"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, full_name=full_name, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "Đăng ký thành công",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "full_name": new_user.full_name,
            "role": new_user.role
        }
    }), 201

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Đăng xuất thành công', 'success')
    return redirect(url_for('auth.login_page'))
