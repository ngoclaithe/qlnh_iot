from datetime import datetime, date
from models import db

class Attendance(db.Model):
    __tablename__ = 'attendances'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    check_in = db.Column(db.DateTime, nullable=False)
    check_out = db.Column(db.DateTime)
    total_hours = db.Column(db.Float)  

    def __repr__(self):
        return f"<Attendance User:{self.user_id} Date:{self.date}>"
