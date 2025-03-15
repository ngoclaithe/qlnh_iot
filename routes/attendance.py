from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.attendance import Attendance
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance')

@attendance_bp.route('/')
def list_attendance():
    user_id = session.get('user_id')
    attendances = Attendance.query.filter_by(user_id=user_id).all()
    return render_template('attendance.html', attendances=attendances)

@attendance_bp.route('/checkin', methods=['POST'])
def check_in():
    user_id = session.get('user_id')
    attendance = Attendance(user_id=user_id, check_in=datetime.utcnow(), date=datetime.utcnow().date())
    db.session.add(attendance)
    db.session.commit()
    flash('Check-in thành công', 'success')
    return redirect(url_for('attendance.list_attendance'))

@attendance_bp.route('/checkout/<int:attendance_id>', methods=['POST'])
def check_out(attendance_id):
    attendance = Attendance.query.get(attendance_id)
    if attendance and not attendance.check_out:
        attendance.check_out = datetime.utcnow()
        attendance.total_hours = (attendance.check_out - attendance.check_in).total_seconds() / 3600
        db.session.commit()
        flash('Check-out thành công', 'success')
    else:
        flash('Không thể check-out', 'danger')
    return redirect(url_for('attendance.list_attendance'))
