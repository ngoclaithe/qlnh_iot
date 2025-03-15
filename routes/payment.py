from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.payment import Payment
from models.order import Order
from datetime import datetime

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

@payment_bp.route('/')
def list_payments():
    payments = Payment.query.all()
    return render_template('payment_list.html', payments=payments)

@payment_bp.route('/create/<int:order_id>', methods=['GET', 'POST'])
def create_payment(order_id):
    order = Order.query.get_or_404(order_id)
    if order.status != 'completed':
        flash('Chỉ có đơn hàng hoàn thành mới có thể thanh toán', 'error')
        return redirect(url_for('orders.view_order', order_id=order_id))
    
    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount'))
        except:
            flash('Số tiền không hợp lệ', 'error')
            return redirect(url_for('payment.create_payment', order_id=order_id))
        
        payment_type = request.form.get('payment_type')
        customer_name = request.form.get('customer_name')
        phone_number = request.form.get('phone_number')
        
        if not payment_type or not customer_name or not phone_number:
            flash('Vui lòng nhập đầy đủ thông tin thanh toán', 'error')
            return redirect(url_for('payment.create_payment', order_id=order_id))
        
        payment = Payment(
            order_id=order_id,
            amount=amount,
            payment_type=payment_type,
            customer_name=customer_name,
            phone_number=phone_number,
            payment_time=datetime.now()
        )
        db.session.add(payment)
        db.session.commit()
        flash('Thanh toán thành công', 'success')
        return redirect(url_for('orders.view_order', order_id=order_id))
    
    return render_template('payment.html', order_id=order_id)
