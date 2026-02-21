from app import create_app
from models import db
from models.product import Product

app = create_app()

with app.app_context():

    products = [
        Product(name="Rice", quantity=3, price=50),
        Product(name="Wheat", quantity=120, price=40),
        Product(name="Milk", quantity=20, price=30),
        Product(name="Oil", quantity=2, price=120),
    ]

    db.session.add_all(products)
    db.session.commit()

    print("Products added")