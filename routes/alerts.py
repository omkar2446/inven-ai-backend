from flask import Blueprint, jsonify
from models.agent_suggestion import AgentSuggestion
from models.product import Product

alerts_bp = Blueprint('alerts', __name__, url_prefix='/api/alerts')


@alerts_bp.route('/', methods=['GET'])
def get_alerts():
    suggestions = AgentSuggestion.query.order_by(AgentSuggestion.created_at.desc()).limit(100).all()
    result = []
    for s in suggestions:
        p = Product.query.get(s.product_id)
        result.append({
            'id': s.id,
            'product': p.name if p else None,
            'type': s.suggestion_type,
            'description': s.description,
            'created_at': s.created_at.isoformat()
        })
    return jsonify(result)
