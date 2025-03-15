from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.user import User
from werkzeug.security import generate_password_hash

manage_user_bp = Blueprint('manage_user', __name__, url_prefix='/manage_user')

@manage_user_bp.route('/')
def list_users():
    users = User.query.filter(User.role.in_(['manager', 'waiter', 'warehouse'])).all()
    return render_template('manage_user.html', users=users)

@manage_user_bp.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        role = request.form.get('role')
        
        if not username or not password or not full_name or not role:
            flash('Vui lòng nhập đầy đủ thông tin.', 'error')
            return redirect(url_for('manage_user.create_user'))
        
        if User.query.filter_by(username=username).first():
            flash('Username đã tồn tại.', 'error')
            return redirect(url_for('manage_user.create_user'))
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, full_name=full_name, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Tài khoản nhân viên đã được tạo thành công.', 'success')
        return redirect(url_for('manage_user.list_users'))
    
    return render_template('manage_user.html')
