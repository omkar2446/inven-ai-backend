from flask import Blueprint, jsonify
from models.product import Product
from models.agent_suggestion import AgentSuggestion
from datetime import date, timedelta

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


@dashboard_bp.route('/stats', methods=['GET'])
def stats():
    total = Product.query.count()
    low_stock = Product.query.filter(Product.quantity <= 5).count()
    overstock = Product.query.filter(Product.quantity >= 100).count()
    near_expiry = Product.query.filter(Product.expiry_date != None).filter(Product.expiry_date <= (date.today() + timedelta(days=30))).count()
    recent_suggestions = AgentSuggestion.query.order_by(AgentSuggestion.created_at.desc()).limit(10).all()
    suggestions = [{'id':s.id,'product_id':s.product_id,'type':s.suggestion_type,'description':s.description} for s in recent_suggestions]
    return jsonify({
        'total_products': total,
        'low_stock': low_stock,
        'overstock': overstock,
        'near_expiry': near_expiry,
        'recent_suggestions': suggestions
    })
