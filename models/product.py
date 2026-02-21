from datetime import datetime
from models import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(64))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    expiry_date = db.Column(db.Date)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    logs = db.relationship('InventoryLog', backref='product', lazy='dynamic')
    suggestions = db.relationship('AgentSuggestion', backref='product', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'quantity': self.quantity,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'created_by': self.created_by
        }