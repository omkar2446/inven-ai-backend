from models.product import Product
from models.agent_suggestion import AgentSuggestion
from models import db
from datetime import date, timedelta


def run():

    overstock_threshold = 100

    for p in Product.query.all():

        suggestion_type = None
        description = None

        # ⭐ OVERSTOCK DISCOUNT
        if p.quantity > overstock_threshold:

            discount = min(50, int((p.quantity - overstock_threshold) / 2))

            suggestion_type = "price_discount"
            description = f"Suggest {discount}% discount on {p.name} to clear overstock."

        # ⭐ EXPIRY CLEARANCE
        elif p.expiry_date and p.expiry_date <= date.today() + timedelta(days=7):

            suggestion_type = "clearance"
            description = f"{p.name} expiring soon. Suggest clearance sale."

        if not suggestion_type:
            continue

        # ⭐ prevent duplicate but update message
        exists = AgentSuggestion.query.filter_by(
            product_id=p.id,
            suggestion_type=suggestion_type
        ).first()

        if exists:
            exists.description = description
        else:
            db.session.add(
                AgentSuggestion(
                    product_id=p.id,
                    suggestion_type=suggestion_type,
                    description=description
                )
            )

    db.session.commit()