import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from werkzeug.utils import secure_filename
from models import db
from models.ingredient import Ingredient
from datetime import datetime
import csv

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
        name_supplier = request.form['name_supplier']
        current_stock = float(request.form.get('current_stock', 0))
        min_stock = float(request.form.get('min_stock', 0))
        target_stock = float(request.form.get('target_stock', 0))
        
        ingredient = Ingredient(
            name=name,
            unit=unit,
            image=image_url,
            name_supplier=name_supplier,
            current_stock=current_stock,
            min_stock=min_stock,
            target_stock=target_stock
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
        ingredient.current_stock = float(request.form.get('current_stock', 0))
        ingredient.min_stock = float(request.form.get('min_stock', 0))
        ingredient.target_stock = float(request.form.get('target_stock', 0))
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
@ingredient_bp.route('/update-stock', methods=['PUT'])
def update_stock():
    try:
        data = request.json
        transaction_date = data.get('date')
        ingredients_data = data.get('ingredients', [])
        
        csv_folder = current_app.config.get('CSV_FOLDER', 'static/exports')
        os.makedirs(csv_folder, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"kitchen_transaction_{timestamp}.csv"
        csv_path = os.path.join(csv_folder, csv_filename)
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['transaction_date', 'ingredient_id', 'ingredient_name', 'used_amount', 'previous_stock', 'new_stock']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for item in ingredients_data:
                ingredient_id = item.get('id')
                used_amount = item.get('used', 0)
                new_stock = item.get('new_stock', 0)
                
                ingredient = Ingredient.query.get(ingredient_id)
                if ingredient:
                    previous_stock = ingredient.current_stock
                    
                    writer.writerow({
                        'transaction_date': transaction_date,
                        'ingredient_id': ingredient_id,
                        'ingredient_name': ingredient.name,
                        'used_amount': used_amount,
                        'previous_stock': previous_stock,
                        'new_stock': new_stock
                    })
                    
                    ingredient.current_stock = new_stock
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Cập nhật kho thành công',
            'csv_path': url_for('static', filename=f'exports/{csv_filename}')
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Lỗi: {str(e)}'
        }), 500