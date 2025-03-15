from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, make_response
from models import db
from utils.statistical import compute_warehouse_daily_statistics, compute_salary_monthly_statistics
from weasyprint import HTML
from datetime import datetime

statistical_bp = Blueprint('statistical', __name__, url_prefix='/statistical')

@statistical_bp.route('/')
def statistical_index():

    return render_template('statistical.html')

@statistical_bp.route('/warehouse/daily', methods=['GET'])
def warehouse_daily():

    selected_date = request.args.get('date')
    stats = None
    if selected_date:
        stats = compute_warehouse_daily_statistics(selected_date)
    return render_template('statistical_warehouse_daily.html', stats=stats, selected_date=selected_date)

@statistical_bp.route('/warehouse/daily/pdf', methods=['GET'])
def warehouse_daily_pdf():

    selected_date = request.args.get('date')
    if not selected_date:
        flash('Bạn phải chọn ngày để xuất PDF', 'error')
        return redirect(url_for('statistical.warehouse_daily'))
    stats = compute_warehouse_daily_statistics(selected_date)
    rendered = render_template('statistical_warehouse_daily_pdf.html', stats=stats, selected_date=selected_date)
    pdf = HTML(string=rendered, base_url=request.base_url).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=warehouse_stats_{selected_date}.pdf'
    return response

@statistical_bp.route('/salary/monthly', methods=['GET'])
def salary_monthly():
    """
    Trang thống kê tiền lương nhân công theo tháng.
    Yêu cầu query parameter 'month' theo định dạng 'YYYY-MM' và nhập mức lương cho các role.
    """
    selected_month = request.args.get('month')
    try:
        manager_rate = float(request.args.get('manager_rate', 50000))
    except:
        manager_rate = 50000
    try:
        waiter_rate = float(request.args.get('waiter_rate', 50000))
    except:
        waiter_rate = 50000
    try:
        warehouse_rate = float(request.args.get('warehouse_rate', 50000))
    except:
        warehouse_rate = 50000

    wage_rates = {'manager': manager_rate, 'waiter': waiter_rate, 'warehouse': warehouse_rate}
    salary_stats = None
    if selected_month:
        salary_stats = compute_salary_monthly_statistics(selected_month, wage_rates)
    return render_template('statistical_salary_monthly.html', salary_stats=salary_stats, selected_month=selected_month, wage_rates=wage_rates)
