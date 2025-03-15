import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from models import db
from models.menu_item import MenuItem
from sqlalchemy import or_

menu_bp = Blueprint('menu', __name__, url_prefix='/menu')

ITEMS_PER_PAGE = 9

@menu_bp.route('/')
def list_menu():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    status = request.args.get('status', '')
    
    query = MenuItem.query
    
    if category:
        query = query.filter(MenuItem.category == category)
    
    if status:
        is_active = status == 'active'
        query = query.filter(MenuItem.active == is_active)
    
    total_items = query.count()
    total_pages = (total_items - 1) // ITEMS_PER_PAGE + 1
    
    menu_items = query.order_by(MenuItem.id.desc()) \
                    .offset((page - 1) * ITEMS_PER_PAGE) \
                    .limit(ITEMS_PER_PAGE) \
                    .all()
    
    return render_template('menu.html', 
                          menu_items=menu_items, 
                          page=page, 
                          total_pages=total_pages)

@menu_bp.route('/create', methods=['GET', 'POST'])
def create_menu_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description')
        price = float(request.form.get('price'))
        category = request.form.get('category')
        active = True if request.form.get('active') == 'on' else False
        image_file = request.files.get('image')
        image_path = None
        
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{timestamp}_{filename}"
            
            upload_dir = os.path.join(current_app.root_path, 'static', 'images', 'menu')
            os.makedirs(upload_dir, exist_ok=True)
            
            image_path = os.path.join('images', 'menu', filename).replace('\\', '/')
            upload_path = os.path.join(current_app.root_path, 'static', image_path)
            image_file.save(upload_path)
        
        menu_item = MenuItem(
            name=name, 
            description=description, 
            price=price,
            category=category, 
            active=active, 
            image=image_path
        )
        
        db.session.add(menu_item)
        db.session.commit()
        flash('Món ăn/đồ uống được tạo thành công', 'success')
        return redirect(url_for('menu.list_menu'))
    
    return render_template('create_menu_item.html')

@menu_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_menu_item(id):
    menu_item = MenuItem.query.get_or_404(id)
    
    if request.method == 'POST':
        menu_item.name = request.form['name']
        menu_item.description = request.form.get('description')
        menu_item.price = float(request.form.get('price'))
        menu_item.category = request.form.get('category')
        menu_item.active = True if request.form.get('active') == 'on' else False
        
        image_file = request.files.get('image')
        if image_file and image_file.filename:
            if menu_item.image:
                old_image_path = os.path.join(current_app.root_path, 'static', menu_item.image)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            
            filename = secure_filename(image_file.filename)
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{timestamp}_{filename}"
            
            upload_dir = os.path.join(current_app.root_path, 'static', 'images', 'menu')
            os.makedirs(upload_dir, exist_ok=True)
            
            image_path = os.path.join('images', 'menu', filename).replace('\\', '/')
            upload_path = os.path.join(current_app.root_path, 'static', image_path)
            image_file.save(upload_path)
            
            menu_item.image = image_path
        
        db.session.commit()
        flash('Món ăn/đồ uống được cập nhật thành công', 'success')
        return redirect(url_for('menu.list_menu'))
    
    return render_template('edit_menu_item.html', menu_item=menu_item)

@menu_bp.route('/toggle/<int:id>')
def toggle_menu_item(id):
    menu_item = MenuItem.query.get_or_404(id)
    menu_item.active = not menu_item.active
    db.session.commit()
    
    status = "kích hoạt" if menu_item.active else "vô hiệu hóa"
    flash(f'Món ăn/đồ uống đã được {status} thành công', 'success')
    return redirect(url_for('menu.list_menu'))
