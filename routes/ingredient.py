import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from models import db
from models.ingredient import Ingredient
from datetime import datetime

ingredient_bp = Blueprint('ingredient', __name__, url_prefix='/ingredient')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ingredient_bp.route('/')
def list_ingredients():
    ingredients = Ingredient.query.all()
    return render_template('ingredient.html', ingredients=ingredients)

@ingredient_bp.route('/create', methods=['GET', 'POST'])
def create_ingredient():
    if request.method == 'POST':
        name = request.form['name']
        unit = request.form['unit']
        
        image_file = request.files.get('image')
        image_url = ''
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'static/uploads/ingredients')
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, filename)
            image_file.save(image_path)
            image_url = url_for('static', filename='uploads/ingredients/' + filename)
        
        current_stock = float(request.form.get('current_stock', 0))
        min_stock = float(request.form.get('min_stock', 0))
        
        ingredient = Ingredient(
            name=name,
            unit=unit,
            image=image_url,
            current_stock=current_stock,
            min_stock=min_stock
        )
        db.session.add(ingredient)
        db.session.commit()
        flash('Nguyên liệu đã được tạo thành công', 'success')
        return redirect(url_for('ingredient.list_ingredients'))
    
    return render_template('create_ingredient.html')

@ingredient_bp.route('/edit/<int:ingredient_id>', methods=['GET', 'POST'])
def edit_ingredient(ingredient_id):
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    if request.method == 'POST':
        ingredient.name = request.form['name']
        ingredient.name_supplier = request.form['name_supplier']
        
        image_file = request.files.get('image')
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'static/uploads/ingredients')
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, filename)
            image_file.save(image_path)
            ingredient.image = url_for('static', filename='uploads/ingredients/' + filename)
        
        ingredient.min_stock = float(request.form.get('min_stock', 0))
        db.session.commit()
        flash('Nguyên liệu đã được cập nhật', 'success')
        return redirect(url_for('ingredient.list_ingredients'))
    return render_template('edit_ingredient.html', ingredient=ingredient)

@ingredient_bp.route('/delete/<int:ingredient_id>', methods=['POST'])
def delete_ingredient(ingredient_id):
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    db.session.delete(ingredient)
    db.session.commit()
    flash('Nguyên liệu đã được xóa', 'success')
    return redirect(url_for('ingredient.list_ingredients'))
