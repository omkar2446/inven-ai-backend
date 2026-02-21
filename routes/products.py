from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from models.product import Product
from models.inventory_log import InventoryLog
from models import db
from utils.helpers import parse_date

products_bp = Blueprint('products', __name__, url_prefix='/api/products')


# ===============================
# ➕ ADD PRODUCT
# ===============================
@products_bp.route('/', methods=['POST'])
def add_product():

    data = request.get_json() or {}

    try:

        name = data.get("name")
        category = data.get("category")
        price = float(data.get("price") or 0)
        quantity = int(data.get("quantity") or 0)

        expiry = parse_date(data.get("expiry_date"))

        p = Product(
            name=name,
            category=category,
            price=price,
            quantity=quantity,
            expiry_date=expiry,
            created_by=None
        )

        db.session.add(p)
        db.session.commit()

        log = InventoryLog(product_id=p.id, change_in_quantity=p.quantity)
        db.session.add(log)
        db.session.commit()

        return jsonify(p.to_dict()),201

    except Exception as e:
        print("🔥 ADD PRODUCT ERROR:",e)
        return jsonify(message=str(e)),500

# ===============================
# ✏ UPDATE PRODUCT
# ===============================
@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):

    data = request.get_json()
    p = Product.query.get_or_404(product_id)

    try:
        old_qty = p.quantity

        p.name = data.get('name', p.name)
        p.category = data.get('category', p.category)
        p.price = float(data.get('price', p.price))
        p.quantity = int(data.get('quantity', p.quantity))

        new_date = parse_date(data.get('expiry_date'))
        if new_date:
            p.expiry_date = new_date

        db.session.commit()

        # inventory log if quantity changed
        if p.quantity != old_qty:
            log = InventoryLog(
                product_id=p.id,
                change_in_quantity=p.quantity - old_qty
            )
            db.session.add(log)
            db.session.commit()

        return jsonify(p.to_dict())

    except Exception as e:
        print("UPDATE ERROR:", e)
        return jsonify(message="Failed to update"), 500


# ===============================
# ❌ DELETE PRODUCT
# ===============================
@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):

    try:
        p = Product.query.get_or_404(product_id)
        db.session.delete(p)
        db.session.commit()

        return jsonify(message='Deleted')

    except Exception as e:
        print("DELETE ERROR:", e)
        return jsonify(message="Failed to delete"), 500


# ===============================
# 📦 GET PRODUCTS
# ===============================
@products_bp.route('/', methods=['GET'])
def get_products():

    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])