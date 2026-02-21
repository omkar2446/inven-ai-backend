from flask import Flask, jsonify
from config import Config
from models import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# blueprints
from routes.auth import auth_bp
from routes.products import products_bp
from routes.alerts import alerts_bp
from    routes.dashboard import dashboard_bp

# agents
from agents import demand_forecast, stock_monitor, supply_analysis, price_optimization

from apscheduler.schedulers.background import BackgroundScheduler
import atexit


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ⭐ ENABLE CORS (VERY IMPORTANT)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # init extensions
    db.init_app(app)
    jwt = JWTManager(app)

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(dashboard_bp)

    @app.route("/")
    def index():
        return jsonify(message="Inventory Multi-Agent API Running")

    # scheduler
    scheduler = BackgroundScheduler()

    with app.app_context():
        db.create_all()

        # -------- AGENT WRAPPERS --------

        def run_demand():
            with app.app_context():
                demand_forecast.run()

        def run_stock():
            with app.app_context():
                stock_monitor.run()

        def run_supply():
            with app.app_context():
                supply_analysis.run()

        def run_price():
            with app.app_context():
                price_optimization.run()

        # schedule jobs
        scheduler.add_job(run_demand, "interval", minutes=1, id="demand")
        scheduler.add_job(run_stock, "interval", minutes=1, id="stock")
        scheduler.add_job(run_supply, "interval", minutes=2, id="supply")
        scheduler.add_job(run_price, "interval", minutes=5, id="price")

    scheduler.start()

    # shutdown scheduler on exit
    atexit.register(lambda: scheduler.shutdown())

    return app


# run app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)