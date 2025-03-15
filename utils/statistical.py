from models.warehouse_transaction import WarehouseTransaction
from models.attendance import Attendance
from models.user import User
from models.ingredient import Ingredient
from models import db
from sqlalchemy import func

def compute_warehouse_daily_statistics(selected_date):
    """
    Lọc các giao dịch kho theo ngày (định dạng 'YYYY-MM-DD') và tạo ra 2 dòng cho mỗi nguyên liệu:
      - Một dòng cho giao dịch IN (nhập kho)
      - Một dòng cho giao dịch OUT (xuất kho)
    Nếu không có giao dịch nào của loại nào thì số liệu sẽ là 0.
    
    Trả về dict với cấu trúc:
      {
         'records': [
             {'transaction_type': 'IN', 'ingredient': 'Gạo', 'quantity': 100, 'value': 500000},
             {'transaction_type': 'OUT', 'ingredient': 'Gạo', 'quantity': 30, 'value': 150000},
             ...
         ],
         'total_import_value': 500000  # Tổng giá trị nhập hàng của tất cả các nguyên liệu
      }
    """
    ingredient_ids = db.session.query(WarehouseTransaction.ingredient_id).filter(
        func.strftime('%Y-%m-%d', WarehouseTransaction.transaction_date) == selected_date
    ).distinct().all()
    ingredient_ids = [id_tuple[0] for id_tuple in ingredient_ids]
    
    records = []
    total_import_value = 0
    for ing_id in ingredient_ids:
        ingredient = Ingredient.query.get(ing_id)

        in_data = db.session.query(
            func.sum(WarehouseTransaction.quantity),
            func.sum(WarehouseTransaction.total_amount)
        ).filter(
            func.strftime('%Y-%m-%d', WarehouseTransaction.transaction_date) == selected_date,
            WarehouseTransaction.ingredient_id == ing_id,
            WarehouseTransaction.transaction_type == 'IN'
        ).first()
        in_quantity = in_data[0] or 0
        in_value = in_data[1] or 0
        
        out_data = db.session.query(
            func.sum(WarehouseTransaction.quantity),
            func.sum(WarehouseTransaction.total_amount)
        ).filter(
            func.strftime('%Y-%m-%d', WarehouseTransaction.transaction_date) == selected_date,
            WarehouseTransaction.ingredient_id == ing_id,
            WarehouseTransaction.transaction_type == 'OUT'
        ).first()
        out_quantity = out_data[0] or 0
        out_value = out_data[1] or 0
        
        records.append({
            'transaction_type': 'IN',
            'ingredient': ingredient.name,
            'quantity': in_quantity,
            'value': in_value
        })
        total_import_value += in_value
        
        records.append({
            'transaction_type': 'OUT',
            'ingredient': ingredient.name,
            'quantity': out_quantity,
            'value': out_value
        })
        
    return {'records': records, 'total_import_value': total_import_value}

def compute_salary_monthly_statistics(selected_month, wage_rates):
    """
    Tính tiền lương nhân công theo tháng (định dạng 'YYYY-MM') dựa trên bảng Attendance.
    wage_rates: dict chứa mức lương theo role, ví dụ:
         {'manager': 70000, 'waiter': 50000, 'warehouse': 55000}
    Trả về danh sách các dict cho mỗi user, bao gồm cả role và tổng giờ làm.
    """
    monthly_data = db.session.query(
        Attendance.user_id,
        func.strftime('%Y-%m', Attendance.date).label('month'),
        func.sum(Attendance.total_hours).label('total_hours')
    ).filter(func.strftime('%Y-%m', Attendance.date) == selected_month
    ).group_by(Attendance.user_id, func.strftime('%Y-%m', Attendance.date)
    ).all()

    result = []
    for record in monthly_data:
        if record.total_hours is None:
            continue
        user = User.query.get(record.user_id)
        role = user.role
        rate = wage_rates.get(role, 50000)  
        total_salary = record.total_hours * rate
        result.append({
            'user_id': record.user_id,
            'username': user.username,
            'full_name': user.full_name,
            'role': role,
            'total_hours': record.total_hours,
            'month': record.month,
            'total_salary': total_salary
        })
    return result
