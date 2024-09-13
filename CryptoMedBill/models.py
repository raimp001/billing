from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    visit_type = db.Column(db.String(50), nullable=False)
    diagnosis = db.Column(db.String(200), nullable=False)
    amount_usd = db.Column(db.Float, nullable=False)
    payment_token = db.Column(db.String(10), nullable=False)
    charge_id = db.Column(db.String(100), nullable=True)
    payment_status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Bill {self.id}>'
