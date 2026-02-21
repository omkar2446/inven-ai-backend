from models.product import Product
from models.agent_suggestion import AgentSuggestion
from models import db
from datetime import date, timedelta


def run():

    low_threshold = 5
    overstock_threshold = 100

    products = Product.query.all()

    for p in products:

        # ---------------- LOW STOCK ----------------
        if p.quantity <= low_threshold:

            create_or_update(
                p,
                "low_stock",
                f"Low stock alert for {p.name}: only {p.quantity} left."
            )

        # ---------------- OVERSTOCK ----------------
        elif p.quantity >= overstock_threshold:

            create_or_update(
                p,
                "overstock",
                f"Overstock alert for {p.name}: {p.quantity} units."
            )

        # ---------------- EXPIRY ----------------
        if p.expiry_date and p.expiry_date <= date.today() + timedelta(days=7):

            create_or_update(
                p,
                "expiry",
                f"{p.name} expiring soon"
            )

    db.session.commit()


# ⭐ helper to avoid duplicate but update text
def create_or_update(product, stype, desc):

    exists = AgentSuggestion.query.filter_by(
        product_id=product.id,
        suggestion_type=stype
    ).first()

    if exists:
        exists.description = desc   # update message
        return

    sug = AgentSuggestion(
        product_id=product.id,
        suggestion_type=stype,
        description=desc
    )

    db.session.add(sug)