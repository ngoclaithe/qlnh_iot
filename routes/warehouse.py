from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from models import db
from models.ingredient import Ingredient
from models.warehouse_transaction import WarehouseTransaction
from datetime import datetime

warehouse_bp = Blueprint('warehouse', __name__, url_prefix='/warehouse')

@warehouse_bp.route('/')
def list_ingredients():
    ingredients = Ingredient.query.all()
    return render_template('warehouse.html', ingredients=ingredients)

@warehouse_bp.route('/transaction', methods=['GET', 'POST'])
def transaction():
    if request.method == 'POST':
        ingredient_id = request.form['ingredient_id']
        transaction_type = request.form['transaction_type']
        quantity = float(request.form['quantity'])
        price = float(request.form['price'])
        note = request.form.get('note', '')
        performed_by = session.get('user_id')
        
        total_amount = price * quantity
        
        transaction = WarehouseTransaction(
            ingredient_id=ingredient_id,
            transaction_type=transaction_type,
            quantity=quantity,
            price=price,
            total_amount=total_amount,
            performed_by=performed_by,
            transaction_date=datetime.utcnow(),
            note=note
        )
        ingredient = Ingredient.query.get(ingredient_id)
        if transaction_type.upper() == 'IN':
            ingredient.current_stock += quantity
        elif transaction_type.upper() == 'OUT':
            ingredient.current_stock -= quantity
        
        db.session.add(transaction)
        db.session.commit()
        flash('Giao dịch kho đã được thực hiện', 'success')
        return redirect(url_for('warehouse.list_ingredients'))
    
    ingredients = Ingredient.query.all()
    return render_template('warehouse_transaction.html', ingredients=ingredients)

