from models.product import Product
from models.agent_suggestion import AgentSuggestion
from models.inventory_log import InventoryLog
from models import db
from sqlalchemy import func


def run():

    products = Product.query.all()

    for p in products:

        # ⭐ basic usage average
        avg_usage = (
            db.session.query(func.avg(InventoryLog.change_in_quantity))
            .filter(InventoryLog.product_id == p.id)
            .scalar()
        )

        # fallback if no logs
        if not avg_usage:
            predicted = p.quantity + 10
        else:
            predicted = int(abs(avg_usage) * 7)

        desc = f"Forecast demand for {p.name}: maintain {predicted} units."

        # ⭐ prevent duplicate
        exists = AgentSuggestion.query.filter_by(
            product_id=p.id,
            suggestion_type="demand_forecast"
        ).first()

        if exists:
            exists.description = desc
        else:
            sug = AgentSuggestion(
                product_id=p.id,
                suggestion_type="demand_forecast",
                description=desc
            )
            db.session.add(sug)

    db.session.commit()