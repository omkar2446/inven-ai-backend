from datetime import datetime
from models import db

class AgentSuggestion(db.Model):
    __tablename__ = 'agent_suggestions'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    suggestion_type = db.Column(db.String(64))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
