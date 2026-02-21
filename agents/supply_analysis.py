from models.product import Product
from models.agent_suggestion import AgentSuggestion
from models import db


def run():
    # placeholder: if a product has been unchanged for long, suggest reorder
    products = Product.query.all()
    for p in products:
        description = f'Supply analysis: consider reordering {p.name} soon.'
        sug = AgentSuggestion(
            product_id=p.id,
            suggestion_type='supply_analysis',
            description=description
        )
        db.session.add(sug)
    db.session.commit()
